package com.shujia.deal;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.StringReader;

public class Test {
    public static void main(String[] args) throws Exception {
        String text = "荣耀畅玩8A 6.09英寸珍珠全面屏 震撼大音量 3GB+64GB 幻夜黑 移动联通电信4G全面屏手机 双卡双待";

        //创建分词对象

        Analyzer anal = new IKAnalyzer(true);
        StringReader reader = new StringReader(text);
        //分词
        TokenStream ts = anal.tokenStream("", reader);
        CharTermAttribute term = ts.getAttribute(CharTermAttribute.class);
        //遍历分词数据
        ts.reset();
        while (ts.incrementToken()) {
            if (term.toString().length()!=1){
                System.out.print(term.toString().toUpperCase() + "|");
            }

        }
        ts.close();
        reader.close();
        System.out.println();
    }
}
