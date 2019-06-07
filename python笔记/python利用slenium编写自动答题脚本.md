# python利用slenium编写自动答题脚本 

> 最近在一次做灯塔在线知识竞答的时候，突然萌生了用python写一个自动化答题的脚本。然后就根据想法在网上查了查相关资料，带着问题找思路。
>
> python如何从浏览器中爬取数据？
>
> python如何控制浏览器？
>
> python如何读取word文档？

##### 经过搜索查阅资料，基本确定思路，首先简单介绍一下slenium： 

Selenium是一个用于Web应用程序测试的工具。Selenium测试直接运行在浏览器中，就像真正的用户在操作一样。支持的浏览器包括IE（7, 8, 9, 10, 11），Mozilla Firefox，Safari，Google Chrome，Opera等。

简单点说，有了这个工具，我们就可以根据自己的想法对浏览器为所欲为了。这里利用python调用slenium对页面数据进行抓取，以及对页面的自动化操作。

##### 然后就是利用python-docx读取word文档

![](https://shirukai.gitee.io/images/2478fb526b4b5adf6593494eca2b4614.gif)



