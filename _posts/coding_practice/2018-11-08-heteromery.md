---
layout:     post
title:      输入不同进制的数，然后找异数（2018小米秋招软件开发工程师第一道编程题）
subtitle:   编程之美
date:       2018-11-08
author:     白夜行的狼
header-img: img/in_post/heteromery/black.jpeg
catalog: true
categories: C++编程实践
tags:
    - 小米软件开发
    - 找异数
    - 字符串处理
    - 进制转换
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/08/heteromery/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 题目描述
定义：数值序列中包含2~16进制整数，如果序列中有一个数，与序列中其他任何一个数大小都不相等，则这个数叫做“异数”。请找出给定数值序列中的所有“异数”。

# 2. 输入
数值序列i行（0 < i）。每一行分别是进制和数值，以“#”分割。如：n#m。其中n是整数，代表n进制（1 < n< 17），m是n进制下的数值。

输入序列以“END”结束。

# 3. 输出
j行（0 < j <= i），每一行都是输入序列的“异数”，要求：

按照输入序列的原序输出

如果没有异数，输出“None”

结束符不用输出。

# 4. 示例
10#15  
4#32  
4#33  
8#17  
END  

输出：4#32  

# 5. 程序
```cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <map>

using namespace std;

int main(int argc, char** argv)
{
    string str, head, num;
    stringstream ss;
    vector<int> heads;
    vector<int> nums;
    vector<string> org_str;
    int temp;
    size_t temp_i;
    bool is_None = true;

    map<int, bool> my_map;
    while (1){
        getline(cin, str);
        if (str == "END")
            break;
        org_str.push_back(str);
        int pos = str.find('#');
        head = str.substr(0, pos);
        num = str.substr(pos+1);
        temp = stoi(num, &temp_i, stoi(head));
        nums.push_back(temp);
    }
    for (int i = 0; i < nums.size(); ++i){
        auto insert_r = my_map.insert(pair<int, bool>(nums[i], false));
        if (insert_r.second == false)
            my_map[nums[i]] = true;
    }
    for (int i = 0; i < nums.size(); ++i){
        if (my_map[nums[i]] == false){
            cout << org_str[i] << endl;
            is_None = false;
        }
    }
    if(is_None)
        cout << "None" << endl;
    return 0;
}
```

# 6. 思路
其实这道题只是考了基本的字符串操作、字符串转整形，进制转换等。熟悉基本的处理函数就一点都不难。详情参考之前的一篇博客[C++字符串处理总结（char、string）](https://haoqchen.site/2018/09/09/string-and-char/)。这里用string来读入，然后找到‘#’后进行字符串分割后，用stoi这个函数来进行进制的转换。接下来使用map这个数据结构以及他的一些特性，判断哪个数是有重复的，在第一个for循环中，插入所有转换成10进制后的数，有重复的数对应map的位置会被置为true。最后一个for就是输出了。最后判断是否为空，再进行输出。稳稳的100%。

这里其实还可以做一些结构和顺序的优化的，时间比较赶就没有做了。

  
<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
