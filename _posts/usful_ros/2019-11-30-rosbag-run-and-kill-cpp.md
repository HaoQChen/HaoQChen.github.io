---
layout:     post
title:      用CPP控制rosbag record的运行和关闭
subtitle:   
date:       2019-11-30
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

本文持续更新地址：<https://haoqchen.site/2019/11/30/rosbag-run-and-kill-cpp/>

我们经常会用rosbag来录一些ROS的消息进行离线调试什么的。如果是在终端运行，输入命令，然后`Ctrl + C`就可以运行和关闭了，但如果我想在C++程序里面去控制什么时候录包，什么时候停止录包呢？

这篇文章对以上的情形进行总结。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 终端操作

终端录包的指令可以参考[ROS官网rosbag的介绍](http://wiki.ros.org/rosbag/Commandline#record)。这里以最简单的情形为例，录`/top2record`话题的数据，将其放到当前文件夹的`bag_name.bag`：

```bash
rosbag record -O ./bag_name.bag /top2record
```

录完只要`Ctrl + C`就可以了。

# 2. CPP操作
rosbag提供了官方的CPP API，但是看着很难用，没有用熟了的命令行那么好用，所以这里是通过CPP启动终端运行命令行，而不是真的rosbag的官方API。

请注意代码中的空格。

**录包：**
```cpp
std::string path = "./bag_name.bag";
std::string topics = " /top2record";
std::string node_name = " __name:=my_record_node";
std::string cmd_str = "gnome-terminal -x bash -c 'rosbag record -O " + path + topics + node_name + "'";
int ret = system(cmd_str.c_str()); // #include <stdlib.h>
```
这样就会弹出一个终端进行录包。这里之所以要通过`__name:=`加节点名称，是为了方便后面关闭，否则就只能用`killall`来杀掉所有record，如果没有这个进程会报错不说，还会因为没有正确关闭节点得到不正确的bag文件（`killall`没有发送终止命令给节点，即没有`Ctrl + C`）。

**停止录包：**
```cpp
#include <ros/ros.h>

ros::V_string v_nodes;
ros::master::getNodes(v_nodes);

std::string node_name = std::string("my_record_node");
auto it = std::find(v_nodes.begin(), v_nodes.end(), node_name.c_str());
if (it != v_nodes.end()){
    std::string cmd_str = "rosnode kill " + node_name;
    int ret = system(cmd_str.c_str());
    std::cout << "## stop rosbag record cmd: " << cmd_str << std::endl;
}
```
这样刚才那个弹框就会消失，录包成功。这里先利用ROS master来判断是否存在这个录包节点，如果存在，调用`rosnode kill`来终止这个node。

如果存在`namespace`请在名字中加上相应前缀`std::string ns = nh_->getNamespace() + std::string("/");`

# 参考

<https://answers.ros.org/question/275441/start-and-kill-rosbag-record-from-bash-shell-script/>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
