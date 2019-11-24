---
layout:     post
title:      rosrun tab 出错
subtitle:   
date:       2019-06-24
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

本文持续更新地址：<https://haoqchen.site/2019/06/24/rosrun-tab-error/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 问题描述

运行rosrun然后tab补全时出现错误：

`rosrun rob[rospack] Warning: error while crawling boost::filesystem::status: Permission denied .gvfs`

# 2. 解决办法

```bash
sudo umount ~/.gvfs
rm -rf .gvfs/
```



# 参考

<http://answers.ros.org/question/76896/permission-denied-gvfs/>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
