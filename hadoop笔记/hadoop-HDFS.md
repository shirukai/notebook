# hadoop-HDFS(分布式文件系统) 

## HDFS设计架构 

基本概念：块(Block)、NameNode、DataNode

### 块（block） 

HDFS的文件被分成块进行存储，HDFS块的默认大小64MB，块是文件存储处理的逻辑单元（在Hadoop-0.x和Hadoop-1.x中默认的块大小为64MB，在Hadoop-2.0及以后的版本中默认的块大小是128MB）

### NameNode 

namenode是管理节点，存放文件元数据

①文件与数据块的映射表

②数据块与数据节点的映射表



![https://shirukai.gitee.io/images/59bf8f810001f54912800720.jpg](https://shirukai.gitee.io/images/59bf8f810001f54912800720.jpg)



### DateNode 

datenode是HDFS的工作节点，存放数据块

## HDFS中数据管理与容错 

### 数据块副本

每个数据块3个副本，分布在两个机架内的三个节点

### 心跳检测 

DataNode定期向NameNode 发送心跳消息，来告诉NameNode自己的运行状态

### 二级NameNode 

二级NameNode定期同步元数据映射文件和修改日志，nameNode发生故障时，备胎转正

## HDFS文件读写流程 

### HDFS读取文件

![https://shirukai.gitee.io/images/5999929d0001645b12800720.jpg](https://shirukai.gitee.io/images/5999929d0001645b12800720.jpg)



客户端（java程序、命令行等）向NameNode发送文件读取请求（把文件名、路径告诉namenode）

Namenode查询元数据，然后返回给客户端

客户端得到Namenode返回值，知道请求的文件都包含哪些块，以及这些块都保存在哪个datanode里，然后客户端把块文件下载下来之后，组装成文件。



### HDFS文件写入 

![https://shirukai.gitee.io/images/5979f2db0001d5f112800720.jpg](https://shirukai.gitee.io/images/5979f2db0001d5f112800720.jpg)



客户端将文件切成块之后，告诉NameNode

NameNode找到一些可用的、当前在线、也有足够空间的datanode返回给客户端

客户端根据返回的信息，对块进行写入。写入第一个块之后，要进行流水线复制，复制完成之后更新元数据

## HDFS的特点 

### 适用性和局限性 

适合数据批量读写，吞吐量高；

不适合交互式应用，低延迟很难满足；



适合一次写入多次读取，顺序读写

不支持多用户并发写相同的文件



## HDFS命令行操作演示 

### 创建目录 

创建一个名字为input的目录

```
hadoop fs -mkdir /input
```

### 写入文件 

把文件anaconda-ks.cfg写入hdfs中的input文件夹里

```
hadoop fs -put anaconda-ks.cfg /input
```

### 查看文件 

查看hdfs中写入的anaconda-ks.cfg文件

```
hadoop fs -cat /input/anaconda-ks.cfg
```

### 读取文件 

从hdfs中读取文件，保存到本地，并重名为getfromhadoop

```
hadoop fs -get /input/anaconda-ks.cfg getfromhadoop
```

### 删除文件 

删除hdfs中 /input目录下的anaconda-ks.cfg文件

```
hadoop fs -rm /input/anaconda-ks.cfg
```

### 查看文件系统里的所有信息 

```
hadoop dfsadmin -report
```

