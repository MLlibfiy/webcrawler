package com.shujia.deal

import com.shujia.util.{HBaseDAOImp, IKUtrl}
import org.apache.commons.codec.digest.DigestUtils
import org.apache.hadoop.hbase.CellUtil
import org.apache.hadoop.hbase.client.Put
import org.apache.hadoop.hbase.util.Bytes
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
      val name = strs(8)

      val words = IKUtrl.getStrs(name)

      val splits = name.split(" ").toList

      words.:::(splits).map(word => (word, id))
    })


    //保存索引数据
    splitWordRDD
      .filter(_._1.nonEmpty)
      .groupByKey()
      .foreachPartition(i => {

        val dao = new HBaseDAOImp()

        i.foreach(kv => {
          val word = kv._1
          //对id去重
          var ids = kv._2.toList.distinct
          //根据词语查询之前的索引，将之前的所有和当前索引去重后写回到hbase

          val md5Word = DigestUtils.md5Hex(word).toUpperCase
          val result = dao.getOneRow("index", md5Word)
          if (!result.isEmpty) {
            val cell = result.listCells().get(0)
            val lastIds = Bytes.toString(CellUtil.cloneValue(cell)).split("_").toList
            ids = ids.:::(lastIds)
          }

          val idsStr = ids.distinct.mkString("_")

          val put = new Put(md5Word.getBytes())
          put.add("info".getBytes(), "ids".getBytes(), idsStr.getBytes())
          dao.save(put, "index")
        })
      })


    //保存商品详细信息
    infoRDD.foreachPartition(lines => {

      val dao = new HBaseDAOImp()

      lines.foreach(line => {
        val info = line.split("\t")
        val id = info(0)
        val price = info(1)
        val StockStateName = info(2)
        val vender = info(3)
        val website = info(4)
        val url = info(5)
        val productColor = info(6)
        val productSize = info(7)
        val name = info(8)
        val put = new Put(id.getBytes())
        put.add("info".getBytes(), "price".getBytes(), price.getBytes)
        put.add("info".getBytes(), "StockStateName".getBytes(), StockStateName.getBytes)
        put.add("info".getBytes(), "vender".getBytes(), vender.getBytes)
        put.add("info".getBytes(), "website".getBytes(), website.getBytes)
        put.add("info".getBytes(), "url".getBytes(), url.getBytes)
        put.add("info".getBytes(), "productColor".getBytes(), productColor.getBytes)
        put.add("info".getBytes(), "productSize".getBytes(), productSize.getBytes)
        put.add("info".getBytes(), "name".getBytes(), name.getBytes)

        dao.save(put, "item_info")

      })
    })


  }
}
