---
layout:     post
title:      扑克牌输赢判断系统（景驰18年秋招第一题）
subtitle:   编程之美
date:       2018-11-08
author:     白夜行的狼
header-img: img/in_post/card_judge/black.jpeg
catalog: true
categories: C++编程实践
tags:
    - 扑克牌
    - 判断输赢
    - 四条、顺子、葫芦、两对、三条、散排
    - 小A
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/11/08/card-judge/>

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 题目描述
这里进行游戏的扑克牌共有52张，共有2,3,4,5,6,7,8,9,T,J,Q,K,A这13种类型的牌，每一种有4张（因此在一个牌组中，同种类的牌最多只会出现4张）。此处为了方便，不考虑花色的情况，即对于每一种牌，如K，4张K的地位是等价的。不同种的牌之间有大小的关系，为A>K>Q>J>T>9>8>7>6>5>4>3>2。

5张牌所能构成的牌组有以下几种情况：

四条：5张牌中有4张相同的种类。如AAAAQ。当两副牌均为四条时，相同的那个种类的牌较大者较大。如AAAAQ大于KKKKQ。当两副牌均为四条且相同的种类的牌也相同时，第5张牌较大者较大。如AAAAQ大于AAAAJ。

葫芦（三带二）：5张牌中共有两种牌，一种有3张，一种有2张。如AAAKK。当两副牌均为葫芦时，3张的那种牌较大者较大。如AAAQQ大于KKKQQ。当两副牌均为葫芦且3张的牌相同时，2张的牌较大者较大。如AAAKK大于AAAQQ。

顺子：5张牌是大小连续的。如34567。注意此处有唯一一个特殊情况A2345也是顺子，但此刻A视为1，因此这个顺子中最大的牌是5。同时TJQKA也是顺子，此时A依然按照单张牌中最大的计算。当两副牌均为顺子时，最大的牌较大者较大。如23456大于A2345;789TJ大于45678;TJQKA则是最大的顺子。

三条：5张牌中有3张相同的牌，剩下的2张与这3张牌种类不同且互相种类不同。如AAAKQ。当两副牌均为三条时，相同的那个种类的牌较大者较大。如AAAKQ大于KKKAQ。当两副牌均为三条且相同种类的牌相同时，剩下2张牌中最大的那张较大者较大。如AAAKJ大于AAAQJ。当两副牌均为三条且相同种类的牌相同且剩下2张牌中最大的那张也相同时，第5张牌较大者较大。如AAAKQ大于AAAKJ。

两对：5张牌中共有三种牌，其中有两种各有2张，第三种有1张。如AAKKQ。此处定义“对子”为一个由两张相同的牌组成的牌组。如AAKKQ就有一个对子AA和另一个对子KK。对子的大小由组成对子的牌的种类决定。如AA大于KK。当两副牌均为两对时，最大的对子较大者较大。如AAQQJ大于KKQQJ。当两副牌均为两对且最大的对子相同时，第二个对子较大者较大。如AAKKJ大于AAQQJ。当两副牌均为两对且两个对子都相同时，第5张牌较大者较大。如AAKKQ大于AAQQJ。

一对：5张牌中有一个对子，剩下的3张牌种类与这个对子不同且互相种类不同。如AAKQJ。当两副牌均为一对时，对子较大者较大。如AAQJT大于KKQJT。当两副牌均为一对且对子相同时，比较剩下的3张牌。优先比较3张中最大的，如AAKJT大于AAQJT。若最大的相同，则比较第2大的，如AAKQT大于AAKJT。否则比较最小的，如AAKQJ大于AAKQT。

散牌：牌组不符合任意以上的牌型则为散牌。散牌无法构成顺子且5张牌种类均不同。如AKJ54。当两副牌均为散牌时，优先比较最大的。如A7654大于K7654。若最大的相同则比较次大的。如AK765大于AQ765。若再相同则比较第3大的，以此类推。

不同的牌组类型中，四条>葫芦>顺子>三条>两对>一对>散牌。小A作为一个新手，并不能熟练的记忆上述的牌型。现在有两副牌组，小A并没有办法快速的判断哪一个更大，你能帮助他吗？

# 2. 输入
第一行是一个不超过100的正整数n，表示一共有n组测试数据。每一组数据包含两行，分别代表两个牌组。

接下来2n行，每2行代表两幅要进行比较的牌组。每副牌组由5个被空格隔开的正整数表示。其中10代表T，11代表J，12代表Q，13代表K，14代表A。因此五个数将会在2到14之间。

输入保证合法，如不会出现2到14以外的数，同样的数也不会出现超过4次。

# 3. 输出
输出共n行，每行一个整数0或1或2。对于每组测试数据，1代表第1个牌组较大，2代表第2个牌组较大，0代表一样大。

# 4. 示例
样例输入:  
3  
2 3 4 5 6  
4 4 4 4 11  
2 3 8 9 10  
10 9 8 3 2  
4 4 7 8 7  
4 4 8 7 8

样例输出:  
2  
0  
2  

# 5. 程序
```cpp
#include <iostream>
#include <map>
#include <algorithm>

using namespace std;

enum Result{EQUAL, WIN, LOSE};
enum CardStyle{SINGLE, ONE_PAIR, TWO_PAIR, THREE, CONTINUES, CUCURBIT, FOUR};

CardStyle get_CardStyle(map<int, int>& _map)
{
    int map_size = _map.size();
    if (map_size == 5){
        //sort(_map.begin(), _map.end());
        auto ite1 = _map.begin();
        auto ite2 = _map.begin();
        while (++ite2 != _map.end()){
            if (ite2->first != (ite1->first + 1))
                break;
            ++ite1;
        }
        if (ite2 == _map.end())
            return CONTINUES;
        else{
            ite1 = _map.end();
            --ite1;
            if (ite1->first == 14){
                ite2 = _map.begin();
                int i = 0;
                for (; i < 4; ++i){
                    if (ite2->first != (i + 2))
                        break;
                    ++ite2;
                }
                if (i == 4){
                    _map.erase(ite1);
                    return CONTINUES;
                }
            }
            return SINGLE;
        }
    }
    else if (map_size == 4)
        return ONE_PAIR;
    else if (map_size == 3){
        for (auto val : _map){
            if (val.second == 2)
                return TWO_PAIR;
            else if (val.second == 3)
                return THREE;
            
        }
    }
    else if (map_size == 2){
        for (auto val : _map){
            if (val.second == 2)
                return CUCURBIT;
            else if (val.second == 3)
                return CUCURBIT;
            else if (val.second == 4)
                return FOUR;
        }
    }
}
Result compare(int* a, int* b, int num)
{
    if (num == 0)
        return EQUAL;
    for (int i = 0; i < num; ++i){
        if (a[i] > b[i])
            return WIN;
        else if (a[i] < b[i])
            return LOSE;
        else{
            return compare(++a, ++b, --num);
        }       
    }
}

Result cards_judge(int* a, int* b)
{
    map<int, int> a_map;
    map<int, int> b_map;
    for (int i = 0; i < 5; ++i){
        ++a_map[a[i]];
        ++b_map[b[i]];
    }
    CardStyle a_style = get_CardStyle(a_map);
    CardStyle b_style = get_CardStyle(b_map);
    if (a_style > b_style)
        return WIN;
    else if (a_style < b_style)
        return LOSE;
    else{
        auto ite_a = a_map.begin();
        auto ite_b = b_map.begin();
        int a_pair[5];
        int b_pair[5];
        int ai, bi = 3;
        switch (a_style){
        case SINGLE:
            ai = 4;
            bi = 4;
            while (ite_a != a_map.end()){
                a_pair[ai--] = ite_a->first;
                b_pair[bi--] = ite_b->first;
                ++ite_a;
                ++ite_b;
            }
            return compare(a_pair, b_pair, 5);
            break;
        case ONE_PAIR:
            ai = 3;
            bi = 3;
            while (ite_a != a_map.end()){
                if (ite_a->second == 1)
                    a_pair[ai--] = ite_a->first;
                else
                    a_pair[0] = ite_a->first;
                if (ite_b->second == 1)
                    b_pair[bi--] = ite_b->first;
                else
                    b_pair[0] = ite_b->first;
                ++ite_a;
                ++ite_b;
            }
            return compare(a_pair, b_pair, 4);
            break;
        case TWO_PAIR:
            ai = 1;
            bi = 1;
            while (ite_a != a_map.end()){
                if (ite_a->second == 2)
                    a_pair[ai--] = ite_a->first;
                else
                    a_pair[2] = ite_a->first;
                if (ite_b->second == 2)
                    b_pair[bi--] = ite_b->first;
                else
                    b_pair[2] = ite_b->first;
                ++ite_a;
                ++ite_b;
            }
            return compare(a_pair, b_pair, 3);
            break;
        case THREE:
            ai = 2;
            bi = 2;
            while (ite_a != a_map.end()){
                if (ite_a->second == 1)
                    a_pair[ai--] = ite_a->first;
                else
                    a_pair[0] = ite_a->first;
                if (ite_b->second == 1)
                    b_pair[bi--] = ite_b->first;
                else
                    b_pair[0] = ite_b->first;
                ++ite_a;
                ++ite_b;
            }
            return compare(a_pair, b_pair, 3);
            break;
        case CONTINUES:
            ite_a = a_map.end();
            ite_b = b_map.end();
            --ite_a;
            --ite_b;
            if (ite_a->first > ite_b->first)
                return WIN;
            else if (ite_a->first < ite_b->first)
                return LOSE;
            else
                return EQUAL;
            break;
            break;
        case CUCURBIT:
            while (ite_a != a_map.end()){
                if (ite_a->second == 2)
                    a_pair[1] = ite_a->first;
                else
                    a_pair[0] = ite_a->first;
                if (ite_b->second == 2)
                    b_pair[1] = ite_b->first;
                else
                    b_pair[0] = ite_b->first;
                ++ite_a;
                ++ite_b;
            }
            return compare(a_pair, b_pair, 2);
            return WIN;
        case FOUR:
            while (ite_a != a_map.end()){
                if (ite_a->second == 1)
                    a_pair[1] = ite_a->first;
                else
                    a_pair[0] = ite_a->first;
                if (ite_b->second == 1)
                    b_pair[1] = ite_b->first;
                else
                    b_pair[0] = ite_b->first;
                ++ite_a;
                ++ite_b;
            }
            return compare(a_pair, b_pair, 2);
            break;
        }
    }
}

int main(int argc, char** argv)
{
    int n = 0;
    int number[2][5] = {0};
    cin >> n;
    if (n > 100 || n <= 0)
        return 1;
    int* result = new int[n];
    for (int i = 0; i < n; ++i){
        for (int i = 0; i < 2; ++i){
            for (int j = 0; j < 5; ++j){
                cin >> number[i][j];
            }
        }
        result[i] = cards_judge(number[0], number[1]);
    }
    for (int i = 0; i < n; ++i){
        cout << result[i] << endl;
    }
    delete[] result;
    return 0;
}
```

# 6. 思路
首先利用map对5张牌进行分类统计。然后通过get\_CardStyle获得5张牌的类型，是散牌、一对还是两对三对。。。。。该函数通过判断map的size及特点进行分类。分类完之后比较两人的牌的类型，这里用枚举enum来定义牌类型，按顺序排好后直接比较大小即可。如果两人牌类型一样，则根据类型switch处理方案。但是比较思路都是一致的，将需要比较的数字依次放入a\_pair、b\_pair中。其实map中的数字已经进行了排序了的，拿一对这种情况来说，将一对的数字放入a\_pair\[0]，将剩下三个数中最大的放入a\_pair\[1]、次大的放入a\_pair\[2]、然后是a\_pair\[3]。对b做同样处理之后通过compare函数进行比较得到结果。
  
<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
