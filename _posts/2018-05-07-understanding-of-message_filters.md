---
layout:     post
title:      message_filters::Subscriber & tf::MessageFilter理解
subtitle:   ROS学习之路
date:       2018-05-07
author:     白夜行的狼
header-img: img/in_post/understanding_of_message_filters/contact-bg.jpg
catalog: true
categories: ROS实用小细节
tags:
    - message_filters
    - tf
    - Subscriber
    - 坐标转换
    - ROS
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/05/07/understanding-of-message_filters/>  
　　因为日常看代码经常能看到tf相关的一些函数，转来转去，绕得很晕，有不懂的就仔细查一下，将自己的理解整理出来，这篇是关于 tf::MessageFilter的。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 两者的关系
　　message_filters，顾名思义是消息过滤器；tf::MessageFilter，顾名思义是tf下的消息过滤器。消息过滤器为什么要用tf呢？tf::MessageFilter可以订阅任何的ROS消息，然后将其缓存，直到这些消息可以转换到目标坐标系，然后进行相应的处理（一般在回调函数中处理）。说白了就是消息订阅+坐标转换。实际上，后者继承于前者：
![relation](/img/in_post/understanding_of_message_filters/relation.png)
![message_filters](/img/in_post/understanding_of_message_filters/message_filters.png)

# 2. 使用实例
## a. amcl中激光雷达的回调
```cpp
tf_ = new TransformListenerWrapper();
message_filters::Subscriber<sensor_msgs::LaserScan>* laser_scan_sub_;
tf::MessageFilter<sensor_msgs::LaserScan>* laser_scan_filter_;

laser_scan_sub_ = new message_filters::Subscriber<sensor_msgs::LaserScan>(nh_, scan_topic_, 100);
laser_scan_filter_ = new tf::MessageFilter<sensor_msgs::LaserScan>(*laser_scan_sub_,
                                                                   *tf_,
                                                                   odom_frame_id_,
                                                                   100);

laser_scan_filter_->registerCallback(boost::bind(&AmclNode::laserReceived, this, _1));

void AmclNode::laserReceived(const sensor_msgs::LaserScanConstPtr& laser_scan){
    this->tf_->transformPose(base_frame_id_, ident, laser_pose);//这个函数的意思是，ident在base_frame_id下的表示为laser_pose
}
```

## b. leg_detector中激光雷达的回调
```cpp
TransformListener tfl_;
message_filters::Subscriber<sensor_msgs::LaserScan> laser_sub_;
tf::MessageFilter<sensor_msgs::LaserScan> laser_notifier_;

laser_sub_(nh_, "scan", 10)
laser_notifier_(laser_sub_, tfl_, fixed_frame, 10)

laser_notifier_.registerCallback(boost::bind(&LegDetector::laserCallback, this, _1))
laser_notifier_.setTolerance(ros::Duration(0.01));

void laserCallback(const sensor_msgs::LaserScan::ConstPtr& scan){
    tfl_.transformPoint(fixed_frame, loc, loc);
}
```

## c. 参考一中的示例
```cpp
class PoseDrawer
{
public:
  PoseDrawer() : tf_(),  target_frame_("turtle1")
  {
      point_sub_.subscribe(n_, "turtle_point_stamped", 10);
      tf_filter_ = new tf::MessageFilter<geometry_msgs::PointStamped>(point_sub_, tf_, target_frame_, 10);
      tf_filter_->registerCallback( boost::bind(&PoseDrawer::msgCallback, this, _1) );
  } ;

private:
  message_filters::Subscriber<geometry_msgs::PointStamped> point_sub_;
  tf::TransformListener tf_;
  tf::MessageFilter<geometry_msgs::PointStamped> * tf_filter_;
  ros::NodeHandle n_;
  std::string target_frame_;

  //  Callback to register with tf::MessageFilter to be called when transforms are available
  void msgCallback(const boost::shared_ptr<const geometry_msgs::PointStamped>& point_ptr) 
  {
      geometry_msgs::PointStamped point_out;
      try 
      {
          tf_.transformPoint(target_frame_, *point_ptr, point_out);
      }
      catch (tf::TransformException &ex) 
      {
          printf ("Failure %s\n", ex.what()); //Print exception which was caught
      }
  };

};

int main(int argc, char ** argv)
{
    ros::init(argc, argv, "pose_drawer"); //Init ROS
    PoseDrawer pd; //Construct class
    ros::spin(); // Run until interupted 
};
```

# 3. 头文件
以上的程序都需要添加以下头文件：
```c
#include "ros/ros.h"
#include "tf/transform_listener.h"
#include "tf/message_filter.h"
#include "message_filters/subscriber.h"
```

# 4. 规律总结
* 定义数据：TransformListener、message_filters::Subscriber、tf::MessageFilter
* 用消息的名称来初始化message_filters::Subscriber
* 用tf、message_filters::Subscriber、目标坐标系来初始化tf::MessageFilter
* 给tf::MessageFilter注册callback
* 编写callback，并在回调中完成坐标转换。至此完成消息订阅+坐标转换

在看message_filters的主页过程中发现，它可以做的远比以上说的多，比如：  
An example is the time synchronizer, which takes in messages of different types from multiple sources, and outputs them only if it has received a message on each of those sources with the same timestamp.

# 参考
[ROS官网tf::MessageFilter教程](http://wiki.ros.org/tf/Tutorials/Using%20Stamped%20datatypes%20with%20tf::MessageFilter)  
[ROS官方tf::MessageFilter文档](http://docs.ros.org/api/tf/html/c++/classtf_1_1MessageFilter.html)  
[ROS官网message_filters主页](http://wiki.ros.org/message_filters)  
[ROS官方message_filters::SimpleFilter文档](http://docs.ros.org/api/message_filters/html/c++/classmessage__filters_1_1SimpleFilter.html)  
[ROS一些传感器数据读取融合问题的思考](https://www.cnblogs.com/yhlx125/p/6818148.html)  
[同时订阅两个话题？看到没测试过](https://answers.ros.org/question/193120/how-to-connect-a-tfmessagefilter-to-two-subscribers/)  

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**