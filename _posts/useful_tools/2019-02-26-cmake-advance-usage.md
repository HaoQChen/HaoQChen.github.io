---
layout:     post
title:      CMake高级用法
subtitle:   
date:       2019-02-26
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

本文持续更新地址：<https://haoqchen.site/2019/02/26/cmake-advance-usage/>

本文将总结自己日常用到的CMake命令以及功能。如有错误，欢迎在评论中指正。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

在这里可以查到关于[命令的官方文档](https://cmake.org/cmake/help/v3.3/manual/cmake-commands.7.html)

## 使用宏定义：macro
```cmake
macro(add_example name)
   add_executable(${name} ${name}.cpp)
   target_link_libraries(${name} dlib::dlib )
endmacro()

add_example(dnn_metric_learning_ex)
```
## 添加外部的CMake：add_subdirectory
有时候自己的CMakeLists需要依赖其他的包，需要先编译这个包；或者一个工程分成几个部分，然后在最外面用一个CMakeLists来统一编译，那就需要包含其他的CMakeLists文件来实现。
使用到：
`add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])`
* **source_dir**：首先需要指出另外这个CMakeLists的目录，可以使用相对路径（相对当前路径）和绝对路径。
* **binary_dir**：接着指明编译生成二进制的目录，可以使用相对路径（相对当前路径）和绝对路径。目标目录是可选项，如不指定，目标文件会被放到`source_dir`
* **EXCLUDE_FROM_ALL**：`source_dir`生成的目标会被排除在原目录的`ALL target`之外，也会排除在其IDE工程文件之外。比如`source_dir`是一些examples，原目录其实是不需要它们的，只是希望他们能编译，就可以添加这个命令。

这个命令的位置需要注意，不能太后面，编译dlib时放在比较后面出现了问题。

例子：
```cmake
add_subdirectory(../dlib dlib_build)
```

**注意**：当运行到该命令时，会立即跳到`source_dir`执行CMake，等到该CMakeLists执行完毕再跳回原来的CMakeLists执行`add_subdirectory`后面的命令。


## 输出消息：message
```cmake
message("No GUI support, so we won't build the ${name} example.")
#name是一个变量
```

## if判断
```cmake
if (DLIB_NO_GUI_SUPPORT)
   message("No GUI support, so we won't build the ${name} example.")
else()
   add_example(${name})
endif()
```

## 设置变量：set
* **设置一般变量**
```cmake
set(CPACK_PACKAGE_NAME "dlib")
set(CPACK_PACKAGE_VERSION_MAJOR "19")
set(CPACK_PACKAGE_VERSION_MINOR "16")
set(CPACK_PACKAGE_VERSION_PATCH "0")
set(VERSION ${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH})
```
* **设置内部变量**
**CMAKE_C_COMPILER**：指定C编译器
**CMAKE_CXX_COMPILER**：
**CMAKE_C_FLAGS**：编译C文件时的选项，如-g；也可以通过add_definitions添加编译选项
**EXECUTABLE_OUTPUT_PATH**：可执行文件的存放路径
**LIBRARY_OUTPUT_PATH**：库文件路径
**CMAKE_BUILD_TYPE**：build 类型(Debug, Release, ...)，CMAKE_BUILD_TYPE=Debug
**BUILD_SHARED_LIBS**：Switch between shared and static libraries
设置内部变量有两种方式，一种是直接在cmake命令后面加`-D+命令+=+值`，如`cmake .. -DBUILD_SHARED_LIBS=OFF`。第二种是在CMakeLists文件中使用`set`命令，如`set(BUILD_SHARED_LIBS OFF)`

## 添加include目录：include_directories
`include_directories([AFTER|BEFORE] [SYSTEM] dir1 [dir2 ...])`
添加include目录到当前CMakeLists（包括build和target）。默认是目录的递归，相对目录是相对当前路径的。

## 查找包：find_package
`find_package(<package> [version] [EXACT] [QUIET] [MODULE]
             [REQUIRED] [[COMPONENTS] [components...]]
             [OPTIONAL_COMPONENTS components...]
             [NO_POLICY_SCOPE])`
查找并加载外部工程，这个命令后，一个`<package>_FOUND`的变量会表明是否找到。
`QUIET`选项忽视找不到的消息；`REQUIRED`选项表明该外部包是必须的，找不到会立刻停止；
例子（这里的判断是没必要的，只是为了说明，因为找不到就会退出）：
```bash
find_package(OpenCV REQUIRED)
if (OpenCV_FOUND)
  include_directories(${OpenCV_INCLUDE_DIRS})
else()
  message("OpenCV not found, so we won't build the project.")
endif()
```

## 链接库目录:link_directories
<https://haoqchen.site/2018/04/26/CMakeLists-setting-relative-path/>

## 生成自己的静态、动态链接库
`add_library(<name> [STATIC | SHARED | MODULE]
            [EXCLUDE_FROM_ALL]
            source1 [source2 ...])`
            
增加一个叫`name`的链接库，可以选择是`STATIC`、`SHARED`或者是`MODULE`类型的。

* **`STATIC`**：静态链接库，当生成可执行程序时进行链接。在Linux下为.a文件
* **`SHARED`**：动态链接库，可执行程序运行时动态加载并链接。在Linux下为.so文件
* **`MODULE`**：模块，可执行程序运行时动态加载，但不链接到可执行程序中。
`BUILD_SHARED_LIBS`变量决定了默认值，如果为`on`则为动态的，否则为静态的

可以通过设置`CMAKE_LIBRARY_OUTPUT_DIRECTORY`变量指定输出的路径
例子：
```cmake
SET(LIBHELLO_SRC hello.c)
ADD_LIBRARY(hello SHARED ${LIBHELLO_SRC})       #添加动态库
#ADD_LIBRARY(hello STATIC ${LIBHELLO_SRC})      #添加静态库
#ADD_LIBRARY(hello_static STATIC ${LIBHELLO_SRC})  
```

需要注意的是源文件前没有逗号。

## C++11
如果用到了C++11特性，需要让CMake支持该特性
`add_definitions(-std=c++11)`

## 移动资源文件、配置文件
有些资源文件或者配置文件需要从源文件目录移动到生成文件目录，这个时候可以使用`file`命令，`file`命令可以进行文件写入、读取、生成、下载、上传、重命名等操作，这里先说一下文件复制的：

`file(<COPY|INSTALL> <files>... DESTINATION <dir>
     [FILE_PERMISSIONS <permissions>...]
     [DIRECTORY_PERMISSIONS <permissions>...]
     [NO_SOURCE_PERMISSIONS] [USE_SOURCE_PERMISSIONS]
     [FILES_MATCHING]
     [[PATTERN <pattern> | REGEX <regex>]
      [EXCLUDE] [PERMISSIONS <permissions>...]] [...])
`

`COPY`一个`<files>`（文件、目录或者链接）到一个目标位置`DESTINATION` `<dir>`。如果使用相对路径，`<files>`将会是相对当前源文件目录，而`<dir>`将会是相对当前build目录。复制默认使用`USE_SOURCE_PERMISSIONS`选项，即保留源文件权限，包括可执行性等，可以通过显式声明`NO_SOURCE_PERMISSIONS`来去除。
实例：
```cmake
file(COPY ./dlib/data/ DESTINATION ./dlib_models)
```

这样子就可以将源文件目录下的一些模型（data文件夹内所有）复制到生成二进制文件的dlib_models目录了。

## 常用宏变量
* **`PROJECT_BINARY_DIR `**：由`project`命令生成，指向build目录的绝对路径
* **`PROJECT_SOURCE_DIR`**：由`project`命令生成，指向CMakeLists目录绝对路径。
这两个配合`file`命令可以设置链接库相对路径。
例子：
```cmake
file(COPY ./voice/libs/X64/ DESTINATION ./)
target_link_libraries(awaken_asr ${PROJECT_BINARY_DIR}/libmsc.so libasound.so)
```

## 将参数传递到cpp中

[cmake教程5-macro宏定义以及传递参数给源文件](https://blog.csdn.net/haluoluo211/article/details/80861543)这个文件中讲了如何通过`.h.in头文件`传递版本号以及通过`option`来传递，另外可以通过`add_definitions(-DPROJECT_DIR="${PROJECT_SOURCE_DIR}")`，然后直接`std::string dir = (std::string)PROJECT_DIR `

# 参考
<https://www.cnblogs.com/narjaja/p/9533169.html>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
