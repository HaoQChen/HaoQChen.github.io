---
layout:     post
title:      ++i、i++、i+=1、i=i+1的区别
subtitle:   深入理解C++
date:       2018-10-15
author:     白夜行的狼
header-img: img/in_post/i_plus_plus/post-bg-halting.jpg
catalog: true
categories: C++深入浅出
tags:
    - 自增
    - 运算符重载
    - 左右值
    - 自增效率
    - i++
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/10/15/difference-between-++i-i++-i+=1-i=i+1/>  
面试被问到，上面这四个有什么区别。总结了一下，如果觉得还不错就关注一下博主呗，博主会长期更新自己的学习和收获。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 首先对于内置类型，对于现代编译器而言，这四个的效率都是没有区别的
我在VS2013下进行编译运行，然后调试->窗口->反汇编，查看汇编代码后发现，这四个都是一样的。。。。。  
![++int](/img/in_post/i_plus_plus/plus_plus_int.png)  
![int++](/img/in_post/i_plus_plus/int_plus_plus.png)  
![int=int+1](/img/in_post/i_plus_plus/int_int_plus.png)  
![int+=1](/img/in_post/i_plus_plus/int_plus_one.png)  
dword 双字 就是四个字节  
ptr pointer缩写 即指针  
\[]里的数据是一个地址值，这个地址指向一个双字型数据  
比如mov eax, dword ptr \[12345678] 把内存地址12345678中的双字型（32位）数据赋给eax寄存器。

# 2. 但是对于自定义类型，这就不一样了
## 2.1 a++与++a区别
1. a++是先赋值再自增，++a是先自增再赋值。
2. a++是先用临时对象保存原来的对象，然后对原对象自增，再返回临时对象，不能作为左值；++a是直接对于原对象进行自增，然后返回原对象的引用，可以作为左值。
3. 由于要生成临时对象，a++需要调用两次拷贝构造函数与析构函数（将原对象赋给临时对象一次，临时对象以值传递方式返回一次）；++a由于不用生成临时变量，且以引用方式返回，故没有构造与析构的开销，效率更高。

左值一般是可以放在赋值符号左边的值，其在内存中有实体；右值一般只能放在赋值符号右边，不具有内存实体，无法通过取地址获得相应对象。

下面将通过实际代码来找出两者的区别，考虑如下类：
```cpp
class Point{
    int x_;
    int y_;
public:
    Point(int x = 0, int y = 0);
    Point(const Point&);
    ~Point();
    Point& operator++();//前置
    const Point operator++(int);//后置
    Point operator+(const Point&);
    Point& operator+=(const Point&);
    void DisplayPoint();
};

Point& Point::operator+=(const Point& _right)
{
    this->x_ += _right.x_;
    this->y_ += _right.y_;
    return *this;
}

Point Point::operator+(const Point& _right)
{
    Point temp;
    temp.x_ = this->x_ + _right.x_;
    temp.y_ = this->y_ + _right.y_;
    return temp;
}


Point& Point::operator++()
{
    ++x_;
    ++y_;
    return *this;
}

const Point Point::operator++(int)
{
    Point temp(*this);
    this->x_++;
    this->y_++;
    return temp;
}

Point::Point(int x, int y)
{
    x_ = x;
    y_ = y;
    cout << "this is constructor" << endl;
}

Point::Point(const Point& b)
{
    this->x_ = b.x_;
    this->y_ = b.y_;
    cout << "this is copy constructor" << endl;
}

Point::~Point()
{
    cout << "this is destructor" << endl;
}

void Point::DisplayPoint()
{
    cout << "x: " << this->x_ << endl;
    cout << "y: " << this->y_ << endl;
}
```

### 2.1.1 效率检测
```cpp
Point a(1,1);
cout << endl << "this is a++: " << endl;
a++;
cout << endl << "this is ++a: " << endl;
++a;
```
将会输出：  
![code out a++&++a](/img/in_post/i_plus_plus/different_a++&++a.png)
可以看到，a++将会有两次的拷贝构造与析构的调用，效率非常低。

### 2.1.2 左右值检测
```cpp
Point b(2, 2);
Point* c;
cout << endl << "this is &b: " << &b << endl;

cout << endl << "this is c = &(++b): ";
c = &(++b);
cout << c << endl;
cout << endl << "this is c = &(b++): ";
c = &(b++);
cout << c << endl;
```
将会输出：  
![code out left or right](/img/in_post/i_plus_plus/left_or_right.png)
可以看到++b返回的对象指针跟b原来的地址是一样的，而b++返回的对象地址跟原来的b地址不一样（应该是临时对象的地址），虽然可以取到地址，但当成左值将有可能导致错误。比如b++ = c;就不会将c给b，达不到原来的目的。为此，我们应该将后置的++函数返回值定义为const类型，就可以避免这种当成左值情况出现：const Point Point::operator++(int)。另外发现返回temp的引用可以减少一次拷贝和析构，但是不建议返回局部变量的引用！！因为函数退出，局部变量将析构，引用就会指向不确定内存。

另外不要在一条语句中使用多个++，因为在不同系统中对这样的情况处理可能不一样，比如y = (4 + x++) + (6 + x++)。这条语句只能保证程序执行到下一条语句之前，x被递增两次，并不能保证4 + x++后立即自增。

## 2.2 a+=b与a=a+b的区别
a+=b返回的是a的引用，中间不涉及构造与析构，效率与++a一样。而a=a+b则会生成临时变量，而且以值传递方式返回，会有两次的构造与析构，与a++一样

# 参考
[i++和++i区别](https://www.cnblogs.com/vinke2013/p/7209187.html)  
《C++ Primer Plus》第六版P133

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**