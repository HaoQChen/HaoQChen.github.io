---
layout:     post
title:      二叉树面试、笔试知识点整理
subtitle:   数据结构与算法
date:       2018-11-08
author:     白夜行的狼
header-img: img/in_post/binary_tree_summary/black.jpeg
catalog: true
categories: 数据结构
tags:
    - 二叉树
    - 面试、笔试
    - 二叉树计算
    - 二叉树基本知识
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/08/binary-tree-summary/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

本文记录了作者在准备秋招笔试面试过程中遇到的跟二叉树有关的题目，同时会总结一下复习到的关键知识点。可能不会太详细。本人学习过程中受到《大话数据结构》这本书的很多启发，推荐大家去买来看。

如果觉得还不错就收藏一个呗，博主会长期更新自己的学习和收获。
# 1. 基本知识点
## 1.1 完全二叉树、满二叉树
**满二叉树：**顾名思义，就是除了叶子外的节点都有左子树和右子树，不缺胳膊少腿，很完美，并且所有叶子节点都在同一层（最底层）。如下图所示。
![full_tree](/img/in_post/binary_tree_summary/full_tree.png)

**完全二叉树：**对一棵具有同样深度的满二叉树进行层序遍历编号，如果该二叉树的层序遍历编号跟满二叉树的编号对应一致，则该二叉树是完全二叉树。相同节点，完全二叉树有最小深度。下图中，只有第一个树是完全二叉树，其余都不是。

|![total1](/img/in_post/binary_tree_summary/total1.png)|![total2](/img/in_post/binary_tree_summary/total2.png)|
|------|------|
|![total3](/img/in_post/binary_tree_summary/total3.png)|![total4](/img/in_post/binary_tree_summary/total4.png)|

## 1.2 二叉树的四种排序
见之前写的另一篇博客：[二叉树前序遍历、中序遍历、后序遍历、层序遍历的直观理解](https://haoqchen.site/2018/05/23/go-through-binary-tree/)
## <a id="1.3">1.3 二叉树的计算性质<a/>
1. 二叉树的第i层上最多有2i-1个节点
2. 深度为k的二叉树最多有2k-1个节点
3. 对任何一棵树，如果其终端节点数为n0，度为2的节点数为n2，则n0=n2+1。
4. 具有n个节点的完全二叉树的深度为[log2n]+1,其中[x]表示不大于x的最大整数。
5. 对有n个节点的完全二叉树，按层序遍历编号，对于第i个节点，其左子树是2i，如2i>n则不存在左子树， 是。叶节点。右子树是2i+1，如2i+1则不存在右子树。由此可得，双亲节点是[i/2]

## 1.4 二叉查找树、平衡二叉树
**二叉查找树（Binary Search Tree、BST）**：又叫二叉排序树，可以是空树，左子树比双亲小，右子树比双亲大。如果按照中序遍历，则刚好按从小到大的顺序排列。一般在结构中加一个数量来实现重复数的插入，具体的插入、删除、查找操作看参考。
![BST](/img/in_post/binary_tree_summary/BST.png)
[二叉查找树参考一](https://songlee24.github.io/2015/01/13/binary-search-tree/)  
[二叉查找树参考二](http://www.cnblogs.com/huangxincheng/archive/2012/07/21/2602375.html)

**平衡二叉树：**平衡的二叉查找树（AVL，发明者为Adel'son-Vel'skii 和 Landis），树的左子树和右子树高度之差不超过1层，超过一层需要旋转，否则失去平衡。平衡二叉树可以确保查找是严格的O(logN)（普通二叉查找树在极限环境下是O(N)）。左子树和右子树的深度之差称为平衡因子，其只能为-1、1、0

[平衡二叉树参考一](http://www.cnblogs.com/huangxincheng/archive/2012/07/22/2603956.html)  
[平衡二叉树参考二](http://lib.csdn.net/article/datastructure/9204)  
[平衡二叉树参考三](https://www.cnblogs.com/suimeng/p/4560056.html)  
# 2. 笔试真题
## 2.1 二叉树遍历类
[相关知识点](https://haoqchen.site/2018/05/23/go-through-binary-tree/)

**注意：**已知前序和后序遍历不能唯一确定一棵二叉树，已知前中可以唯一确定，已知后中也可以。

### 2.1.1 前序遍历序列是ABCDEF，中序遍历序列是CBAEDF，问后序遍历结果
**答案：**CBEFDA，如果你对上面的知识点足够熟悉，就应该能推出这样的结构：
![search_an1](/img/in_post/binary_tree_summary/search_an1.png)

### 2.1.2 来个难一点的，后序遍历序列是453297861，中序遍历是243519768，求前序遍历
**答案：**123459768（这一题是作者自己虐自己的。。不一定对，能发现这一题有问题，那你已经强了）
![search_an](/img/in_post/binary_tree_summary/search_an.png)
## 2.2 节点数相关计算
相关知识点是[1.3](#1.3)
### 2.2.1 某棵完全二叉树上有555个节点，则该二叉树的叶子节点数为
**答案：**278

思路1：[log2555]+1=9+1，所以是有10层，第9层有2的8次方即256个，1-9层共256*2-1个，所以第10层有44个。总的叶子数等于最后一层，加上第9层中没有子树的节点，即256-44/2+44=278

思路2：由n0=n2+1，而555=n1+n0+n2，由于完全二叉树n1最多只可能是1，而555是单数，不存在n1，故555=n0+n2，n0=（555+1）/2=278
### 2.2.2 某二叉树有2000个结点，则该二叉树的最小高度为
**答案：**11

思路：[log2 2000]+1=10+1=11
### 2.2.3 在一棵二叉树中有30个叶子结点，仅有一个孩子的结点有20个，则该二叉树共有() 个结点
**答案：**79

思路：利用1.3性质的第三点，n0=30，n1=20，n2=n0-1=29，n=n0+n1+n2=79
# 3. 注意事项
## 3.1 深度与高度
树的高度=树的深度，但是结点的深度！=结点的高度。对于结点而言，深度是从上到下的，根结点深度是0（也有说是1）；高度是从下到上的，叶结点的高度是0（也有说1），某个结点的高度是从该结点向下到某个叶结点的最长路径。

# 参考
《大话数据结构》  
牛客网上相关试题  
<https://blog.csdn.net/xiaoquantouer/article/details/65631708>  
<http://www.cnblogs.com/huangxincheng/archive/2012/07/21/2602375.html>  

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
