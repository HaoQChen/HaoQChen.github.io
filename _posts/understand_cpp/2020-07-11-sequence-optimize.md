---
layout:     post
title:      优化代码逻辑
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

本文持续更新地址：<https://haoqchen.site/2020/07/11/sequence-optimize/>

很多人写代码很随意，先把功能实现了，等性能不够再来刻意地优化，但其实很多优秀的习惯能帮助我们一步到位，写出更高效的代码。

本文将总结遇到的一些例子，同一个功能，优化一下逻辑，换个写法性能就有很大提升的。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 函数放在循环内VS函数放在循环外

例子：判断一组二维的点中有哪些是满足一定条件的，比如在一个box内：

以下代码显示了关键代码，详细代码请参考[github sequence_optimize.cpp](https://github.com/HaoQChen/code_test/blob/master/sequence_optimize.cpp)这个文件

```cpp
bool isInBox(const std::pair<int, int>& point, 
             std::pair<int, int> box_pose, std::pair<int, int> box_size)
{
    return ((std::abs(point.first - box_pose.first) < (box_size.first / 2)) 
         && (std::abs(point.second - box_pose.second) < (box_size.second / 2)));
}

void findPointInBox(std::vector<std::pair<int, int>>& src, 
                    std::vector<std::pair<int, int>>& dst, 
                    std::pair<int, int> box_pose, std::pair<int, int> box_size)
{
    for (auto& point : src){
        if ((std::abs(point.first - box_pose.first) < (box_size.first / 2)) 
         && (std::abs(point.second - box_pose.second) < (box_size.second / 2))) {
            dst.push_back(point);
        }
    }
}

// （1）对每个点，调用判断函数进行判断
mul.start();
for (auto& point : data){
    if (isInBox(point, std::make_pair<int, int>(500, 1000), std::make_pair<int, int>(600, 600))){
        result.push_back(point);
    }
}
mul.stop();
// （2）将所有点传到函数中，在函数中循环进行判断
result.clear();
plus.start();
findPointInBox(data, result, std::make_pair<int, int>(500, 1000), std::make_pair<int, int>(600, 600));
plus.stop();
```

不开启编译器优化（或者O1也可以，但O2两者的时间相差不大，可能是因为判断的函数太短，使用O2优化个别编译器会将其内联），使用以下指令进行编译：

`g++ ./sequence_optimize.cpp -std=c++11 -O0`

得到结果如下：

![](/img/in_post/sequence_optimize/loop_function.png)

因为调用函数会有很多的花销，比如将当前状态压栈等，甚至比判断本身都要多，由上面可以看出，将函数放到循环中将会导致时间增加很多。可以考虑将一些非常耗时的操作放在循环外。

当然，这里的耗时操作不仅限与函数，还有一些**无关紧要的判断**：

```cpp
bool is_save data = false;

for (auto d : data){
    if (is_save_data){ // 判断和跳转本身也会占很多的资源，应尽可能减少
        saveData(d);
    }
}

// VS
if (is_save_data){
    for (auto d : data){
        saveData(d);
    }
}
```

一些**常数的计算**，比如我第一个例子中的`box_size.first / 2`，就可以将他用一个变量存起来，不用每个循环都进行计算

# 2. 根据命中成本调整判断顺序

## 2.1 &&和||运算

根据[C++关于逻辑运算的定义](https://en.cppreference.com/w/cpp/language/operator_logical)，对于内置的`&&`运算和`||`运算，如果第一个值已经能知道结果，将不再判断第二个值。

`Builtin operators && and || perform short-circuit evaluation (do not evaluate the second operand if the result is known after evaluating the first), but overloaded operators behave like regular function calls and always evaluate both operands`

所以，**将哪个条件放在第一就显得尤为重要**了，考虑下面两种情况：

```cpp
if (is_ok || checkData()) // 情况1

if (checkData() || is_ok) // 情况2
```

`is_ok`是个bool变量。

+ `checkData`是个很复杂的运算，每次需要花费很多的时间，而`is_ok`很大概率是true，情况1明显更大概率可以减少时间。
+ 如果`is_ok`比较大概率是false，`checkData`又很简单，那么情况2会更合适。

不要以为一个判断无关紧要，之前做腾讯的题，就是多一个判断和少一个判断决定了能不能AC～～（虽然有了面试机会，最后岗位也不合适，没影响最终结果）。

## 2.2 if和else

考虑将概率大的放在前面，这样能尽量减少跳转的次数。

# 3. 通过推导降低复杂度

## 3.1 逻辑推导

**每一个暴力遍历都可以有一个更优的替代方案。**

经常刷LeetCode或者企业题库的同学应该深有体会，暴力搜索往往是TLE(Time Limit Exceed)的，需要你另谋出路，降低复杂度。

之前刷的两题就真的深有体会：

+ [三根木棒凑三角形问题](https://blog.csdn.net/u013834525/article/details/82793473)
+ [等差数列偶数被除2删除后的恢复问题](https://blog.csdn.net/u013834525/article/details/82793694)

## 3.2 数学推导

纯数学推导往往是不考虑计算成本的，但要代码实现，就需要一些技巧来重写公式了：

+ 能不能重用一些计算模块，比如一个复杂的公式有很多`sin(alpha) * cos(beta)`，那我就可以将这个变成一个局部变量来重用了。
+ 能否变成递推的形式，这样每次更新就可以减少计算量了。
+ 能否化简或者将某些部分变成常量，减少运算

# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
