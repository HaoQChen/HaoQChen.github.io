---
layout:     post
title:      有n根长度不同的木棒，随意选取三根凑一个合法的三角形，求总拼凑方案的数量（2018腾讯软件开发-后台开发方向秋招补考试题第三题）
subtitle:   编程之美
date:       2018-11-08
author:     白夜行的狼
header-img: img/in_post/triangle_numbers/black.jpeg
catalog: true
categories: C++编程实践
tags:
    - 腾讯后台
    - 编程题
    - 三角形
    - 木棒
    - 拼凑三角形
--- 
# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/08/triangle-numbers/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**
# 1. 题目描述
有n根长度不同的木棒，随意选取三根凑一个合法的三角形，求总拼凑方案的数量。对于两个方案，只要有一根木棒的长度不同，则视为不同拼凑方案。
# 2. 输入
第一行为正数t（0 <= t <= 10），表示测试用例数

接下来每两行一个测试数据，第一行一个整数n（3 <= n <= 2000）表示木棒数量

第二行n个不一样的正整数li（1 <= li <= 10^9），表示每根木棒的长度。
# 3. 输出
对于每一个测试用例，输出一个正整数表示方案数
# 4. 示例
2  
4  
14 21 94 35  
6  
10 16 87 43 51 75  
# 5. 程序
```cpp
using namespace std;

typedef unsigned int T;

int triangle_nums(T* data, int size)
{
    int counts = 0;
    sort(data, data + size);
    for (int x = 0; x < size-2; ++x){
        for (int y = x + 1; y < size - 1; ++y){
            T xy = data[x] + data[y];
            for (int z = y + 1; z < size; ++z){
                if (xy > data[z]){
                    //if ((data[z] + data[x]) > data[y] && (data[z] + data[y]) > data[x])
                        ++counts;
                }
                else{
                    break;
                }
            }
        }
    }
    return counts;
}

int main(int argc, char** argv)
{
    int t;
    int n;
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> t;
    if (t < 1 || t > 10)
        return 0;
    T* l = new T[2000];
    while (t--){
        cin >> n;
        if (n < 3 || n > 2000){
            delete[]l;
            return 0;
        }
        for (int i = 0; i < n; ++i)
            cin >> l[i];
        cout << triangle_nums(l, n) << endl;
    }
    delete[]l;
    return 0;
}
```

# 6. 思路
一开始使用暴力求解，三层遍历，然后x+y>z&&y+z>x&&x+z>y。但复杂度太大，达到了n^3，后面超出时间，只通过了50%。后来想到了先从小到大排序（时间复杂度nlog(n)）。再进行x+y>z，这样只要某个z不满足条件，后续的z也肯定不满足，就可以提前退出。修改后增加到60%左右，同样出现了超时，完全没辙了。最后一分钟仔细思考发现，如果是已经排序了的，只要确保x+y>z就可以，因为y+z>x&&x+z>y这个时候是肯定满足的。最后注释掉代码中的一个if就100%了。


  
<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
