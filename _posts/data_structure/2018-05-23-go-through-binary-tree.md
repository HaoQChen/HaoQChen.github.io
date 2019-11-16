---
layout:     post
title:      二叉树前序遍历、中序遍历、后序遍历、层序遍历的直观理解
subtitle:   数据结构与算法
date:       2018-05-23
author:     白夜行的狼
header-img: img/in_post/go_through_binary_tree/black.jpeg
catalog: true
categories: 数据结构
tags:
    - 前序遍历
    - 中序遍历
    - 后序遍历
    - 层序遍历
    - 二叉树
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/05/23/go-through-binary-tree/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

复习到二叉树，看到网上诸多博客文章各种绕，记得头晕。个人觉得数学、算法这些东西都是可以更直观简洁地表示，然后被记住的，并不需要靠死记硬背。

本文的程序基本来源于《大话数据结构》，个人感觉是一本非常好的书，推荐去看。
# 1. 为什么叫前序、后序、中序
一棵二叉树由根结点、左子树和右子树三部分组成，若规定 D、L、R 分别代表遍历根结点、遍历左子树、遍历右子树，则二叉树的遍历方式有 6 种：DLR、DRL、LDR、LRD、RDL、RLD。由于先遍历左子树和先遍历右子树在算法设计上没有本质区别，所以，只讨论三种方式：

* DLR--前序遍历（根在前，从左往右，一棵树的根永远在左子树前面，左子树又永远在右子树前面 ）

* LDR--中序遍历（根在中，从左往右，一棵树的左子树永远在根前面，根永远在右子树前面）

* LRD--后序遍历（根在后，从左往右，一棵树的左子树永远在右子树前面，右子树永远在根前面）

# 2. 需要注意几点
1. 根是相对的，对于整棵树而言只有一个根，但对于每棵子树而言，又有自己的根。比如对于下面三个图，对于整棵树而言，A是根，A分别在最前面、中间、后面被遍历到。而对于D，它是G和H的根，对于D、G、H这棵小树而言，顺序分别是DGH、GDH、GHD；对于C，它是E和F的根，三种排序的顺序分别为： CEF、ECF、EFC。是不是根上面的DLR、LDR、LRD一模一样呢～～
2. 整棵树的起点，就如上面所说的，从A开始，前序遍历的话，一棵树的根永远在左子树前面，左子树又永远在右子树前面，你就找他的起点好了。
3. 二叉树结点的先根序列、中根序列和后根序列中，所有叶子结点的先后顺序一样
4. 建议看看文末第3个参考有趣详细的推导

|前序遍历（DLR）|中序遍历（LDR）|后序遍历（LRD）|
|:------:|:------:|:------:|
|![pre](/img/in_post/go_through_binary_tree/pre.png)|![mid](/img/in_post/go_through_binary_tree/mid.png)|![back](/img/in_post/go_through_binary_tree/back.png)|

# 3. 算法上的前中后序实现
除了下面的递归实现，还有一种使用栈的非递归实现。因为递归实现比较简单，且容易关联到前中后，所以
```cpp
typedef struct TreeNode
{
    int data;
    TreeNode * left;
    TreeNode * right;
    TreeNode * parent;
}TreeNode;
 
void pre_order(TreeNode * Node)//前序遍历递归算法
{
    if(Node == NULL)
        return;
    printf("%d ", Node->data);//显示节点数据，可以更改为其他操作。在前面
    pre_order(Node->left);
    pre_order(Node->right);
}
void middle_order(TreeNode *Node)//中序遍历递归算法
{
    if(Node == NULL)
        return;
    middle_order(Node->left);
    printf("%d ", Node->data);//在中间
    middle_order(Node->right);
}
void post_order(TreeNode *Node)//后序遍历递归算法
{
    if(Node == NULL)
        return; 
    post_order(Node->left);
    post_order(Node->right);
    printf("%d ", Node->data);//在最后
}
```
# 4. 层序遍历
层序遍历嘛，就是按层，从上到下，从左到右遍历，这个没啥好说的。
![layer](/img/in_post/go_through_binary_tree/layer.png)
# 参考
《大话数据结构》  
<https://cnbin.github.io/blog/2016/01/05/er-cha-shu-de-bian-li/>  
<https://blog.csdn.net/soundwave_/article/details/53120766>
    

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
