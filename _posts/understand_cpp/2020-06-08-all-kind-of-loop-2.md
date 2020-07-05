---
layout:     post
title:      C++各种循环方式梳理及对比（2）高级循环
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

上一篇文章[C++各种循环方式梳理及对比之深入到汇编看while和for](https://haoqchen.site/2020/05/08/all-kind-of-loop-1/)深入到汇编对比了while和for的效率问题，这篇将集中在另外几种看上去比较高大上的循环写法。

这些写法一般只是for或者while的一层封装，效率与自己实现的for循环相当，甚至要差。但他们优势在于简化了代码，并且减少了代码出错的可能。另外，C++17之后的algorithm库实现了并行运算的功能，可以快捷地通过参数配置并行计算，不用自己敲多线程。我暂时还没有到C++17，没能力介绍这方面的内容，有兴趣可以看看对应的官网链接，在参考中有给出。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. std::for_each与std::for_each_n

## 1.1 定义

### 1.1.1 std::for_each
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

### 1.1.2 std::for_each_n

```cpp
template< class InputIt, class Size, class UnaryFunction > // since C++17
InputIt for_each_n( InputIt first, Size n, UnaryFunction f );
```

`std::for_each`只遍历n个的版本，与下面的代码等效：

```cpp
template<class InputIt, class Size, class UnaryFunction>
InputIt for_each_n(InputIt first, Size n, UnaryFunction f)
{
    for (Size i = 0; i < n; ++first, (void) ++i) {
        f(*first);
    }
    return first;
}
```

在不设置并行执行规则`ExecutionPolicy`的情况下，这两个函数的执行是保证按顺序执行的。

## 1.2 用法
最简单就是使用lambda表达式来实现了：

```cpp
#include <vector>
#include <algorithm>
std::vector<int> container(10, 0);

std::for_each(container.begin(), container.end(), [](int& i){
    i+= 10;
});

std::for_each_n(container.begin(), 10, [](int& i){
    i+= 10;
});
```
比如求平均等更多的应用可以参考[如何使用std::for_each以及基于范围的for循环 ](https://elloop.github.io/c++/2015-12-22/learning-using-stl-26-std-for-each)这篇文章。

我尝试去找这种用法跟我们最原始的for-loop的区别，各位大佬的意思是，for_each是auto之前的产物，主要防止新手用for-loop各种出错，而且能避免不会用而导致性能下降。还有降低圈复杂度的？？？

比如很多人会写成`for(auto it = c.begin(); it <= c.end(); ++it)`，但不是所有迭代器都实现了小于、大于号，要写成`for(auto it = c.begin(); it != c.end(); ++it)`

# 2. 基于范围(range-based)的for循环

## 2.1 定义

这是**C++ 11新增**的一种循环，主要作用是简化一种常见的循环任务：对数组或容器类（如vector和array）的每个元素执行相同的操作。

```cpp
attr(optional) for ( range_declaration : range_expression ) 
loop_statement                                      // (until C++20)

attr(optional) for ( init-statement(optional)range_declaration : range_expression )
loop_statement                                      // (since C++20)
```

+ **attr**：函数前缀，貌似声明一些特性有用的，可选。目前不是很清楚，有兴趣可了解[attribute specifier sequence(since C++11)](https://en.cppreference.com/w/cpp/language/attributes)
+ **init-statement(optional**：这个是C++20才加上的，一个以分号`;`结尾的表达式。一般是一个初始化表达式
+ **range_declaration**：声明一个变量，变量的类型为range_expression的类型或者这个类型的引用，一般用auto来自动匹配即可。这个可以是结构化绑定声明（Structured binding declaration）。
+ **range_expression**：需要循环的数组、容器或花括号初始化列表，如果为容器，必须要实现begin函数和end函数。

基于范围的for循环可等效成下面的for：

```cpp
{
    auto && __range = range_expression ;
    for (auto __begin = begin_expr, __end = end_expr; __begin != __end; ++__begin) {
        range_declaration = *__begin;
        loop_statement
    } // (until C++17)
}
```

结构化绑定声明：

```cpp
for (auto&& [first,second] : mymap) { // since C++17
    // 使用 first 和 second 
}
```

**注意**：

+ `range_expression`不能返回临时变量，例如不能是一个返回值的函数，否则将导致不确定行为。
+ 如果`range_declaration`不是引用，而且存在`copy-on-write`特性，基于范围的for循环可能会触发一个深拷贝

## 2.2 用法

借用cppreference的一个例子来说明：

```cpp
#include <iostream>
#include <vector>
 
int main() {
    std::vector<int> v = {0, 1, 2, 3, 4, 5};
 
    for (const int& i : v) // 以 const 引用访问
        std::cout << i << ' ';
    std::cout << '\n';
 
    for (auto i : v) // 以值访问，i 的类型是 int
        std::cout << i << ' ';
    std::cout << '\n';
 
    for (auto& i : v) // 以引用访问，i 的类型是 int&
        std::cout << i << ' ';
    std::cout << '\n';
 
    for (int n : {0, 1, 2, 3, 4, 5}) // 初始化器可以是花括号初始化器列表
        std::cout << n << ' ';
    std::cout << '\n';
 
    int a[] = {0, 1, 2, 3, 4, 5};
    for (int n : a) // 初始化器可以是数组
        std::cout << n << ' ';
    std::cout << '\n';
 
    for (int n : a)  
        std::cout << 1 << ' '; // 不必使用循环变量
    std::cout << '\n';
 
}
```

# 3. std::transform

## 3.1 定义
这个函数的作用是将输入的，具有迭代器的1个或2个容器`InputIterator`做一定的操作，并将结果保存到`result`的起始位置中，**执行顺序不做保证**。

```cpp
// 定义1
template <class InputIterator, class OutputIterator, class UnaryOperation>
OutputIterator transform (InputIterator first1, InputIterator last1,
                          OutputIterator result, UnaryOperation op);
// 定义2
template <class InputIterator1, class InputIterator2,
          class OutputIterator, class BinaryOperation>
OutputIterator transform (InputIterator1 first1, InputIterator1 last1,
                          InputIterator2 first2, OutputIterator result,
                          BinaryOperation binary_op);
```

+ **unary operation**将[first1,last1)范围内的每一个元素进行op操作，并将每个op的的返回值存储到result中
+ **binary operation**将[first1,last1)的每一个元素和起始地址为`first2`对应的元素，分别作为参数1和参数2放到`binary_op`中，并将每个返回值放到result中

根据官网的介绍，这个函数等效与一下循环：

```cpp
template <class InputIterator, class OutputIterator, class UnaryOperator>
OutputIterator transform (InputIterator first1, InputIterator last1,
                          OutputIterator result, UnaryOperator op)
{
    while (first1 != last1) {
        *result = op(*first1);  // or: *result=binary_op(*first1,*first2++);
        ++result; ++first1;
    }
    return result;
}
```

## 3.2 用法

借鉴官方的例子：

```cpp
// transform algorithm example
#include <iostream>     // std::cout
#include <algorithm>    // std::transform
#include <vector>       // std::vector
#include <functional>   // std::plus

int op_increase (int i) { return ++i; }

int main () {
    std::vector<int> foo;
    std::vector<int> bar;

    // set some values:
    for (int i=1; i<6; i++)
        foo.push_back (i*10);                         // foo: 10 20 30 40 50

    bar.resize(foo.size());                         // allocate space

    std::transform (foo.begin(), foo.end(), bar.begin(), op_increase);
                                                    // bar: 11 21 31 41 51

    // std::plus adds together its two arguments:
    std::transform (foo.begin(), foo.end(), bar.begin(), foo.begin(), std::plus<int>());
                                                    // foo: 21 41 61 81 101

    std::cout << "foo contains:";
    for (std::vector<int>::iterator it=foo.begin(); it!=foo.end(); ++it)
        std::cout << ' ' << *it;
    std::cout << '\n';

    return 0;
}
```

**注意**

+ `result`可以指向输入
+ `result`容器的size要大于等于[first1,last1)的大小，如果`result`为空时，需要使用`std::back_inserter(result)`，[std::back_inserter](http://www.cplusplus.com/reference/iterator/back_inserter/?kw=back_inserter)要求result实现了`push_back`函数。这个时候会导致性能下降，详情请参考我另一篇文章[emplace_back VS push_back](https://haoqchen.site/2020/01/17/emplace_back-vs-push_back/)

# 4. std::transform、std::for_each、for的区别

1. `for_each`返回的是函数，所以可以通过函数对象来对数据求和，比如：
   
```cpp
class MeanValue
{
public:
    MeanValue() : count_(0), sum_(0) {}
    void operator() (int val)
    {
        sum_ += val;
        ++count_;
    }
    operator double()
    {
        if ( count_ <= 0 )
        {
            return 0;
        }
        return sum_ / count_;
    }
private:
    double      sum_;
    int         count_;
};
//for_each returns a copy of MeanValue(), then use operator double().
// same with:
// MeanValue mv = for_each(coll2.begin(), coll2.end(), MeanValue());
// double meanValue = mv;
// for_each返回传入MeanValue()的副本，然后调用operator double()转换为double.
double meanValue = for_each(coll2.begin(), coll2.end(), MeanValue());                       
  ```

2. `transform`的参数要求更严格点，他要求操作有返回值，而`for_each`忽略了操作返回值，所以没有这个要求
3. C++17之后algorithm相关算法都支持并行计算，修改一个参数就行，如果是for循环，需要自己实现多线程。
4. 需要注意一点，调用函数是有压栈、出栈的性能损失的，循环地调用函数性能会受很大影响。可以将整个vertor传入到函数中，再在函数中进行for循环，这样可减少这样的性能损失，这只能通过自己实现最原始的for循环实现。
5. 不并行运算的情况下，`for_each`保证执行的顺序，而`transform`不能保证执行的顺序。
6. for_each和transform都默认使用迭代器，原始for循环可以使用索引`[]`，在一些编译器上，这两者的效率是有很大区别的。具体可以参考这个测试：[c++ - bool数组上的Raw循环比transform或for_each快5倍](https://www.coder.work/article/122015)
7. 在循环次数很大时，algorithm的一些实现就可以忽略不计，各种的效率几乎是一样的。

# 参考

+ 文中连接
+ [std::for_each](https://en.cppreference.com/w/cpp/algorithm/for_each)
+ [Range-based for loop (since C++11)](https://en.cppreference.com/w/cpp/language/range-for)
+ [std::for_each_n](https://en.cppreference.com/w/cpp/algorithm/for_each_n)
+ [std::transform](https://en.cppreference.com/w/cpp/algorithm/transform)

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
