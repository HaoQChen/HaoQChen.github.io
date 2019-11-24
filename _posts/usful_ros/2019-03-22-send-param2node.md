---
layout:     post
title:      ROS向节点传递参数的方法总结（rosrun，launch） + （参数服务器，main函数参数）
subtitle:   
date:       2019-03-22
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

本文持续更新地址：<https://haoqchen.site/2019/03/22/send-param2node/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

ROS的节点有很多中调用方式，包括rosrun，launch，直接运行等，向节点内传递参数的方式也有很多，在此做个总结。

# 1. rosrun + 参数服务器传递
```cpp
ros::init(argc, argv, "imu2txt");
ros::NodeHandle nh("~");
std::string file_name;
nh.param<std::string>("file_name", file_name, "./imu_data.txt");
```
首先在节点初始化之后获取参数服务器的参数，并设置初始值，如上面的程序就是在参数服务器的`～`空间（即节点本身）获取名字为`"file_name"`的参数放到`std::string file_name`中，默认参数为后面那个。

接着就可以rosrun了。下面是命令
`rosrun package node _parameter:=value`

在我们这里就是`rosrun datatxt imu2txt _file_name:=~/Documents/test.txt`就可以将节点内的参数改为想要的值了。

**注意:** string不需要加双引号，string第一个字符不能是数字

# 2. roslaunch + 参数服务器传递
同样是上面的例子，我们如果想通过roslaunch来调用的话，可以像下面这样，将参数放在node之间。
```xml
<launch>
    <node name="imu2txt" pkg="data2txt" type="imu2txt" respawn="false" output="screen" >
        <param name="file_name"         type="string" value="/home/night_fury/Documents/record_bags/calibration/imudata_to_wall.txt"/>  
    </node>
</launch>
```

# 3. rosrun + main参数传递
`int main(int argc, char** argv) `

main函数有两个参数argc， argv。argc = length(argv)，argv[0]是程序的名字，argv[1]到argv[argc - 1]是传递给程序的参数，按空格分割参数后以char指针的形式存储。这是C、C++的特性，跟ros无关，你编写的C++程序也可以这么用。你编写的ros程序甚至可以直接运行，并通过这种方式传递参数，而不用rosrun或者roslaunch。

比如我们常用的map_server、rosbag就是用的这种参数传递方式。

`rosrun map_server map_saver -f ~/Documents/test`或者直接找到二进制文件后`map_saver -f ~/Documents/test`

像上面这样运行程序，那么
```
argc=3  
argv[0]="map_server"  
argv[1]="-f"  
argv[0]="test"  
```

你就可以在程序中使用这些参数了。

# 4. roslaunch + main参数传递
续上，如果使用main参数传递，那在roslaunch应该怎么样呢？如下，使用`args`：

```xml
<launch>
    <node name="map_server" pkg="map_server" type="map_server" args="$(find costmap_2d)/test/willow-full-0.025.pgm 0.025" />
    <node name="rosplay" pkg="rosbag" type="play"
        args="-s 5 -r 1 --clock --hz=10 $(find costmap_2d)/test/simple_driving_test_indexed.bag" />
</launch>
```

 
# 参考
<http://wiki.ros.org/rosbash#rosrun>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
