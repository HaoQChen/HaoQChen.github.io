---
layout:     post
title:      C++各种循环方式梳理及对比（1）
subtitle:   
date:       2020-05-08
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories: 深入理解C++
published: true
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2020/05/08/all-kind-of-loop-1/>

在学习的过程中发现C++有各种各样的循环方式，比如最基本的:

+ for
+ while

后面增加的：

+ [std::for_each](http://www.cplusplus.com/reference/algorithm/for_each/)
+ [基于范围的for循环](https://zh.cppreference.com/w/cpp/language/range-for)
+ [std::for_each_n](https://zh.cppreference.com/w/cpp/algorithm/for_each_n)
+ [std::transform](http://www.cplusplus.com/reference/algorithm/transform/)

这些循环方式各有特点，调用方式也不同。本文将整理他们的异同，并尝试比较他们的效率。很多情况下，程序80%的时间会被20%的代码消耗，而这20%的代码多为循环。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 结论

将结论写在前面，是因为深入探究这个东西会又长又臭，很多人没那个耐心看下去。但你如果能耐心看下去，相信还是会有更深刻的收获的。

1. for和while的汇编都是一样的。
2. for中的判断，最好是将函数的值给一个const型变量，像下面这样：
   ```cpp
   const int size = getSize();
   for (int i = 0; i < size; ++i){

   }
   ```
3. 对于现代编译器，将i写在循环外和循环内没有区别

# 2. for与while

## 2.1 for与while的区别

测试代码：

```cpp
#include <iostream>

int main (int argc, char** argv)
{
    int i = 0;
    const int data_size = 100;
    int data[data_size] = {0};
    for (; i < data_size; ++i){
        data[i] = i;
    }

    i = 0;
    while(i < data_size){
        data[i] = i;
        ++i;
    }
    return 0;
}
```

在命令行输入一下命令

```bash
g++ ./objdump.cpp -g # ./objdump.cpp是我的文件，-g输出调试信息 
objdump -S a.out -M intel # 使用objdump进行汇编分析，-M指定汇编风格
```

这种汇编分析的好处是能让C++代码跟汇编代码一一对应，但是看起来不够整体。认真理解了代码对应后，直接将`cpp`文件转成汇编`.s`文件:

```bash
g++ ./objdump.cpp -S -masm=intel -O0 # -S输出汇编指令，-masm指定汇编风格为intel
```

得到汇编文件`objdump.s`，其中与for和while循环相关的汇编如下：

```x86asm
.L3:
    cmp  DWORD PTR [rbp-424], 99             ; 先将i与99对比
    jg   .L2                                 ; 不符合直接跳转到下面
    mov  eax, DWORD PTR [rbp-424]            ; 将i移到累加寄存器eax
    cdqe                                     ; 该指令将EAX签名扩展为RAX。它是movslq %eax, %rax的简短形式，与AT&T风格的cltq等效
    mov  edx, DWORD PTR [rbp-424]            ; 将i移到edx寄存器，该寄存器总是用来存放整数除法产生的余数
    mov  DWORD PTR [rbp-416+rax*4], edx      ; 将edx移到对应的data[i]地址
    add  DWORD PTR [rbp-424], 1              ; i + 1
    jmp  .L3                                 ; 跳回for循环
.L2:
    mov  DWORD PTR [rbp-424], 0
.L5:
    cmp  DWORD PTR [rbp-424], 99
    jg   .L4
    mov  eax, DWORD PTR [rbp-424]
    cdqe
    mov  edx, DWORD PTR [rbp-424]
    mov  DWORD PTR [rbp-416+rax*4], edx
    add  DWORD PTR [rbp-424], 1
    jmp  .L5
.L4:
    mov  eax, 0
    mov  rsi, QWORD PTR [rbp-8]
    xor  rsi, QWORD PTR fs:40
    je  .L7
    call  __stack_chk_fail
```

可以看到，while和for的汇编都是一样的，性能也就肯定一样啦。

## 2.2 for中的判断应该怎么写

```cpp
// A
for (int i = 0; i < vec.size(); ++i){

}
// B
const int size = vec.size();
for (int i = 0; i < size; ++i){

}
```

for里面有一个判断条件，经常会纠结，到底是A好，还是B好。

测试代码：

```cpp
#include <iostream>

const int kDataSize = 100;
int data_size = 100;

const int getSize(void)
{
    return kDataSize;
}

int main (int argc, char** argv)
{
    int data[kDataSize] = {0};
    for (int i = 0; i < getSize(); ++i){
        data[i] = i;
    }

    for (int i = 0; i < kDataSize; ++i){
        data[i] = i;
    }

    for (int i = 0; i < data_size; ++i){
        data[i] = i;
    }
    return 0;
}
```

生成主要汇编代码如下：

```x86asm
    .globl  _Z7getSizev                             ; getSize函数，LFB是函数开始，LFE是函数结尾，LBB和LBE是功能块
    .type  _Z7getSizev, @function
_Z7getSizev:
.LFB1021:
    .cfi_startproc
    push  rbp
    .cfi_def_cfa_offset 16
    .cfi_offset 6, -16
    mov   rbp, rsp
    .cfi_def_cfa_register 6
    mov   eax, 100
    pop   rbp
    .cfi_def_cfa 7, 8
    ret
    .cfi_endproc
.LFE1021:
    .size  _Z7getSizev, .-_Z7getSizev

    mov   DWORD PTR [rbp-428], 0
.L5:                                                   ; 调用函数的for循环
    call  _Z7getSizev                                  ; 每个for循环都要调用函数，造成浪费
    cmp   eax, DWORD PTR [rbp-428]                     ; 比较函数结果（在函数内被放到了eax）与i的大小  
    ; eax是32位寄存器，ax是eax的低16位，ah是ax的高8位，al是ax的低8位。
    setg  al                                           ; setg al ; ZF==0 并 SF==0 并 OF==0 时 al=1;
    ; test会根据操作数运算设置加法器相关标志位，一般用来判断操作数是否为0
    test  al, al                                       ; al和al两个操作数进行按位与操作，al本身不变
    je    .L4                                          ; 等于则跳转
    mov   eax, DWORD PTR [rbp-428]
    cdqe
    mov   edx, DWORD PTR [rbp-428]
    mov   DWORD PTR [rbp-416+rax*4], edx
    add   DWORD PTR [rbp-428], 1
    jmp   .L5
.L4:
    mov   DWORD PTR [rbp-424], 0
.L7:                                                   ; 与2.1节一样
    cmp   DWORD PTR [rbp-424], 99
    jg    .L6                                          ; 有符号大于则跳转
    mov   eax, DWORD PTR [rbp-424]
    cdqe
    mov   edx, DWORD PTR [rbp-424]
    mov   DWORD PTR [rbp-416+rax*4], edx
    add   DWORD PTR [rbp-424], 1
    jmp   .L7
.L6:
    mov   DWORD PTR [rbp-420], 0
.L9:
    mov   eax, DWORD PTR data_size[rip]                ; 比上一个for多了将data_size移到eax这一步
    cmp   DWORD PTR [rbp-420], eax
    jge   .L8                                          ; 有符号大于等于则跳
    mov   eax, DWORD PTR [rbp-420]
    cdqe
    mov   edx, DWORD PTR [rbp-420]
    mov   DWORD PTR [rbp-416+rax*4], edx
    add   DWORD PTR [rbp-420], 1
    jmp   .L9
```

总结：

1. L7和L9，也即后面两个循环，一个是const int， 一个是int类型的变量。L7跟前面2.1是完全一样的，L9由于不是const变量，所以必须要每次都读取到eax寄存器中，多了一步。
2. 如果判断条件是函数，将会额外进行非常多的操作。
3. 对比,2.1和2.2可以发现，将i放在循环内还是循环外，在现代编译器看来都是一样的。

# 参考

+ 文中用到的一些链接

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
