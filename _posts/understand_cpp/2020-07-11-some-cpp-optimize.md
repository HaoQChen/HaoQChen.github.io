---
layout:     post
title:      一些凑不成一篇文章的C++优化技巧
subtitle:   
date:       2020-07-11
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories:  C++深入浅出
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2020/07/11/some-cpp-optimize/>

有一些比较小的优化技巧，凑不成一篇文章，在这里做个记录。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. Strength reduction

译作`强度折减`？这是编译器的优化技术，现在一般的编译器都已经能够自动识别，不需要我们自己实现。但有些比较老，或者功能不强的编译器还是最好自己整一下。

这个概念诞生是因为不同指令在CPU中的执行时间是不一样的，比如乘法的执行时间就远远大于移位，乘法也远远大于加法。那自然就有人会想将乘法这种高强度的计算转换成移位或者加法。

## 1.1 基本运算
以下是一些可以进行Strength reduction的操作，引自维基百科：

![](/img/in_post/some_cpp_optimize/strength_reduction_operation.png)

目前常见的编译器应该都会对操作数是`2^n`的进行优化，但其他的不太敢保证。实在不放心可以自己优化，记得很早前做单片机的时候，那些编译器就真的需要自己优化，否则分分钟不够时间。

## 1.2 浮点数除法转乘法

这里有一点值得提醒，同一类型**乘法占用的CPU时间是比除法要少**的，所以能写乘法就不要写除法。

快到什么程度呢，1个除法比3个乘法还要耗时，即使是开了O2优化：

详细代码请参考[github中的strength_reduction.cpp](https://github.com/HaoQChen/code_test/blob/master/strength_reduction.cpp)

```cpp
// （1）两次除法，一次加法
mul.start();
for (int j = 0; j < i; ++j){
    result[j] = a1[j] / b1[j] + a2[j] / b2[j];
}
mul.stop();
// （2）一次除法，一次加法，三次乘法
result.clear();
plus.start();
for (int j = 0; j < i; ++j){
    result[j] = (a1[j] * b2[j] + a2[j] * b1[1]) / (b1[j] *b2[j]);
}
plus.stop();
```

![](/img/in_post/some_cpp_optimize/mul_vs_division.png)

# 2. 用空间换时间

这个最常见的就是先进行预计算，然后存到数组中备用。比如`sin`和`cos`，在机器人以及定位建图等经常会用到，而他们耗时又非常多，我们可以搞个36000大小的数组，预先计算好`sin`的值，0.01度的分辨率已经能满足大多数人对精度的要求了。

但也有人指出，使用lookup table的方式时，内存读取有时会比重新计算还要耗时，尤其是多线程存在race condition时。

# 3. 减少临时对象的产生

## 3.1 多使用+=、-=、*=和/=

```cpp
int a = 0;
a = 10 + a; // 有临时变量产生

a += 10; // 无临时变量产生
```

## 3.2 理清赋值与构造的区别

```cpp
std::string s3_1; 
s3_1 = s1 + s2; // 此处是先构造再赋值，产生临时对象，这是最差的代码

std::string s3_2 = s1 + s2; // 此处是直接构造，产生临时对象，次好

std::string s3_3(a);
s3_3 += b; // 不产生临时变量，最好
```

## 3.3 使用std::move充分利用临时变量

当某个临时变量后面不需要再用到时，可以在赋值或emplace_back时使用`std::move`将其变为右值，这样能减少一次析构和一次构造，让临时变量得到充分利用。

## 3.4 使用std::make_shared替代new表达式
像下面这样的语句：

`std::shared_ptr<MyClass> p(new MyClass("hello", 123));`

其实是会调用两次内存管理器：第一次用于创建 MyClass 的实例，第二次用于创建被隐藏起来的
引用计数对象。`make_shared`可以分配一块独立的内存来同时保存引用计数和`MyClass`
的一个实例：

`std::shared_ptr<MyClass> p = std::make_shared<MyClass>("hello", 123);`


# 4. 一句话就能说明的事
### 4.1 延迟声明局部变量

这是C++相对于C的改进，C的函数中，变量的定义必须放在最开头，但C++的变量定义可以放在函数的任意地方，甚至可以放在return前（虽然没什么用）。延迟声明的意思是要用到再声明，这样就只会在用到时再声明，没用到时就省了。

### 4.2 构造函数使用参数列表初始化

参数列表初始化会直接往内存里填值或者in-place构造，如果不用参数列表初始化，需要先生成内存和对象，再进行一次赋值操作，时间浪费很多。

### 4.3 尽量用std::array替代std::vector

前者的size在编译的时候就确定下来，所以它的数据可以存放在栈区，一般是C风格的数组的一个简单封装。后者size是可以动态调整的，所以一般是放在堆区，当数据量非常大时，从堆中读取数据会造成很多的`cache misses`导致效率下降。但栈区不适合放size很大的array，所以比较大的还是需要放vector。

### 4.4 减少条件分支

正常情况下，在执行一条指令的过程中，下一条指令已经被缓存了。但如果存在条件分支时，只有分支确定了，对应的指令才会被加载，这段时间相当于被白白浪费。

### 4.5 简化表达式

`y = a*x*x*x + b*x*x + c*x + d;` VS `y = (((a*x + b)*x) + c)*x + d;`

后者比前者少了三次乘法运算，这使用了**霍纳法则**


# 参考

+ [Strength reduction的Wiki](https://en.wikipedia.org/wiki/Strength_reduction?spm=a2c4e.10696291.0.0.2ae519a4lbLrYm)
+ [C++性能优化一个大牛的总结](https://developer.aliyun.com/article/412574)值得细度很多遍
+ [Tips for Optimizing C/C++ Code](https://people.cs.clemson.edu/~dhouse/courses/405/papers/optimize.pdf)
+ 《C++性能优化指南》

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
