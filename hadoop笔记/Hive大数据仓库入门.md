# Hive大数据仓库入门 

> 什么是Hiv？

Hive是构建在hadoop HDFS上的一个数据仓库

## 1 数据仓库 

### 1.1基本概念

数据仓库是一个面向主题的、集成的、不可更新的、随时间不变化的数据集合，它用于支持企业活组织的决策分析处理。

### 1.2数据仓库的结构和构建过程 

![](https://shirukai.gitee.io/images/201711210920_648.png)



### 1.3OLTP应用与OLAP应用 

OLTP（On line Transaction Processing）:连接事务处理（银行转账）面向事务

OLAP（On line Analytical Processing）:连接分析处理（商品推荐系统）

### 1.4数据仓库中数据模型 

#### 1.4.1星型模型

![](https://shirukai.gitee.io/images/201711210923_3.png)

#### 1.4.2 雪花模型 

基于星型模型

![](https://shirukai.gitee.io/images/201711210925_508.png)

## 2 Hive 

### 2.1什么是Hive？

* Hive是简历在Hadoop HDFS上的数据仓库基础架构
* Hive可以用来进行数据提取转化加载（ETL）
* Hive定义了简单的类似SQL查询语言，HQL它允许熟悉SQL的用户查询数据
* Hive允许数据MapReduce开发者的开发自动以的mapper和reducer来处理内置的mapper和reducer无法完成的复杂的分析工作。
* Hive是SQL解析引擎，他将SQL语句转移成M/R Job ,然后在Hadoop执行
* Hive的表其实就是HDFS的目录/文件

### 2.2 Hive的体系结构 

#### 2.2.1 Hive的元数据 

* Hive将元数据存储在数据库中（metastore），支持Mysql、derby等数据库，默认的是保存在derby数据库中。
* Hive中的元数据包括表的名字，标的列和分区及其属性，表的属性（是否诶外部表等），表的数据所在目录等

#### 2.2.2 一条HQL语句如何在Hive中进行查询的？ 

解释器、编译器、优化器完成HQL查询语句从词法分析、语法分析、编译、优化以及查询计划（Plan）的生成。生成的查询计划存储在HDFS中，并在随后有MapReduce调用执行

![](https://shirukai.gitee.io/images/201711210936_886.png)

#### 2.2.3Hive具体的体系结构 

![](https://shirukai.gitee.io/images/201711210941_566.png)

## 3 Hive安装

### 3.1 安装模式 

#### 3.1.1嵌入模式

* 元数据信息被存储在Hive自带的Derby数据库中
* 只允许创建一个连接
* 多用于Demo



#### 3.1.2本地模式 

* 元数据信息被存储在MySql数据库中
* mysql数据库与Hive运行在同一台物理机上
* 多用于开发和测试

#### 3.1.3远程模式 

- 元数据信息被存储在MySql数据库中
- mysql数据库与Hive运行不在同一台物理机上



### 3.2 Hive本地模式安装（在hadoop环境下）

下载官网：http://mirrors.hust.edu.cn/apache/hive/hive-2.3.2/

#### 3.2.1 下载Hive 安装文件

```
cd /usr/lib
wget http://mirrors.hust.edu.cn/apache/hive/hive-2.3.2/apache-hive-2.3.2-bin.tar.gz
```

#### 3.2.2 下载Hive 源码文件 

```
wget http://mirrors.hust.edu.cn/apache/hive/hive-2.3.2/apache-hive-2.3.2-src.tar.gz
```

#### 3.2.3 解压

```
tar -zxvf apache-hive-2.3.2-bin.tar.gz
tar -zxvf apache-hive-2.3.2-src.tar.gz
```

#### 3.2.4 配置环境变量 

```
vim /etc/profile
```

添加如下环境变量

```
#set hive
export HIVE_HOME=/usr/lib/apache-hive-2.3.2-bin
export PATH=$HIVE_HOME/bin:$PATH
```

使改变生效

```
. /etc/profile
```

#### 3.2.5 配置数据库 (前提是已经安装好mysql数据库)

切换到配置文件目录

```
cd /usr/lib/apache-hive-2.3.2-bin/conf
```

创建一个hive-site.xml文件,里面是数据库的相关信息，详细配置可以参考官网文档

https://cwiki.apache.org/confluence/display/Hive/AdminManual+MetastoreAdmin#AdminManualMetastoreAdmin-RemoteMetastoreServer

```
<configuration>
        <property>
                <name>javax.jdo.option.ConnectionURL</name>
                <value>jdbc:mysql://localhost/hive?createDatabaseIfNotExist=true</value>
        </property>

        <property>
                <name>javax.jdo.option.ConnectionDriverName</name>
                <value>com.mysql.jdbc.Driver</value>
        </property>


        <property>
                <name>javax.jdo.option.ConnectionUserName</name>
                <value>root</value>
        </property>

        <property>
                <name>javax.jdo.option.ConnectionPassword</name>
                <value>root</value>
        </property>

</configuration>

```

#### 3.2.6 初始化数据库 

```
schematool -dbType mysql -initSchema
```

## 4 Hive的管理 

### 4.1 Hive的启动方式 

* CLI（命令行）方式
* Web界面方式
* 远程服务启动方式



### 4.2 Hive命令行 

```
#进入
hive
#退出
exit;
```

#### 4.2.1 清屏

Ctrl+ L 或者

```
! clear
```

#### 4.2.2 查看数据仓库中的表 

```
show tables;
```

#### 4.2.3 查看数据仓库中内置的函数 

```
show functions;
```

#### 4.2.4 查看表结构 

```
desc 表名
```

#### 4.2.5 查看HDFS上的文件 

```
dfs -ls 目录
```

#### 4.2.6 执行操作系统的命令 

```
! 命令
```

#### 4.2.7 执行HQL语句 

```
select * from ***
```

例如：查询test1中的数据

```
select * from test1;
```

#### 4.2.8 执行SQL的脚本

```
source SQL文件
```

#### 4.2.9 直接在系统命令行运行 

```
hive -e 'show tables';
```

### 4.3 web界面方式(在2.2.0之后已经废除这个功能)

### 4.4 HiveServer2 

#### 4.4.1 什么是HiveServer2 

[HiveServer2](https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Overview)（HS2）是服务器接口，使远程客户端执行对蜂巢的查询和检索结果（更详细的介绍[这里](https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Overview)）。目前基于Thrift RPC的实现是[HiveServer](https://cwiki.apache.org/confluence/display/Hive/HiveServer)的改进版本，支持多客户端并发和身份验证。它旨在为JDBC和ODBC等开放API客户端提供更好的支持。

#### 4.4.2配置 

#### 4.4.3 启动 

```
hiveserver2
```

## 5 Hive 的数据类型 

### 5.1 基本数据类型 

* tinyint/smallint/int/bigint : 整数类型
* float/double : 浮点数类型
* boolean: 布尔类型
* string : 字符串类型

创建一个表

```
hive> create table person
    > (prd int,
    > pname string,
    > married boolean,
    > salary double);
```



查看表结构

```
hive> desc person;
OK
prd                 	int                 	                    
pname               	string              	                    
married             	boolean             	                    
salary              	double              	                    
Time taken: 0.274 seconds, Fetched: 4 row(s)
```

### 5.2 复杂数据类型 

* Array : 数组类型，由一系列相同数据类型的元数据组成
* Map: 集合类型，包含key-value键值对，可以通过key来访问元素
* Struct: 结构类型，可以包含不同数据类型的元素，这些元素可以通过“点语法”的方式来得到所需要的元素

##### Array 

创建表

```
hive> create table student
    > (sid int,
    > sname string,
    > grade array<float>);
OK
Time taken: 0.173 seconds

```

查看表结构

```
hive> desc student
    > ;
OK
sid                 	int                 	                    
sname               	string              	                    
grade               	array<float>        	                    
Time taken: 0.139 seconds, Fetched: 3 row(s)
```

##### Map 

创建表

```
hive> create table student1
    > (sid int,
    > sname string,
    > grade map<string,float>);
OK
Time taken: 9.566 seconds
```

查看表结构

```
hive> desc student1;
OK
sid                 	int                 	                    
sname               	string              	                    
grade               	map<string,float>   	                    
Time taken: 0.349 seconds, Fetched: 3 row(s)

```

##### Struct

创建表

```
hive> create table student4
    > (sid int,
    > info struct<name:string,age:int,sex:string>);
OK
Time taken: 0.178 seconds
```

查看表结构

```
hive> desc student4;
OK
sid                 	int                 	                    
info                	struct<name:string,age:int,sex:string>	                    
Time taken: 0.115 seconds, Fetched: 2 row(s)

```

### 5.3 时间类型

* Date： 从Hvie0.12.0开始支持
* Timestamp：从Hive0.8.0开始支持

## 6 Hive的数据存储 

* 基于HDFS
* 没有专门的数据存储格式
* 存储结构主要包括：数据库、文件、表、视图
* 可以直接加载文本文件（.txt文件等）
* 创建表时，指定Hive数据的列分隔符与行分隔符

### 6.1表

* Table 内部表
* Partition 分区表
* External Table 外部表
* Bucket Table 桶表

### 6.2 视图

### 6.3 内部表 

* 与数据库中的Table 在概念上是类似
* 每一个Table在Hive中都有一个相应的目录存储数据
* 所有的Table数据（不包括 External Table ）都保存在这个目录中
* 删除表时，元数据与数据都会被删除

#### 6.3.1 创建内部表 

不指定位置创建表：

```
hive> create table t1
    > (tid int,tname string,age int);
OK
Time taken: 0.185 seconds
```

如果没有指定位置他会在hdfs中的/user/hive/warehouse中生成一个目录

![](https://shirukai.gitee.io/images/201711222024_673.png)



指定位置创建表：

```
hive> create table t2
    > (tid int, tname string, age int)
    > location '/mytables/t2';
OK
Time taken: 0.162 seconds
```

创建以逗号分隔的表：

```
hive> create table t3
    > (tid int,tname string,age int)
    > row format delimited fields terminated by ',';
OK
Time taken: 8.122 seconds
```

删除表

```
drop table
```

### 6.4 分区表（提高查询效率）

http://blog.csdn.net/skywalker_only/article/details/30224309

* Partition对应于数据库的Partition列的密集索引
* 在HIve中，表中的一个Partition对应于表下的一个目录，所有的Partition的数据都存储在对应的目录中

#### 创建分区表 

```
hive> create table partition_table
    > (sid int, name string)
    > partitioned by (gender string)
    > row format delimited fields terminated by ',';
OK
Time taken: 0.384 seconds
```

#### 查看表结构

```
hive> desc partition_table;
OK
sid                 	int                 	                    
name                	string              	                    
gender              	string              	                    
	 	 
# Partition Information	 	 
# col_name            	data_type           	comment             
	 	 
gender              	string              	                    
Time taken: 0.281 seconds, Fetched: 8 row(s)
```

#### 向表中插入数据 

插入sex为M的数据

```
hive> insert into table partition_table partition(gender='M') select sid,sname from sample_data where sex='M';
```

插入sex为F的数据

```
hive> insert into table partition_table partition(gender='F') select sid,sname from sample_data where sex='F';
```

在HDFS的/user/hive/warehouse/partition_table目录下，会生成两个文件

![](https://shirukai.gitee.io/images/201711230942_344.png)



#### 通过查看执行计划，对比分区表和普通表的查询效率  

普通表查询性别为M的数据

```
hive> explain select * from sample_data where sex='M';
OK
STAGE DEPENDENCIES:
  Stage-0 is a root stage
STAGE PLANS:
  Stage: Stage-0
    Fetch Operator
      limit: -1
      Processor Tree:
        TableScan
          alias: sample_data
          Statistics: Num rows: 1 Data size: 45 Basic stats: COMPLETE Column stats: NONE
          Filter Operator
            predicate: (sex = 'M') (type: boolean)
            Statistics: Num rows: 1 Data size: 45 Basic stats: COMPLETE Column stats: NONE
            Select Operator
              expressions: sid (type: int), sname (type: string), 'M' (type: string)
              outputColumnNames: _col0, _col1, _col2
              Statistics: Num rows: 1 Data size: 45 Basic stats: COMPLETE Column stats: NONE
              ListSink
Time taken: 0.949 seconds, Fetched: 20 row(s)
```

分区表查询性别为M的数据

```
hive> explain select * from partition_table where gender='M';
OK
STAGE DEPENDENCIES:
  Stage-0 is a root stage
STAGE PLANS:
  Stage: Stage-0
    Fetch Operator
      limit: -1
      Processor Tree:
        TableScan
          alias: partition_table
          Statistics: Num rows: 3 Data size: 18 Basic stats: COMPLETE Column stats: NONE
          Select Operator
            expressions: sid (type: int), name (type: string), 'M' (type: string)
            outputColumnNames: _col0, _col1, _col2
            Statistics: Num rows: 3 Data size: 18 Basic stats: COMPLETE Column stats: NONE
            ListSink
Time taken: 0.84 seconds, Fetched: 17 row(s)
```

### 6.5 外部表 

* 指向已经在HDFS中存在的数据，可以创建Partition
* 它和内部表示在元数据的组织上是相同的，而实际数据的存储则有较大的差异
* 外部表只有一个过程，加载数据和创建表同时完成，并不会移动到数据仓库中，知识外部数据建立一个连接。当伤处一个外部表时 ，仅伤处该连接。



#### 6.5.1 创建外部表 

##### 在linux下创建三个文件 

student01.txt

```
[root@Master hadoop_practice]# cat student01.txt
Tom,23
Mary,20
```

student02.txt

```
[root@Master hadoop_practice]# cat student02.txt
Mike,25
```

student03.txt

```
[root@Master hadoop_practice]# cat student03.txt
Scott,21
King,20
```

##### 在hdfs中创建/student目录 

```
[root@Master hadoop_practice]# hdfs dfs -mkdir /student
```

##### 上传文件到hdfs的/student目录下 

```
hdfs dfs -put student01.txt /student
hdfs dfs -put student02.txt /student
hdfs dfs -put student03.txt /student
```

##### 创建外部表 

```
hive> create external table external_student
    > (sname string,age int)
    > row format delimited fields terminated by ','
    > location '/student';
OK
Time taken: 0.187 seconds
```

##### 查看外部表数据 

```
hive> select * from external_student;
OK
Tom	23
Mary	20
Mike	25
Scott	21
King	20
Time taken: 0.699 seconds, Fetched: 5 row(s)
```

### 6.6 桶表

* 桶表是对数据进行哈希取值，然后放到不同文件中存储

#### 创建桶表

```
hive> create table bucket_table
    > (sid int,sname string,age int)
    > clustered by (sname) into 5 buckets;
OK
Time taken: 0.294 seconds

```

### 6.7 视图 

* 视图是一种需表，是一个逻辑概念；可以跨越多张表
* 视图建立在已有表的基础上，视图赖以建立的这些表称为基表
* 视图可以简化复杂的查询

## 总结

数据仓库的基本概念

什么是Hive？Hive的体系结构

Hive的安装和管理

Hive的数据模型