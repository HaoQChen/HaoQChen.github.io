---
layout:     post
title:      ROS之rviz显示历史运动轨迹、路径的各种方法（visualization_msgs/Marker、nav_msgs/Path）
subtitle:   ROS学习之路
date:       2018-05-25
author:     白夜行的狼
header-img: img/in_post/ROS_show_trajectory/post-bg-infinity.jpg
catalog: true
categories: ROS实用小细节
tags:
    - visualization_msgs/Marker
    - rviz轨迹
    - ROS轨迹
    - 机器人轨迹路径
    - nav_msgs/Path
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/05/25/ROS-show-trajectory/>

　　在使用ROS进行机器人控制的时候，有时候会希望能够显示并且保留机器人的历史运动轨迹，比如最近在做行人跟踪，就希望能够保留多个行人的轨迹以及机器人的运动。本文将会介绍网上搜罗到的各种方法，并粗略比较一些优劣。

github地址：<https://github.com/HaoQChen/show_trajectory>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

喜欢的帮我github点个赞，点个关注呗～～～～

# 1. visualization_msgs/Marker
　　如名字所示，就是画出可视化的标志物。利用Marker有两种方法可以实现画出轨迹。相对于后面的方法来说，使用Marker可以有丰富的形状选择。首先看这个类包含的成员： 
```cpp
//各种标志物类型的定义，每一个的具体介绍和形状可以到这里查看：http://wiki.ros.org/rviz/DisplayTypes/Marker
uint8 ARROW=0//箭头
uint8 CUBE=1//立方体
uint8 SPHERE=2//球
uint8 CYLINDER=3//圆柱体
uint8 LINE_STRIP=4//线条（点的连线）
uint8 LINE_LIST=5//线条序列
uint8 CUBE_LIST=6//立方体序列
uint8 SPHERE_LIST=7//球序列
uint8 POINTS=8//点集
uint8 TEXT_VIEW_FACING=9//显示3D的文字
uint8 MESH_RESOURCE=10//网格？
uint8 TRIANGLE_LIST=11//三角形序列
//对标记的操作
uint8 ADD=0
uint8 MODIFY=0
uint8 DELETE=2
uint8 DELETEALL=3

Header header
string ns   //命名空间namespace，就是你理解的那样
int32 id    //与命名空间联合起来，形成唯一的id，这个唯一的id可以将各个标志物区分开来，使得程序可以对指定的标志物进行操作
int32 type  //类型
int32 action    //操作，是添加还是修改还是删除
geometry_msgs/Pose pose       # Pose of the object
geometry_msgs/Vector3 scale   # Scale of the object 1,1,1 means default (usually 1 meter square)
std_msgs/ColorRGBA color      # Color [0.0-1.0]
duration lifetime             # How long the object should last before being automatically deleted.  0 means forever
bool frame_locked             # If this marker should be frame-locked, i.e. retransformed into its frame every timestep

#Only used if the type specified has some use for them (eg. POINTS, LINE_STRIP, ...)
geometry_msgs/Point[] points//这个是在序列、点集中才会用到，指明序列中每个点的位置
#Only used if the type specified has some use for them (eg. POINTS, LINE_STRIP, ...)
#number of colors must either be 0 or equal to the number of points
#NOTE: alpha is not yet used
std_msgs/ColorRGBA[] colors

# NOTE: only used for text markers
string text

# NOTE: only used for MESH_RESOURCE markers
string mesh_resource
bool mesh_use_embedded_materials
```

## 1.1 使用lifetime实现
　　每次获取到机器人的位姿后，就在对应点发布一个标志，然后将lifetime设为0，也就是无限久地保存～～但是需要注意一点，让ns或者id变量每次都不一样，否则ns和id一直一样的话，后面的操作会覆盖前面的操作，也就一直只能看到最新的了。建议每次让id+=1。代码见marker.cpp，这个是稍微修改了[ROS官网Markers: Sending Basic Shapes (C++)](http://wiki.ros.org/rviz/Tutorials/Markers%3A%20Basic%20Shapes)的代码。大家不要被颜色形状什么的干扰～～～我只是懒得调。  
![lifetime](/img/in_post/ROS_show_trajectory/lifetime.png)  

## 1.2 使用标志序列或者点集实现
　　这个没啥好说的，程序都是copy[官网的教程](http://wiki.ros.org/rviz/Tutorials/Markers%3A%20Points%20and%20Lines)。但这个有个不好的是，如果时间比较久，需要保存一个很长的数组来存储历史轨迹的坐标。见marker_list.cpp
![point_set](/img/in_post/ROS_show_trajectory/point_set.png)  

# 2. nav_msgs/Path
　　这个功能是利用rviz中的Path类型实现的，只需要发布nav_msgs/Path类型的消息，然后在rviz上订阅该消息就可以显示轨迹路径。而nav_msgs/Path类型的数据很简单，就是一个位姿的集合。navigation功能包集中显示规划路径用的就是这个东西。

　　这个有点像Marker中的序列和点集一样，需要维护一个数组。在rviz中可以对路径的颜色、宽度、透明度等进行设置，另外可以设置显示箭头和坐标。最终显示的结果根Marker差不多，个人感觉是简单方便，不用想这么多。代码见path.cpp

```cpp
//nav_msgs/Path数据类型  
Header header  
geometry_msgs/PoseStamped[] poses  
//类型扩展：  
Header header  
    uint32 seq  
    time stamp  
    string frame_id  
geometry_msgs/PoseStamped[] poses  
    Header header  
        uint32 seq  
        time stamp  
        string frame_id  
    geometry_msgs/Pose pose  
        geometry_msgs/Point position  
            float64 x  
            float64 y  
            float64 z  
        geometry_msgs/Quaternion orientation  
            float64 x  
            float64 y  
            float64 z  
            float64 w
```

效果图： 

![nav_path](/img/in_post/ROS_show_trajectory/nav_path.png)  

# 3. 未完待续
看到github上一个开源项目，上面有更多可视化的图形～～～～有兴趣可以取看看：

[github上的rviz_visual_tools](https://github.com/PickNikRobotics/rviz_visual_tools)

据说nav_msgs/Odometry也可以～～没时间研究了

# 参考
<http://wiki.ros.org/rviz/Tutorials/Markers%3A%20Basic%20Shapes>  
<http://wiki.ros.org/rviz/Tutorials/Markers%3A%20Points%20and%20Lines>  
<https://blog.csdn.net/ktigerhero3/article/details/70256437>  

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**