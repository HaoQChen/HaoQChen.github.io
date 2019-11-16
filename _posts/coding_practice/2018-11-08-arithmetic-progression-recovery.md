---
layout:     post
title:      等差数列偶数被除2删除后的恢复问题（2018小马智行秋招计算机视觉第三道编程题）
subtitle:   编程之美
date:       2018-11-08
author:     白夜行的狼
header-img: img/in_post/arithmetic_progression_recovery/black.jpeg
catalog: true
categories: C++编程实践
tags:
    - 小马智行
    - 等差数列
    - 等差数列恢复问题
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/08/arithmetic-progression-recovery/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**
# 1. 题目描述
小P写下了一个等差数列，然后小Q将等差数列中的所有偶数都除以2（一直除以2，直到变成奇数为止）。然后小P发现等差数列被改了，现在他要还原出原来的等差数列。如果有多种可能的答案，请输出首项最小的等差数列。
# 2. 输入
第一行一个整数N（4 <= N <= 50），表示等差数列的整数数量。

之后N行，每行一个奇数A[i]，依次表示小Q除以2之后得到的奇数列，保证1 <= A[i] <= 1000.
# 3. 输出
N行，每行一个整数，表示小P原来写下的等差数列。
# 4. 示例
6  
1  
1  
3  
1  
5  
3  
# 5. 程序
没有提交系统，只在本地测试了样例
```cpp
#include <iostream>
#include <algorithm>

using namespace std;

typedef short int T;

struct ARI_PRO{
    T begin;
    T step;
};

bool is_double(T a, T b)
{
    while (a < b){
        a = a << 1;
    }
    if (a == b)
        return true;
    return false;
}

ARI_PRO get_ari_pro(T* A, T N)
{
    int i = 0;
    int temp = 0;
    ARI_PRO result;
    T step = A[1] - A[0];
    for (i = 2; i < N; ++i){//begin with odd, step by even
        if ((A[i] - A[i - 1]) != step)
            break;
    }
    if (i == N){
        result.begin = A[0];
        result.step = step;
        return result;
    }
    temp = A[0];
    step = (A[2] - A[0]) / 2;//begin with odd, step by odd
    for (i = 1; i < N; ++i){
        temp = temp + step;
        if ((i & 1) && !is_double(A[i], temp))
            break;
        else if ((!(i & 1)) && A[i] != temp)
            break;      
    }
    if (i == N){
        result.begin = A[0];
        result.step = step;
        return result;
    }
    step = (A[3] - A[1]) / 2;//begin with even, step by odd
    temp = A[1] - step;
    for (i = 0; i < N; ++i){
        if ((!(i & 1)) && !is_double(A[i], temp))
            break;
        else if ((i & 1) && A[i] != temp)
            break;
        temp = temp + step;
    }
    if (i == N){
        result.begin = A[0];
        result.step = step;
        return result;
    }
}

int main(int argc, char** argv)
{
    T N;
    cin >> N;
    if (N > 50 || N < 4)
        return 0;
    T* A = new T[N];
    T temp;
    for (int i = 0; i < N; ++i)
        cin >> A[i];
    ARI_PRO result = get_ari_pro(A, N);
    temp = result.begin;
    for (int i = 0; i < N; ++i){
        cout << temp << endl;
        temp += result.step;
    }
    delete[] A;
    return 0;
}
```
# 6. 思路
很多人可能会想用动态规划去求解。。。这个复杂度是指数级别的~~~~

其实仔细分析一下可以知道，实际只有以下四种情况

|`start`\\*step* | *odd（奇数）* | *even（偶数）*|
| :------:  |  :------:  |  :------:  |
|`odd（奇数）`| （2）第0,2个数没变，作差/2就可以求出step，然后构建正确的等差数列。对奇数数列进行遍历，如果是双数的索引（从0开始）则判断是否相等，如是奇数索引则判断奇数数列中的数一直乘以2能否等于正确的等差数列。|（1）原来就所有数都是奇数，所以整个数列并没有改变，直接判断是否正确即可|
|`even（偶数）`|（3）第1，3个数没有变，作差/2即可求出step。然后剩下步奏与（2）相似 | 其实偶偶的话是会退化为剩下三种的，所以不必考虑|

考虑到如果有多个结果，输出首项最小的，所以安排了（1）（2）（3）的判断顺序。理论上负责度还是n*K，K很小？

不过只通过了测试用例，没上传到系统检验
  
<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
