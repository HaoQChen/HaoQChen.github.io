---
layout:     post
title:      编程常用数据结构与函数总结（vector、list、stack、deque、字符串）
subtitle:   磨刀不误砍柴工
date:       2018-09-05
author:     白夜行的狼
header-img: img/in_post/helpful_struct_for_coding/black.jpeg
catalog: true
categories: 数据结构
tags:
    - vector
    - list
    - stack
    - deque
    - 总结
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/09/05/helpful-struct-for-coding/>

本文总结了STL的编程常用数据结构，包括vector、list、stack、deque、字符串等。主要是为了方便日常编程使用，不用记得那么辛苦，也不用整天翻文档。

喜欢的话收藏一个呗，博主会长期更新自己的学习和收获。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**
# 1. STL容器总结
1. 序列容器：vector, list, deque, string.

2. 关联容器：set, multiset, map, mulmap, hash_set, hash_map, hash_multiset, hash_multimap

3. 其他的杂项：stack, queue, valarray, bitset

# 2. vector
拥有一段连续的内存空间，因此支持随机存取，也重载了\[]运算符。但是删除和插入需要进行内容的拷贝，甚至需要重新开辟内存后整片拷贝，性能会有所下降
## 2.1 插入、删除
注意vector是连续内存存储，所以删除操作将导致该迭代器及后面的迭代器自动加一（因后面的元素将向前移动）
```cpp
#include <vector>
#include <algorithm>    // std::remove
vector<int> vin;
vector<int>::iterator itr = vin.begin();
for(int i=0;i<10;++i)vin.push_back(i);
vin.pop_back();//删除最后一个元素
itr = vin.erase(vin.begin()+5);//删除第6个元素
vin.erase(vin.begin(),vin.begin()+3);//删除前3个

vin.push_back(10);
vin.push_back(11);
vin.push_back(10);
vector<int>::iterator ret = remove(Numbers.begin(), Numbers.end(), 10);//删除vector中的10，注意，该函数只是将等于10的元素删除，然后将后面元素前移，但vector中的size并没有变，返回的迭代器指向第一个无效元素。ret->end都是无效的，一般等于原来的值

vin.clear();//删除所有元素，size变为0，但是容器体积不一定变化
```
## 2.2 首尾
```cpp
vin.front() -= vin.back();//注意，这里返回的是引用，是会改变该值的
vector<int>::iterator itr = vin.begin();//返回第一个元素位置
vector<int>::iterator itr = vin.end();//返回最后一个元素后面一个位置
```
## 2.3 容器尺寸
```cpp
bool is_empty = vin.empty();//size == 0
int size = vin.size();//实际存储的大小
vin.resize(5);//将size变成5，原本多于5的只取前面5个，原本少于5的则增加到5个
vin.resize(8,1);//如果像这样设定了填充值的话就变成填充值，否则变成0，如果超过capacity就重新申请内存
int cap = vin.capacity();//容器大小一般是2 4 8 16不够就增长两倍
vin.reserve(100);//将capacity设置成100
```
## 2.4 反转
```cpp
#include <algorithm>    // std::reverse  
std::vector<int> myvector;
for (int i=1; i<10; ++i) myvector.push_back(i);   // 1 2 3 4 5 6 7 8 9
std::reverse(myvector.begin(),myvector.end());    // 9 8 7 6 5 4 3 2 1
```
# 3. list
通过双向链表实现，随机存取没效率，但是对插入和删除的支持很好。需要注意的是，由于是双向链表实现，故插入对迭代器没影响，删除只会使当前迭代器失效，对其他迭代器无效。
## 3.1 插入与删除
```cpp
#include <list>
list<int> lin(10,0);
lin.push_back(1);
lin.insert(lin.begin+1,10);//在迭代器前插入
lin.pop_back();//删除最后的元素
lin.push_front(1);//从前面插入
lin.pop_front();//删除最前的元素
lin.remove(10);//根据值来删除
lin.erase(lin.begin()+2);//根据迭代器来删除
lin.clear();//删除所有值
```
## 3.2 首尾、尺寸与反转同vector
## 3.3 遍历
vector是可以通过\[]来进行遍历的，list则需要使用迭代器。但C++11引入auto之后可以直接用auto遍历：for(auto val : lin){cout << val << endl;}
## 3.4 sort、unique
```cpp
lin.sort();//根据小于号来排序，也可以自定义排序函数，bool comp(const int& a, const int& b)，将函数名comp作为参数。
lin.unique();//只保留第一个出现的值，将后面相同的值删除，可重定义两种类型的判断函数作为参数传入：
// a binary predicate implemented as a function:
bool same_integral_part (double first, double second)
{ return ( int(first)==int(second) ); }

// a binary predicate implemented as a class:
struct is_near {
  bool operator() (double first, double second)
  { return (fabs(first-second)<5.0); }
};
```
# 4. deque
分段连续存储，不存在capacity()和reserve()函数。相对于vector，其除了可以在前段进行插入删除外，其在不同段中的插入删除效率都是一样的，而连续存储的vector越靠近首部效率越低。
## 4.1 插入删除
```cpp
#include <deque>
deque<int> din;
din.push_back(0);
din.push_front(1);//在最前面插入1
din.pop_back();
din.pop_front();//将最前面元素推出
int front = din.front();
int back = din.back();//返回最后元素的引用
din.clear();//清除所有元素
din.erase(din.begin()+1);//删除迭代器所在位置
din.insert(din.begin(), 10);//在迭代器前插入10
din.insert(din.begin(), 2， 10);//在迭代器前插入两个10
```
## 4.2 没有反转、size、resize、empty与vector一致。
# 5. stack
默认用deque来作为存放元素的实际容器，之所以用deque是因为其移除元素会释放内存，并且不用重新分配内存时复制所有元素。也可以显式地声明容器，如std::stack\<int,std::vector\<int\> \> st;只要其支持back(),push\_back(),pop\_back()等操作。
## 5.1 插入与删除
```cpp
#include <stack>
stack<int> sin(10,0);
sin.push(10);//在最顶端插入一个数
sin.top();//最顶端元素的引用
sin.pop();//将最顶端元素删除
```
# 6. map
```cpp
//类模板定义：
template < class Key,                                     // map::key_type
           class T,                                       // map::mapped_type
           class Compare = less<Key>,                     // map::key_compare
           class Alloc = allocator<pair<const Key,T> >    // map::allocator_type
           > class map;
```
map是一个关联容器，它存储的元素是一个关键值（Key）与该关键值映射的值（T）的组合。传统的数组其实是以整数作为关键值，且关键值连续，这样就可以通过array\[int]来访问映射值。map是一种特殊的数组，其键值不一定是整数，如student\[xiao_ming]就可以得到学生小明对应的信息。map的键值是唯一的。map是通过Compare函数来对Key进行排序的，其默认是小于号，一般通过平衡二叉搜索树（红黑树）来实现（已经排好序，查找时间复杂度是O(logn)）。然后通过pair\<const Key,T\>的分配器来动态分配内存。
## 6.1 构造、插入、访问与删除
```cpp
#include <map>
map<string, int> score;//如果是自定义的类型做key需要自定义比较函数传进去，如下
struct classcomp {
  bool operator() (const char& lhs, const char& rhs) const
  {return lhs<rhs;}
};
std::map<char,int,classcomp> fourth; 
//插入方式
score.insert(pair<string,int>("stu1", 100));
score.insert(map<string, int>::value_type("stu2", 100));
pair<map<string, int>::iterator, bool> insert_r; 
insert_r = score.insert(map<string, int>::value_type("stu1", 100));
if(insert_r.second == true)//如果插入成功是真，如果已经存在对应关键值则插入失败，键值维持不变
score["stu2"] = 99;//这样的插入方式，如果键值已存在则可以直接覆盖。
//访问
//1、应用前向迭代器
map<string, int>::iterator i_map;
for(i_map = score.begin(); i_map != score.end(); i_map++)
//2、应用反向迭代器
map<string, int>::reverse_iterator i_map;
for(i_map = score.rbegin(); i_map != score.rend(); i_map++)
//3、[]方式，上面已经演示，这里不再说
//查找
int count = score.count("stu2");//返回stu2出现的次数～～～因为是唯一的，so出现过就是1，没有就是0
i_map = score.find("stu2");//返回迭代器，如果不是.end()就是存在的
int a = i_map->second
也可以使用[]方式进行查找，但是如果不存在，会以默认构造函数插入一个新的。
//删除
score.clear();//清空
bool is_empty = score.empty();
score.erase(i_map);//删除迭代器所在位置
score.erase(i_map, i_map+5)
```
## 6.2 二维map
# 7. 字符串处理
详情请参考我的另一篇博客：[C++字符串处理总结（char、string）](https://haoqchen.site/2018/09/09/string-and-char/)

# 参考
[STL中map用法详解](https://blog.csdn.net/bat603/article/details/1456141)

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
