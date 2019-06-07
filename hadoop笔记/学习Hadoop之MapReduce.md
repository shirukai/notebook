# 学习Hadoop之MapReduce笔记

##  MapReduce最简单的例子 

> 如下图所示，假如我们要计算一份海报的数据，那么我们应该怎么快速计算出结果呢？

​	首先，我们要知道的是，我们对于一份非常大的文件上传到我们的HDFS分布式系统上时，它已经不是一个文件了，而是被物理分割成了很多份，至于被分成多少块那就要看文件的大小了，假如文件的大小是1g，HDFS默认的Block Size（区块）大小是128M，那么1g的文件就被分成了8个区块，每个区块对应一个Mapper，8个区块对应着8个Mapper，每个Mapper执行完自己任务之后把结果传到Reducer ，等Mapper执行完毕之后Reducer把八个子结果综合起来就是我们要的最后结果。

​	我们以下面这个简单的例子来说，假如我们要计算1+5+7+3+4+9+3+5+6的值，我们为了快速计算，先把1+5+7、3+4+9、3+5+6 分成三个区块，这三个区块分别用三台电脑来计算，每台电脑都相当于一个Map，当三台电脑各自计算完自己分到的数字之和后传到Reducer，Reducer再把三个Map计算出来的中间值13、16、14相加，这样就可以得到最终结果43，这就是简单的MapRdeuce原理。

![http://img.blog.csdn.net/20160916095459034?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center](http://img.blog.csdn.net/20160916095459034?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

## MapReduce概述 

* Mapreduce 作业是一种大规模数据集的并行计算的编程模型，我们可以将HDFS中存放的海量数据，通过MapReduce作业进行计算，得到目标数据。
* MR由两个阶段组成：Map和Reduce，用户只需要实现map()和reduce() 两个函数，即可实现分布式计算，非常简单。
* 这两个函数的形参是key、value对，表示函数的输入信息。

## MapReduce架构 

> 在Hadoop2.0中MapReduce是运行在Yarn之上的，Yarn的老大是ResourceManager，小弟是NodeManager，ResourceManager用来管理资源的分配调度，NodeManager负责做具体的事情，那么对于分布式处理来说，框架的原理是什么呢？

### 第1步

Client端会把可运行的Jar包先上传到HDFS分布式系统，那么大家有可能会问既然ResourceManager是资源管理者，那么为什么不把资源直接上传到ResourceManager上呢？这是因为每一个可运行的Jar包都可能包含很多依赖的内容，资源所占的大小可能很大，当成千上万个运行资源都上传到ResourceManager时势必会导致ResourceManager崩溃，而我们的HDFS分布式系统则刚好就是用来处理大数据的，它可以处理海量数据，当然也就可以存储运行所需要的资源文件了。因此我们把资源都上传到HDFS分布式系统上。

### 第2步

Client把在HDFS上的存储信息列表发送给ResourceManager，存储信息包括文件的大小，文件在HDFS系统上存放的路径，该文件被物理分割成了几块，每个块分别放在了什么位置等信息。

### 第3步

ResourceManager和NodeManager之间是通过心跳机制来保持联系的，就是NodeManager每隔一段时间就要向ResourceManager报告一下自己还活着的信息，如果ResourceManager长期得不到NodeManager的信息，那么就认为该NodeManager已经挂掉了，需要再启动一台设备做为NodeManager。那么我们思考一下，我们是让ResourceManager把主动把任务下发给各个NodeManager好呢还是NodeManager主动向ResourceManager领任务好呢？我想大家肯定很明确的就会做出答复：那就是NodeManager主动向ResourceManager领取任务的方式比较好，因为这样可以大大减轻ResourceManager做为管理者的压力。

### 第4步 

NodeManager向ResourceManager领取到任务后便通过HTTP协议从HDFS系统上下载运行所需要的资源，NodeManager当中一个Block块对应着一个Map，每个Map处理一个块的内容，当所有Map都处理完之后再通过Reducer进行合并。

### 第5步

NodeManager把处理好的内容再上传给HDFS分布式系统，从而完成了整个流程。

![http://img.blog.csdn.net/20160917083936556?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center](http://img.blog.csdn.net/20160917083936556?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

**上面我们说了MapReduce的架构，接下来我们具体来看一下MapReduce的原理，也就是NodeManager当中具体发生了什么，如下图所示。我们看页面左下角，我们发现一个file文件有可能被物理切分成block1、block2...blockN个块，一个块又被切分成了两个切片，每个切片对应着一个MapperTask，每个Mapper把处理后的结果（Map）传给shuffle处理，shuffle处理完之后再交给Reducer进行处理，Reducer处理完之后把处理结果写到结果文件当中，每个Reducer对应一个结果文件。**

![http://img.blog.csdn.net/20160916184801674?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center](http://img.blog.csdn.net/20160916184801674?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)



## MapReduce的四个阶段 

* Split阶段 分片输入阶段
* Map阶段（需要编码）
* Shuffle阶段
* Reduce阶段（需要编码）

## 从分片输入到map

block块的大小：

Hadoop1.x默认大小是64MB

Hadoop2.x默认大小是128MB

可以在hdfs-site.xml设置参数：dfs.block.size

### 分片输入阶段 split



摘录参考文章：http://blog.csdn.net/u012453843/article/details/52554125



