package com.shujia.deal;

import com.shujia.util.IKUtrl;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.StringReader;

public class Test {
    public static void main(String[] args) throws Exception {
        //加密后的字符串
        String encodeStr = DigestUtils.md5Hex("数加");
        System.out.println("MD5加密后的字符串为:encodeStr=" + encodeStr.toUpperCase());
    }
}
