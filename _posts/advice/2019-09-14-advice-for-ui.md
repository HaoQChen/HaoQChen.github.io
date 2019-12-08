---
layout:     post
title:      关于用户界面编写的几点建议
subtitle:   过来人的建议
date:       2019-09-14
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories: 经验小结
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/11/14/advice-for-ui/>

本文档介绍一些编写UI界面时的建议，主要是日常工作中发现的，能够帮助提升代码质量，提高用户体验的方法和技巧。我曾经用过Matlab、Qt、MFC、Labview来编写界面，都会涉及到与硬件的交互，个人感觉最强的是Qt。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 对UI的 一点想法

UI是直接面向用户的，要清楚你的用户的能力水平，对于一些能力不强的用户，UI应尽量做到“傻瓜式”。结构设计中有个名词叫“防呆”，工程师会设计一些不对称的形状，用户只有在规定方向才能插进去，呆子也不会出错。软件工程中也应该尽量做到防呆，永远不要高估用户的智商，哪怕你的使用手册写得非常好。

# 2. 建议

## 2.1. 善用Enable
   
比如Qt就给每个控件提供了该函数，设置为false就可以将控件禁用，用户无法输入。可以通过密码等设置不同权限，根据当前权限开放设置。比如要进行用户管理，需要管理员权限，对于普通用户，直接将相关按钮、输入框disable掉，根本不用操心用户误操作或者要做一些提示。

## 2.2. 输入框先输入后判断
   
比如你想限定用户只能输入数字，一般做法是直接设置输入框只能输入数字，别的输进去没反应，但是这种做法对新手来说，一直输不进去会很烦躁。又比如输入浮点数，我想把小数点前面的数字删了换一个，删了之后就不符合数字规范了，竟然不让我删，但这种操作是很正常的操作。建议可以先让用户随意输入，输入完成后再进行判断，如果有问题再设置回默认值或原来的值，并通过其他方式告知用户。

## 2.3. 统一到一个回调函数里面修改
   
+ 举个例子，一个LineEdit输入框输入路径信息，然后还有一个Open的按钮来选择输入的信息。对于程序里面被修改的这个变量，应该统一在LineEdit的回调函数里面被修改，Open按钮的回调应直接调用LineEdit的回调，而不应再写一个。并且对应的这个变量应该只在LineEdit的回调里被修改，而不应该污染到整个mainwindow.cpp。后者将导致后续程序开发出现混乱，影响代码阅读性。

+ 再比如，界面有一个停止按钮和一个中断按钮，停止负责停止机器人，中断是出现了特殊情况及时中断所有操作。比较机智的做法是，在中断中直接调用停止的回调，而不是在中断函数中再实现一遍停电机等函数。

## 2.4. 性质功能相似的几个控件应尽量统一在一个回调里进行
下面的程序就很好地运用lambda表达式的隐式引用值传递方式将4*6个控件集中到了一个回调函数里  

```cpp
for (int i = 0; i < 6; ++i)
{
    QObject::connect(marker_dspinbox_[0][i], &QDoubleSpinBox::editingFinished, this,
                    [&]() { updateMarkerInformation(0); });
    QObject::connect(marker_dspinbox_[1][i], &QDoubleSpinBox::editingFinished, this,
                    [&]() { updateMarkerInformation(1); });
    QObject::connect(marker_dspinbox_[2][i], &QDoubleSpinBox::editingFinished, this,
                    [&]() { updateMarkerInformation(2); });
    QObject::connect(marker_dspinbox_[3][i], &QDoubleSpinBox::editingFinished, this,
                    [&]() { updateMarkerInformation(3); });
}
```

## 2.5. 不要在状态判断中进行大量耗时操作
类似下面这样的操作
```cpp
if (is_connected_)
{
    for (int i = 0; i < 10; ++i)
    {
        doHardWorking();
    }
    doHardWork2();
}
```

其中`doHardWorking()`需要`is_connected_ == true`才能工作，而且`doHardWorking()`耗时很长。

这样处理的最大问题是，用户可能在其他线程或者中断中修改了`is_connected_`的状态，导致`doHardWorking()`一直处于卡死状态。

如果非要做这种耗时且循环的操作，建议改成每次运行前判断一次：

```cpp

for (int i = 0; i < 10; ++i)
{
    if (is_connected_)
    {
        doHardWorking();
    }
}
if (is_connected_)
{
    doHardWorking2();
}
```

## 2.6 定义时便明确状态变量的意义

比如`is_start_`、`is_working_`、`is_stoping_`，你可能会定义一堆这样的状态变量，然后在整个程序中使用。

问题在于，时间久了，你可能也忘记了哪个变量是什么含义，别人看可能会更乱。另外有些模糊边界到底用哪个比较好？

建议在定义前先仔细思考整个程序到底需要哪些状态，定义的时候在后面注释明确每个变量的具体使用场景

比如：

```cpp
bool is_start_; // user push the start button
bool is_working_; // computer connect with robot, and start to control it
bool is_stoping_; // user push the stop button, after stop the robot, is_working_ will be false
```

## 2.7 编程时考虑线程间同步问题

带UI的工程往往是一个线程在维护UI的交互，另外至少一个线程在运行其他正常功能。尽量想清楚哪些变量是会同时在两个线程出现的，做好同步处理。但往往设计时没有那么清晰的界限，写着写着就混用了，工程大了出了BUG非常难定位和补救。

## 2.8 状态变量流程化

凡涉及交互的，包括跟用户交互，机器人跟程序的交互等，都不是一个瞬间就能完成的过程。拿机器人跟电脑交互举例，他的过程可能包括：`连接成功`->`启动`->`行进`->`停车ing`->`完全停止`->`断开连接`。

如果对于上面的状态都弄一个状态变量，就有6个之多，而且非常容易造成混乱。很多时候，这些都是顺序的，没连接成功就不可能启动，没启动就不可能行进，没行进就无所谓停车，没有停车ing就没有完全停止的说法。所以可以用一个`enum`来管理这些状态：
```cpp
enum{
    ROBOT_STATE_CONNECTED = 0,
    ROBOT_STATE_ON,
    ROBOT_STATE_RUNNING,
    ROBOT_STATE_STOPPING,
    ROBOT_STATE_STOPED,
    ROBOT_STATE_DISCONNECT
};
int state = ROBOT_STATE_DISCONNECT;
if (state > ROBOT_STATE_ON){
    runRobot();
}
```

## 2.9 考虑用户重复按同一个键

相信大家都会有过这样的体验，因为不确定有没有按对按键，会一直重复按一个按钮。比如计算器中进行+2操作，如果按键的回调函数不做重复考虑，按了n次就会调用n次，你要确定这是否是用户想要的？

可以通过一些状态设置去判断该回调是否已经被调用过，重复按时进行其他提醒。

# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
