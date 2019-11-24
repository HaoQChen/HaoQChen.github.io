---
layout:     post
title:      Qt编译错误undefined vtable for mainwindow
subtitle:   
date:       2019-06-23
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories: 常见错误总结 
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/06/23/undefined-vtable-mainwindow/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 问题描述

Qt编译出现错误`undefined reference to ‘vtable for MainWindow'`

我是用CMake来构建Qt工程时出现了这个错误，直观意思是MainWindow的虚表没有定义，猜测是某些子类没有构建成功，无法链接。我这里已经按照官方的意思把

`set(CMAKE_AUTORCC ON)`
`set(CMAKE_AUTOUIC ON)`
`set(CMAKE_AUTOMOC ON)`
`set(CMAKE_PREFIX_PATH 、yourQtPath/5.10.1/gcc_64)`

等等都设置了，不至于不成功。

# 2. 解决办法

找到了几种可能导致这个error的问题：

1. 类的构造函数、析构函数没有进行定义（只在.h中声明没定义）
2. 头文件中出现了一些Qt的关键词，如`Q_OBJECT`、`signals`等，这时候要将头文件也放到`CMakeLists.txt`的`add_executable`中，不然不会将这些关键词编译，也就没有办法正确生成类了。如果使用Qt工程，头文件则要放到.pro文件的`HEADERS`中。

我是第二种。

# 参考

[“undefined reference to `vtable for …’ errors” in Qt derived classes](https://lizardo.wordpress.com/2009/04/24/undefined-reference-to-vtable-for-errors-in-qt-derived-classes/)

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
