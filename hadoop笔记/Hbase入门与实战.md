# Hbase入门与实战 

## 1 课程目标

* HBase的引用场景及特点
* HBase的概念与定位
* HBase架构体系与设计模型
* HBase的安装部署
* HBase shell使用

## 2 HBase的应用场景及特点 

### 2.1 HBase能做什么？ 

* 海量数据存储（上百亿行乘以上百万列）
* 准实时查询

### 2.2 举例说明HBase实际业务场景中的应用 

* 交通
* 金融
* 电商
* 移动

### 2.3 HBase 的特点 

* #### 容量大

HBase单表可以有百亿行、百万列，数据矩阵横向和纵向两个维度所支持的数据量都非常具有弹性。

（普通关系型数据库单表不超过五百万行，超过五百行要做封表封库处理。当然单表列不会超过30列，超过30列会被认为设计不合理。）

* #### 面向列 

HBase是面向列的存储和权限控制，并支持独立检索。列式存储，其数据在表中是按照某列存储的，这样在查询只需要少数几个字段的时候，能大大减少读取的数据量。

* #### 多版本 

HBase每一个列的数据存储有多个Version

* #### 稀疏性 

为空的列并不占用存储空间，表可以设计的非常稀疏

* #### 扩展性 

底层依赖与HDFS

* #### 高可靠性 

WAL机制保证了数据写入时不会因为集群异常而导致写入数据丢失：Replication 机制保证了在集群出现严重问题时，数据不会发生丢失或损坏。而且HBase底层使用HDFS ，HDFS本身已有备份。

* #### 高性能 

底层的LSM数据结构和Rowkey有序排列等架构上的独特设计，使得HBase具有非常高的写入性能。region切分、主键索引和缓存机制使得HBase在海量数据下具备一定的随机读取性能，该性能针对Rowkey的查询能够到达毫秒级别。



## 3 HBase d的概念与定位 

![](https://shirukai.gitee.io/images/201711241407_140.png)



### 如何选择合适的HBase版本 ？

官网下载网址：http://mirrors.hust.edu.cn/apache/hbase/

### 认识HBase在Hadoop2.X 生态系统中的定位 

![](https://shirukai.gitee.io/images/201711241414_796.jpg)



## 4 HBase架构体系与设计模型 

### HBase架构体系 

![](https://shirukai.gitee.io/images/201711241417_753.png)



### HBase表结构模型并举例说明 

![](https://shirukai.gitee.io/images/201711241421_124.png)



![](https://shirukai.gitee.io/images/201711241422_360.png)



### HBase数据模型并举例说明 



![](https://shirukai.gitee.io/images/201711241425_806.png)



![](https://shirukai.gitee.io/images/201711241426_573.png)



![](https://shirukai.gitee.io/images/201711241427_972.png)



### HBase表与关系型数据库表结构的对比 

![](https://shirukai.gitee.io/images/201711241429_313.png)



## 5 HBase的安装部署 

### 5.1 zookeeper安装 （hadoop环境，Master主机）

要安装HBase首相要安装zookeeper，在之前的hadoop环境下，我们来安装zookeeper。

#### 5.1.1 下载zookeeper 

官网：http://mirrors.hust.edu.cn/apache/zookeeper/

```
wget http://mirrors.hust.edu.cn/apache/zookeeper/zookeeper-3.5.0-alpha/zookeeper-3.5.0-alpha.tar.gz
```

解压到/usr/lib

```
tar -zxvf zookeeper-3.5.0-alpha.tar.gz -C /usr/lib
```

#### 5.1.2 配置zookeeper 

创建 zoo.cfg文件

```
clientPort=2181
dataDir=/usr/lib/zookeeper-3.5.0-alpha/zkData
syncLimit=5
initLimit=10
tickTime=2000
dynamicConfigFile=/usr/lib/zookeeper-3.5.0-alpha/bin/../conf/zoo.cfg.dynamic

```

#### 5.1.3 在/usr/lib/zookeeper-3.5.0-alpha目录下创建zkData目录 

```
cd /usr/lib/zookeeper-3.5.0-alpha
mkdir zkData
```

#### 5.1.4 将zookeeper分发到另外两台机子上 

```
scp -r /usr/lib/zookeeper-3.5.0-alpha Slave1.Hadoop:/usr/lib
scp -r /usr/lib/zookeeper-3.5.0-alpha Slave2.Hadoop:/usr/lib
```



#### 5.1.5 启动zookeeper 

```
/usr/lib/zookeeper-3.5.0-alpha/bin/zkServer.sh start
```

#### 5.1.6 关闭zookeeper 

```
/usr/lib/zookeeper-3.5.0-alpha/bin/zkServer.sh stop
```

#### 5.1.7 检测zookeeper是否开启 

```
[root@Master conf]# jps
2970 QuorumPeerMain
3022 Jps
```

### 5.2 安装HBase 

#### 5.2.1 下载并解压HBase 

```
wget http://mirror.bit.edu.cn/apache/hbase/1.3.1/hbase-1.3.1-bin.tar.gz
```

解压到/usr/lib下

```
tar -zxvf hbase-1.3.1-bin.tar.gz -C /usr/lib
```



#### 5.2.2 配置HBase 

##### hbase-env.sh 

修改/usr/lib/hbase-1.3.1/conf下的hbase-env.sh文件

```
vim hbase-env.sh
```

修改大约27行JAVA_HOME

```
 export JAVA_HOME=/usr/lib/jdk1.8.0_151
```

将下面两行注释

```
#export HBASE_MASTER_OPTS="$HBASE_MASTER_OPTS -XX:PermSize=128m -XX:MaxPermSize=128m"
#export HBASE_REGIONSERVER_OPTS="$HBASE_REGIONSERVER_OPTS -XX:PermSize=128m -XX:MaxPermSize=128m"
```

修改大约128行值为false

```
export HBASE_MANAGES_ZK=false
```

保存退出

##### hbase-site.xml 

添加如下配置：

```
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://Master.Hadoop:9000/hbase</value>
  </property>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.zookeeper.quorum</name>
    <value>Master.Hadoop,Slave1.Hadoop,Slave2.Hadoop</value>
  </property>
  <property>
    <name>hbase.tmp.dir</name>
    <value>/usr/lib/hbase-1.3.1/data/tmp</value>
  </property>
</configuration>

```

具体配置参考官网 http://hbase.apache.org/book.html#_configuration_files

##### regionservers 

修改 regionservers

添加如下内容，跟hadoop配置slave一样，这里需要配置hbase的regionservers,将regionservers的hostname填到这里。

```
Slave1.Hadoop
Slave2.Hadoop
```



##### 在 /usr/lib/hbase-1.3.1/下创建 data/tmp目录 

```
mkdir -p data/tmp
```



#### 5.2.5 配置环境变量 

```
[root@Master conf]# vim /etc/profile
```

添加如下配置

```
#set HBase
export HBASE_HOME=/usr/lib/hbase-1.3.1
export PATH=$PATH:$HBASE_HOME/bin
```

使配置生效

```
. /etc/profile
```



#### 5.2.4 分发到Slave1和Slave2中 

```
scp -r /usr/lib/hbase-1.3.1 Slave1.Hadoop:/usr/lib
scp -r /usr/lib/hbase-1.3.1 Slave2.Hadoop:/usr/lib
```



#### 5.2.5 启动HBase 

关闭是stop-hbase.sh

```
start-hbase.sh
```

#### 5.2.6 访问 Master.Hadoop:60010 

![](https://shirukai.gitee.io/images/201711241940_995.png)