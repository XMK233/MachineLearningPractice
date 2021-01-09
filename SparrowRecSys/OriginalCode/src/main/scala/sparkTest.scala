import org.apache.log4j.{Level, Logger}

object sparkTest{
  def main(args: Array[String]): Unit = {

    Logger.getLogger("org").setLevel(Level.OFF)
    Logger.getLogger("akka").setLevel(Level.OFF)

    // about how to import, refer to this: https://stackoverflow.com/questions/59903993/cannot-resolve-symbol-read-in-org-apache-spark-read
    import org.apache.spark.sql.SparkSession
    val spark : SparkSession = SparkSession.builder
      .appName("test")
      .master("local[2]") // 我估计这个是为了在单机上跑spark, 才要设置的.
      .getOrCreate()
    import spark.implicits._

    val textFile = spark.read.textFile("D:\\MachineLearningPractice\\SparrowRecSys\\OriginalCode\\src\\main\\scala\\heheda.txt")
    val wordCounts = textFile.flatMap(line => line.split(" ")).groupByKey(identity).count()

    // 这是一个元组. 参考了 https://www.runoob.com/scala/scala-tuples.html
    // 来遍历元组.
    wordCounts.collect().foreach{ i => println("Value = " + i )}
  }
}