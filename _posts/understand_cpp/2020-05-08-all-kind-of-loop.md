---
layout:     post
title:      C++各种循环方式梳理及对比
subtitle:   
date:       2020-05-08
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories: 深入理解C++
published: false
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2020/05/08/all-kind-of-loop/>

在学习的过程中发现C++有各种各样的循环方式，比如最基本的:

+ for
+ while

后面增加的：

+ [std::for_each](https://zh.cppreference.com/w/cpp/algorithm/for_each)
+ [基于范围的for循环](https://zh.cppreference.com/w/cpp/language/range-for)
+ [std::for_each_n](https://zh.cppreference.com/w/cpp/algorithm/for_each_n)
+ [std::transform](https://zh.cppreference.com/w/cpp/algorithm/transform)

这些循环方式各有特点，调用方式也不同。本文将整理他们的异同，并尝试比较他们的效率。很多情况下，程序80%的时间会被20%的代码消耗，而这20%的代码多为循环。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**



# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
