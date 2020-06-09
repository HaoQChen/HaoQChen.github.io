---
layout:     post
title:      C++各种循环方式梳理及对比之高级循环
subtitle:   
date:       2020-06-08
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories:  C++深入浅出 
publish: false
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2020/06/08/all-kind-of-loop-2/>

上一篇文章深入到汇编对比了while和for的效率问题，这篇将集中在几种看上去比较高大上的循环写法。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. std::for_each

# 1.1 定义

```cpp
template <class InputIterator, class Function>
Function for_each (InputIterator first, InputIterator last, Function fn);
```

第一和第二个参数分别是迭代器的首尾地址，最后一个传入的是函数对象。这就要求：

1. 遍历的对象必须是实现了迭代器的结构，比如std::vector、std::queue等。
2. 要将处理方法封装成函数对象，包括lambda表达式、仿函数对象、函数指针、std::function等。

官网说了，这个函数的功能跟下面的代码是等效的：

```cpp
template<class InputIterator, class Function>
Function for_each(InputIterator first, InputIterator last, Function fn)
{
  while (first!=last) {
    fn (*first);
    ++first;
  }
  return fn;      // or, since C++11: return move(fn);
}
```

说白了就是一个利用迭代器实现的while遍历，这是在C++11的auto之前出现的。

# 2. 用法

最简单就是使用lambda表达式来实现了：

```cpp
std::vector<int> container;
...
std::for_each(container.begin(), container.end(), [](int& i){
    i+= 10;
});
```
更多的应用可以参考[如何使用std::for_each以及基于范围的for循环 ](https://elloop.github.io/c++/2015-12-22/learning-using-stl-26-std-for-each)这篇文章。

我尝试去找这种用法跟我们最原始的for-loop的区别，各位大佬的意思是，for_each是auto之前的产物，主要防止新手用for-loop各种出错，而且能避免不会用而导致性能下降。还有降低圈复杂度的？？？

比如很多人会写成`for(auto it = c.begin(); it <= c.end(); ++it)`，但不是所有迭代器都实现了小于、大于号，要写成`for(auto it = c.begin(); it != c.end(); ++it)`



# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
