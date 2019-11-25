---
layout:     post
title:      fatal err Eigen/Dense No such file or directory
subtitle:   
date:       2019-03-26
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

本文持续更新地址：<https://haoqchen.site/2019/03/26/eigen-directory-error/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 问题描述

`fatal err Eigen/Dense No such file or directory`

除了Eigen/Dense，unsupported/Eigen/FFT、Eigen/Core也是一样的道理

自己在编译一个程序的时候遇到了这个问题。搜索网上的一些答案，很多都说得不详，或者解决办法不好。最后找到了stackoverflow的一个问题，终于解决了，在此分享一下，避免大家走弯路。有帮助到你的话点个赞或者关注呗～～～

# 2. 解决办法

究其原因，就是编译器找不到这个头文件了，首先要确保你已经安装了Eigen3.

Eigen其实只是一个纯头文件的库，你直接安装放到include目录就好。

到[官网](http://eigen.tuxfamily.org/index.php?title=Main_Page)下载一个稳定的版本,然后解压放到`/usr/local/include`或者`/usr/include`目录即可。

或者通过apt安装：`sudo apt-get install libeigen3-dev`。

出现这个问题主要是因为eigen3的文件结构导致的：

![](/img/in_post/eigen_directory_error/eigen_file_constructure.png)

如图，编译器会直接去`/usr/local/include`或者`/usr/include`目录找头文件，但是找到的是eigen3，并没有Eigen和unsupported。所以我们可以建立一个软连接到这两个文件夹。

```bash
#要先确定你的Eigen安装在/usr/local/include还是/usr/include
cd /usr/local/include
sudo ln -sf eigen3/Eigen Eigen
sudo ln -sf eigen3/unsupported unsupported
```
修改完后即可。

# 参考
<https://stackoverflow.com/questions/23284473/fatal-error-eigen-dense-no-such-file-or-directory>


<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
