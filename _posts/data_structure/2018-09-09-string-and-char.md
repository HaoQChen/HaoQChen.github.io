---
layout:     post
title:      C++字符串处理总结（char、string）
subtitle:   磨刀不误砍柴工
date:       2018-09-09
author:     白夜行的狼
header-img: img/in_post/string_and_char/black.jpeg
catalog: true
categories: 数据结构
tags:
    - char
    - string
    - 字符串
    - 总结
--- 

# 0. 写在最前面
本文持续更新地址：<https://haoqchen.site/2018/09/09/string-and-char/>

也欢迎收藏我的另一篇总结：[编程常用数据结构与函数总结（vector、list、stack、deque、字符串）](https://haoqchen.site/2018/09/05/helpful-struct-for-coding/)

C++字符串处理有最原始的char以及string两种方式，这里对两种方式常用的功能进行总结及对比。

如果觉得还不错就收藏一下呗，博主会长期更新自己的学习和收获。

**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

|               |        string          |         char*、char[]        |
|:------:|------|------|
|**头文件**|#include \<string\>|不需要|
|**定义与初始化**|string s1("abc");<br>string s2(s1);<br>string s3(4, 's');//初始化为4个's'|char* a = "test";//数据存在静态存储区，不能修改<br>char a[] = "test";//开辟数组再存储，可以修改<br>char* a = new char[10];<br>memset(a, '0', sizeof(char)*10);|
|**相互转化**|char* p = "hello";<br>string s(p);<br>s = p;|string str("test");<br>const char* p = str.data();//记得要加const或者强制类型转换成(char*\)<br>const char\* p = str.c\_str();<br>char p[10];<br>std::size\_t length = str.copy(p,5,0);//从第0个开始复制5个，返回有效复制的数量，需要在p最后添加'\\0'<br>char * cstr = new char \[str.length()+1\];<br>std::strcpy \(cstr, str.c_str\(\)\);<br>或者逐个复制|
|**实际大小**|str.size()   |  std::strlen\(p\)//#include \<cstring\>（C++写法）或者<string.h\>（C写法）| 
|**容器大小**|str.capacity()|数组形式p[]，可以使用sizeof(p)来获得数组大小<br>指针形式没有容器概念，除非是new的，对指针用sizeof将得到指针本身的大小，由系统位数决定|
|**倒置**|#include \<algorithm\> // std::reverse<br>std::reverse(str.begin(),str.end());|char* strrev(char* s);|
|**查找字符&字符串**|find//从头开始找<br>rfind//从尾开始找<br>**这四个函数都有四种重载：**<br>size_t find (const string& str, size_t pos = 0);//查找子string，默认从父string的第0个字符开始，如果要查找多个相似的，则可以将pos设置为上次查找到的+1<br>size_t find (const char* s, size_t pos = 0);//查找字符串，默认从0开始<br>size_t find (const char* s, size_t pos, size_type n);//同上，但只比较n个<br>size_t find (char c, size_t pos = 0);//比较字符。<br>当然，形参初始化的值可能不一样，返回的都是地址索引，需要通过found!=std::string::npos判断是否有效。<br><br>find_first_of<br>find_last_of<br>find_first_not_of<br>find_last_not_of<br>也有上面四种重载，不过这里是返回第一个出现、没有出现在子str的字符的索引。<br>如<br>std::string str ("look for non-alphabetic characters...");<br>std::size_t found = str.find_first_not_of("abcdefghijklmnopqrstuvwxyz ");<br>将返回'-'的索引|char* strchr(char* s, char c);//查找字符串s中首次出现字符c的位置，返回c位置的指针，如不存在返回NULL<br><br>char * strrchr(const char *str, int c);//查找字符倒数第一次出现的位置<br><br>char *strstr(const char *s1,const char *s2);//查找第一次出现s2的位置，返回s2的位置指针，如不存在返回NULL<br><br>char *strrstr(const char *s1,const char *s2);//查找倒数第一个出现s2的位置<br><br>int strspn(const char *s,const char *accept);//作用同右侧find_first_not_of。返回s中第一个没有在accept出现的字符的索引。通过两个for循环来实现<br><br>int strcspn(const char *s,const char *reject);//返回s中第一个在reject出现的字符的索引|
|**大小写转换**|两者都是不提供这个功能的，但是C++有两个库函数，头文件是#include \<ctype.h\>：<br>int tolower ( int c );<br>int toupper ( int c );|实现也很简单：<br>int tolower(int c)<br>{<br>　　if ((c >= 'A') && (c <= 'Z'))<br>　　　　return c + ('a' - 'A');<br>　　return c;<br>}|
|**比较字符串大小**|一共五种重载形式<br>int compare (const string& str);<br>int compare (size_t pos, size_t len, const string& str);<br>int compare (size_t pos, size_t len, const string& str, size_t subpos, size_t sublen);<br>int compare (const char* s) const;<br>int compare (size_t pos, size_t len, const char* s);<br>int compare (size_t pos, size_t len, const char* s, size_t n);<br>返回与右边一致，其中pos表示从str的第几个元素开始比较，一共比较len个字符，如果不够，则有多少比较多少。subpos、sublen是相对比较字符串而言的<br><br>string重载了==、<等符号，可以直接用符号比较<br>string没有提供不区分大小写的比较，感觉可以读取出数据后通过右侧的函数来进行比较。|int strcmp(char* s1, char* s2);//区分字母大小写比较<br>当s1 < s2时，返回值<0； //对于第一个不相等的字符，s1对应的小于s2对应的，或者全相等，但是s1的字符数量少于s2的字符数量<br>当s1 = s2时，返回值=0；<br>当s1 > s2时，返回值>0。<br><br>int stricmp(char* s1, char* s2);//不区分字母大小写<br><br>int strncmp(char* s1, char* s2, int n);//只比较前n个字符，区分大小<br><br>int strnicmp(char* s1, char* s2, int n);//之比较前n，不区分大小写|
|**数字转字符串**|1、stringstream（多次使用需要使用clear()清除）<br>int N = 10;<br>stringstream ss;//#include \<sstream\><br>string str;<br>ss << N;<br>ss >> str;<br>2、string = std::to_string(N)方法<br>只需包含\<string\>头文件即可|1、使用sprintf：#include \<stdio.h\><br>char c[100];<br>int k=255;<br>sprintf(c,"%d",k);//d是有符号10进制数，u是无符号10进制<br><br>double a=123.321;<br>sprintf(c,”%.3lf”,a);<br><br>sprintf(c,"%x",k);//转换成16进制，如果想要大写的话可以用X，8进制是o<br>//c包含"ff" c[0]='f' c[1]='f'<br><br>2、itoa貌似跟平台有关，不建议使用。|
|**字符串转数字**|1、N = stringToNum\<int\>(str);//需要#include \<sstream\><br><br>2、在\<string\>中实现的<br><br>int stoi (const string& str, size_t* idx = 0, int base = 10);//idx返回第一个非数字的指针索引，base默认10进制<br><br>long stol、unsigned long stoul、long long stoll、unsigned long long stoull、float stof、double stod、long double stold<br><br>3、stringstream//#include \<sstream\><br>string a = "123.32";<br>double res;<br>stringstream ss;<br>ss << a;<br>ss >> res;|char a[10] = {"255"};<br>int b;<br>sscanf(a,"%d",&b);<br><br>char a[10] = {"ff"};//十六进制<br>int b;<br>sscanf(a,"%x",&b);<br><br>char str[]=”123.321”; <br>double a; <br>sscanf(str,”%lf”,&a);<br><br>另外也可以用atoi(),atol(),atof()|
|**拷贝与合并**|char p[10];<br>std::size_t length = str.copy(p,5,0);//从第0个开始复制5个，返回有效复制的数量，需要在p最后添加'\0'<br><br>合并直接用+号即可<br>或者用.append()<br>string& append (const string& str);<br>string& append (const string& str, size_t subpos, size_t sublen);<br>string& append (const char* s);<br>string& append (const char* s, size_t n);<br>string& append (size_t n, char c);|char* strcpy(char* dest, char* src);//把从src地址开始且含有 ‘\0’结束符的字符串复制到以dest开始的地址空间。返回指向dest的指针。<br><br>char* strncpy(char* dest, char* src, int size_tn);//复制n个，这个复制不保证NULL结尾，需要自己初始化。<br><br>char* strcat(char* dest, char* src);//把src所指字符串添加到dest结尾处(覆盖dest结尾处的 ‘\0’)并添加 ‘\0’。返回指向dest的指针。且内存不可重叠。<br><br>char* strncat(char* dest, char* src, int n);//部分合并<br><br>用sprintf也行，但是效率不高。|
|**插入与替换**|string& insert (size_t pos, const string& str);<br>string& insert (size_t pos, const string& str, size_t subpos, size_t sublen);<br>string& insert (size_t pos, const char* s);<br>string& insert (size_t pos, const char* s, size_t n);<br>string& insert (size_t pos,   size_t n, char c);<br><br>string& replace (size_t pos,        size_t len,        const string& str);<br>string& replace (size_t pos,        size_t len,        const string& str,                 size_t subpos, size_t sublen);<br>string& replace (size_t pos,        size_t len,        const char* s);<br>string& replace (size_t pos,        size_t len,        const char* s, size_t n);<br>string& replace (size_t pos,        size_t len,        size_t n, char c);|不存在|
|**字符串切割**|string substr (size_t pos = 0, size_t len = npos)：<br><br>std::string str2 = str.substr (3,5);//返回str的第3个开始的5个元素。可以配合find函数来实现针对特殊元素的切割|char* strtok (char* str,constchar* delimiters );//以delimiters中的每个字符作为分割符，将str剪切，返回一个个字符串。传入NULL时代表继续切割后续的。下面的程序预计输出hello boy this is heima。第二个参数可以是" ,\\t\n\\\\"等。（其实就是将被切割的换成'\\0'？待分割字符串的完整性会被破坏，而且线程不安全。具体分析请看[strtok的安全性探讨](https://blog.csdn.net/yishizuofei/article/details/78232946?locationNum=5&fps=1)）<br>![code](/img/in_post/string_and_char/code.png)|
|**IO函数**|std::getline (std::cin,str,s);//这个不需要固定大小，但是速度慢，生成文件大。默认终止符是换行|cin.get(arrayname,size,s)//读取size-1个字符，在末尾添加'\0'遇终止符停止，返回是否成功。读取玩指针指向终止符。s默认换行<br><br>cin.getline(arrayname,size,s)//同上，只是指针指向终止符之后|

<br>
**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
