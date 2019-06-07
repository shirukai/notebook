# windows搭建scrapy爬虫环境

## 一、安装 Anaconda 

官网下载：https://www.anaconda.com/download/#windows

1.下载完成后进行安装，【Next】

![](https://shirukai.gitee.io/images/201801301557_945.png)

2.点击【I Agree】同意条款

![](https://shirukai.gitee.io/images/201801301558_628.png)

3.选择安装类型，第一个是安装到当前用户，第二个是安装到所有用户。

![](https://shirukai.gitee.io/images/201801301600_379.png)

4.选择安装路径

![](https://shirukai.gitee.io/images/201801301600_78.png)



5.勾选Add Anaconda to my PATH environment variable选项，将 anaconda加入的环境变量里。

![](https://shirukai.gitee.io/images/201801301605_543.png)

6.点击【Install】即可等待安装完成。

## 二、安装scrapy 

命令行输入

```
conda install scrapy
```

安装过程会检查相关依赖，输入【Y】即可继续安装。

![](https://shirukai.gitee.io/images/201801301613_752.png)

## 三、Scrapy使用 

### 1.创建项目 

在自己的代码仓库文件夹下，执行下列命令(tutorial 是项目名)：

```
scrapy startproject tutorial
```

![](https://shirukai.gitee.io/images/201801301617_902.png)

创建完成后可以导入到pycharm里，然后看一下项目结构：

```
tutorial/
    scrapy.cfg
    tutorial/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
```

![](https://shirukai.gitee.io/images/201801301619_902.png)

### 2.定义Item 

Item 是保存爬取到的数据的容器；其使用方法和python字典类似。虽然您也可以在Scrapy中直接使用dict，但是 Item 提供了额外保护机制来避免拼写错误导致的未定义字段错误。 They can also be used with [Item Loaders](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/loaders.html#topics-loaders), a mechanism with helpers to conveniently populate Items.

类似在ORM中做的一样，您可以通过创建一个 [`scrapy.Item`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/items.html#scrapy.item.Item) 类， 并且定义类型为 [`scrapy.Field`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/items.html#scrapy.item.Field) 的类属性来定义一个Item。 (如果不了解ORM, 不用担心，您会发现这个步骤非常简单)

首先根据需要从dmoz.org获取到的数据对item进行建模。 我们需要从dmoz中获取名字，url，以及网站的描述。 对此，在item中定义相应的字段。编辑 `tutorial` 目录中的 `items.py` 文件:

```
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
```

### 3.编写第一个爬虫(Spider) 

Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。

其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 [item](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/items.html#topics-items) 的方法。

为了创建一个Spider，您必须继承 [`scrapy.Spider`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/spiders.html#scrapy.spiders.Spider) 类， 且定义一些属性:

- [`name`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/spiders.html#scrapy.spiders.Spider.name): 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
- [`start_urls`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/spiders.html#scrapy.spiders.Spider.start_urls): 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
- [`parse()`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/spiders.html#scrapy.spiders.Spider.parse) 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 [`Response`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/request-response.html#scrapy.http.Response) 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 [`Request`](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/request-response.html#scrapy.http.Request) 对象。

以下为我们的第一个Spider代码，保存在 `tutorial/spiders` 目录下的 `dmoz_spider.py` 文件中:

```
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html",
        "http://blog.51cto.com/linuxliu/2066060"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
```

### 4.爬取 

进入项目的根目录，执行下列命令启动spider:

```
scrapy crawl dmoz
```

![](https://shirukai.gitee.io/images/201801301705_32.png)

运行完成后，后再当前目录下生成两个页面：

![](https://shirukai.gitee.io/images/201801301706_26.png)

### 5.pycharm 调试scrapy项目 

> scrapy在pycharm里是没法直接运行调试的，我们可以通过以下方式，对齐进行调试输出。

我们可以尝试在pycharm里直接对scrapy项目进行调试

首相在项目根目录下创建一个main.py：

```
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'dmoz'])
```

然后直接右击运行main.py

![](https://shirukai.gitee.io/images/201801301710_512.png)

这是会发现，报错：

```
    from cryptography.hazmat.bindings._openssl import ffi, lib
ImportError: DLL load failed: 操作系统无法运行 %1。
```

#### 解决方法：

安装 OpenSSL 并将安装目录/bin下的 libeay.dll 和 ssleay.dll复制到 C:\Windows\System32目录下。

OpenSSL 64位的版本，在这个链接下载：http://ov1a6etyz.bkt.clouddn.com/201801301720_87.exe

注意安装的时候，这一步，选择【The OpenSSL binaries（/bin）directory】这个选项。这样在安装目录的bin下才会找到需要的两个.dll文件。

![](https://shirukai.gitee.io/images/201801301722_244.png)

 

