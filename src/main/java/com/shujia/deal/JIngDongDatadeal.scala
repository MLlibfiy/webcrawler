package com.shujia.deal

import org.apache.spark.{SparkConf, SparkContext}

object JIngDongDatadeal {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("JIngDongDatadeal").setMaster("local[4]")

    val sc = new SparkContext(conf)

    var comment = sc.textFile("data/jingdong/comment_tmp/time=*")
    val info = sc.textFile("data/jingdong/info_tmp/time=*")


    comment = comment.cache()

    val commentRDD = comment.map(line => (line.split("\t")(1), line))

    val infoRDD = info.map(line => (line.split("\t")(0), line))


    //关联评价表和基本信息表，不全基本信息表的数据

    val joinRDD = commentRDD.join(infoRDD, 1)

    //获取基本信息数据
    joinRDD.map(x => {
      val comment = x._2._1.split("\t")
      val info = x._2._2
      val productColor = comment(4)
      val productSize = comment(5)
      val name = comment(9)
      info + "\t" + productColor + "\t" + productSize + "\t" + name
    }).distinct().saveAsTextFile("data/jingdong/info/")


    //删除评价数据里面冗余的字段
    comment.map(line => {
      val commentStr = line.split("\t")
      val id = commentStr(0)
      val pid = commentStr(1)
      val score = commentStr(2)
      val nickname = commentStr(3)
      val userClientShow = commentStr(6)
      val userLevelName = commentStr(7)
      val content = commentStr(8)
      val referenceTime = commentStr(10)

      id + "\t" + pid + "\t" + score + "\t" + nickname + "\t" + userClientShow + "\t" + userLevelName + "\t" + content + "\t" + referenceTime
    }).repartition(1).saveAsTextFile("data/jingdong/comment/")


  }
}
