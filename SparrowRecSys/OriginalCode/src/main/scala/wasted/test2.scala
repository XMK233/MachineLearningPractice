object test2 {

  def main(args: Array[String]): Unit = {
    val lines = List("hadoop hive spark scala","spark hive habase",
      "hive spark java")
    //数据转换
    val mappedWords = lines.flatMap(_.split(" ").map(_.trim)).filterNot(_
      .isEmpty).map((_,1))
    println("---------------输出分割后的值-----------------")
    println(mappedWords)
    //根据数据进行分组
    val groupedWords: Map[String, List[(String, Int)]] = mappedWords.groupBy(tuple=>tuple._1)
    //每组进行数据计算
    println("---------------输出分组后的值-----------------")
    println(groupedWords)

    val result = groupedWords.map(tuple=>{
      //获得Word单词（key）
      val word = tuple._1
      //计算该Word对应的数量（value）
      val count = tuple._2.map(t=>t._2).sum
      //返回结果
      (word,count)
    })
    println("---------------输出合并后的值-----------------")
    println(result)
    println("---------------转换成list的值-----------------")
    println(result.toList)
  }

}

