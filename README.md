**最终效果：<https://haoqchen.site>**  
如果喜欢可以直接使用我修改后的主题。

**但是请一定要将我的信息替换成你自己的，另外请不要保留我的博客。**

主体来源于：[Hux Blog](https://github.com/Huxpro/huxpro.github.io)  
跟着这个博客教程走：[如何快速搭建自己的github.io博客](https://blog.csdn.net/walkerhau/article/details/77394659?utm_source=debugrun&utm_medium=referral)  
同时受到了这个博客的很大帮助：[利用 GitHub Pages 快速搭建个人博客](https://www.jianshu.com/p/e68fba58f75c)  

# 以下部分借鉴[GJXS1980](https://github.com/GJXS1980/gjxs.github.io)  
## 动态鼠标曲线  
添加模块`canvas-nest.min.js`到js目录下 修改`layouts/post.html`文件在开始添加下面代码  
``` js
 <!-- canvas-nest.min.js -->
<script type="text/javascript" src="../../../../js/canvas-nest.min.js"></script>
```
更喜欢简介一点，尤其手机看起来很乱，所以注释掉了这个。

## 返回顶部  
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

## 显示站点访问总量
具体教程参考:[不蒜子](http://ibruce.info/2015/04/04/busuanzi/)

## 添加CSDN博客  
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

# 以下部分借鉴[利用 GitHub Pages 快速搭建个人博客](https://www.jianshu.com/p/e68fba58f75c)  
## 百度统计  
直接申请，然后在\_config.yml中填写码就行。

## 删除friend  
直接将\_config.yml中的friend注释了就好。

## 修改网站图标  
在博客`img`目录下找到并替换`favicon.ico`这个图标即可，图标尺寸为32x32。

## 增加Gitalk评论功能  
参考[为博客添加 Gitalk 评论插件](http://qiubaiying.top/2017/12/19/%E4%B8%BA%E5%8D%9A%E5%AE%A2%E6%B7%BB%E5%8A%A0-Gitalk-%E8%AF%84%E8%AE%BA%E6%8F%92%E4%BB%B6/)  
以及官网[Gitalk](https://github.com/gitalk/gitalk/blob/master/readme-cn.md)

# 以下是我自己的一些更改
## 删除portolio  
根据[Jekyll官网](https://www.jekyll.com.cn/docs/pages/)的说法，只要直接删除文件夹即可

## 增加搜索栏
<https://github.com/HaoQChen/jekyll-search>  
另外我修改了搜索栏的位置，放到了右上方。只需要修改增加到`_includes/footer.html`中设置位置的px值即可。
```
<div style="position: fixed; right: 16px; top: 62px;">
    <img src="/search/img/cb-search.png"  id="cb-search-btn"  title="双击ctrl试一下"/>
</div>
```

## 删除标题前的#  
只需要删除`_layouts/post.html`中189行的icon中的#即可，应该可以修改成任意值。

## 修改文章列表中的排序  
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

## 导航栏分级标题  
根据[#116](https://github.com/Huxpro/huxpro.github.io/issues/116)来修改的。找到`css`目录下的`hux-blog.min.css`，不知道为什么我的sublime显示这个文件只有一行，很长的一行。我尝试过在一些网站恢复格式，但是保存后导致网页显示有问题。最后就只能在这个只有很长一行的文件中搜索到相应位置修改。  
`这里需要注意的是，如果想h1、h2等都不同，需要删除逗号，要注意格式～～～`

## 更改最底下的作者链接  
貌似链接到作者的github获取star数，加载网页会比较花时间，我就直接删除了，并修改了一下下。主要修改都在`_includes/footer.html`中

## 修改About中只留下中文自我介绍  
主要修改about.html。删除了`<!-- Language Selector -->`、`<!-- English Version -->`。最主要要将`multilingual: false`

## 在谷歌、百度搜索引擎中登记自己的网站
自己刚建的网站别人是搜索不到的，搜索引擎的爬虫不会这么快爬到你的网站，但是你可以在谷歌和百度中进行登记，这样可以加快进程(也要等几天)。  
要查看自己的网站是否已经被某个搜索引擎收录，可以在搜索框中输入：`site:https://haoqchen.github.io/`  
登记方法：  导航栏分级标题
* Google网站站长[Google Search Console](https://search.google.com/search-console?hl=zh-CN)。在这里添加资源，并按要求验证即可。我是选择了第一个，下载html文件，然后放在主目录下（跟archive同一目录）。我不会用什么sitemap，就很蠢地一篇篇博客提交给Google去抓取，地址在`旧版Search Console->抓取>Google抓取工具`。添加每一篇的地址，然后点`抓取`，然后点`请求编入索引`（最好抓取一篇请求一篇，而且一次不要提交太多，隔天吧，我的请求到后面出现错误，不知道为什么）。这样你的博客就能出现在`site:https://haoqchen.github.io/`中了，也可以直接在Google中搜索到了。  
* [百度链接提交](https://ziyuan.baidu.com/linksubmit/url)。百度也有要验证网站的～～～我忘了当时是怎么进去的了。（github禁止了百度的爬虫，所以怎么设置，百度都不可能搜索到博客的。需要另外搞。）

注：新版Google站长网站不支持一篇一篇添加，我参考[jekyll-sitemap插件](https://github.com/jekyll/jekyll-sitemap)自动生成了sitemap，也就是在`_config.yml`中添加了`plugins: [jekyll-paginate, jekyll-sitemap]`，然后在站长网站->站点地图->添加新的站点地图中填上`sitemap.xml`


## 安装本地调试
这个真的很多坑。。。。
参考:
[安装Jekyll本地调试环境](http://lazybios.com/2014/09/install-jekyll-in-locate/)

[ubuntu16.04安装jekyll 3.3.1](https://www.cnblogs.com/litifeng/p/6337614.html)

[Ubuntu 升级 Ruby](https://blog.csdn.net/henryhu712/article/details/89224467)

[run jekyll serve failed ''cannot load such file -- jekyll-paginate](https://github.com/Huxpro/huxpro.github.io/issues/62)

1. 安装编译相关：
   ```bash
   sudo apt-get install build-essential
   ```
2. 安装ruby：
   由于默认的安装版本太低，直接安装会出问题，要按照下面的安装：
   ```bash
   sudo add-apt-repository ppa:brightbox/ruby-ng
   sudo apt-get update
   sudo apt-get install ruby2.6 ruby2.6-dev
   ```
3. 安装并更新RubyGems：
   ```bash
   sudo apt-get install rubygems
   sudo gem update --system
   ```
4. 安装NodeJS：
   ```bash
   curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```
5. 安装gem install jekyll：
   ```bash
   sudo gem install jekyll
   sudo gem install github-pages
   ```
随后在自己的文件夹目录下创建一个`Gemfile`文件，将下面的内容填到该文件中

```bash
source 'https://rubygems.org'      
gem 'github-pages'
```

随后执行以下命令即可在`http://127.0.0.1:4000/`中看到自己的博客

```bash
bundle install
bundle exec jekyll serve
```

## 域名
尝试买了一个域名，想让百度搜索引擎能爬到，然后在coding.me上也弄一个类似github pages的，将百度或者国内的重定向到coding.me，最后放弃。目前域名全部重定向到给github pages，但github.io的域名就不能用了～～～～而且登记搜索引擎等等这些又要重新弄，很烦。

* 2018-11-29决定放弃coding.me。百度搜索引擎太垃圾，coding.me连本ReadMe显示都有问题，不想浪费时间了，让它去抓取CSDN吧，在CSDN上发布一篇好了。

## 谷歌分析
在官网创建账号和地址什么的，然后将ID填到\_config.yml的`ga_track_id:`就好。

## 自动化脚本
增加了一个add\_new\_article.sh脚本，只要`add_new_article.sh article_title`就可以自动完成img中模板文件夹的复制，模板md文件的复制、重命名以及模板文件中一些基本信息的替换

## 修改字体
需要在本地调试，然后改一堆东西。不是很懂，希望有前端的大佬给科普一下
首先装用于实时更新css的`grunt`，除了第一个命令，其余需要在仓库目录下运行：
```bash
sudo npm install -g grunt-cli
npm install grunt --save-dev
npm install grunt-contrib-uglify --save-dev
npm install grunt-contrib-less --save-dev
npm install grunt-banner --save-dev
npm install grunt-contrib-watch --save-dev
```
假设你已经在本地启动了server，那么再运行`grunt watch`，就可以将你在`./less/`文件加下的修改实时更新到博客（通过实时编译成`./css/`文件夹下的文件实现）。

随后在`./less/hux-blog.less`中修改第一个p如下，然后再刷新下你的博客，是不是就可以修改了

```less
p {
  margin: 30px 0; //缩进
  font-size: 16px;//字体大小
  line-height: 1.5;//行距
  letter-spacing: 1px//每个字的间距
}
```

上面的[导航栏分级标题](#导航栏分级标题)修改方法只是临时修改生成的css的，要想修改源码，可以在less/side-catalog.less中找到`h1_nav`这一项，然后按照你的需求改就好，比如我的：

```less
.h1_nav{
            margin-left: 0;
            font-size: 15px;
            font-weight: bold;
        }
.h2_nav{
    margin-left: 10px;
    font-size: 13px;
    font-weight: bold;
}
.h3_nav{
    margin-left: 20px;
    font-size: 11px;
    font-weight: bold;
}
.h4_nav,.h5_nav,.h6_nav{
    margin-left: 30px;
    font-size: 10px;
    a{
        max-width: 170px;
    }
}
```

## 分类

主要参考：<https://blog.webjeda.com/jekyll-categories/>，目前能在标题下方显示，并且能导向一个分类列表，但不怎么显眼。希望能做成像<https://chaooo.github.io/>这样的。

主要有三个步骤：

1. 在每个文章的头部增加一个分类，如`categories: Personal`
2. 新建一个`categories.html`放在主目录下，文件内容可直接看我的源码
3. 在每篇文章的适当位置增加指向`categories.html`的链接。我主要是通过修改`intro-header.html`中的文章标题部分实现的。详见代码中`<header class="intro-header style-text">`部分

但是一定要注意，根据[Jekyll官网永久链接](http://jekyllcn.com/docs/permalinks/)的描述，文章生成的链接默认是`/:categories/:year/:month/:day/:title/`。如果没有分类名就留空，有分类名会导致以前的链接都不能用，需要修改`_config.yml`中的`permalink`为`/:year/:month/:day/:title/`。

## 404改成宝贝回家

在[wordzzzz的博客](https://wordzzzz.github.io/404.html)中看到404变成了宝贝回家的页面，深受感动，所以将自己的404也变成了宝贝回家。

具体做法是将404.html的内容换成下面这样的：

```html
<!DOCTYPE HTML>
<html>
<head>
  <meta http-equiv="content-type" content="text/html;charset=utf-8;"/>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="robots" content="all" />
  <meta name="robots" content="index,follow"/>
  <link rel="stylesheet" type="text/css" href="https://qzone.qq.com/gy/404/style/404style.css">
</head>
<body>
  <script type="text/plain" src="http://www.qq.com/404/search_children.js"
          charset="utf-8" homePageUrl="/"
          homePageName="回到我的主页">
  </script>
  <script src="https://qzone.qq.com/gy/404/data.js" charset="utf-8"></script>
  <script src="https://qzone.qq.com/gy/404/page.js" charset="utf-8"></script>
</body>
</html>
```

## 不显示某篇文章
比如正在创作中，不想别人看到，可以在文章头部增加一个`published: false`就可以了。

## 增加赞赏功能
参考[一之笔的博客](https://github.com/yizibi/yizibi.github.io)，首先将`reward.css`放到css文件夹下，然后修改`_layouts->post.html`，在{{content}}后面增加以下内容：

```html
<!-- 打赏功能 -->
<link href="/css/reward.css?v=6.2.0" rel="stylesheet" type="text/css" />

<div>
    <hr>
    <div style="padding: 10px 0; margin: 20px auto; width: 90%; text-align: center;">
        <div id="wechat"><p>如果你觉得这篇文章帮你节省了时间，增长了知识，请支持我写出更多这样的文章</p></div>
        <br>
        <button id="rewardButton" disable="enable" onclick="var qr = document.getElementById('QR'); if (qr.style.display === 'none') {qr.style.display='block';} else {qr.style.display='none'}">
            <span>打赏</span>
        </button>
        <div id="QR" style="display: none;">              
            <div id="wechat" style="display: inline-block">
                <img id="wechat_qr" src="/img/reward/wechat.png" alt="白夜行的狼 微信支付"/>
                <p>微信支付</p>
            </div>
                                
            <div id="alipay" style="display: inline-block">
                <img id="alipay_qr" src="/img/reward/alipay.png" alt="白夜行的狼 支付宝"/>
                <p>支付宝</p>
            </div>
        </div>
    </div>
    <hr>     
</div>
```

## 修改文章占总页面的宽度

需要修改`page.html`中的`col-lg-`、`col-lg-offset-`、`col-md-`、`col-md-offset-`参数，这几个参数的意思可以百度，大致是在不同屏幕分辨率时显示的比例，总数都是12。


## @TODO
* 最下面增加“你可能感兴趣的文章，导向同一个分类的”
* 能不能将给博客的点赞重定向到给github点赞
* 代码高亮[GJXS1980的博客](https://github.com/GJXS1980/gjxs.github.io)



**建议**
* 多看github中的issue，很多问题其实别人都遇到过了，有些甚至给出了解决方法。
* 域名建议去阿里云的万网买。。。。百度的解析只有自己的百度搜索引擎，真的坑。
* 如果更新了域名，记得重新申请一下Gitalk的ClientID，不然无法评论

