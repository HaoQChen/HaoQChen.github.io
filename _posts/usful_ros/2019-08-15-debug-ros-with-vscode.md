---
layout:     post
title:      如何配置VSCode来调试ROS节点
subtitle:   
date:       2019-08-15
author:     白夜行的狼
header-img: img/black.jpeg
catalog: true
categories:  ROS实用小细节
tags:
    - 
    - 
    - 
    - 
    - 
--- 

# 0. 写在最前面

本文持续更新地址：<https://haoqchen.site/2019/08/15/debug-ros-with-vscode/>

本文档介绍了如何用VSCode的Debug功能来调试ROS的CPP节点。ROS节点的调试一直非常麻烦，在此之前尝试过gdb、CLion、Qt插件，用起来都不太顺手，直到发现了VSCode的调试功能

调试的好处有：
1. bug导致的`core dumped`、`segmentation fault`等会停到相应的位置，方便查找
2. 想到什么，断点停那里就可以看到变量状态，不用增加输出代码再编译这么麻烦
3. 条件中断，这个也不用再增加if判断再重新编译

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 推荐几个VSCode插件
* [C/C++插件][cpp_plugin]：这个是微软官方的CPP插件，装了后就可以愉快地编写、编译C++代码了。

* [C++ Intellisense](https://marketplace.visualstudio.com/items?itemName=austin.code-gnu-global)：这个插件能够很好地辅助C++开发者进行开发，提供包括代码跳转，自动完成，智能提示等功能。

* [ROS (deprecated)](https://marketplace.visualstudio.com/items?itemName=ajshort.ros)：这个插件作者已经停止更新了，现在主要用来启动roscore～～～

# 2. debug原理及配置

## 2.1 debug原理
VSCode中是以`workspace`的概念处理文件关联的，每个`workspace`文件夹下会有一个`.vscode`文件夹，该文件夹下放置的是关于该`workspace`的路径配置、任务配置、运行配置等文件，我们正是通过编辑这些配置文件实现对工程的管理。

微软提供的[C/C++插件][cpp_plugin]集成了gdb调试功能，并提供变量界面显示以及断点、监视以及调用堆栈等功能。你只需要在.vscode文件夹中配置好`launch.json`，就可以按下`F5`快捷键启动相应调试。

由于目前并没有集成的ROS调试器，所以只能将每一个node当成一个CPP程序来进行调试。

## 2.2 编译配置

在VSCode中需要在.vscode文件夹中配置好`tasks.json`文件(没有的话可自己新建一个)后，就可以按`Ctrl + Shift + B`快捷键（这个快捷键需要将task归到build的group里才行，普通的task要`Ctrl + Shift + P`选`Run Task`），并选择相关的任务进行编译等操作。

![](/img/in_post/debug_ros_with_vscode/vscode_runtask.png)

下面展示的配置文件主要配置了`prerun`、`catkin build`、`catkin clean`以及`ccb`四个任务。下面简介一些用到的变量，详情请看[VSCode的tasks页面][VSCode_tasks]。将鼠标停留在相关变量上也可以看到。

+ **label**
  就是一个名字，你按下快捷键的时候用以区分不同task

+ **type**
  任务的类型，可设置成`shell`和`process`。前者将任务当成命令，启动终端运行，后者直接运行。

+ **command**
  实际运行的命令

+ **args**
  运行的参数，这里需要注意的是，如果需要进行调试，需要设置为`Debug`模式，并且要检查相应package中的CMakeLists.txt中有没有设置成`Release`模式，CMake中txt的设置优先级是最高的。比如我们的驱动就设置`Release`，所以即使你在这里怎么设置都没用的。

+ **group**
  这个是分组的，貌似可以从命令行来运行分组的任务，暂时没用到

+ **presentation**
  关于输出显示的设置，这里设置为总是输出到集成的终端，可通过`"panel": "new"`设置每次都启动新的终端

+ **problemMatcher**
  错误分析器，可以分析到输出的信息中有哪些错误并显示

+ **dependsOn**
  运行依赖，运行该task前会运行这些依赖的task，如果想要他们按顺序运行，需要显式声明`dependsOrder`

+ **其他选型**
  看到还有可以重定义当前路径等很多详细的功能。


`tasks.json`文件配置：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "prerun",
            "type": "shell",
            "command": "source ./devel/setup.zsh && export ROS_MASTER_URI=http://localhost:11311/ "
        },
        {
            "label": "catkin build",
            "type": "shell",
            "command": "catkin",
            "args": [
                "build",
                "-DCMAKE_BUILD_TYPE=Debug"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always"
            },
            "problemMatcher": "$msCompile"
        },
        {
            "label": "catkin clean",
            "type": "shell",
            "command": "catkin",
            "args": [
                "clean",
                "-y"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always"
            },
            "problemMatcher": "$msCompile"
        },
        {
            "label": "ccb",
            "dependsOrder": "sequence",
            "dependsOn": [
                "catkin clean",
                "catkin build"
            ],
            "problemMatcher": [
                "$msCompile"
            ]
        }
    ]
}
```

## 2.3 debug配置

主要是配置`launch.json`，这里只介绍几个常用参数，详细请参考[VSCode中关于Debugging的介绍][VSCode_debugging]

+ **name**
  任务的名字，该名字会在VSCode的Debug中显示，用户可选择需要调试的任务。
  ![](/img/in_post/debug_ros_with_vscode/vscode_debug_name.png)

+ **tpye**
  调试器名称。

+ **request**
  有`launch`和`attach`两种方式，前者直接运行，后者将程序绑定到之前启动的程序

+ **program**
  这里需要写生成的二进制路径

+ **args**
  传进去的参数，这里分为ROS参数服务器形式传进去的参数以及以main函数参数传进去的参数，这里介绍的是前者。有兴趣可以Google一下。

+ **stopAtEntry**
  是否在运行前暂停

+ **cwd**
  设置当前路径，如果程序中用的是相对路径，则需要设置该参数为当前路径。

+ **environment**
  环境变量设置

+ **externalConsole**
  是否启动外部终端（默认是用集成终端）

+ **preLaunchTask**
  在启动前启动一个task，这个prerun在前面一节有说，主要是设置source当前ROS路径等

+ **postDebugTask**
  运行完了之后启动的task，节点运行完了进行清理工作

+ **MIMode**
  调试器名称

+ **setupCommands**
  是给gdb的参数

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "cloud_node",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/devel/.private/rslidar_pointcloud/lib/rslidar_pointcloud/cloud_node",
            "args": [
                "_model:=RS16",
                "_resolution_type:=1.0cm"
            ],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "preLaunchTask": "prerun",
            "MIMode": "gdb",
            "avoidWindowsConsoleRedirection": true,
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

## 2.4 多任务调试

根据[VSCode中关于Debugging的介绍][VSCode_debugging]，可以启动完一个任务后再启动另外一个即可同时debug多个。

写完多个节点后，可以通过compounds来进行配置，但compounds不能确保顺序执行，尝试通过preLaunchTask延时2秒启动来实现顺序执行，但preLaunchTask任务启动的终端跟节点启动的终端不是同一个。

```json
"compounds": [
  {
      "name": "rslidar",
      "configurations": [
          "rslidar_node",
          "cloud_node",
          "rviz_node"
      ]
  }
]
```

另外还有一个问题是，不知道怎么确保同一个程序下次运行还用同一个终端，现在是会新建一个终端，每次重启就新建一个，多次之后就一堆要自己删。

# todo feature

+ 集成其他好用的外部调试器：[Debugger Extension](https://code.visualstudio.com/api/extension-guides/debugger-extension)
+ 条件断点在[VSCode中关于Debugging的介绍][VSCode_debugging]中有介绍
+ 在同一个终端启动名字相同的节点。

[cpp_plugin]: https://code.visualstudio.com/docs/languages/cpp
[VSCode_tasks]: https://code.visualstudio.com/docs/editor/tasks#vscode
[VSCode_debugging]: https://code.visualstudio.com/Docs/editor/debugging

# 参考

+ <https://blog.csdn.net/weixin_35695879/article/details/85254422>
+ <https://answers.ros.org/question/313371/vscode-debug-cpp-ros-node/>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
