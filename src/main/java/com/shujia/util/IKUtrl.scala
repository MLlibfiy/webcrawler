package com.shujia.util

import java.io.StringReader

import org.apache.lucene.analysis.Analyzer
import org.apache.lucene.analysis.TokenStream
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute
import org.wltea.analyzer.lucene.IKAnalyzer

import scala.collection.mutable.ListBuffer

object IKUtrl {

  /**
    * 分词工具类
    *
    * @param line
    */
  def getStrs(line: String): List[String] = {

    val list = new ListBuffer[String]
    //创建分词对象
    val anal = new IKAnalyzer(true)
    val reader = new StringReader(line)
    //分词
    val ts = anal.tokenStream("", reader)
    val term = ts.getAttribute(classOf[CharTermAttribute])
    //遍历分词数据
    ts.reset()
    while (ts.incrementToken) {
      if (term.toString.length != 1) {
        list.+=(term.toString)
      }
    }

    ts.close()
    reader.close()

    list.toList

  }

}
