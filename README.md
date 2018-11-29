主体来源于：[Hux Blog](https://github.com/Huxpro/huxpro.github.io)  
跟着这个博客教程走：[如何快速搭建自己的github.io博客](https://blog.csdn.net/walkerhau/article/details/77394659?utm_source=debugrun&utm_medium=referral)  
同时受到了这个博客的很大帮助：[利用 GitHub Pages 快速搭建个人博客](https://www.jianshu.com/p/e68fba58f75c)  

以下部分借鉴[GJXS1980](https://github.com/GJXS1980/gjxs.github.io)  
* 动态鼠标曲线  
添加模块`canvas-nest.min.js`到js目录下 修改`layouts/post.html`文件在开始添加下面代码  
``` js
 <!-- canvas-nest.min.js -->
<script type="text/javascript" src="../../../../js/canvas-nest.min.js"></script>
```

* 返回顶部  
把在rocket.css、signature.css和toc.css下载到css的目录下，然后在 include目录下的head.html文件的头部添加下面代码：  
``` html
<link rel="stylesheet" href="/css/rocket.css">
<link rel="stylesheet" href="/css/signature.css">
<link rel="stylesheet" href="/css/toc.css">
```

把在totop.js和toc.js下载到js的目录下，然后在include目录下的footer.html的最后添加下面代码：  
```
<a id="rocket" href="#top" class=""></a>
<script type="text/javascript" src="/js/totop.js?v=1.0.0" async=""></script>
<script type="text/javascript" src="/js/toc.js?v=1.0.0" async=""></script>
```

* 显示站点访问总量
具体教程参考:[不蒜子](http://ibruce.info/2015/04/04/busuanzi/)

* 添加CSDN博客  
在\_config.yml用户名那里添加一栏:`CSDN_username:      u013834525`  
在`_includes/sns-links.html`中对应位置（其他网站账户附近）添加
```
{% if site.CSDN_username %}
    <li>
      <a target="_blank" href="http://blog.csdn.net/{{ site.CSDN_username }}">
        <span class="fa-stack fa-lg">
          <i class="fa fa-circle fa-stack-2x"></i>
          <i class="fa fa-CSDN fa-stack-1x fa-inverse">C</i>
        </span>
      </a>
    </li>
{% endif %}
```

以下部分借鉴[利用 GitHub Pages 快速搭建个人博客](https://www.jianshu.com/p/e68fba58f75c)  
* 百度统计  
直接申请，然后在\_config.yml中填写码就行。

* 删除friend  
直接将\_config.yml中的friend注释了就好。

* 修改网站图标  
在博客`img`目录下找到并替换`favicon.ico`这个图标即可，图标尺寸为32x32。

* 增加Gitalk评论功能  
参考[为博客添加 Gitalk 评论插件](http://qiubaiying.top/2017/12/19/%E4%B8%BA%E5%8D%9A%E5%AE%A2%E6%B7%BB%E5%8A%A0-Gitalk-%E8%AF%84%E8%AE%BA%E6%8F%92%E4%BB%B6/)  
以及官网[Gitalk](https://github.com/gitalk/gitalk/blob/master/readme-cn.md)

以下是我自己的一些更改
* 删除portolio  
根据[Jekyll官网](https://www.jekyll.com.cn/docs/pages/)的说法，只要直接删除文件夹即可

* 增加搜索栏
<https://github.com/HaoQChen/jekyll-search>  
另外我修改了搜索栏的位置，放到了右上方。只需要修改增加到`_includes/footer.html`中设置位置的px值即可。
```
<div style="position: fixed; right: 16px; top: 62px;">
    <img src="/search/img/cb-search.png"  id="cb-search-btn"  title="双击ctrl试一下"/>
</div>
```

* 删除标题前的#  
只需要删除`_layouts/post.html`中189行的icon中的#即可，应该可以修改成任意值。

* 修改文章列表中的排序  
原来只是按照年份排序的，我增加了月份。修改`archive.html`中59行为
```
{%- assign _currentdate = _article.date | date: '%Y-%m' -%}
```
并且每篇文章我也增加了日期，在副标题下添加这一句  
``` html
<h4 class="post-date">
    {{ _article.date | date: '%Y-%m-%d' }}
</h4>
```

* 导航栏分级标题  
根据[#116](https://github.com/Huxpro/huxpro.github.io/issues/116)来修改的。找到`css`目录下的`hux-blog.min.css`，不知道为什么我的sublime显示这个文件只有一行，很长的一行。我尝试过在一些网站恢复格式，但是保存后导致网页显示有问题。最后就只能在这个只有很长一行的文件中搜索到相应位置修改。  
`这里需要注意的是，如果想h1、h2等都不同，需要删除逗号，要注意格式～～～`

* 更改最底下的作者链接  
貌似链接到作者的github获取star数，加载网页会比较花时间，我就直接删除了，并修改了一下下。主要修改都在`_includes/footer.html`中

* 修改About中只留下中文自我介绍  
主要修改about.html。删除了`<!-- Language Selector -->`、`<!-- English Version -->`。最主要要将`multilingual: false`

* 在谷歌、百度搜索引擎中登记自己的网站
自己刚建的网站别人是搜索不到的，搜索引擎的爬虫不会这么快爬到你的网站，但是你可以在谷歌和百度中进行登记，这样可以加快进程(也要等几天)。  
要查看自己的网站是否已经被某个搜索引擎收录，可以在搜索框中输入：`site:https://haoqchen.github.io/`  
登记方法：  
* Google网站站长[Google Search Console](https://search.google.com/search-console?hl=zh-CN)。在这里添加资源，并按要求验证即可。我是选择了第一个，下载html文件，然后放在主目录下（跟archive同一目录）。我不会用什么sitemap，就很蠢地一篇篇博客提交给Google去抓取，地址在`旧版Search Console->抓取>Google抓取工具`。添加每一篇的地址，然后点`抓取`，然后点`请求编入索引`（最好抓取一篇请求一篇，而且一次不要提交太多，隔天吧，我的请求到后面出现错误，不知道为什么）。这样你的博客就能出现在`site:https://haoqchen.github.io/`中了，也可以直接在Google中搜索到了。  
* [百度链接提交](https://ziyuan.baidu.com/linksubmit/url)。百度也有要验证网站的～～～我忘了当时是怎么进去的了。（github禁止了百度的爬虫，所以怎么设置，百度都不可能搜索到博客的。需要另外搞。）

* 安装本地调试
gem版本太低，更新步骤太复杂，放弃了。

* 2018-11-29决定放弃coding.me。百度搜索引擎太垃圾，coding.me连本ReadMe显示都有问题，不想浪费时间了，让它去抓取CSDN吧，在CSDN上发布一篇好了。



**建议**
* 多看github中的issue，很多问题其实别人都遇到过了，有些甚至给出了解决方法。
* 域名建议去阿里云的万网买。。。。百度的解析只有自己的百度搜索引擎，真的坑。

