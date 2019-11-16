---
layout:     post
title:      ROS Navigation之move_base完全详解
subtitle:   ROS学习之路之Navigation包解读
date:       2018-11-27
author:     白夜行的狼
header-img: img/in_post/move_base_code/black.jpeg
catalog: true
categories: ROS&nbsp;Navigation源码完全详解
tags:
    - Navigation
    - move_base
    - actionlib::SimpleActionServer
    - planner
    - recovery
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/27/move-base-code/>

本文将介绍自己在看ROS的Navigation stack中的move\_base包源代码时的一些理解。作者的ROS版本是indigo，move\_base版本是1.12.13。如有错误，欢迎在评论中指正。

如果觉得写得还不错，就请收藏一下啦～～～也可以找一下我写的其他包的源码解读来看一下。关注一下我的专栏什么的。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. package.xml与CMakeLists.txt
**package**的介绍说，这个包提供了一个基于[actionlib](http://www.ros.org/wiki/actionlib)的实现，即提供一个目标点，move\_base会尝试通过全局以及局部的路径规划，让移动机器人移动到设定的目标点。  

用户可以自定义任意的全局路径规划器、局部路径规划器，只需要将其跟`nav_core::BaseGlobalPlanner`、`nav_core::BaseLocalPlanner`接口对接上即可。这两个接口的实现在[nav_core包](http://www.ros.org/wiki/nav_core)。

move\_base维护了两种`costmaps`，分别给全局、局部规划器用。具体实现请看[costmap_2d包](http://www.ros.org/wiki/costmap_2d)

**CMakeLists**中定义生成以下：  
* 动态参数服务器，可以在线修改一些参数。怎么用的话看[高博的博客](http://www.guyuehome.com/1173)
* `move_base`动态链接库，其实就定义了一个`MoveBase`类，详细看[第2章](#2)
* `move_base_node`节点，其实就定义了一个`MoveBase`对象。
* 安装选项。

# <a id="2">2. MoveBase类<a/>
该类利用`actionlib::SimpleActionServer<move_base_msgs::MoveBaseAction>`给出的接口来实现：给定一个目标，然后控制移动机器人走到目标点的功能。  

关于[actionlib](http://wiki.ros.org/actionlib)我也不是很懂，就不坑大家了，大概就是ROS提供的一个基础框架，通过客户端向服务器发送一个goal，服务器做出相应处理。相对于基础的ROS service，该框架提供了取消请求、获取周期性反馈、抢占任务等功能，适合长时间的服务。MoveBase实现的就是服务器功能，我们就可以在其他地方声明客户端来申请相应的服务。
![actionlib_struct](/img/in_post/move_base_code/actionlib_struct.png)  

## 2.1 重要成员及参数
```cpp
MoveBaseActionServer* as_;//就是actionlib的服务器

//全局路径规划器、局部路径规划器加载并创建实例后的指针
boost::shared_ptr<nav_core::BaseGlobalPlanner> planner_;
boost::shared_ptr<nav_core::BaseLocalPlanner> tc_;
//这个是转圈圈的？恢复状态
std::vector<boost::shared_ptr<nav_core::RecoveryBehavior> > recovery_behaviors_;

//通过这个值将goal在MoveBase::executeCb与MoveBase::planThread()之间传递
geometry_msgs::PoseStamped planner_goal_;

//以插件形式实现全局规划器、局部规划器和丢失时恢复规划器。
//插件形式可以实现随时动态地加载C++类库，但需要在包中注册该插件，不用这个的话需要提前链接（相当于运行时加载）
pluginlib::ClassLoader<nav_core::BaseGlobalPlanner> bgp_loader_;
pluginlib::ClassLoader<nav_core::BaseLocalPlanner> blp_loader_;
pluginlib::ClassLoader<nav_core::RecoveryBehavior> recovery_loader_;

//一般保存规划器中新鲜出路的路径，然后将其给latest_plan_
std::vector<geometry_msgs::PoseStamped>* planner_plan_;
//作为一个桥梁，在MoveBase::executeCycle中传递给controller_plan_
std::vector<geometry_msgs::PoseStamped>* latest_plan_;
std::vector<geometry_msgs::PoseStamped>* controller_plan_;

//boost的一种结合了互斥锁的用法，可以使一个线程进入睡眠状态，然后在另一个线程触发唤醒。
boost::condition_variable planner_cond_;
```

```cpp
recovery_behavior_enabled: true//是否启用recovery行为
controller_frequency: 3.0//控制频率,可以理解为executeCycle函数调用频率
```
## 2.1 MoveBase(tf::TransformListener& tf)
`move_base_node`中就只调用了这个构造函数。 
1. 首先初始化一些成员，然后定义一个名为`move_base`的SimpleActionServer。该服务器的Callback为`MoveBase::executeCb`，可参见[Simple Action Server的教程](http://wiki.ros.org/actionlib_tutorials/Tutorials/SimpleActionServer%28ExecuteCallbackMethod%29)。
2. 从参数服务器获取一些参数，包括两个规划器名称、代价地图坐标系、规划频率、控制周期等
3. 新建planner线程，入口为`MoveBase::planThread`
4. 订阅`geometry_msgs::PoseStamped`类型的`goal`话题，cb为`MoveBase::goalCB`，你在rviz中输入的目标点就是通过这个函数来响应的
5. 从参数服务器获取代价地图相关的一些参数
6. 初始化global planner，包括查看规划器是否有效，通过代价地图创建实例等@TODO 还不是很懂
7. 初始化local planner，包括查看规划器是否有效，通过代价地图创建实例等@TODO 还不是很懂
8. 开启根据传感器数据更新代价地图@TODO 等开完代价地图部分
9. 定义一个名为`make_plan`的服务，cb为`MoveBase::planService`；定义一个名为`clear_costmaps`的服务，cb为`MoveBase::clearCostmapsService`
10. 先`loadRecoveryBehaviors`，不行再`loadDefaultRecoveryBehaviors`加载用户自定义的恢复规划器，这里包括了该死的找不到路自转360°
11. 启动actionlib服务器，并启动动态参数服务器(回调函数为`reconfigureCB`，详细介绍看[高博的博客](http://www.guyuehome.com/1173))

## 2.2 goalCB
作用如2.1.4所示，其实是为rviz等提供一个简单的调用，该回调函数将`geometry_msgs::PoseStamped`形式的goal转换成`move_base_msgs::MoveBaseActionGoal`，再发布到对应类型的`goal`话题中

## 2.3 bool MoveBase::planService
如2.1.9所示，这是movebase提供的一个服务。搜了一下发现，除了movebase，navfn以及global\_planner这两个包也会发布这个服务，但是没有节点订阅～～～～。这三个包的cb其实都是调用相应的全局规划器来获得一条path返回给客户端。

## 2.4 void executeCb(const move_base_msgs::MoveBaseGoalConstPtr& move_base_goal)
如2.1.1所示，这个是`movebase`这个actionlib服务的回调函数。我们什么时候会用到这个回调呢？当Action Server在`move_base_msgs::MoveBaseActionGoal`类型的`goal`话题上收到一个消息，然后将其放到Sample Action Server的待定槽时。如2.1.4中被更换类型后重新发布的goal，再如在做行人跟踪时，创建一个`move_base`服务器的客户端时，通过sendgoal函数来在该话题上发布目标位姿，这时Action Server就会收到一个goal，然后就将其放到待定槽，如2.4.1中介绍的。

第一次接收到goal时会进入该函数，但如果没有完成任务，尚未退出时，再有接收到goal并不会再新建线程进入一次（应该也可以这样操作，这里并没有这样选择），而是通过抢断信号的形式通知该函数，所以在处理goal的时候需要经常查看`isPreemptRequested`函数的返回，看是否有抢占。

该函数流程是
1. 第一次进入后接收goal，判断有效性等，然后开启规划线程得到路径。
2. 然后在`while(n.ok())`循环中调用`executeCycle(goal, global_plan);`来控制机器人进行相应跟随。
3. 期间会不断检测是否有新的goal抢占，或者坐标系变换等，如果有则在while循环中重复步骤1的初始化再跟随
4. 如果有被空抢占（如cancel等）则清除退出
5. 如果跟随完成则退出
6. 会进行控制周期约束。 

### 2.4.1 插播一段actionlib的Goal执行流程
如下图所示，在Action接收到goal C时，并不立即抢断正在执行的goal，而是进入到`Pending Goal`待定槽里，如果待定槽里已经有一个goal，则将其清出进入Recalled状态。到此都是actionlib底层架构自动完成的
![simple_goal_reception](/img/in_post/move_base_code/simple_goal_reception.png)  
接下来，Simple Action Server的用户就可以收到新goal到来的通知（有两种方式，我们这里是通过回调函数的方式）。用户可以接收新的goal，将`Current Goal`槽指向新的goal，并将状态机跟新的goal关联起来，将其改为active状态，其他的就会自动变为待定或者完成状态状态
![simple_goal_accept](/img/in_post/move_base_code/simple_goal_accept.png)  
这里需要注意的是，一个goal从客户端发送过来是通过goal话题，cancel是通过cancel话题发送的，一个Simple Action Client发布的goal有`Pending、Active、Down`三种状态，cancel后并不是立马就消失的，还存在与内存中，需要服务器去清除。
![simple_client_state_transitions](/img/in_post/move_base_code/simple_client_state_transitions.png)  

下面通过关键代码来看一下它做了什么工作，详细代码请自己下载下来阅读
```cpp
  void MoveBase::executeCb(const move_base_msgs::MoveBaseGoalConstPtr& move_base_goal)
  {
    //判断goal有效性
    //统一转换到全局坐标系
    geometry_msgs::PoseStamped goal = goalToGlobalFrame(move_base_goal->target_pose);

    //启动2.1.3中所说的新线程来获取规划路径
    runPlanner_ = true;
    //唤醒等待条件变量的一个线程：即调用planner_cond_.wait()的MoveBase::planThread()
    planner_cond_.notify_one();

    current_goal_pub_.publish(goal);//这个话题貌似只有一些rviz上用来显示的

    ros::NodeHandle n;
    while(n.ok())
    {
      if(c_freq_change_)
      {
        //更改控制周期
      }

      if(as_->isPreemptRequested()){//是否有抢占请求，根据参考1第8点的说法，SimpleActionServer的政策是，新的goal都会抢占旧的goal，这里应该只是为了清除新goal的一些状态。（那些待定的goal也有可能抢占，或者可以直接cancel抢占Current？）
        if(as_->isNewGoalAvailable()){//如果是新的goal这个函数会将其他goal设置为被抢占状态
          //if we're active and a new goal is available, we'll accept it, but we won't shut anything down
          move_base_msgs::MoveBaseGoal new_goal = *as_->acceptNewGoal();//接收new goal

          if(!isQuaternionValid(new_goal.target_pose.pose.orientation)){
            return;//无效退出
          }

          goal = goalToGlobalFrame(new_goal.target_pose);//统一转换到全局坐标系

          //唤醒规划线程
          lock.lock();
          planner_cond_.notify_one();
          lock.unlock();
        }
        else {//如果是cancel了
          //if we've been preempted explicitly we need to shut things down
          resetState();//停止规划线程、停车等
          as_->setPreempted();//设置current goal被抢占

          return;
        }
      }

      //we also want to check if we've changed global frames because we need to transform our goal pose
      if(goal.header.frame_id != planner_costmap_ros_->getGlobalFrameID()){
        goal = goalToGlobalFrame(goal);//判断这段时间是否改了坐标系
      }

      //the real work on pursuing a goal is done here
      bool done = executeCycle(goal, global_plan);//这是控制机器人跟踪的主要函数，下面详细讲

      //if we're done, then we'll return from execute
      if(done)
        return;
      r.sleep();//控制周期睡眠
    }

    //ros不ok时清除退出
    return;
  }
```


## 2.5 void planThread()
如2.1.3所示，这是planner线程的入口。这个函数需要等待actionlib服务器的cb`MoveBase::executeCb`来唤醒启动。主要作用是调用全局路径规划获取路径，同时保证规划的周期性以及规划超时清除goal。

下面是本函数的一些主要代码，详细代码请自行下载查看。
```cpp
  void MoveBase::planThread(){
    bool wait_for_wake = false;
    boost::unique_lock<boost::mutex> lock(planner_mutex_);
    while(n.ok()){
      //check if we should run the planner (the mutex is locked)
      while(wait_for_wake || !runPlanner_){
        planner_cond_.wait(lock);//使线程进入睡眠，等待MoveBase::executeCb，以及规划周期的唤醒
        wait_for_wake = false;
      }

      //planner_goal_是在MoveBase::executeCb中得到的目标位姿，需要上锁保证线程安全
      geometry_msgs::PoseStamped temp_goal = planner_goal_;
      lock.unlock();

      //run planner
      planner_plan_->clear();//清除原来规划出的路径向量
      //MoveBase::makePlan作用是获取机器人的位姿作为起点，然后调用全局规划器的makePlan返回规划路径，存储在planner_plan_
      bool gotPlan = n.ok() && makePlan(temp_goal, *planner_plan_);

      if(gotPlan){//如果规划出路径则更新相应路径，并将state_转换为CONTROLLING状态
        std::vector<geometry_msgs::PoseStamped>* temp_plan = planner_plan_;

        lock.lock();
        planner_plan_ = latest_plan_;
        latest_plan_ = temp_plan;//将最新的全局路径放到latest_plan_中，其在MoveBase::executeCycle中被传递到controller_plan_中，利用锁来进行同步

        //make sure we only start the controller if we still haven't reached the goal
        if(runPlanner_)
          state_ = CONTROLLING;
        lock.unlock();
      }
      //如果没有规划出路径，并且处于PLANNING状态，则判断是否超过最大规划周期或者规划次数
      //如果是则进入自转模式，否则应该会等待MoveBase::executeCycle的唤醒再次规划
      else if(state_==PLANNING){//仅在MoveBase::executeCb及其调用的MoveBase::executeCycle
        //或者重置状态时会被设置为PLANNING，一般是刚获得新目标，或者得到路径但计算不出下一步控制时重新进行路径规划
        ros::Time attempt_end = last_valid_plan_ + ros::Duration(planner_patience_);

        lock.lock();
        if(runPlanner_ &&
           (ros::Time::now() > attempt_end || ++planning_retries_ > uint32_t(max_planning_retries_))){
          //we'll move into our obstacle clearing mode
          state_ = CLEARING;
          publishZeroVelocity();//直接向cmd_vel话题发布000的速度信息
          recovery_trigger_ = PLANNING_R;
        }
        lock.unlock();
      }

      //take the mutex for the next iteration
      lock.lock();

      //如果还没到规划周期则定时器睡眠，在定时器中断中通过planner_cond_唤醒，这里规划周期为0
      if(planner_frequency_ > 0){
      }
    }
  }
```

## 2.6 bool executeCycle
该函数的两个参数分别是目标点位姿以及规划出的全局路径。  
实现的是通过上述两个已知，利用局部路径规划器直接输出轮子速度，控制机器人按照路径走到目标点，成功返回真，否则返回假。在actionlib server的回调`MoveBase::executeCb`中被调用。

先看movebase的三种状态：
```cpp
enum MoveBaseState {
  PLANNING,//在规划路径中
  CONTROLLING,//在控制机器人运动中
  CLEARING//规划或者控制失败在恢复或者清除中。
};
```
一般默认状态或者接收到一个有效goal时是PLANNING，在规划出全局路径后state_会由PLANNING->CONTROLLING，如果规划失败则由PLANNING->CLEARING。在MoveBase::executeCycle中，会分别对这三种状态做处理：  
* 还在PLANNING中则唤醒规划线程让它干活
* 如果已经在CONTROLLING中，判断是否已经到达目的地，否则判断是否出现震动？否则调用局部路径规划，如果成功得到速度则直接发布到cmd_vel，失败则判断是否控制超时，不超时的话让全局再规划一个路径。
* 如果出现了问题需要CLEARING（仅有全局规划失败、局部规划失败、长时间困在一片小区域三种原因），则每次尝试一种recovery方法，直到所有尝试完

movebase为recovery行为定义了如下三种原因
```cpp
enum RecoveryTrigger
{
  PLANNING_R,//全局规划失败
  CONTROLLING_R,//局部规划失败
  OSCILLATION_R//长时间困在一片小区域
};
```

直接看代码
```cpp
bool MoveBase::executeCycle(geometry_msgs::PoseStamped& goal, std::vector<geometry_msgs::PoseStamped>& global_plan){
    //变量定义并获取机器人坐标发布给server的feedback。

    //check to see if we've moved far enough to reset our oscillation timeout
    if(distance(current_position, oscillation_pose_) >= oscillation_distance_)
    {
      last_oscillation_reset_ = ros::Time::now();
      oscillation_pose_ = current_position;

      //if our last recovery was caused by oscillation, we want to reset the recovery index 
      if(recovery_trigger_ == OSCILLATION_R)
        recovery_index_ = 0;
    }

    if(!controller_costmap_ros_->isCurrent()){
      //如果观测传感器数据不够新，则让机器人停机并退出函数
    }

    if(new_global_plan_){//该变量在规划器线程中，当新的路径被规划出来，该值被置1
      //完成latest_plan_到controller_plan_的转换

      if(!tc_->setPlan(*controller_plan_)){//将全局路径设置到局部路径规划器中
        //ABORT and SHUTDOWN COSTMAPS
        //同时也关闭规划器线程，没必要规划了
      }

      if(recovery_trigger_ == PLANNING_R)//如果全局路径有效，则不需要recovery
        recovery_index_ = 0;
    }

    //the move_base state machine, handles the control logic for navigation
    switch(state_){//对状态机进行处理
      //if we are in a planning state, then we'll attempt to make a plan
      case PLANNING:
        //唤醒规划线程
        break;

      //if we're controlling, we'll attempt to find valid velocity commands
      case CONTROLLING:
        //check to see if we've reached our goal
        if(tc_->isGoalReached()){//如果已经到达结果
          resetState();
          //重置状态，关闭规划器线程，设置告知Client结果
          return true;
        }

        //check for an oscillation condition
        //last_oscillation_reset_获得新目标会重置,距离超过震荡距离（默认0.5）会重置，进行recovery后会重置
        //所以是太久没有发生上面的事就震动一下，防止长时间在同一个地方徘徊？？？？这里oscillation_timeout_默认为0 ，不发生。
        if(oscillation_timeout_ > 0.0 &&
            last_oscillation_reset_ + ros::Duration(oscillation_timeout_) < ros::Time::now())
        {
          publishZeroVelocity();
          state_ = CLEARING;
          recovery_trigger_ = OSCILLATION_R;
        }
        
        if(tc_->computeVelocityCommands(cmd_vel)){//如果局部路径规划成功
          last_valid_control_ = ros::Time::now();
          //make sure that we send the velocity command to the base
          vel_pub_.publish(cmd_vel);//发布控制速度信息。
          if(recovery_trigger_ == CONTROLLING_R)
            recovery_index_ = 0;
        }
        else {//局部规划失败
          if(ros::Time::now() > attempt_end){//判断是否控制超时
            //we'll move into our obstacle clearing mode
            publishZeroVelocity();
            state_ = CLEARING;
            recovery_trigger_ = CONTROLLING_R;
          }
          else{
            //没超时则启动规划器线程重新规划   
          }
        }
        break;

      case CLEARING://三种原因需要recovery，上面有说
        if(recovery_behavior_enabled_ && recovery_index_ < recovery_behaviors_.size()){//遍历recovery方法
          recovery_behaviors_[recovery_index_]->runBehavior();
          recovery_index_++;
        }
        else{//遍历完还是不行 
          if(recovery_trigger_ == CONTROLLING_R){//分原因发布消息
          }
          else if(recovery_trigger_ == PLANNING_R){
          }
          else if(recovery_trigger_ == OSCILLATION_R){
          }
          resetState();
          return true;//已经done了。
        }
        break;
      default:
    }
    //we aren't done yet
    return false;
  }
```

## 2.6 谈一谈recovery
![move_base_interfaces](/img/in_post/move_base_code/move_base_interfaces.png)
recovery是指恢复的规划器，其跟全局规划器和局部规划器是同一个等级的。不同的是，它是在机器人在局部代价地图或者全局代价地图中找不到路时才会被调用，比如[rotate_recovery](http://wiki.ros.org/rotate_recovery)让机器人原地360°旋转，[clear_costmap_recovery](http://wiki.ros.org/clear_costmap_recovery)将代价地图恢复到静态地图的样子。

这些规划器都通过`nav_core::RecoveryBehavior`这个接口来被movebase调用。在movebase中，在构造函数通过`MoveBase::loadRecoveryBehaviors`和`MoveBase::loadDefaultRecoveryBehaviors()`两个函数来加载。一般情况下没有自定义则加载上述两个规划器。然后在`MoveBase::executeCycle`中视情况调用。

用户可以通过将`recovery_behavior_enabled: false`参数设置为false来取消recovery行为


# 参考
1. [ROS actionlib](http://wiki.ros.org/actionlib)
2. [actionlib::SimpleActionServer\<ActionSpec\> Class Template Reference](https://docs.ros.org/diamondback/api/actionlib/html/classactionlib_1_1SimpleActionServer.html#a4964ef9e28f5620e87909c41f0458ecb)  
3. [Writing a Simple Action Server using the Execute Callback](http://wiki.ros.org/actionlib_tutorials/Tutorials/SimpleActionServer%28ExecuteCallbackMethod%29)  
4. 文中已附带的链接  

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
