---
layout:     post
title:      Linux下常用小工具、命令行
subtitle:   
date:       2019-02-28
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories:  
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/02/28/useful-linux-tool/>

本文记录一些比较有用的linux下的小工具和命令行，如无特殊说明，都是在Ubuntu下亲测可用的。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 小工具

## 1.1 查看系统信息

### 1.1.1 查看CPU信息
CPU全部信息：
cat /proc/cpuinfo
支持的指令集：
cat /proc/cpuinfo | grep flags

### 1.1.2 运行状态监视
* **indicator-sysmonitor**：可以监视CPU、内存占用率；网速；电池电量；IP；硬盘剩余大小。可以像下面这样显示在右上角状态栏，很方便。
  ![](/img/in_post/useful_linux_tool/indicator.png)
  安装方法：
  ```bash
  sudo add-apt-repository ppa:fossfreedom/indicator-sysmonitor  
  sudo apt-get update 
  sudo apt-get install indicator-sysmonitor   
  ```
* **radeontop**：可以监视AMD的GPU。
  安装方法：
  ```bash
  sudo apt install radeontop
  ```
* **nvidia-smi**：N卡自带的GPU监视器
  使用方法：
  ```bash
  watch -n 2 nvidia-smi
  ```
  其中`watch -n`表示刷新频率，2表示2秒刷新一次，表中的含义可以参考这个博客：[Linux查看GPU信息和使用情况](https://blog.csdn.net/dcrmg/article/details/78146797)
# 2. 命令行
## 2.1 文件管理
### 2.1.1 删除文件
* **删除相同后缀**：
示例：一次性删除某目录及其子目录下所有以.exe为后缀的文件。
`find . -name '*.exe' -type f -print -exec rm -rf {} \;`
说明：
find：使用find命令搜索文件，使用它的-name参数指明文件后缀名。
. :是当前目录，因为Linux是树形目录，所以总有一个交集目录，这里根据需要设置
'*.exe': 指明后缀名，*是通配符
" -type f : "查找的类型为文件
"-print" :输出查找的文件目录名
-exec: -exec选项后边跟着一个所要执行的命令，表示将find出来的文件或目录执行该命令。
注意：exec选项后面跟随着所要执行的命令或脚本，然后是一对儿{}，一个空格和一个\，最后是一个分号。
可以先运行前半部分，看是否是你想删除的再加`rm`。

* **删除空文件夹**：
`find -type d -empty `

### 2.1.2 文件格式转换

Windows下的文件格式（中文主要是gb2312）在Linux下（主要是UTF-8）有时候是会乱码的，`enca`这个命令行小工具可以帮助我们检测原来的文件格式是什么，还能帮我们进行格式转换

安装工具：

`sudo apt-get install enca`

用法：

`enca -L zh_CN file_path`：检查文件的编码

`enca -L zh_CN -x UTF-8 file_path`：将文件编码转换为`UTF-8`编码

`enca -L zh_CN -x UTF-8 < file1 > file2`：转换为`UTF-8`编码，并复制到新的文件。


# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
