---
layout:     post
title:      Ubuntu（Linux）下更新CMake，最安全的更新
subtitle:   
date:       2019-03-13
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

本文持续更新地址：<https://haoqchen.site/2019/03/13/update-cmake/>

本文将介绍一种在Ubuntu系统下快速升级CMake到指定版本的方法。之前找了很多方法，要么需要删除原来的版本，如果安装不成功会非常危险，之前的编译环境都没了。另外就是ppa的更新，我试了也不行。本文介绍的方法只需要下载安装包，然后改一下CMake的链接即可。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 更新cmake

各版本安装包下载地址：<https://cmake.org/files/>

1. **下载**
首先到上面的地址下载相应版本安装包，注意需要是Linux-x86_x64一类后缀的版本，这个是已经针对Linux环境编译好的二进制包。比如我这里下载`cmake-3.6.0-Linux-x86_64.tar.gz`。

2. **解压**
直接右键解压或者命令行～～～然后将文件夹放置到你平时的安装目录，建议是home目录下建一个applications的文件夹，放在里面。

3. **找到并替换**
在命令行输入`which cmake`，可以看到你的cmake安装位置，默认为`/usr/bin/cmake`。这里将其剪切到桌面备份`sudo mv /usr/bin/cmake ~/Desktop`。

然后为刚才解压的文件夹下的bin目录下的cmake创建软连接

` sudo ln -s /home/trobot/aplications/cmake-3.6.0-Linux-x86_64/bin/cmake /usr/bin/cmake`

注意这里一定要用绝对路径，不能用相对路径，不然不行。

然后运行`cmake --version`，cmake版本就变成你想要的版本啦。

* **更新后注意**
这里提醒一下，之前安装的一些包会将自己的cmake配置放在`/usr/share/cmake-2.8/Modules`下，这些配置是你在使用find_packages命令时查找的，更新后并不会将其复制到新目录，会出现一些找不到对应`.cmake`的情况，比如我就出现了`Eigen3`找不到的情况，这里可以用同样的方法，创建软连接到我们自己的模块文件夹下：
`ln -s /usr/share/cmake-2.8/Modules/FindEigen3.cmake /home/trobot/aplications/cmake-3.6.0-Linux-x86_64/share/cmake-3.6/Modules/FindEigen3.cmake`


# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
