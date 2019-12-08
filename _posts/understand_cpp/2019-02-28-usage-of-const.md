---
layout:     post
title:      C++const的多种用法
subtitle:   
date:       2019-02-28
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories: C++深入浅出 
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/02/28/usage-of-const/>

在看《effective C++》前觉得代码都是自己写的，加不加这些const修饰，注不注意格式都无所谓啦，反正自己知道。看完后印象比较深的两点，一个是你设计的类有可能会给别人用，你这些良好的习惯可以防止别人在用你的类的时候出现一些低级错误，从而浪费时间。多人合作的时候也能够节省很多交流和统一意见的时间，一个合适的const使得代码一目了然。二则，代码会有版本更迭，再过一段时间，你或许会忘记自己当初的想法，良好的习惯这个时候就能给自己节省很多时间。所以，**在合适的地方加上合适的const吧**

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 在函数末尾
一般在类中使用，表明其是const成员函数，不能修改成员变量，也即意味着不能调用非const成员函数。除非非静态成员变量前面加上了`mutable`修饰符，表明其是多变的。
```cpp
void print2() const{
    cout<<num<<endl;
}
```
# 在函数前面
修饰函数返回值为const类型，只能读取，不能修改。
```cpp
const bool is_man(){
    return true;
}
bool a = is_man();//error
const bool b = is_man();//right
```
# 作为函数参数
作为函数参数有三种形式，一种是普通的变量前面，如下面的第二个参数。一般只是起到警示的作用，因为形参本来就不可改变，函数内部会再生成一个实参。第二种是指针，详见下面指针部分的介绍。这里重点说下第三种，常引用，如下面函数第一个形参。一般用于数据量比较大的数据类型，不想生成实参的过程中产生大量的拷贝消耗，就只好用引用呗，又不想函数修改这个形参，那就加个const咯。
```cpp
void saveImage(const Mat& m, const string path)
```


# 在指针前后
如果是普通类型，那大家应该都知道，表明这个变量是常量，不可变，如
```cpp
const int kValue;
int const kValue;
```
但如果用const修饰的指针，const在前还是在后就差距很大了。
```cpp
//kValue是常量指针，其指向的值不可变
const int* kValue;
int const *kValue;//不建议这种写法
//kPointer是常指针，指针本身不可变
int* const kPointer;
//两者都不可变
const int* const kPV
```

# 修饰成员变量
同上面一样，常量是需要在初始化时就赋值的，后面不能再修改。由于类的特殊机制，其初始化是在进入类的构造函数之前进行的，所以其唯一的初始化方法就是使用参数初始化表的形式：
```cpp
Box::Box(int h, int w, int t):height(h), width(w), kThreshold(t){}
```
这里kThreshold就是类常量成员。

# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
