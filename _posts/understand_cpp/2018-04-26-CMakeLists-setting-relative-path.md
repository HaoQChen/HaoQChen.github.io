---
layout:     post
title:      ROS CMakeLists中target_link_libraries相对路径设置
subtitle:   ROS学习之路
date:       2018-04-26
author:     白夜行的狼
header-img: img/about-bg-walle.jpg
catalog: true
categories: C++深入浅出
tags:
    - ROS
    - CMakeLists
    - target_link_libraries
    - link_directories
    - 相对路径
--- 
本文持续更新地址：<https://haoqchen.site/2018/04/26/CMakeLists-setting-relative-path/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

先看我的CMakeLists文件：
```cmake
link_directories(libs/X64)

add_executable(${PROJECT_NAME} 
    src/play_audio.c 
    src/awaken.c
)
add_executable(show_order
    src/test_listener.cpp
)

target_link_libraries(${PROJECT_NAME}
    ${catkin_LIBRARIES}
    libmsc.so
    libasound.so
 )

target_link_libraries(show_order
    ${catkin_LIBRARIES}
)
```

因为我这里用到了科大讯飞的一个链接库 libmsc.so，放到了我package目录下的libs/X64文件夹下，出于移植的考虑，不想使用绝对路径。所以这里使用link_directories添加相对路径的目录，然后在target_link_libraries中添加库目录名字。

**注意：**
1. **link_directories必须要放到add_executable前面，因为这个命令只对后续命令生效。**
2. **ROS官网建议不要使用link_directories，直接放在target_link_libraries中。我试过很多次，这样的话无法使用相对路径。不知道为何**

**参考：**
[ROS官网的CMakeLists文档](http://wiki.ros.org/catkin/CMakeLists.txt)
[参考博客](https://blog.csdn.net/pbe_sedm/article/details/8826001)

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
