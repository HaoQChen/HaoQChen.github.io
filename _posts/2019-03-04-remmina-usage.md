---
layout:     post
title:      使用Remmina远程登录Ubuntu系统并实现文件共享（可实现类似Teamviewer功能）
subtitle:   
date:       2019-03-04
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

本文持续更新地址：<https://haoqchen.site/2019/03/04/remmina-usage/>

最近teamviewer开始想要收费了，越来越限制功能，迫不得已用回Remmina，使用Ubuntu远程连接另外一台Ubuntu还是很方便的。下面将介绍如何实现远程登录和文件共享。

如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

Remmina是一个集成多种协议的远程连接终端，Ubuntu系统中自带有，不需要安装，仅需做一些其他的设置即可。

**假设你操作的电脑为A，需要远程连接的电脑为B**

# 1. 设置B支持远程连接
出于安全考虑，你的电脑是不能让人随便连接的，除非你自己将连接权限开放。这部分权限可以通过`dconf-editor`进行设置。`dconf-editor`只是将一些系统权限进行可视化，设置起来方便，也可以通过更原始的方式进行设置。
首先安装`dconf-editor`：
`sudo apt-get install dconf-editor`
然后运行：
`dconf-editor`

在界面中依次展开org->gnome->desktop->remote-access

将`enable`勾上，将加密`requre-encryption`去掉，并将`prompt enabled`去掉，如下图所示：

![](/img/in_post/remmina_usage/dconf.png)

设置完成后，你也可以在`桌面共享`（英文`Desktop Sharing`）中进行其他的一些设置，比如要求每次连接都要确认，展示消息等。

![](/img/in_post/remmina_usage/share_preference.png)

# 2. 设置B支持文件共享
需要安装`ssh-server`来实现文件共享。
执行命令：`sudo apt-get install openssh-server` 
查看ssh服务是否启动，输入命令`sudo ps -e |grep ssh`，如果有sshd，那么ssh服务正常启动，如果没有，使用命令：`sudo service ssh start`即可启动。

# 3. 设置A远程连接客户端
运行`Remmina`客户端，直接在查找中输入程序名，或者在终端输入后按`tab`即可。

![](/img/in_post/remmina_usage/search_remmina.png)

运行后在界面中按那个`+`号，新添加一个远程连接

![](/img/in_post/remmina_usage/add_client.png)

自己定一个名字，协议这里选择`VNC虚拟网络电脑`，server输入远程电脑IP地址，用户名、密码输入远程电脑的用户名和密码。保存后双击即可远程连接。

![](/img/in_post/remmina_usage/client_name.png)

如果需要进行文件共享，则还需要设置旁边的SSH：

设置远程电脑的用户名，选择密码登录，保存。

![](/img/in_post/remmina_usage/ssh_enable.png)


然后双击就大功告成啦

现在在Ubuntu1404下出了个文件共享的BUG，
`SSH password authentication failed: Wrong state during pending SSH call`
原来还好好的，现在不能用了，据说是SSH的版本BUG，需要更新。先不用SSH文件共享了

# 参考
<https://blog.csdn.net/haolvshiqi/article/details/53945244>
<https://blog.csdn.net/sunnylgz/article/details/40779973>

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
