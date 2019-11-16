---
layout:     post
title:      ROS Navigation之nav_core完全详解
subtitle:   ROS学习之路之Navigation包解读
date:       2018-12-29
author:     白夜行的狼
header-img: img/in_post/nav_core_code/black.jpeg
catalog: true
categories: ROS&nbsp;Navigation源码完全详解
tags:
    - nav_core
    - Navigation
    - 规划器接口
    - planner
    - recovery
--- 

# <a id="0">0. 写在最前面<a/>
本文持续更新地址：<https://haoqchen.site/2018/12/29/nav-core-code/>

本文将介绍自己在看ROS的Navigation stack中的nav\_core包源代码时的一些理解。作者的ROS版本是indigo，nav\_core版本是1.12.13。如有错误，欢迎在评论中指正。

如果觉得写得还不错，就请收藏一下啦～～～也可以找一下我写的其他包的源码解读来看一下。关注一下我的专栏什么的。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# <a id="1">1. package.xml与CMakeLists.txt<a/>
**package**说这个包目前提供了三个导航用到的，机器人特定动作的一般接口，分别是`BaseGlobalPlanner`, `BaseLocalPlanner`, `RecoveryBehavior`，即全局路径规划器、局部路径规划器和恢复行为规划器。接口的作用一般是为了统一不同规划器的输出、输入，使得后续程序可以适应不同规划器。

**CMakeLists**`catkin_package`的作用是，当其他包`find_package(nav_core)`时，应该迭代依赖`std_msgs, geometry_msgs, tf, costmap_2d`四个包，并且`include`的路径。其实整个包只包含了三个文件：base\_global\_planner.h、base\_local\_planner.h、recovery\_behavior.h。这三个包分别定义了三个纯虚类，如下图所示：
<img src="https://haoqchen.site/img/in_post/nav_core_code/move_base_interfaces.png"/>

# <a id="1">1. base\_global\_planner.h<a/> 
```cpp
namespace nav_core {
  /**
   * @class BaseGlobalPlanner
   * @brief Provides an interface for global planners used in navigation. All global planners written as plugins for the navigation stack must adhere to this interface.
   */
  class BaseGlobalPlanner{
    public:
      /**
       * @brief Given a goal pose in the world, compute a plan
       * @param start The start pose 
       * @param goal The goal pose 
       * @param plan The plan... filled by the planner
       * @return True if a valid plan was found, false otherwise
       */
      virtual bool makePlan(const geometry_msgs::PoseStamped& start, 
          const geometry_msgs::PoseStamped& goal, std::vector<geometry_msgs::PoseStamped>& plan) = 0;

      /**
       * @brief  Initialization function for the BaseGlobalPlanner
       * @param  name The name of this planner
       * @param  costmap_ros A pointer to the ROS wrapper of the costmap to use for planning
       */
      virtual void initialize(std::string name, costmap_2d::Costmap2DROS* costmap_ros) = 0;

      /**
       * @brief  Virtual destructor for the interface
       */
      virtual ~BaseGlobalPlanner(){}

    protected:
      BaseGlobalPlanner(){}
  };
};
```
声明了一个纯虚的类，用户在实现全局规划器时需继承自该类，并给出这几个函数的具体实现。其中makePlan函数在[move_base](https://haoqchen.site/2018/11/27/move-base-code/)的`void planThread()`中被调用，用于根据参数一（起始点）以及参数二（终点）来规划路径，并通过引用的形式返回给参数三。

目前Navigation Stack实现的全局路径规划器有：  
* global_planner: 一个快速的，内插值的路径规划器，其能更灵活地代替navfn
* navfn: 一个基于栅格的全局路径规划器，利用导航函数来计算路径
* carrot\_planner: 一个简单的全局规划器，其接收用户指定的全局点，并尝试让机器人尽可能靠近目标点（目标点可以为障碍）。

# <a id="2">2. base\_local\_planner.h<a/> 
同上，定义了局部路径规划器的纯虚类
```cpp
namespace nav_core {
 
  class BaseLocalPlanner{
    public:
      virtual bool computeVelocityCommands(geometry_msgs::Twist& cmd_vel) = 0;
      
      virtual bool isGoalReached() = 0;
      
      virtual bool setPlan(const std::vector<geometry_msgs::PoseStamped>& plan) = 0;
     
      virtual void initialize(std::string name, tf::TransformListener* tf, costmap_2d::Costmap2DROS* costmap_ros) = 0;

      virtual ~BaseLocalPlanner(){}
    protected:
      BaseLocalPlanner(){}
  };
};
```
其中`setPlan`函数在[move_base](https://haoqchen.site/2018/11/27/move-base-code/)中的MoveBase::executeCycle函数中被调用，当全局路径规划成功就将其传递到局部路径规划器。

然后在`MoveBase::executeCycle`中调用`computeVelocityCommands`计算出速度发送到`cmd_vel`话题。

目前Navigation Stack实现的局部路径规划器有：  
* base\_local\_planner: 实现了DWA和Trajectory Rollout
* dwa\_local\_planner: 相对于上者的DWA，使用了更清晰、更容易的接口来实现了一个更容易明白的DWA模块，并为完整机器人提供了更灵活的的y轴。
* eband\_local\_planner: 实现了`Elastic Band method on the SE2 manifold`，我也不知道是啥。
* teb\_local\_planner: 实现了`Timed-Elastic-Band method for online trajectory optimization`，也没听过。

# <a id="3">3. recovery\_behavior.h<a/> 
同上
```cpp
namespace nav_core {
  class RecoveryBehavior{
    public:
      virtual void initialize(std::string name, tf::TransformListener* tf, costmap_2d::Costmap2DROS* global_costmap, costmap_2d::Costmap2DROS* local_costmap) = 0;

      virtual void runBehavior() = 0;

      virtual ~RecoveryBehavior(){}
    protected:
      RecoveryBehavior(){}
  };
};
```

[move_base](https://haoqchen.site/2018/11/27/move-base-code/)中多处用到了`runBehavior()`这个函数，一般是出现了异常情况，需要恢复，或者不知道干啥的时候，具体看文章。

目前Navigation Stack实现的恢复路径规划器有：  
* clear\_costmap_recovery: 一定程度上恢复代价地图
* rotate\_recovery: 360°旋转来尝试清出空间

# 参考
[nav_core官网](http://wiki.ros.org/nav_core?distro=melodic)

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
