---
layout:     post
title:      同步Sublime Text配置
subtitle:   
date:       2019-03-21
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

本文持续更新地址：<https://haoqchen.site/2019/03/21/sublime-syncing/>

sublime是一款很好的跨平台代码编辑器，相信很多人都在用。但它的配置也是一件很烦的事，因此很多人都希望多个系统的sublime配置能够一样。本文就是讲解如何最正确地同步Sublime Text的配置。

网上很多教程其实都是错的，官网给出了最好的同步建议：
https://packagecontrol.io/docs/syncing

不想看英文的我简单说下。



如果觉得写得还不错，可以找我其他文章来看看哦～～～可以的话帮我github点个赞呗。
**你的[Star](https://github.com/HaoQChen/HaoQChen.github.io)是作者坚持下去的最大动力哦～～～**

# 1. 同步用户设置
网上很多人说要同步整个`Packages/`和`Installed Packages/`文件夹，这是错的！！！！因为有些包在不同系统下是不一样的，Linux下能用，在Windows就不一定能用。最好的方法是同步用户设置，然后让`Package Control`自己去重新下载！！

1. 在软件中打开`Preference->Browse Packages`
2. 在打开的文件夹中找到到`User`文件夹
3. 将`User`文件夹备份即可（你可以用github，也可以用百度云，甚至可以直接用U盘复制）

如果是github备份的话，可以写个.gitignore文件删掉一些缓存文件。至于怎么用github或者怎么用.gitgithub，请自己百度，作为一个程序员连github都不知道的话也不会用Sublime不是？

# 2. 安装`Package Control`
在新的环境安装完成Sublime Text后，首先需要安装`Package Control`

安装方法有两种，一种是通过命令行安装，另一种是直接下载包安装。官网安装方法：https://packagecontrol.io/installation#st3

* **命令行方法**
Ctrl + `打开Sublime Text的命令行，在其中输入以下命令并按下确认键即可（注意，下面命令针对Sublime3，如果是2的话请到上面的安装链接找）

`import urllib.request,os,hashlib; h = '6f4c264a24d933ce70df5dedcf1dcaee' + 'ebe013ee18cced0ef93d5f746d80ef60'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)`

但我在Windows下安装失败了（Linux下可以），只能自己下载安装。

* **人工安装**
1. 点击 `Preferences > Browse Packages`到文件夹
2. 回到上一层目录找到`Installed Packages`文件夹
3. 下载`Control.sublime-package`然后复制到`Installed Packages`目录下。下载目录：https://packagecontrol.io/Package%20Control.sublime-package
4. 重启sublime

然后将自己备份的`User`文件夹替换掉现有的就行。

**PS：我的配置github地址**：<https://github.com/HaoQChen/SublimeSetting>参考很多博客配置的，最终样子长这样：

![](/img/in_post/sublime_syncing/my_sublime.png)

喜欢的话帮我github点个赞呗。

# 参考

<br>

**喜欢我的文章的话Star一下呗[Star](https://github.com/HaoQChen/HaoQChen.github.io)**

**版权声明：本文为白夜行的狼原创文章，未经允许不得以任何形式转载**
