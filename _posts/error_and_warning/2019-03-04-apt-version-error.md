---
layout:     post
title:      Ignoring Provides line with DepCompareOp for package gdb-minimal
subtitle:   
date:       2019-03-04
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

本文持续更新地址：<https://haoqchen.site/2019/03/04/apt-version-error/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 问题描述
Ubuntu1404下运行`sudo apt-get update`出现warning`Ignoring Provides line with DepCompareOp for package gdb-minimal`

# 2. 解决办法

经过查找后发现是因为系统的apt版本太低，导致一些包安装不了，需要更新apt。

![](/img/in_post/apt_version_error/apt_error.png)

但这个warning是影响不大的，如果不必要，最好还是不要更新apt

# 参考
<https://askubuntu.com/questions/946402/apt-get-update-warning-ignoring-provides-line-with-depcompareop-for-package>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
