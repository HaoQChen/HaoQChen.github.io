---
layout:     post
title:      emplace_back VS push_back
subtitle:   
date:       2020-01-17
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories:  深入理解C++
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2020/01/17/emplace_back-vs-push_back/>

`std::vector`中实现了这两个函数，主要作用都是向一个`vector`中增加一个元素，但它们其实有很多细微的差别。有很多人似乎对这两个函数有一些误解，找了一些资料，然后自己做了个实验总结了一下这两个函数的异同。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 总结及推荐
## 1.1 异同点

1. 如果参数是**左值**，两个调用的都是copy constructor
2. 如果参数是**右值**，两个调用的都是move constructor（C++ 11后push_back也支持右值）
3. 最主要的**区别**是，emplace_back支持in-place construction，也就是说emplace_back(10, "test")可以只调用一次constructor，而push_back(MyClass(10, "test"))必须多一次构造和析构

## 1.2 需要澄清的一些误解

1. `emplace_back`的效率比`push_back`高，无论什么情况下都高，所以可以无脑用。从上面1、2点可以看到，两者其实没有区别
2. `push_back`不支持右值参数，不能调用move constructor，效率低。由[C++ Reference](http://www.cplusplus.com/reference/vector/vector/push_back/)可以得知，C98是没有右值形参的，但C++11已经增加了。
3. `emplace_back`的优势是右值时的效率优化。这是最大的误解，`emplace_back`的最大优势是它可以直接在vector的内存中去构建对象，不用在外面构造完了再copy或者move进去！！！

## 1.3 使用建议

1. 左值用`push_back`
2. 右值用`emplace_back`
3. 局部变量尽量使用`emplace_back`in-place构建，不要先构建再拷贝或移动。

# 2. 实际测试

## 2.1 测试代码

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <time.h>

class BaseClass
{
public:
  BaseClass(const std::string name, int count) : name_(name), count_(count)
  {
    std::cout << name_ << " constructor called" << std::endl;
  } 
  BaseClass(const BaseClass& b)
  {
    this->name_ = b.name_;
    std::cout << name_ << " copy constructor called" << std::endl;
  } 
  BaseClass(BaseClass&& b)
  {
    this->name_ = b.name_;
    std::cout << name_ << " move constructor called" << std::endl;
  } 
  virtual ~BaseClass()
  {
    std::cout << name_ << " destructor called" << std::endl;
  }
private:
  std::string name_;
  int count_;
};

int main(int argc, char** argv)
{
  std::vector<BaseClass> vec_bc;
  std::vector<std::string> vec_s;
  vec_bc.reserve(10); // 不提前reserve会有多次拷贝操作

  std::cout << "--------------------------------emplace_back rvalue:" << std::endl;
  vec_bc.emplace_back(BaseClass("b1", 1));
  vec_bc.emplace_back("b1_1", 1);

  std::cout << "--------------------------------push_back rvalue:" << std::endl;
  vec_bc.push_back(BaseClass("b3", 1));
  // vec_bc.push_back("b4_1");// 不能通过编译

  std::cout << "--------------------------------emplace_back lvalue:" << std::endl;
  BaseClass b2("b2", 1);
  vec_bc.emplace_back(b2);
  vec_bc.emplace_back(std::move(b2));

  std::cout << "--------------------------------push_back lvalue:" << std::endl;
  BaseClass b4("b4", 1);
  vec_bc.push_back(b4);
  vec_bc.push_back(std::move(b4));

  // vec_bc.shrink_to_fit(); // 存在移动的可能
  std::cout << "--------------------------------destruct:" << std::endl;
}
```

## 2.2 编译指令

```bash
g++ emplace_push_back.cpp -std=c++11 -o test -O0
```

## 2.3 结果输出

```
--------------------------------emplace_back rvalue:
b1 constructor called
b1 move constructor called
b1 destructor called
b1_1 constructor called
--------------------------------push_back rvalue:
b3 constructor called
b3 move constructor called
b3 destructor called
--------------------------------emplace_back lvalue:
b2 constructor called
b2 copy constructor called
b2 move constructor called
--------------------------------push_back lvalue:
b4 constructor called
b4 copy constructor called
b4 move constructor called
--------------------------------destruct:
b4 destructor called
b2 destructor called
b1 destructor called
b1_1 destructor called
b3 destructor called
b2 destructor called
b2 destructor called
b4 destructor called
b4 destructor called
```

## 2.4 结果分析

1. 可以看到，emplace和push对于右值是没有差异的，左值也是没有差异的，调用的构造函数类型和数量都是一样的。
2. 区别在于`b1_1`这种构造方式，`emplace_back`只调用一次普通构造函数，`push_back`直接不支持这种操作。

## 2.5 我该怎么办

先来看两者的实现源码：

```cpp
void push_back(const value_type& __x)
{
    if (this->_M_impl._M_finish != this->_M_impl._M_end_of_storage)
    {
        _Alloc_traits::construct(this->_M_impl, this->_M_impl._M_finish, __x);
        ++this->_M_impl._M_finish;
    }
    else
    #if __cplusplus >= 201103L
        _M_emplace_back_aux(__x);
    #else
        _M_insert_aux(end(), __x);
    #endif
}



void push_back(value_type&& __x)
{ 
    emplace_back(std::move(__x)); 
}



#if __cplusplus >= 201103L
template<typename _Tp, typename _Alloc>
template<typename... _Args>
void vector<_Tp, _Alloc>::emplace_back(_Args&&... __args)
{
    if (this->_M_impl._M_finish != this->_M_impl._M_end_of_storage)
    {
        _Alloc_traits::construct(this->_M_impl, this->_M_impl._M_finish, std::forward<_Args>(__args)...);
        ++this->_M_impl._M_finish;
    }
    else
        _M_emplace_back_aux(std::forward<_Args>(__args)...);
}
#endif
```

可以看到：

1. 当参数是左值时，`push_back`和`emplace_back`的区别在于后者对参数多进行了一个`std::forward`操作
2. 当参数是右值时，`push_back`其实是调用的`emplace_back`实现的。

所以什么时候该用什么就很明显了。

# 3. 题外话

上面的代码有两句话特别注释了，分别是：


```cpp
vec_bc.reserve(10); // 不提前reserve会有多次拷贝操作
```

以及

```cpp
// vec_bc.shrink_to_fit(); // 存在移动的可能
```

大家可以注释掉第一句或者取消第二句的注释试试，会出现非常多莫名其妙的copy constructor和析构。

`push_back`和`emplace_back`的说明里都有类似的一句话：“This effectively increases the container size by one, which causes an automatic reallocation of the allocated storage space if -and only if- the new vector size surpasses the current vector capacity.”

意思就是vector的`size`超过`capacity`时会重新进行内存分配（一般是double），并把原有的数据拷贝到新申请的地址。这是vector的实现细节，有兴趣可以自己钻研。

# 参考

+ [C++ Reference std::vector::push_back](http://www.cplusplus.com/reference/vector/vector/push_back/)
+ [C++ Reference std::vector::emplace_back](http://www.cplusplus.com/reference/vector/vector/emplace_back/)

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
