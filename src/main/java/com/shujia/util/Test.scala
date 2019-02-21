package com.shujia.util

object Test {
  def main(args: Array[String]): Unit = {
   val l1 = List(1,2,3)
   val l2 = List(4,5,6)

    print(l1.:::(l2))
  }
}
