import org.apache.spark.sql.SparkSession
import org.apache.log4j.Logger
import org.apache.log4j.Level

object SimpleApp {
  def main(args: Array[String]) {

    Logger.getLogger("org").setLevel(Level.OFF)
    Logger.getLogger("akka").setLevel(Level.OFF)

    val logFile = "D:\\MachineLearningPractice\\SparrowRecSys\\OriginalCode\\src\\main\\scala\\heheda.txt" // Should be some file on your system
    val spark = SparkSession.builder.appName("Simple Application")
      .config("spark.master", "local")
      .getOrCreate()
    val logData = spark.read.textFile(logFile).cache()
    val numAs = logData.filter(line => line.contains("a")).count()
    val numBs = logData.filter(line => line.contains("b")).count()

    println(s"Lines with a: $numAs, Lines with b: $numBs")
    spark.stop()
  }
}