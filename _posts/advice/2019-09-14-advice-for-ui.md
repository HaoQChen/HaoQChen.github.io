---
layout:     post
title:      关于用户界面编写的几点建议
subtitle:   过来人的建议
date:       2019-09-14
author:     白夜行的狼
header-img: img/in_post/article_name/black.jpeg
catalog: true
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

# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
