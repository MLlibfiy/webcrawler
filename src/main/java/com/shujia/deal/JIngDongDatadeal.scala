package com.shujia.deal

import org.apache.spark.{SparkConf, SparkContext}

object JIngDongDatadeal {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("JIngDongDatadeal").setMaster("local[2]")

    val sc = new SparkContext(conf)

    val comment = sc.textFile("data/jingdong/comment/time=*")
    val info = sc.textFile("data/jingdong/info/time=*")

    info.repartition(1).foreach(println)

    comment.repartition(1).foreach(println)

    val infoRDD = info.map(line => (line.split("\t")(0), line))


    comment.map(line => (line.split("\t")(1), line)).join(infoRDD, 1)
      .map(x => {
        val comment = x._2._1.split("\t")
        var info = x._2._2

        val id = comment(0)
        val productId = comment(1)
        val score = comment(2)
        val nickname = comment(3)
        val productColor = comment(4)
        val productSize = comment(5)
        val userClientShow = comment(6)
        val userLevelName = comment(7)
        val content = comment(8)
        val referenceName = comment(9)
        val referenceTime = comment(10)

        info = info + "\t" + productColor + "\t" + productSize + "\t" + referenceName

        (info, comment)
      }).map(_._1).distinct().foreach(println)

  }
}
