---
layout:     post
title:      C++字符串处理总结（char、string）
subtitle:   磨刀不误砍柴工
date:       2018-09-09
author:     白夜行的狼
header-img: img/in_post/string_and_char/black.jpeg
catalog: true
tags:
    - char
    - string
    - 字符串
    - 总结
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.github.io/2018/09/09/string-and-char/>

C++字符串处理有最原始的char以及string两种方式，这里对两种方式常用的功能进行总结及对比。

如果觉得还不错就收藏一下呗，博主会长期更新自己的学习和收获。
|               |        string          |         char*、char[]        |
|------|------|------|
|头文件|#include \<string>|不需要|
|定义与初始化|string s1("abc");<br>string s2(s1);<br>string s3(4, 's');//初始化为4个's'|char* a = "test";//数据存在静态存储区，不能修改<br>char a[] = "test";//开辟数组再存储，可以修改<br>char* a = new char[10];<br>memset(a, '0', sizeof(char)*10);|
|相互转化|char* p = "hello";<br>string s(p);<br>s = p;|string str("test");<br>const char* p = str.data();//记得要加const或者强制类型转换成(char*)<br>const char* p = str.c_str();<br>char p[10];<br>std::size_t length = str.copy(p,5,0);//从第0个开始复制5个，返回有效复制的数量，需要在p最后添加'\0'<br>char * cstr = new char [str.length()+1];<br>std::strcpy (cstr, str.c_str());<br>或者逐个复制|
||||
||||
||||
||||
||||
||||
||||
||||
||||
||||
||||
||||
||||
||||
||||


# 参考
**版权声明：未经允许不得以任何形式转载**
