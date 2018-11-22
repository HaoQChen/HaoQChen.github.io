主体来源于：[Hux Blog](https://github.com/Huxpro/huxpro.github.io)  
跟着这个博客教程走：[如何快速搭建自己的github.io博客](https://blog.csdn.net/walkerhau/article/details/77394659?utm_source=debugrun&utm_medium=referral)  
同时受到了这个博客的很大帮助：[利用 GitHub Pages 快速搭建个人博客](https://www.jianshu.com/p/e68fba58f75c)  

以下部分借鉴[GJXS1980](https://github.com/GJXS1980/gjxs.github.io)  
* 动态鼠标曲线  
添加模块`canvas-nest.min.js`到js目录下 修改`layouts/post.html`文件在开始添加下面代码
```js
 <!-- canvas-nest.min.js -->
<script type="text/javascript" src="../../../../js/canvas-nest.min.js"></script>
```

* 返回顶部
把在rocket.css、signature.css和toc.css下载到css的目录下，然后在 include目录下的head.html文件的头部添加下面代码：
```html
<link rel="stylesheet" href="/css/rocket.css">
<link rel="stylesheet" href="/css/signature.css">
<link rel="stylesheet" href="/css/toc.css">
```

把在totop.js和toc.js下载到js的目录下，然后在include目录下的footer.html的最后添加下面代码：  
```html
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
    <img src="/search/img/cb-search.png"  id="cb-search-btn"  title="双击ctrl试一下"/>       <img src="/search/img/cb-search.png"  id="cb-search-btn"  title="双击ctrl试一下"/>
</div>  </div>
```

* 删除标题前的#
只需要删除`_layouts/post.html`中189行的icon中的#即可，应该可以修改成任意值。

**建议**
* 多看github中的issue，很多问题其实别人都遇到过了，有些甚至给出了解决方法。







