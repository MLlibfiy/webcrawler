package com.shujia.producer

import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Durations, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}

object JingDongCommentStreaming {
  def main(args: Array[String]): Unit = {


    /**
      *
      * 读取kafka数据
      *
      *
      *
      */

    val conf = new SparkConf().setAppName("JingDongCommentStreaming").setMaster("local[2]")

    val sc = new SparkContext(conf)

    val ssc = new StreamingContext(sc, Durations.seconds(5))


    val DS = KafkaUtils.createStream(
      ssc,
      "node1:2181,node2:2181,node3:2181",
      "JingDongCommentStreaming",
      Map("jingdong_comment" -> 1) //1  接收数据的并行读
    )

    DS.map(_._2)
      .foreachRDD(rdd => {
        val basePath = "E:\\第二期\\大数据\\项目\\网络爬虫\\webcrawler\\data\\jingdong\\comment_tmp\\"
        val time = System.currentTimeMillis().toString.substring(0, 10)
        val path = basePath + "time=" + time
        rdd.saveAsTextFile(path)
      })


    ssc.start()
    ssc.awaitTermination()
    ssc.stop()


  }
}
