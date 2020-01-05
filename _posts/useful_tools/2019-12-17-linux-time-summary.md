---
layout:     post
title:      Linux时间相关函数总结
subtitle:   
date:       2019-12-17
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories:  
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/12/17/linux-time-summary/>

最近写程序涉及到时间相关的，包括当前时间呀，进程运行的时间差呀，线程某段程序的时间消耗呀等等。然后查了比较多Linux下的时间函数。发现每个函数之间都有或多或少的区别，应用场景很不一样。在此做个总结和记录。

如无特殊说明，我的系统是Ubuntu1604（64bit）

对ROS的时间有兴趣的可以看看我的另一篇文章<https://haoqchen.site/2018/11/08/ROS-time/>

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 系统类函数
这里所说的系统类函数主要是C标准库中的函数。

## 1.1 gettimeofday

在终端下运行`man gettimeofday`可以看到其官方说明，我摘录一些重点：

|项目|说明|备注|
|:---:|:---|:---|
|头文件|#include <sys/time.h>||
|原型|int gettimeofday(struct timeval *tv, struct timezone *tz);||
|功能|获取从`Epoch`（1970年1月1日00:00:00 UTC，到2038年会挂那个）到当前所经过的时间（不考虑闰秒）以及当前时区，分辨率达us||
|return|成功返回0，失败返回-1，可通过errno查看错误码||

其中`struct timeval`：

```cpp
struct timeval {
    time_t      tv_sec;     /* seconds */
    suseconds_t tv_usec;    /* microseconds */
};
```

其中`time_t`和`suseconds_t`是跟系统有关的类型，我在自己系统下看到的是`long int`

用法：

```cpp
struct timeval t_start, t_end;
gettimeofday(&t_start, NULL);
do_something();
gettimeofday(&t_end, NULL);
long int time_cost = (t_start.tv_sec - t_end.tv_sec) * 1000 + (t_start.tv_usec - t_end.tv_usec)
printf("Cost time: %ld ms\n", time_cost);
```

## 1.2 times

|项目|说明|备注|
|:---:|:---|:---|
|头文件|#include <sys/times.h>||
|原型|clock_t times(struct tms *buf);||
|功能|返回当前进程的相关时间，包括用户时间，系统时间，子进程用户时间，子进程系统时间||
|return|失败时返回-1，成功时返回过去某一时间点到现在经过的CPU计数，每秒的脉冲数用`sysconf(_SC_CLK_TCK)`获取|这个值可能溢出|

其中`tms`，单位都是CPU计数：
```cpp
struct tms {
    clock_t tms_utime;  /* user time */
    clock_t tms_stime;  /* system time */
    clock_t tms_cutime; /* user time of children */
    clock_t tms_cstime; /* system time of children */
};
```

## 1.3 clock_gettime

|项目|说明|备注|
|:---:|:---|:---|
|头文件|#include \<time.h\>||
|原型|int clock_gettime(clockid_t clk_id, struct timespec *tp);||
|功能|获取系统某一时钟从`Epoch`到当前的时间，可精确到纳秒||
|return|成功返回0，失败返回-1||

其中`timespec`：
```cpp
struct timespec {
    time_t   tv_sec;        /* seconds */
    long     tv_nsec;       /* nanoseconds */
};
```

可用的时钟：
+ `CLOCK_REALTIME`：就是所说的`wall-clock`，会受非连续跳跃影响，比如人为修改了时钟。或者增量的调整，比如使用`adjtime`函数
+ `CLOCK_REALTIME_COARSE`：精简版的`CLOCK_REALTIME`，很快，但精度受损。
+ `CLOCK_MONOTONIC`：单调的时钟？从某个不确定的时刻开始跳动，不受非连续跳跃的影响，但是受增量的调整影响。
+ `CLOCK_MONOTONIC_COARSE`：精简版的`CLOCK_MONOTONIC`，很快，但精度受损。
+ `CLOCK_MONOTONIC_RAW`：与`CLOCK_MONOTONIC`类似，但输出的是原始的时钟，不受其他调整影响
+ `CLOCK_BOOTTIME`：与`CLOCK_MONOTONIC`完全一致，但把系统暂停的时间也算在内
+ `CLOCK_PROCESS_CPUTIME_ID`：统计进程所有线程消耗的时间
+ `CLOCK_THREAD_CPUTIME_ID`：线程消耗的时间，这个ID是针对当前线程的，如果想获得其他线程的ID，需要调用`pthread_getcpuclockid`

用法：
```cpp
#include <time.h>
#include <string>
#include <sstream>

auto time2String = [](struct timespec t_start, struct timespec t_end) -> const std::string {
    std::string result;
    std::stringstream ss;
    long double temp = 0.0;
    temp += (t_end.tv_sec - t_start.tv_sec);
    temp += static_cast<long double>((t_end.tv_nsec - t_start.tv_nsec) / 1000u) / static_cast<long double>(1000000.0);
    ss.precision(6);
    ss.setf(std::ios::fixed);
    ss << temp  ;
    ss >> result;
    return result;
};

struct timespec time_start;
struct timespec time0;
time0.tv_sec = 0;
time0.tv_nsec = 0;
if (0 == clock_gettime(CLOCK_THREAD_CPUTIME_ID, &time_start)){
    std::cout << "start time: " << time2String(time0, time_start) << "--------------" << std::endl;
}

struct timespec time_1;
if (0 == clock_gettime(CLOCK_THREAD_CPUTIME_ID, &time_1)){
    std::cout << "1st time: " << time2String(time_start, time_1) << std::endl;
}

```

## 1.4 clock

同样可从man中看到相关说明

|项目|说明|备注|
|:---:|:---|:---|
|头文件|#include <time.h>||
|原型|clock_t clock(void);||
|功能|返回程序所用的处理器时间**近似**，也就是目前为止所用的CPU时间，是否包括sleep的时间与系统有关|在32位系统由于位数关系，约每72分钟循环一次|
|return|返回CPU的时钟计数，错误返回-1。`clock_t`在我的系统下是`long int`，要获得时间，需要除以`CLOCKS_PER_SEC`||

**注意：**
+ Linux中，返回的时间不包括wait子线程的时间，其他系统不确定。可通过`times`函数来获得
+ 在glibc 2.17及之前的版本，clock是基于`times`来实现的，在后续版本，为了提高精度，其基于`clock_gettime`实现。
+ 在C标准中，程序开始时clock的返回值可为任意值，每个系统的实现会有不同，所以最好的方式是程序开始时获取一个初始值，后面的时间减去这个初始值。
+ `CLOCKS_PER_SEC`在所有`XSI-conformant`系统中被定义为1000000，也即时间分辨率为1us

注：个人感觉这个函数没啥用，精度不及其他，然后又诸多限制

# 2. C++标准类函数

## 2.1 time

|项目|说明|备注|
|:---:|:---|:---|
|头文件|#include <ctime>||
|原型|std::time_t time( std::time_t *time );||
|功能|返回日历时间，即从`Epoch`到当前所经过的秒数||
|return|如上，失败时返回-1||

一般情况下，我们需要的是时间描述，而不是一个干巴巴的秒数，所以会调用`struct tm * localtime (const time_t * timer);`函数将其转换成一个时间描述结构，其包括：

```cpp
int tm_sec
int tm_min
int tm_hour
int tm_mday
int tm_mon
int tm_year
int tm_wday
int tm_yday
int tm_isdst
```

如上所述，时间精确到秒。

如果你想进一步转换成字符串描述，可以调用`char* asctime( const struct tm* time_ptr );`进行转换。

**参考：**
+ <http://www.enseignement.polytechnique.fr/informatique/INF478/docs/Cpp/en/cpp/chrono/c/time.html>
+ <http://www.cplusplus.com/reference/ctime/localtime/>
+ <https://zh.cppreference.com/w/c/chrono/asctime>


## 2.2 std::chrono时间库
详见[chrono的CPPReference说明](http://www.cplusplus.com/reference/chrono/)，这个库主要提供三个时钟的获取和处理，这三个时钟被封装成类，并且都是通过返回当前的`time_point`时间节点来获得时间。在chrono库中，所有的时间节点都是相对于`Epoch`的

|时钟类|特点|
|:---:|:---|
|steady_clock|1. 设计用于计算时间间隔<br>2. 计数间隔是稳定的，间隔1ns（官方说明的代码受double精度限制是us的）<br>3. 一般是系统启动的时间，且保证后面的时间永远不比前面得到的时间小|
|system_clock|1. 设计用于表示真实时间，即日历时间，刻度为1个tick，_XTIME_NSECS_PER_TICK纳秒<br>2. 时间点可为负数<br>3. 系统中所有进程用该时钟，时间节点都是一样的<br>4. 可与`time_t`相互转换|
|high_resolution_clock|1. 该时钟是系统中频率最高的<br>2. 该时钟有可能与上述两个时钟是一样的|

**参考：**
+ [chrono的CPPReference说明](http://www.cplusplus.com/reference/chrono/)

# 3. 使用建议

+ **自由度**最高的是[clock_gettime](#13-clockgettime)
+ 由于系统存在**线程**调度的问题，所以获取日历时钟计算时间差都是有可能包含其他无关线程的执行时间的（一般约10ms）。要想只获取当前线程的时间差，貌似只能用[clock_gettime](#13-clockgettime)
+ 如果只关心自身**进程**，可使用[clock_gettime](#13-clockgettime)、[clock](#14-clock)、[times](#12-times)，其中`times`还可以方便地统计哪些是系统消耗的，哪些是自身消耗的。
+ 如果是想方便地**输出字符串**信息，可使用[C++的time](#21-time)
+ 其实目前的晶振频率都挺高的，无论用哪个时钟，精度都能得到保证，更多地应该考虑系统调度的问题。


# 参考

+ <https://www.cnblogs.com/zhongpan/p/7490657.html>
+ <https://stackoverflow.com/questions/38252022/does-standard-c11-guarantee-that-high-resolution-clock-measure-real-time-non>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
