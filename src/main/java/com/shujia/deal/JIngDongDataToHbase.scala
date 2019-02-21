package com.shujia.deal

import com.shujia.util.IKUtrl
import org.apache.spark.{SparkConf, SparkContext}

object JIngDongDataToHbase {


  /**
    * 需求：根据用户传入的关键字查询商品的基本信息返回给用户
    *
    *
    * 实现：
    * 1、对所有的商品描述建立索引表,hbae表
    * 2、将数据表存到hbase
    * 3、根据用户传入的关键字先查询索引表，根据索引表查询回来的商品id查询数据表
    *
    */

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local[4]").setAppName("JIngDongDataToHbase")
    val sc = new SparkContext(conf)
    val infoRDD = sc.textFile("data/jingdong/info")


    //对商品名字分词
    val splitWordRDD = infoRDD.flatMap(line => {
      val strs = line.split("\t")
      val id = strs(0)
      val name = strs(7)

      val words = IKUtrl.getStrs(name)

      val splits = name.split(" ").toList

      words.:::(splits).map(word => (word, id))
    })

    splitWordRDD
      .groupByKey()
      .map(kv => {
        val word = kv._1
        //对id去重
        val ids = kv._2.toList.distinct

        //根据词语查询之前的索引，将之前的所有和当前索引去重后写回到hbase


      })


  }
}
