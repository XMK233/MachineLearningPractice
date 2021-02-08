package com.system.online.scalaFeatureEngineering

import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.expressions.{UserDefinedFunction, Window}
import org.apache.spark.sql.functions.{format_number, _}
import org.apache.spark.sql.types.{DecimalType, FloatType, IntegerType, LongType, StringType, StructField, StructType}
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import org.apache.spark.sql.Row
import redis.clients.jedis.Jedis
import redis.clients.jedis.params.SetParams

import scala.collection.immutable.ListMap
import scala.collection.{JavaConversions, mutable}
import scala.collection.mutable.ArrayBuffer
import java.util

import com.system.online.datamanager.RedisClient

;

object DeepFMFeatureEng {
  def prt(): Unit ={
    print("nimabi");
  }
  /////////////////////////////////////////
  val NUMBER_PRECISION = 2

  val redisEndpoint = "localhost"
  val redisPort = 6379

  Logger.getLogger("org").setLevel(Level.ERROR)
  val conf = new SparkConf()
    .setMaster("local")
    .setAppName("featureEngineering")
    .set("spark.submit.deployMode", "client")
  val spark = SparkSession.builder.config(conf).getOrCreate()
  val redisClient = new Jedis(redisEndpoint, redisPort)

  def addSampleLabel(ratingSamples:DataFrame): DataFrame ={
//    ratingSamples.show(10, truncate = false)
//    ratingSamples.printSchema()
    val sampleCount = ratingSamples.count()
    ratingSamples.groupBy(col("rating")).count().orderBy(col("rating"))
      .withColumn("percentage", col("count")/sampleCount)
//      .show(100,truncate = false)

    ratingSamples.withColumn("label", when(col("rating") >= 3.5, 1).otherwise(0))
  }

  def addMovieFeatures(movieSamples:DataFrame, ratingSamples:DataFrame): DataFrame ={

    //add movie basic features
    val samplesWithMovies1 = ratingSamples.join(movieSamples, Seq("movieId"), "left")
    //add release year
    val extractReleaseYearUdf = udf({(title: String) => {
      if (null == title || title.trim.length < 6) {
        1990 // default value
      }
      else {
        val yearString = title.trim.substring(title.length - 5, title.length - 1)
        yearString.toInt
      }
    }})

    //add title
    val extractTitleUdf = udf({(title: String) => {title.trim.substring(0, title.trim.length - 6).trim}})

    val samplesWithMovies2 = samplesWithMovies1.withColumn("releaseYear", extractReleaseYearUdf(col("title")))
      .withColumn("title", extractTitleUdf(col("title")))
      .drop("title")  //title is useless currently

    //split genres
    val samplesWithMovies3 = samplesWithMovies2.withColumn("movieGenre1",split(col("genres"),"\\|").getItem(0))
      .withColumn("movieGenre2",split(col("genres"),"\\|").getItem(1))
      .withColumn("movieGenre3",split(col("genres"),"\\|").getItem(2))

    //add rating features
    val movieRatingFeatures = samplesWithMovies3.groupBy(col("movieId"))
      .agg(count(lit(1)).as("movieRatingCount"),
        format_number(avg(col("rating")), NUMBER_PRECISION).as("movieAvgRating"),
        stddev(col("rating")).as("movieRatingStddev"))
      .na.fill(0).withColumn("movieRatingStddev",format_number(col("movieRatingStddev"), NUMBER_PRECISION))


    //join movie rating features
    val samplesWithMovies4 = samplesWithMovies3.join(movieRatingFeatures, Seq("movieId"), "left")
//    samplesWithMovies4.printSchema()
//    samplesWithMovies4.show(10, truncate = false)

    samplesWithMovies4
  }

  val extractGenres: UserDefinedFunction = udf { (genreArray: Seq[String]) => {
    val genreMap = mutable.Map[String, Int]()
    genreArray.foreach((element:String) => {
      val genres = element.split("\\|")
      genres.foreach((oneGenre:String) => {
        genreMap(oneGenre) = genreMap.getOrElse[Int](oneGenre, 0)  + 1
      })
    })
    val sortedGenres = ListMap(genreMap.toSeq.sortWith(_._2 > _._2):_*)
    sortedGenres.keys.toSeq
  }}

  def addUserFeatures(ratingSamples:DataFrame): DataFrame ={
//    val samplesWithUserFeatures1 = ratingSamples
//      .withColumn(
//        "userPositiveHistory", collect_list(when(col("label") === 1, col("movieId")).otherwise(lit(null)))
//          .over(Window.partitionBy("userId").orderBy(col("timestamp")).rowsBetween(-100, -1))
//      )
//      .withColumn("userPositiveHistory", reverse(col("userPositiveHistory")))
//    samplesWithUserFeatures1.show(100, false)
    //
    val samplesWithUserFeatures = ratingSamples
      .withColumn("userPositiveHistory", collect_list(when(col("label") === 1, col("movieId")).otherwise(lit(null)))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1)))
      .withColumn("userPositiveHistory", reverse(col("userPositiveHistory")))
      .withColumn("userRatedMovie1",col("userPositiveHistory").getItem(0))
      .withColumn("userRatedMovie2",col("userPositiveHistory").getItem(1))
      .withColumn("userRatedMovie3",col("userPositiveHistory").getItem(2))
      .withColumn("userRatedMovie4",col("userPositiveHistory").getItem(3))
      .withColumn("userRatedMovie5",col("userPositiveHistory").getItem(4))
      .withColumn("userRatingCount", count(lit(1))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1)))
      .withColumn("userAvgReleaseYear", avg(col("releaseYear"))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1)).cast(IntegerType))
      .withColumn("userReleaseYearStddev", stddev(col("releaseYear"))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1)))
      .withColumn("userAvgRating", format_number(avg(col("rating"))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1)), NUMBER_PRECISION))
      .withColumn("userRatingStddev", stddev(col("rating"))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1)))
      .withColumn("userGenres", extractGenres(collect_list(when(col("label") === 1, col("genres")).otherwise(lit(null)))
        .over(Window.partitionBy("userId")
          .orderBy(col("timestamp")).rowsBetween(-100, -1))))
      .na.fill(0)
      .withColumn("userRatingStddev",format_number(col("userRatingStddev"), NUMBER_PRECISION))
      .withColumn("userReleaseYearStddev",format_number(col("userReleaseYearStddev"), NUMBER_PRECISION))
      .withColumn("userGenre1",col("userGenres").getItem(0))
      .withColumn("userGenre2",col("userGenres").getItem(1))
      .withColumn("userGenre3",col("userGenres").getItem(2))
      .withColumn("userGenre4",col("userGenres").getItem(3))
      .withColumn("userGenre5",col("userGenres").getItem(4))
      .drop("genres", "userGenres", "userPositiveHistory") //
    .filter(col("userRatingCount") > 1)

    samplesWithUserFeatures
  }

  case class RatingRecord(userId: String, movieId: String, rating: String, timestamp: String)

  def getNewFeatures(userId: String, movieId: String, spark: SparkSession, redisClient: Jedis): Unit = {
    // https://blog.csdn.net/shirukai/article/details/81085642
    ///////////////////////////////////////////////////////////////////////////
    val schema_rating = StructType(List(
      StructField("userId", StringType, true),
      StructField("movieId", StringType, true),
      StructField("rating", StringType, true),
      StructField("timestamp", StringType, true)
    ))
    val dataList1 = new util.ArrayList[Row]()
    ///////
    val schema_movie = StructType(List(
      StructField("movieId", StringType, true),
      StructField("title", StringType, true),
      StructField("genres", StringType, true),
    ))
    val dataList = new util.ArrayList[Row]()

    ///////
    var haveRecord: Int = 0;
    for ( x <- redisClient.keys("rating-user_" + userId + "-*").toArray()){
      val key = x.toString
      val mid = key.split("-")(2).split("_")(1)
      if (mid == movieId){
        haveRecord = 1
      }
      val rating = redisClient.hget(x.toString, "rating");
      val timestamp = redisClient.hget(x.toString, "timestamp");
      dataList1.add(
        Row(
          userId, mid,
          rating, timestamp,
        )
      )
      dataList.add(
        Row(
          mid,
          redisClient.hget("movie-" + mid, "title"),
          redisClient.hget("movie-" + mid, "genres")
        )
      )
    }

    if (haveRecord != 1){
      val now = new util.Date()
      dataList1.add(
        Row(
          userId, movieId,
          "6.0", now.getTime.toString//System.currentTimeMillis()
        )
      )
      dataList.add(
        Row(
          movieId,
          redisClient.hget("movie-" + movieId, "title"),
          redisClient.hget("movie-" + movieId, "genres")
        )
      )
    }
    val ratingSamples = spark.createDataFrame(dataList1, schema_rating)
//    ratingSamples.show()
    ////////////////////////////////////////////////////////////////////////
    val movieSamples = spark.createDataFrame(dataList,schema_movie) //
//    movieSamples.show()

    val ratingSamplesWithLabel = addSampleLabel(ratingSamples)
    val samplesWithMovieFeatures = addMovieFeatures(movieSamples, ratingSamplesWithLabel)
    val samplesWithUserFeatures = addUserFeatures(samplesWithMovieFeatures)

//    var rst = samplesWithUserFeatures.filter(
//      samplesWithUserFeatures("userId") === userId &&
//        samplesWithUserFeatures("movieId") === movieId
//    )

    var rst_1 = samplesWithUserFeatures.filter(
      samplesWithUserFeatures("userId") === userId &&
        samplesWithUserFeatures("movieId") === movieId
    ).withColumn(
      "movieRatingCount",
      when(
//        col("movieId").eq(movieId),
        col("movieId").equalTo(movieId),
        redisClient.hget("mf-" + movieId, "movieRatingCount")
      ).otherwise(col("movieRatingCount"))
    ).withColumn(
      "movieAvgRating",
      when(
        //        col("movieId").eq(movieId),
        col("movieId").equalTo(movieId),
        redisClient.hget("mf-" + movieId, "movieAvgRating")
      ).otherwise(col("movieAvgRating"))
    ).withColumn(
      "movieRatingStddev",
      when(
        //        col("movieId").eq(movieId),
        col("movieId").equalTo(movieId),
        redisClient.hget("mf-" + movieId, "movieRatingStddev")
      ).otherwise(col("movieRatingStddev"))
    )
//    rst.show()
//    rst_1.show()
//    for (x <- ){
//      print(x)
//    }
    rst_1.rdd.collect()(0)

  }

  def main(args: Array[String]): Unit = {
    getNewFeatures("1", "567", spark, redisClient)
  }

}
