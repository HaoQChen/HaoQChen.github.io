---
layout:     post
title:      ROS节点的初始化及退出详解（ros::init、SIGINT、ros::ok、ros::NodeHandle）
subtitle:   ROS学习之路
date:       2018-04-28
author:     白夜行的狼
header-img: img/in_post/ROS_node_init/post-bg-os-metro.jpg
catalog: true
categories: ROS实用小细节
tags:
    - ros::init
    - ros::ok
    - ros::NodeHandle
    - ROS初始化及退出
    - SIGINT
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/04/28/ROS-node-init/>

作者会长期更新自己的所学，觉得写得还不错就收藏一波呀～～一起学习进步

很多ROS新手编写节点的时候都不知道要怎么才能Ctrl+c退出，根本都没有注意到一个节点的生命流程，看完你就懂了~~

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

先上程序：

完整版工程已经上传到github：<https://github.com/HaoQChen/init_shutdown_test>，下载完麻烦大家点个赞

所有知识点都写在注释里了，请慢慢阅读，每个语句前面的注释是ROS官方注释，后面的注释则是作者自己写的

```cpp
#include "ros/ros.h"
#include <signal.h>

void MySigintHandler(int sig)
{
    //这里主要进行退出前的数据保存、内存清理、告知其他节点等工作
    ROS_INFO("shutting down!");
    ros::shutdown();
}

int main(int argc, char** argv){
//ros::init()
    /**
      * The ros::init() function needs to see argc and argv so that it can perform
      * any ROS arguments and name remapping that were provided at the command line. For programmatic
      * remappings you can use a different version of init() which takes remappings
      * directly, but for most command-line programs, passing argc and argv is the easiest
      * way to do it.  The third argument to init() is the name of the node.
      *
      * You must call one of the versions of ros::init() before using any other
      * part of the ROS system.
    */
    ros::init(argc, argv, "ist_node");
    //初始化节点名字必须在最前面，如果ROS系统中出现重名，则之前的节点会被自动关闭
    //如果想要多个重名节点而不报错，可以在init中添加ros::init_options::AnonymousName参数
    //该参数会在原有节点名字的后面添加一些随机数来使每个节点独一无二
    //ros::init(argc, argv, "my_node_name", ros::init_options::AnonymousName);

//ros::NodeHandle
    /**
      * NodeHandle is the main access point to communications with the ROS system.
      * The first NodeHandle constructed will fully initialize this node, and the last
      * NodeHandle destructed will call ros::shutdown() to close down the node.
    */
    ros::NodeHandle h_node;
    //获取节点的句柄,init是初始化节点，这个是Starting the node
    //如果不想通过对象的生命周期来管理节点的开始和结束，你可以通过ros::start()和ros::shutdown() 来自己管理节点。
    
    ros::Rate loop_rate(1);
    //loop once per second
    //Cannot use before the first NodeHandle has been created or ros::start() has been called.

//shut down
    signal(SIGINT, MySigintHandler);
    //覆盖原来的Ctrl+C中断函数，原来的只会调用ros::shutdown()
    //为你关闭节点相关的subscriptions, publications, service calls, and service servers，退出进程

//run status
    int sec = 0;
    while(ros::ok() && sec++ < 5){
        loop_rate.sleep();
        ROS_INFO("ROS is ok!");
        ros::spinOnce();
    }
    //ros::ok()返回false，代表可能发生了以下事件
        //1.SIGINT被触发(Ctrl-C)调用了ros::shutdown()
        //2.被另一同名节点踢出 ROS 网络
        //3.ros::shutdown()被程序的另一部分调用
        //4.节点中的所有ros::NodeHandles 都已经被销毁
    //ros::isShuttingDown():一旦ros::shutdown()被调用（注意是刚开始调用，而不是调用完毕），就返回true
    //一般建议用ros::ok()，特殊情况可以用ros::isShuttingDown()

    ROS_INFO("Node exit");
    printf("Process exit\n");
    return 0;
}
```
下载工程运行后可以看到，终端每隔一秒会输出ROS is ok!的信息

1. 如果5秒之内没有按下Ctrl+C正常退出，则会正常退出。输出：
![without5s](/img/in_post/ROS_node_init/without5s.png)

2. 如果5秒内按下了Ctrl+C，则会调用MySigintHandler，然后ros::shutdown();从终端信息我们可以看到，调用ros::shutdown();后，所有ROS服务已经不可以使用，连ROS_INFO也是不能用的，输出信息失败。所以在程序中要密切注意退出部分的程序不要使用ROS的东西。
![within5s](/img/in_post/ROS_node_init/within5s.png)

# 参考
[ROS官网：编写简单的消息发布器和订阅器 (C++)](http://wiki.ros.org/cn/ROS/Tutorials/WritingPublisherSubscriber%28c%2B%2B%29)  
[ROS官网：roscppOverviewInitialization and Shutdown](http://wiki.ros.org/roscpp/Overview/Initialization%20and%20Shutdown)  
<https://blog.csdn.net/wuguangbin1230/article/details/76889753>  
<http://blog.sina.com.cn/s/blog_8a2281f70102xi2v.html>  

  
<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
