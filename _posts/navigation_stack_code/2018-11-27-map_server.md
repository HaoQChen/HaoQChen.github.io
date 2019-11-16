---
layout:     post
title:      ROS Navigation之map_server完全详解
subtitle:   ROS学习之路之Navigation包解读
date:       2018-11-27
author:     白夜行的狼
header-img: img/in_post/map_server/black.jpeg
catalog: true
categories: ROS&nbsp;Navigation源码完全详解
tags:
    - map_server
    - map_saver
    - ROS Navigation
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/27/map_server/>

本文将介绍自己在看ROS的Navigation stack中的map\_server包源代码时的一些理解。作者的ROS版本是indigo，map\_server版本是1.12.13。如有错误，欢迎在评论中指正。

如果觉得写得还不错，就请收藏一下啦～～～也可以找一下我写的其他包的源码解读来看一下。关注一下我的专栏什么的。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. package.xml与CMakeLists.txt
**package**介绍中说，`mapserver提供了一个ROS节点，该节点通过一个ROS Service来提供地图数据，同时提供了一个命令行程序来动态地将生成的地图保存到文件中`。其依赖一些库，特别需要注意的是`sdl-image（用来加载地图图片）`、`yaml-cpp（配置中用到挺多yaml文件的）`和`tf`。

**CMakeLists**中定义生成以下：  
* image\_loader动态库，详见[第2章](#2)
* map\_server可执行程序，详见[第3章](#3)
* map\_saver可执行程序，详见[第4章](#4)
* 其余是test和安装的步骤，不是重点就不看了

# <a id="2">2. image_loader动态库<a/>
其实就是封装了一下`SDL_image`的功能写了一个`loadMapFromFile`函数。函数参数中会传进来地图的分辨率\[meters/pixel\]、`occ_th`（超过该值的像素为占据，归一化值）、`free_th`（低于为自由，归一化值）、`origin`（图像左下角的2D坐标，x、y、yaw，yaw是逆时针）。处理后最终将图片封装成`nav_msgs::GetMap::Response*`结构。  

该结构有三种表示方法。分别是Trinary，即占据（像素用100表示），free（像素用0表示）、不明（像素用-1表示）；Scale，占据与free与三值一样，但是不明变成了(0,100)；Raw，所有像素用[0, 255]表示。

# <a id="3">3. map\_server可执行程序<a/>
**调用形式：**  
`map_server <map.yaml>`，其中`map.yaml`是map\_saver中生成的地图描述文件，包括了resolution、图片名、原点信息、阈值等。  
除此之外也可以像下面这样调用，但不建议：  
`map_server <map> <resolution>`。map是图片名字，这样子直接跳过了描述文件，不建议。  

主要流程：  
1. 在main函数中定义了一个`MapServer`对象。在该对象的构造函数中，通过描述文件和ROS参数服务器获得地图相应参数后，调用[image\_loader动态库][image\_loader动态库]中的`loadMapFromFile`函数将地图加载到私有成员`nav_msgs::GetMap::Response map_resp_`中。  

2. 然后提供一个名为`static_map`的服务，回调函数是`MapServer::mapCallback`。关于ROS服务器和客户端是什么，不懂的可以看ROS教程[编写简单的服务器和客户端 (C++)](http://wiki.ros.org/cn/ROS/Tutorials/WritingServiceClient%28c%2B%2B%29)。该服务器做的就是将地图`map_resp_`深拷贝给客户端。amcl中就是通过这个服务获得地图的

3. 接着发布一个内容为`nav_msgs::MapMetaData`，名为`map_metadata`的话题。  
```cpp
time map_load_time
float32 resolution
uint32 width
uint32 height
geometry_msgs/Pose origin
```
`nav_msgs::MapMetaData`的信息如上，应该只是一些地图的基本信息，查找了一下，基本没人订阅这个话题，除了一个test。

4. 最后发布一个内容为`nav_msgs::OccupancyGrid`，名为`map`的话题，并将加载到的`map_resp_.map`发布上去。  
```cpp
std_msgs/Header header
nav_msgs/MapMetaData info
int8[] data
```
`nav_msgs::OccupancyGrid`的信息如上。就是地图了。查了一下发现，GMapping中也会往`map`这个话题发布消息。除了一些test节点，目前只发现amcl中有在一定条件下订阅`map`这个话题。然而据我了解，amcl中实际也没有订阅话题，而是直接通过上述的服务器来获得地图的。

# <a id="4">4. map\_saver可执行程序<a/>
**调用形式：**  
`map_saver [-f <mapname>] [ROS remapping args]"`，比如想将GMapping中生成的地图保存下来，可以：  
`rosrun map_server map_saver -f ~/robot_ws/map/gmapping`

main函数中定义了一个`MapGenerator`类对象，该类初始化之后订阅`map`话题。在订阅的回调函数中，将订阅得到的map按照一定格式保存到当地的.pgm文件，同时将地图信息保存到对应的.yaml文件中。

需要注意的是，如果你是想保存Cartographer生成的地图，是需要对源代码做一些修改的。因为Cartographer的map格式跟GMapping中的格式不太一样。具体不一样如下：

| point type | GMapping value | Cartographer value |
|:----:|:----:|:----:|
| free | 0 | 0-N |
| occupied | 100 | M-100 |
| unknown | -1 | -1 & N-M |
我按照这个不同对map_server包做了一些修改，详情看github：<https://github.com/HaoQChen/map_server>。如果觉得有用，记得star一下哦。

# 参考
* [map_server官网](http://wiki.ros.org/map_server)

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**
  
**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
