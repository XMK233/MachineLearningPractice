import org.apache.spark

object test3 {
  def main(args: Array[String]): Unit = {

    import org.apache.spark.sql.SparkSession
    val spark : SparkSession = SparkSession.builder
      .appName("test")
      .master("local[2]")
      .getOrCreate()
    import spark.implicits._

    val fp = "wordcount.txt"
    val ds = spark.read.textFile(fp)

    val words = ds.flatMap(line => line.split(" "))

    val wordCounts = words.groupByKey(identity).count()

    
  }

}
