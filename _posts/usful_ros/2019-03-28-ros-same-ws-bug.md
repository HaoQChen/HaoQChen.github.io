---
layout:     post
title:      ROS多个工作空间存在同名包的BUG
subtitle:   
date:       2019-03-28
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories: ROS实用小细节 
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/03/28/ros-same-ws-bug/>

为了测试方便，我有多个工作空间。不同工作空间会存在一些同名的包。按照[官网教程](http://wiki.ros.org/cn/ROS/Tutorials/InstallingandConfiguringROSEnvironment)的说法，只要source了setup就可以将当前工作空间设置为ROS顶层。一天在测试的时候发现，并不能通过修改`.bashrc`来修改当前活跃的工作空间。之前source的工作空间仍然存在，一直调用的是之前的工作空间的包。

![](/img/in_post/ros_same_ws_bug/my_source.png)

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 问题描述
查看你当前的ROS包路径：
```bash
echo $ROS_PACKAGE_PATH
```
输出：
`/home/night_fury/robot_ws/src:/home/night_fury/catkin_ws/src:/home/night_fury/JDD_ws/src/cartographer_ros/cartographer_rviz:/home/night_fury/JDD_ws/src/cartographer_ros/cartographer_ros:/home/night_fury/JDD_ws/src/cartographer_ros/cartographer_ros_msgs:/opt/ros/indigo/share:/opt/ros/indigo/stacks`

会输出你所有的ROS工作空间路径，如果有同名的包，则调用顺序为`echo $ROS_PACKAGE_PATH`显示的顺序。
像我这里，一直调用的是robot_ws空间的包，无法调用catkin_ws的包，哪怕我已经按照前面那样子吧robot_ws注释掉了。

甚至我删掉`ROS_PACKAGE_PATH`变量再重新source仍然无效，`ROS_PACKAGE_PATH`仍然会重新变为所有的工作空间。应该是catkin_ws中的setup.bash文件被污染了，导致了明明只source `catkin_ws`工作空间，但实际`source`所有的工作空间。这应该是一个bug。

# 2. 解决办法
1. 删掉`build`和`devel`文件夹
2. 删掉`ROS_PACKAGE_PATH`环境变量：`unset ROS_PACKAGE_PATH`
3. 重新编译你的包
4. 注释掉`~/.bashrc`中无关的包的bash，只保留想要的工作空间，如图一。
5. `source ~/.bashrc`

完成以上五步就可以实现多个工作空间的分离，调用同名的包了。

# 参考
<http://wiki.ros.org/cn/ROS/Tutorials/InstallingandConfiguringROSEnvironment>
<https://blog.csdn.net/moondog123/article/details/88432341>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
