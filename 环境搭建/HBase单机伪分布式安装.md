# HBase单机伪分布式安装

> 版本说明：
>
> hadoop-2.7.6
>
> zookeeper-3.4.13
>
> hbase-2.1.0

## 1 下载安装包

官网地址：http://hbase.apache.org/downloads.html

### 1.1 下载安装包

在官网下载相应版本的安装包，这里下载的是hbase-2.1.0版本。

```shell
wget http://mirror.bit.edu.cn/apache/hbase/2.1.0/hbase-2.1.0-bin.tar.gz
```

### 1.2 解压并重命名

解压下载好的安装包

```shell
tar -zxvf hbase-2.1.0-bin.tar.gz
```

重命名为 hbase-2.1.0

```shell
mv hbase-2.1.0-bin hbase-2.1.0
```

## 2 环境参数参数配置

### 2.1 设置HBASE_HOME环境变量

将HBase添加到环境变量里

```shell
vi ~/.base_profile
```

添加内容：

```shell
#set hbase
export HBASE_HOME=/Users/shirukai/apps/hbase-2.1.0
export PATH=$HBASE_HOME/bin:$PATH
```

### 2.2 修改HBase相关参数

进入HBase 的配置目录

```shell
cd $HBASE_HOME/conf
```

#### 2.2.1 修改hbase-env.sh

该文件主要是hbase启动的一些环境参数，这里主要修改如下内容：

```shell
# 导出JAVA_HOME
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_171.jdk/Contents/Home
# 不使用HBase管理ZK
export HBASE_MANAGES_ZK=false
```

#### 2.2.2 修改hbase-site.xml

该文件是hbase的配置文件，主要修改内容有：

```xml
 <property>
    <name>hbase.rootdir</name>
    <value>hdfs://localhost:9000/hbase</value>
  </property>
  <!--集群模式 -->
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.zookeeper.quorum</name>
    <value>localhost:2181</value>
  </property>

```

#### 2.2.3 修改regionservers

将所有的regionserver的hostname添加到这个文件，因为我们是单机伪分布式所以只有一个regionserver就是localhost，这里无需修改

```shell
localhost
```

## 3 启动测试

在启动HBase之前，我们要确保我们的hdfs、zookeeper出去开启状态。

### 3.1 启动HBase

```shell
sh $HBASE_HOME/bin/start-hbase.sh
```

### 3.2 测试

#### jps查看进程是否启动

```shell
jps
```

![](http://shirukai.gitee.io/images/bbad5b8570fc3a41351d7fe91ffd8fd6.jpg)

#### 查看web ui

访问http://localhost:16010

![](http://shirukai.gitee.io/images/e5ce53ab1e5a918d94dedd06fa1bf7ad.jpg)

#### 启动hbase shell

```shell
hbase shell
```

查看版本号

```shell
hbase(main):003:0> version
2.1.0, re1673bb0bbfea21d6e5dba73e013b09b8b49b89b, Tue Jul 10 17:26:48 CST 2018
Took 0.0004 seconds
```

查看当前状态

```shell
hbase(main):004:0> status
1 active master, 0 backup masters, 1 servers, 0 dead, 3.0000 average load
Took 0.6481 seconds
```

创建一张表

```shell
hbase(main):005:0> create 'table1','name','age'
Created table table1
Took 0.8107 seconds                                                                                                                                                         
=> Hbase::Table - table1
```

查看表描述

```shell
hbase(main):006:0> describe 'table1'
Table table1 is ENABLED                                                                                                                                                     
table1                                                                                                                                                                      
COLUMN FAMILIES DESCRIPTION                                                                                                                                                 
{NAME => 'age', VERSIONS => '1', EVICT_BLOCKS_ON_CLOSE => 'false', NEW_VERSION_BEHAVIOR => 'false', KEEP_DELETED_CELLS => 'FALSE', CACHE_DATA_ON_WRITE => 'false', DATA_BLOC
K_ENCODING => 'NONE', TTL => 'FOREVER', MIN_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', CACHE_INDEX_ON_WRITE => 'false', IN_MEMORY => 'false', CACHE_BL
OOMS_ON_WRITE => 'false', PREFETCH_BLOCKS_ON_OPEN => 'false', COMPRESSION => 'NONE', BLOCKCACHE => 'true', BLOCKSIZE => '65536'}                                            
{NAME => 'name', VERSIONS => '1', EVICT_BLOCKS_ON_CLOSE => 'false', NEW_VERSION_BEHAVIOR => 'false', KEEP_DELETED_CELLS => 'FALSE', CACHE_DATA_ON_WRITE => 'false', DATA_BLO
CK_ENCODING => 'NONE', TTL => 'FOREVER', MIN_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', CACHE_INDEX_ON_WRITE => 'false', IN_MEMORY => 'false', CACHE_B
LOOMS_ON_WRITE => 'false', PREFETCH_BLOCKS_ON_OPEN => 'false', COMPRESSION => 'NONE', BLOCKCACHE => 'true', BLOCKSIZE => '65536'}                                           
2 row(s)
Took 0.1657 seconds 
```






