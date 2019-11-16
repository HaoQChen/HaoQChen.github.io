---
layout:     post
title:      N城市N人，通过公交车运输乘客，一定指令之后输出乘客位置和城市里人的数量（景驰18年秋招第三题）
subtitle:   编程之美
date:       2018-11-08
author:     白夜行的狼
header-img: img/in_post/NcityNpeople/black.jpeg
catalog: true
categories: C++编程实践
tags:
    - 笔试复习
    - 公司编程题
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/08/NcityNpeople/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 题目描述
运输公司A承包了某一地区的乘客运输服务。这个地区有N个城市（编号从1到N），并且在一开始，每个城市中都有且只有一位乘客，并且乘客的编号与城市的相同。由于人手短缺，这家公司在任意时刻只能派出一辆公交车。这辆车可以把一个城市中的所有乘客都运送到另一个城市中。为了更好的调配车辆，这家公司想知道在给定车辆运输记录之后，每个乘客的位置，以及这个乘客所在城市中有多少人。

总共有两种指令：  
1. 运输指令（T a b）：代表派出一辆车，把城市a中的所有乘客都送到城市b中。
2. 查询指令（Q x）：输出乘客x所在的城市，以及这个城市中有多少乘客，用空格隔开。

# 2. 输入
第一行输入包含了两个整数，N 和 A (2 < N <= 50000 , 2 < A <= 100000)。N代表了有多少个城市，A代表了有多少条指令。

接下来有A行，每行都是一条指令。

# 3. 输出
一个查询指令，对应了一行输出。每个输出包含两个用空格隔开的整数： X Y。X代表了乘客所在的城市，Y代表了这个城市中有多少乘客。

# 4. 示例
样例输入：  
3 3

T 1 2

T 3 2

Q 2

样例输出：  
2 3

# 5. 程序
```cpp
#include <iostream>
#include <vector>
#include <list>

using namespace std;

void transport(int a, int b, int* _passenger, vector<list<int>>& _city)
{
    if (a == b)
        return;
    while (!_city[a].empty()){
        _city[b].push_back(_city[a].front());
        _passenger[_city[a].front()] = b;
        _city[a].pop_front();
    }
}

int main(int argc, char** argv)
{
    int N, A = 0;
    char order;
    int temp1, temp2 = 0;
    //vector<int> Q;
    cin >> N >> A;
    if (N <= 2 || N > 50000 || A <= 2 || A > 100000)
        return 1;
    int* passenger = new int[N + 1];
    vector<list<int>> city;
    city.resize(N + 1);
    for (int i = 1; i <= N; ++i){
        passenger[i] = i;
        city[i].push_back(i);
    }
    while (A--){
        cin >> order;
        if (order == 'Q'){
            cin >> temp1;
            //Q.push_back(temp1);
            cout << passenger[temp1] << ' ' << city[passenger[temp1]].size() << endl;
        }
        else{
            cin >> temp1 >> temp2;
            transport(temp1, temp2, passenger, city);
        }
    }
    //for (int i = 0; i < Q.size(); ++i){
    //cout << passenger[Q[i]] << ' ' << city[passenger[Q[i]]].size() << endl;
    //}
    return 0;
}
```
  
<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
