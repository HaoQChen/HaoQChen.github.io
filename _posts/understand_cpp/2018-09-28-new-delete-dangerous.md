---
layout:     post
title:      C++的new、delete需要注意的一点：使用危险函数导致的越界
subtitle:   深入理解C++
date:       2018-09-28
author:     白夜行的狼
header-img: img/in_post/new_delete_dangerous/404-bg.jpg
catalog: true
categories: C++深入浅出
tags:
    - 危险函数
    - 数组越界
    - new
    - delete
    - 安全函数
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/09/28/new-delete-dangerous/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

这里假设大家都知道怎么用new和delete来进行堆空间的申请和释放。这种错误比较难发现，希望大家引以为鉴。

如果觉得还不错就关注一下呗，博主会长期更新自己的学习和收获。

# 1. new、delete需要注意的一个特性
正常情况new一个数组之后，用delete释放是没有问题的。但是当对new得到的堆区进行越界的写入操作（读操作不会）将会导致delete时出现段错误，无法进行删除。如下面的程序所示：

```cpp
//正常操作，delete正常进行，程序运行正常
char* data = new char[10];
data[N-1] = 0x0;
delete[] data;

//越界读操作，delete正常进行，程序运行正常，但是不建议进行这种越界操作。
char* data = new char[10];
char temp = data[N];
delete[] data;

//越界写入，将导致delete操作失败，程序中断
char* data = new char[10];
data[N] = 0x0;
delete[] data;
```
![debug_error](/img/in_post/new_delete_dangerous/debug_error.png)

# 2. C语言自带的危险函数
[C语言中的危险函数（危险函数介绍博客）](https://blog.csdn.net/Subifuchen/article/details/78908465)

我是在做华为的面试题时用到了一个危险函数，导致了越界写入，然后delete失败。那什么是危险函数呢，简单地说就是有一些字符串处理函数、输入输出流函数，它没有进行越界检测，哪怕被写入数组已经越界仍然会继续写入。举个例子，比如

char* strcpy(char* dest, char* src);

这个函数是从src地址开始且含有'\0'结束符的字符串复制到以dest开始的地址空间，返回dest的指针。如果dest指向的内存没有足够大小去存放src字符串怎么办？strcpy函数可不管这些，它会继续进行复制，霸道的进行越界写入！

现在问题已经很清楚了吧，如果你对了new到的堆使用了危险函数，将导致段错误。当然，如果是直接声明存放在栈区的数组进行这样的越界操作，也会导致如下错误

![runtime_error](/img/in_post/new_delete_dangerous/runtime_error.png)

另外再说一个比较奇葩的情况： 

scanf("%x", data);//16进制输入

该函数是默认输入一个int型的数的，而不是像cin那样自动检测数据类型？比如输入“0x01”，该函数将会直接修改4个字节而不是只修改一个字节（我这里是64位机器）。
//data[0] = 0x01
//data[1] = 0x00
//data[2] = 0x00
//data[3] = 0x00

我写代码的时候就是在这里被坑了~~~~导致了数组越界。

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
