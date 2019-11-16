---
layout:     post
title:      各种排序算法的C++实现（冒泡排序、选择排序、插入排序、希尔排序、归并排序、快速排序、堆排序）
subtitle:   数据结构与算法
date:       2018-10-10
author:     白夜行的狼
header-img: img/in_post/all_kind_of_sort/black.jpeg
catalog: true
categories: 数据结构
tags:
    - 排序算法
    - 快速排序
    - C++
    - 归并排序
    - 堆排序
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/10/10/all-kind-of-sort/>

如果觉得还不错就关注一个呗，博主会长期更新自己的学习和收获。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

各个算法的详细介绍请参考这个博客：[十大经典排序算法（动图演示）](https://www.cnblogs.com/onepixel/articles/7674659.html)。博客有动图，介绍得非常详细，我是在此基础上用C++实现了一遍，原博客不是C++。文末有一些自己的想法，关于面试手撕代码的。

另外，希尔排序和堆排序参考了维基百科中的相关词条：

[维基百科-堆排序](https://zh.wikipedia.org/wiki/%E5%A0%86%E6%8E%92%E5%BA%8F)  
[维基百科-希尔排序](https://zh.wikipedia.org/wiki/%E5%B8%8C%E5%B0%94%E6%8E%92%E5%BA%8F)

另外，如果大家也想写一下，然后牛客网这里有一道题，大家可以到这里来测试：

[牛客网排序算法编程题](https://www.nowcoder.com/questionTerminal/508f66c6c93d4191ab25151066cb50ef)  
```
测试数据：
//11 2 5 4 1 3 9 7 8 6 11 10

//88 84419 10584 452 996650 6754 957 239 91700 9405 8560 807347 20205 957730 195132 171 45249 729108 856 6264 713998 558 2726 17671 39225 333 27534 79588 19111 62133 314 296433 940 19684 222752 741 7009 7240 49455 9348 103829 384565 1749 177 497 3953 649 46593 2630 245 270603 297637 99204 99867 89431 3986 99454 8089 934666 434 983492 39929 6769 955109 65704 18568 76695 6435 5578 744 13680 139812 775563 93104 99663 322628 6592 12941 403547 619774 5506 1515 72955 9755 728165 78168 1485 94370 7373
```
**代码:**
```cpp
#include <iostream>

using  namespace std;

void swap(int& a, int& b)
{
    int temp = b;
    b = a;
    a = temp;
}

//依次为最好的时间负责度、平均时间复杂度、最坏时间复杂度、空间复杂度

//如果左边比右边大则交换，依次冒泡出最大次大。。放到数组末尾（满足才交换，故最优是n，选择排序无论如何都需要交换）
void BubbleSort(int* _nums, int _len)//1. 冒泡排序：稳定、n n^2 n^2、1
{
    int end;
    for (int i = 0; i < _len - 1; ++i){
        end = _len - i - 1;
        for (int j = 0; j < end; ++j)
            if (_nums[j] > _nums[j + 1])
                swap(_nums[j], _nums[j + 1]);
    }
}

//依次选择最大次大。。。。放到数组末尾，冒泡不同的是，不进行交换
void SelectionSort(int* _nums, int _len)//2. 选择排序：不稳定、n^2 n^2 n^2、1
{
    int end, largest_index;
    for (int i = 0; i < _len; ++i){
        end = _len - i;
        largest_index = 0;
        for (int j = 0; j < end; ++j){
            if (_nums[j] > _nums[largest_index]){
                largest_index = j;
            }
        }
        swap(_nums[largest_index], _nums[end - 1]);
    }
}

//从左到右，向左比较，如果左边更大则将左边向右移动，直至不比左边小则插入
void InsertionSort(int* _nums, int _len)//3. 插入排序：稳定、n n^2 n^2、1
{
    int j, temp;
    for (int i = 1; i < _len; ++i){
        temp = _nums[i];
        j = i - 1;
        for (; j >= 0; --j){
            if (temp < _nums[j])
                _nums[j + 1] = _nums[j];
            else
                break;
        }
        _nums[j + 1] = temp;
    }
}

//也叫递减增量排序算法，以递减的间隔进行插入排序。
void ShellSort(int* _nums, int _len)//4. 希尔排序：不稳定、时间复杂度与间隔的选择有关，比n^2要小、1
{
    int gap = 1;
    int temp, j;
    while (gap < _len / 3)
        gap = 3 * gap + 1;
    while (gap >= 1){
        for (int i = gap; i < _len; ++i){
            temp = _nums[i];
            for (j = i; j >= gap && _nums[j - gap] > temp; j -= gap)
                _nums[j] = _nums[j - gap];
            _nums[j] = temp;
        }
        gap /= 3;
    }
}

void Merge(int** _numss, int _head, int _tail, int _arr_index)
{
    if ((_tail - _head) < 1){
        _numss[_arr_index][_tail] = _numss[0][_tail];
        return;
    }

    int mid = (_tail - _head) / 2 + _head;
    int i = _head, j = mid + 1, k = _head;

    Merge(_numss, _head, mid, 1 - _arr_index);
    Merge(_numss, mid + 1, _tail, 1 - _arr_index);

    while (i <= mid && j <= _tail){
        if (_numss[1 - _arr_index][i] > _numss[1 - _arr_index][j])
            _numss[_arr_index][k++] = _numss[1 - _arr_index][j++];
        else
            _numss[_arr_index][k++] = _numss[1 - _arr_index][i++];
    }
    while (i <= mid)
        _numss[_arr_index][k++] = _numss[1 - _arr_index][i++];
    while (j <= _tail)
        _numss[_arr_index][k++] = _numss[1 - _arr_index][j++];
}

//分治法来进行排序，即二分排序，然后对已排序的两部分进行合并
void MergeSort(int* _nums, int _len)//5. 归并排序：稳定、nlogn nlogn nlogn、n
{
    int* temp = new int[_len];
    int* numss[2] = { _nums, temp };
    Merge(numss, 0, _len - 1, 0);
    delete[] temp;
}

void Partition(int* _nums, int _head, int _tail)
{
    if (_head >= _tail)
        return;
    int small = _head;
    for (int i = _head; i < _tail; ++i){
        if (_nums[i] <= _nums[_tail]){
            swap(_nums[i], _nums[small]);
            ++small;
        }
    }
    swap(_nums[_tail], _nums[small]);
    Partition(_nums, _head, small - 1);
    Partition(_nums, small + 1, _tail);
}

//随机选择一个基准，然后以此基准将数组分成大于、小于基准两部分。迭代下去。这里以最后一个值作为基准，不随机了
void QuickSort(int* _nums, int _len)//6. 快速排序：不稳定、nlogn nlogn n^2、nlogn（迭代产生的？）
{
    Partition(_nums, 0, _len - 1);
}

void max_headify(int* _nums, int _head, int _tail)
{
    int dad = _head;
    int son = (_head << 1) + 1;
    while (son <= _tail){
        if ((son + 1) <= _tail && _nums[son + 1] > _nums[son])
            ++son;
        if (_nums[dad] > _nums[son])
            return;
        else{
            swap(_nums[dad], _nums[son]);
            dad = son;
            son = (dad << 1) + 1;
        }
    }
}

//利用数组构建最大堆，其中子节点=父节点*2+1。先对前半部分进行倒序找出最大点，然后遍历交换首尾、找出最大点
void HeapSort(int* _nums, int _len)//7. 堆排序：不稳定、nlogn nlogn nlogn、1
{
    for (int i = (_len / 2 - 1); i >= 0; --i)
        max_headify(_nums, i, _len - 1);
    for (int i = _len - 1; i >= 0; --i){
        swap(_nums[0], _nums[i]);
        max_headify(_nums, 0, i - 1);
    }
}


int main(int argc, char** argv)
{
    int n;
    cin >> n;
    if (n < 1 || n > 100)
        return 1;
    int* nums = new int[n];
    for (int i = 0; i < n; ++i)
        cin >> nums[i];
    QuickSort(nums, n);
    for (int i = 0; i < n; ++i)
        cout << nums[i] << ' ';
    delete[] nums;
    return 0;
}
```

如果是面试**现场手撕代码**的话，不知道可不可以写成函数模板，让面试官耳目一新？像酱紫：

```cpp
template<typename T>
void swap(const T& a, const T& b)
{
    T temp = b;
    b = a;
    a = temp;
}

template <typename T, typename Compare>
void max_headify(T* _nums, int _head, int _tail, Compare _comp)
{
    int dad = _head;
    int son = (_head << 1) + 1;
    while (son <= _tail){
        if ((son + 1) <= _tail && _comp(_nums[son], _nums[son + 1]))
            ++son;
        if (_comp(_nums[son], _nums[dad]))
            return;
        else{
            swap(_nums[dad], _nums[son]);
            dad = son;
            son = (dad << 1) + 1;
        }
    }
}

//利用数组构建最大堆，其中子节点=父节点*2+1。先对前半部分进行倒序找出最大点，然后遍历交换首尾、找出最大点
template <typename T, typename Compare>
void HeapSort(T* _nums, int _len, Compare _comp)//7. 堆排序：不稳定、nlogn nlogn nlogn、1
{
    for (int i = (_len / 2 - 1); i >= 0; --i)
        max_headify(_nums, i, _len - 1, _comp);
    for (int i = _len - 1; i >= 0; --i){
        swap(_nums[0], _nums[i]);
        max_headify(_nums, 0, i - 1, _comp);
    }
}

template <typename T>
void HeapSort(T* _nums, int _len)
{
    HeapSort(_nums, _len, less<T>());
}
```
这样调用形式可以有很多种：

```cpp
//默认用小于号形式，即从小到大排序
int nums[10] = {9, 8, 6, 3, 2, 1, 7, 0, 4, 5};
HeapSort(nums, 10);

//lambda表达式，比如下面这样就可以变成从大到小排序
HeapSort(nums, 10, [](int a, int b) -> bool {return a > b? true : false;});

//类重载小于号的运算符，比如下面就是将小于号重载，重载后实际变成了大于，排序变成从大到小
class B{
public:
    int a;
    friend bool operator < (const B& a, const B& b);
};

bool operator < (const B& a, const B& b)
{
    return a.a > b.a ? true : false;
}
B test[3];
test[0].a = 10;
test[1].a = 5;
test[2].a = 11;
HeapSort(test, 3);

//函数指针形式
bool comp_B(const B& a, const B& b)
{
    return a.a > b.a ? true : false;
}
HeapSort(test, 3, comp_B);

//仿函数对象
HeapSort(nums, 10, greater<int>());
//或者
class comp_class {
public:
    bool operator()(const B& a, const B& b) {
        return a.a > b.a;
    }
};
HeapSort(test, 3, comp_class());
```

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**