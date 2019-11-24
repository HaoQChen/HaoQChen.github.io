---
layout:     post
title:      Failed to fetch http://packages.microsoft.com/repos/vscode/dists/stable/main/binary-amd64/Package
subtitle:   
date:       2019-03-21
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

本文持续更新地址：<https://haoqchen.site/2019/03/21/update-vscode-source-error/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 问题描述

`W: Failed to fetch http://packages.microsoft.com/repos/vscode/dists/stable/main/binary-amd64/Packages  Hash Sum mismatch`

`E: Some index files failed to download. They have been ignored, or old ones used instead.`

在Ubuntu下sudo apt-get update时出现了这个bug，但我本身其实没有安装vscode，不知道为什么会有这个源。

# 2. 解决办法

我选择直接删除这个list，不去fetch它了：

`cd /etc/apt/sources.list.d`
`sudo rm ./vscode.list`

然后再`sudo apt-get update`即可

# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
