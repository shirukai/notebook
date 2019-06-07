# Hive数据定义语言DDL学习

https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL

## 1 创建/删除/修改/使用数据库

```
CREATE (DATABASE|SCHEMA) [IF NOT EXISTS] database_name
  [COMMENT database_comment]
  [LOCATION hdfs_path]
  [WITH DBPROPERTIES (property_name=property_value, ...)];
```

### 1.1 创建一个简单的数据库

database 跟 schema 作用是一样的。

```
create database newdb;
```

这时候会在hdfs的/user/hive/warehouse目录中生成一个newdb.db目录，在这个数据库中创建的内部表都会存在这个目录。

![](https://shirukai.gitee.io/images/201711301517_202.png)



### 1.2 创建一个指定位置的数据库 （如果目录不存在会自动创建）

> 指定hdfs中的位置为hive数据库的目录位置

创建一个名字为 foreign_path_hiveDB的数据库，指定它的目录为 /hiveLearn/foreign_path_hiveDB

```
create database foreign_path_hiveDB location '/hiveLearn/foreign_path_hiveDB';
```

### 1.3 修改数据库 

```
ALTER (DATABASE|SCHEMA) database_name SET DBPROPERTIES (property_name=property_value, ...);   -- (Note: SCHEMA added in Hive 0.14.0)
 
ALTER (DATABASE|SCHEMA) database_name SET OWNER [USER|ROLE] user_or_role;   -- (Note: Hive 0.13.0 and later; SCHEMA added in Hive 0.14.0)
 
ALTER (DATABASE|SCHEMA) database_name SET LOCATION hdfs_path; -- (Note: Hive 2.2.1, 2.4.0 and later)
```

#### 1.3.1 修改数据库属性 

```
alter database foreign_path_hiveDB set DBPROPERTIES('testName'='testValue');
```

```
0: jdbc:hive2://localhost:10000> show create database foreign_path_hiveDB;
+----------------------------------------------------+
|                   createdb_stmt                    |
+----------------------------------------------------+
| CREATE DATABASE `foreign_path_hivedb`              |
| LOCATION                                           |
|   'hdfs://Master.Hadoop:9000/hiveLearn/foreign_path_hiveDB' |
| WITH DBPROPERTIES (                                |
|   'testName'='testValue')                          |
+----------------------------------------------------+
```

#### 1.3.2 修改数据库所有者和角色 

```
ALTER (DATABASE|SCHEMA) database_name SET OWNER [USER|ROLE] user_or_role;   -- (Note: Hive 0.13.0 and later; SCHEMA added in Hive 0.14.0)
```

### 1.4 修改数据库目录位置 

ALTER DATABASE ……SET LOCATION 语句不会讲数据库当前目录的内容移动到新指定的位置，它不会更改与指定数据库下的任何表/分区关联的位置。它只会改变默认的父目录，这个数据库将会添加新的表格，这种行为（应该是2.4.0之后才可以使用）

```
ALTER (DATABASE|SCHEMA) database_name SET LOCATION hdfs_path; -- (Note: Hive 2.2.1, 2.4.0 and later)
```

### 1.5 删除数据库

```
0: jdbc:hive2://localhost:10000> drop database whatisschema;
No rows affected (0.588 seconds)
```



### 1.6 查看所有数据库 

```
0: jdbc:hive2://localhost:10000> show databases;
+----------------------+
|    database_name     |
+----------------------+
| default              |
| foreign_path_hivedb  |
| newdb                |
+----------------------+
3 rows selected (0.337 seconds)
```

### 1.7 使用数据库 

```
use newdb;
```

### 1.8 查看当前使用的数据库 

```
 select current_database();
```

## 2 创建/删除/截断表 

### 2.1 创建表格

```
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name    -- (Note: TEMPORARY available in Hive 0.14.0 and later)
  [(col_name data_type [COMMENT col_comment], ... [constraint_specification])]
  [COMMENT table_comment]
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)] --(将字段设置为分区)
  [CLUSTERED BY (col_name, col_name, ...) [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS] --(CLUSTERED BY按哪个字段分桶，SORTED BY按照哪个字段排序，升序or降序，INTO放进几个桶里)
  [SKEWED BY (col_name, col_name, ...)                  -- (Note: Available in Hive 0.10.0 and later)]
     ON ((col_value, col_value, ...), (col_value, col_value, ...), ...)
     [STORED AS DIRECTORIES]
  [
   [ROW FORMAT row_format] 
   [STORED AS file_format]
     | STORED BY 'storage.handler.class.name' [WITH SERDEPROPERTIES (...)]  -- (Note: Available in Hive 0.6.0 and later)
  ]
  [LOCATION hdfs_path]
  [TBLPROPERTIES (property_name=property_value, ...)]   -- (Note: Available in Hive 0.6.0 and later)
  [AS select_statement];   -- (Note: Available in Hive 0.5.0 and later; not supported for external tables)
 
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name
  LIKE existing_table_or_view_name
  [LOCATION hdfs_path];
 
data_type
  : primitive_type
  | array_type
  | map_type
  | struct_type
  | union_type  -- (Note: Available in Hive 0.7.0 and later)
 
primitive_type
  : TINYINT
  | SMALLINT
  | INT
  | BIGINT
  | BOOLEAN
  | FLOAT
  | DOUBLE
  | DOUBLE PRECISION -- (Note: Available in Hive 2.2.0 and later)
  | STRING
  | BINARY      -- (Note: Available in Hive 0.8.0 and later)
  | TIMESTAMP   -- (Note: Available in Hive 0.8.0 and later)
  | DECIMAL     -- (Note: Available in Hive 0.11.0 and later)
  | DECIMAL(precision, scale)  -- (Note: Available in Hive 0.13.0 and later)
  | DATE        -- (Note: Available in Hive 0.12.0 and later)
  | VARCHAR     -- (Note: Available in Hive 0.12.0 and later)
  | CHAR        -- (Note: Available in Hive 0.13.0 and later)
 
array_type
  : ARRAY < data_type >
 
map_type
  : MAP < primitive_type, data_type >
 
struct_type
  : STRUCT < col_name : data_type [COMMENT col_comment], ...>
 
union_type
   : UNIONTYPE < data_type, data_type, ... >  -- (Note: Available in Hive 0.7.0 and later)
 
row_format
  : DELIMITED [FIELDS TERMINATED BY char [ESCAPED BY char]] [COLLECTION ITEMS TERMINATED BY char]
        [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
        [NULL DEFINED AS char]   -- (Note: Available in Hive 0.13 and later)
  | SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, property_name=property_value, ...)]
 
file_format:
  : SEQUENCEFILE
  | TEXTFILE    -- (Default, depending on hive.default.fileformat configuration)
  | RCFILE      -- (Note: Available in Hive 0.6.0 and later)
  | ORC         -- (Note: Available in Hive 0.11.0 and later)
  | PARQUET     -- (Note: Available in Hive 0.13.0 and later)
  | AVRO        -- (Note: Available in Hive 0.14.0 and later)
  | INPUTFORMAT input_format_classname OUTPUTFORMAT output_format_classname
 
constraint_specification:
  : [, PRIMARY KEY (col_name, ...) DISABLE NOVALIDATE ]
    [, CONSTRAINT constraint_name FOREIGN KEY (col_name, ...) REFERENCES table_name(col_name, ...) DISABLE NOVALIDATE 
```



### 2.2 存储格式

| Storage Format               | Description                              |
| ---------------------------- | ---------------------------------------- |
| STORED AS TEXTFILE           | 存储为纯文本，TEXTFILE是默认的文件格式，除非配置参数hive.default.fileformat |
| STORED AS SEQUENCEFILE       | 存储为压缩序列文件                                |
| STORED AS ORC                | 存储为ORC文件格式，支持ACID事务和基于成本的优化器。存储列级元素。     |
| STORED AS PARQUET            | 以Parquet列存储格式存储为Parquet格式                |
| STORED AS AVRO               | 存储为Avro格式                                |
| STORED AS RCFILE             | 存储为记录列文件格式                               |
| STORED BY                    | 以非本地表格式存储，创建或连接到非本地表，例如HIBase，Druid或Accumulo支持的表 |
| INPUTFORMAT and OUTPUTFORMAT | 在file_format中指定一个相应的InputFormat和OutputFormat类的名字作为一个字符串。 |



### 2.3 分区表 

可以使用PARTITIONED BY 子句创建分区表，一个表可以有一个或多个分区列，并为分区列中的每个不同的值组合创建单独的数据目录。此外可以使用   CLUSTERED BY 列   将表或分区分区，并且可以通过   SORT BY 列    在该分区内对数据进行排序，这可以提高某些查询的性能。

如果在创建表的时候出现："FAILED: Error in semantic analysis: Column repeated in partitioning columns," 这个错误，这意味着我们尝试去创建的分区列在之前已经出现过了。

#### 2.3.1 作用 

分区是hive在处理大型表时常用的方法。分区（partition）在hive的物理存储中，体现为表名下的某个目录（按列分区），这个目录下存储着这个分区下对应的数据。分区的好处在于缩小查询扫描范围，从而提高速度。

#### 2.3.2 动态分区、静态分区 

分区分为两种：静态分区static partition和动态分区dynamic partition。静态分区和动态分区的区别在于导入数据时，是手动输入分区名称，还是通过数据来判断数据分区。对于大数据批量导入来说，显然采用动态分区更为简单方便。

创建一个分区表 

```
CREATE TABLE page_view(viewTime INT, userid BIGINT,
     page_url STRING, referrer_url STRING,
     ip STRING COMMENT 'IP Address of the User')
 COMMENT 'This is the page view table'
 PARTITIONED BY(dt STRING, country STRING)
 STORED AS SEQUENCEFILE;
```

#### 2.3.3 静态分区

##### 设置开启静态分区 

```
0: jdbc:hive2://localhost:10000> set hvie.exec.dynamic.partition=false;
```

##### 创建静态分区表 

```
0: jdbc:hive2://localhost:10000> create table static_par_tab (name string,nation string) partitioned by (sex string) row format delimited fields terminated by ",";
```

##### 查看表结构 

```
0: jdbc:hive2://localhost:10000> desc static_par_tab;
+--------------------------+-----------------------+-----------------------+
|         col_name         |       data_type       |        comment        |
+--------------------------+-----------------------+-----------------------+
| name                     | string                |                       |
| nation                   | string                |                       |
| sex                      | string                |                       |
|                          | NULL                  | NULL                  |
| # Partition Information  | NULL                  | NULL                  |
| # col_name               | data_type             | comment               |
|                          | NULL                  | NULL                  |
| sex                      | string                |                       |
+--------------------------+-----------------------+-----------------------+
8 rows selected (0.81 seconds)
```

##### 准备本地数据文件par_tab.txt 内容是姓名+逗号+国籍，将以性别作为分区 假设这些人的性别都是man

```
jan,china
mary,america
lilei,china
yiku,japan
emoji,japan
```

##### load 本地数据到静态分区表 

```
0: jdbc:hive2://localhost:10000> load data local inpath '/root/hiveTest/par_tab.txt' into table static_par_tab partition (sex='man');
No rows affected (2.011 seconds)
```

##### 查看表数据 

```
0: jdbc:hive2://localhost:10000> select * from static_par_tab;
+----------------------+------------------------+---------------------+
| static_par_tab.name  | static_par_tab.nation  | static_par_tab.sex  |
+----------------------+------------------------+---------------------+
| jan                  | china                  | man                 |
| mary                 | america                | man                 |
| lilei                | china                  | man                 |
| yiku                 | japan                  | man                 |
| emoji                | japan                  | man                 |
+----------------------+------------------------+---------------------+
5 rows selected (2.07 seconds)
```

我们load的数据是两列，加到分区表中后变成了三列。

##### hdfs变化 

查看分区表在hdfs中的目录，可以看出，生成了一个名字为sex=man的目录，里面存放的是我们刚刚load上去的数据。

![](https://shirukai.gitee.io/images/201712130927_498.png)

##### 再准备本地数据 par_tab1.txt，内容如下，假设这些人的性别都为woman 

```
lily,china
nancy,china
cls,japan
```

##### load以上数据到分区表中 

```
0: jdbc:hive2://localhost:10000> load data local inpath '/root/hiveTest/par_tab1.txt' into table static_par_tab partition (sex='woman');
No rows affected (1.124 seconds)
```

##### 查看表数据 

```
0: jdbc:hive2://localhost:10000> select * from static_par_tab;
+----------------------+------------------------+---------------------+
| static_par_tab.name  | static_par_tab.nation  | static_par_tab.sex  |
+----------------------+------------------------+---------------------+
| jan                  | china                  | man                 |
| mary                 | america                | man                 |
| lilei                | china                  | man                 |
| yiku                 | japan                  | man                 |
| emoji                | japan                  | man                 |
| lily                 | china                  | woman               |
| nancy                | china                  | woman               |
| cls                  | japan                  | woman               |
+----------------------+------------------------+---------------------+
8 rows selected (0.395 seconds)
```

这时候会发现，表中的多了三行数据，并且数据的sex列都为woman

##### hdfs变化 

可以看出，hdfs目录下又生成了一个新目录 sex=woman

![](https://shirukai.gitee.io/images/201712130936_842.png)



#### 创建多列分区 

##### 上面创建的是以sex这一列分区的表，下面我们来创建以sex 和data分区的表 

```
0: jdbc:hive2://localhost:10000> create table static_par_tb_muilt (name string,nation string) partitioned by (sex string,dat string) row format delimited fields terminated by ",";
No rows affected (0.288 seconds)
```

##### 查看表结构 

```
0: jdbc:hive2://localhost:10000> desc static_par_tb_muilt;
+--------------------------+-----------------------+-----------------------+
|         col_name         |       data_type       |        comment        |
+--------------------------+-----------------------+-----------------------+
| name                     | string                |                       |
| nation                   | string                |                       |
| sex                      | string                |                       |
| dat                      | string                |                       |
|                          | NULL                  | NULL                  |
| # Partition Information  | NULL                  | NULL                  |
| # col_name               | data_type             | comment               |
|                          | NULL                  | NULL                  |
| sex                      | string                |                       |
| dat                      | string                |                       |
+--------------------------+-----------------------+-----------------------+
10 rows selected (0.378 seconds)
```

##### load之前创建好的本地数据 

```
jan,china
mary,america
lilei,china
yiku,japan
emoji,japan
```

设置性别分区为man，dat 为2017-12-12

```
0: jdbc:hive2://localhost:10000> load data local inpath '/root/hiveTest/par_tab.txt' into table static_par_tb_muilt partition (sex='man',dat='2017-12-12');
No rows affected (1.392 seconds)
```



```
lily,china
nancy,china
cls,japan
```

设置性别分区为woman，dat 为2017-12-11

![](https://shirukai.gitee.io/images/201712130955_432.png)

##### 查看hdfs变化 

![](https://shirukai.gitee.io/images/201712130956_597.png)

同样在表目录下又生成了两个目录 sex=man 和sex=woman,但是请注意了，我们不是创建了两个分区列吗，怎么就生成了sex目录，那dat目录去哪了？

![](https://shirukai.gitee.io/images/201712130958_137.png)

发现了吗，在每个sex目录下都会生成一个dat目录。

可见，新建表时定义的分区顺序partitioned by (sex string,dat string) ，决定了hdfs中目录顺序（排在前面的为父目录，后面的为子目录。正是有了这个层级关系，当我们查询性别为man的数据时，man目录下所有日期下的所有数据都会被查询到。而如果我们查询日期dat的时候，无论是man目录、还是womam目录，只要包含这个时间段的数据都会被查询出来。

#### 2.3.4 动态分区 

通过上面的静态分区的创建和数据导入，我们发现，每次导入数据的时候都要手动去设置将数据导入到哪个分区，有几个分区，我们既要load几次。显然是很麻烦的，那能不能只load一次，根据要load的数据，来判断我要把数据放到哪个分区里？答案是可以的，这就需要动态分区。

##### 设置启用动态分区

```
0: jdbc:hive2://localhost:10000> set hvie.exec.dynamic.partition=true;
No rows affected (0.026 seconds)
```

##### 创建动态分区表 

```
0: jdbc:hive2://localhost:10000> create table dynamic_par_tb (name string,nation string) partitioned by (sex string) row format delimited fields terminated by ",";
No rows affected (0.367 seconds)
```

##### load 本地数据到分区表 

本地数据如下

```
jan,china,man
mary,america,woman
lilei,china,man
yiku,japan,woman
emoji,japan,woman
```

结果发现，如果用load方法像表中插入数据时，必须要指定分区的，不会自动去分配分区的。

##### insert……select插入数据 

下面我们来用insert……select语句来插入数据

```
insert into table dynamic_par_tb partition(sex) select name,nation,sex from static_par_tab;
```

发现报错

```
Error: Error while compiling statement: FAILED: SemanticException [Error 10096]: Dynamic partition strict mode requires at least one static partition column. To turn this off set hive.exec.dynamic.partition.mode=nonstrict (state=42000,code=10096)
```

hive的hive.exec.dynamic.partition.mode这个属性默认是strict，即不允许分区列全部是动态的，这是为了防止用户有可能只愿意在自分区内进行动态建分区，但是由于疏忽忘记为主分区列指定值了，这将导致一个dml语句在短时间内创建大量的新的分区（对应大量新的文件夹），对系统性能带来影响。

为了使语句能执行，我们需要设置

```
set hive.exec.dynamic.partition.mode=nonstrict
```

##### 查看数据 

```
0: jdbc:hive2://localhost:10000> select * from dynamic_par_tb;
+----------------------+------------------------+---------------------+
| dynamic_par_tb.name  | dynamic_par_tb.nation  | dynamic_par_tb.sex  |
+----------------------+------------------------+---------------------+
| jan                  | china                  | man                 |
| mary                 | america                | man                 |
| lilei                | china                  | man                 |
| yiku                 | japan                  | man                 |
| emoji                | japan                  | man                 |
| lily                 | china                  | woman               |
| nancy                | china                  | woman               |
| cls                  | japan                  | woman               |
+----------------------+------------------------+---------------------+
8 rows selected (0.269 seconds)

```



##### hdfs变化 

![](https://shirukai.gitee.io/images/201712131051_106.png)

并且在每个目录下会生成一个经过MapReduce后生成的文件。

![](https://shirukai.gitee.io/images/201712131052_55.png)

#### 2.3.5分区操作 

http://blog.csdn.net/skywalker_only/article/details/30224309

##### 新增分区

新增分区可以新增一个空的分区，指定分区名即可，这时会在hdfs对应的表目录下创建相应的目录。

也可以新增一个有数据的分区，比如我们在/hivetest/gender=S下存放着数据，我们需要把它加到表t_partition中分区名为gender=S里，在添加分区的时候，指定目录即可。

如：

先查看表t_partition的表结构

```
0: jdbc:hive2://localhost:10000> desc partition_table;
+--------------------------+-----------------------+-----------------------+
|         col_name         |       data_type       |        comment        |
+--------------------------+-----------------------+-----------------------+
| sid                      | int                   |                       |
| name                     | string                |                       |
| gender                   | string                |                       |
|                          | NULL                  | NULL                  |
| # Partition Information  | NULL                  | NULL                  |
| # col_name               | data_type             | comment               |
|                          | NULL                  | NULL                  |
| gender                   | string                |                       |
+--------------------------+-----------------------+-----------------------+
```

可以看出这个表的分区列为gender。

查看这个表的分区

```
0: jdbc:hive2://localhost:10000> show partitions partition_table;
+------------+
| partition  |
+------------+
| gender=F   |
| gender=M   |
+------------+
2 rows selected (0.229 seconds)
```

hdfs 目录

![](https://shirukai.gitee.io/images/201711290942_424.png)

##### 现在我们需要新增一个分区gender=S，空分区无数据。

```
0: jdbc:hive2://localhost:10000> alter table partition_table add partition(gender='S');
No rows affected (0.252 seconds)
```

查看表的分区

```
0: jdbc:hive2://localhost:10000> show partitions partition_table;
+------------+
| partition  |
+------------+
| gender=F   |
| gender=M   |
| gender=S   |
+------------+
3 rows selected (0.313 seconds)
```

查看对应的hdfs目录

![](https://shirukai.gitee.io/images/201711290945_209.png)

添加本地数据到新建分区

> 在添加分区之前，我们需要查看一下表是以什么分割的，这样我们才能插入固定的格式。

```
0: jdbc:hive2://localhost:10000> show create table partition_table;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `partition_table`(                    |
|   `sid` int,                                       |
|   `name` string)                                   |
| PARTITIONED BY (                                   |
|   `gender` string)                                 |
| ROW FORMAT SERDE                                   |
|   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  |
| WITH SERDEPROPERTIES (                             |
|   'field.delim'=',',                               |
|   'serialization.format'=',')                      |
| STORED AS INPUTFORMAT                              |
|   'org.apache.hadoop.mapred.TextInputFormat'       |
| OUTPUTFORMAT                                       |
|   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' |
| LOCATION                                           |
|   'hdfs://Master.Hadoop:9000/user/hive/warehouse/partition_table' |
| TBLPROPERTIES (                                    |
|   'transient_lastDdlTime'='1511398771')            |
```

通过上面的信息，我们可以知道当前表之间的数据是以“，”分割。所所以我们在linux本地新建一个文本文件，然后按照表结构创建数据如下：

/root/testpartition.txt

```
22,shirukai
```

然后我们将本地数据load到新建分区里

```
load data local inpath '/root/testpartition.txt' into table partition_table partition(gender='S');
```

查看数据

```
0: jdbc:hive2://localhost:10000> select * from partition_table;
+----------------------+-----------------------+-------------------------+
| partition_table.sid  | partition_table.name  | partition_table.gender  |
+----------------------+-----------------------+-------------------------+
| 2                    | Mary                  | F                       |
| 5                    | Mike                  | F                       |
| 1                    | Tom                   | M                       |
| 3                    | Jerry                 | M                       |
| 4                    | Rose                  | M                       |
| 22                   | shirukai              | S                       |
+----------------------+-----------------------+-------------------------+
6 rows selected (0.312 seconds)
```

可以看出我们新数据已经存在新建分区了。

##### 删除分区

删除分区，会将我们的元数据、以及hdfs文件中的数据一起删除。

```
0: jdbc:hive2://localhost:10000> alter table partition_table drop partition(gender='S');
No rows affected (0.316 seconds)
```

![](https://shirukai.gitee.io/images/201711291011_47.png)

hdfs中的数据也被删除了。

##### 现在我们要新建一个分区，并将hdfs中已经存在的一个目录，及里面的数据加载到这个表分区里

首先需要在hdfs中创建一个目录，然后将数据文件上传到这个目录里。

如我们要新建一个分区，名字为gender=W  数据是hdfs中的/hivetest/gender=W目录下的数据文件。

具体操作：

1 在linux下创建一个gender=w.txt文件

```
22,test1
23,test2
24,test3
```

2 将文件传到hdfs的/hivetest/gender=W目录下

创建目录

```
hdfs dfs -mkdir -p /hivetest/gender=W
```

上传文件

```
hdfs dfs -put /root/gender\=w.txt /hivetest/gender=W
```

3 为partition_table表创建分区，并指定目录/hivetest/gender=W

```
0: jdbc:hive2://localhost:10000> alter table partition_table add partition(gender='W') location '/hivetest/gender=W';
No rows affected (0.22 seconds)
```

4 查看分区

```
0: jdbc:hive2://localhost:10000> show partitions partition_table;
+------------+
| partition  |
+------------+
| gender=F   |
| gender=M   |
| gender=W   |
+------------+
3 rows selected (0.234 seconds)
```

5 查看数据

```
0: jdbc:hive2://localhost:10000> select * from partition_table;
+----------------------+-----------------------+-------------------------+
| partition_table.sid  | partition_table.name  | partition_table.gender  |
+----------------------+-----------------------+-------------------------+
| 2                    | Mary                  | F                       |
| 5                    | Mike                  | F                       |
| 1                    | Tom                   | M                       |
| 3                    | Jerry                 | M                       |
| 4                    | Rose                  | M                       |
| 22                   | test1                 | W                       |
| 23                   | test2                 | W                       |
| 24                   | test3                 | W                       |
+----------------------+-----------------------+-------------------------+
8 rows selected (0.51 seconds)
```

6 删除分区

这时，我们删除分区。删除表中元数据并将hdfs中/hivetest目录下的gender=W目录以及内容给删除

```
0: jdbc:hive2://localhost:10000> alter table partition_table drop partition(gender='W');
No rows affected (0.396 seconds)
```

##### 重命名分区

```
0: jdbc:hive2://localhost:10000> alter table partition_table partition(gender='M') rename to partition(gender='S');
No rows affected (0.57 seconds)
```



### 2.4 外部表 

EXTERNAL关键字允许您创建一个表并提供LOCATION，以便Hive不使用此表的默认位置。如果您已经有数据生成，这个就派上用场了。删除EXTERNAL表时，表中的数据*不会*从文件系统中删除。

EXTERNAL表指向任何HDFS存储位置，而不是存储在由配置属性指定的文件夹中`hive.metastore.warehouse.dir`。

#### 2.4.1 创建外部表  

比如我在hdfs上hiveLearn目录下有个 student的目录，目录里存放着如下格式的文件

1.txt

```
201457507201,student1,18,01
201457507202,student2,19,01
201457507203,student3,18,02
```

2.txt

```
201457507204,student3,18,01
201457507205,student4,19,01
201457507206,student5,18,02
```

现在我们创建一个名字为student的外部表，表结构包括 sno int, sname string, sage int, sex int

```
create external table student
(sno bigint,
sname string,
sage int,
sex string) 
row format delimited fields terminated by ',' 
stored as textfile
location '/hiveLearn/student';
```

用关键字location来指向hdfs中的存储位置。

查询表数据

```
0: jdbc:hive2://localhost:10000> select * from student;
+---------------+----------------+---------------+--------------+
|  student.sno  | student.sname  | student.sage  | student.sex  |
+---------------+----------------+---------------+--------------+
| 201457507201  | student1       | 18            | 01           |
| 201457507202  | student2       | 19            | 01           |
| 201457507203  | student3       | 18            | 02           |
| 201457507204  | student3       | 18            | 01           |
| 201457507205  | student4       | 19            | 01           |
| 201457507206  | student5       | 18            | 02           |
+---------------+----------------+---------------+--------------+
6 rows selected (0.535 seconds)
```

####  2.4.2 通过查询别的表的数据来创建一个新表（CTAS）（结构、数据都复制）

也可以通过在一个create-table-as-select（CTAS）语句中查询的结果来创建和填充表。由CTAS创建的表是原子的，这意味着在填充所有查询结果之前，表不会被其他用户看到。所以其他用户将会看到带有完整查询结果的表格，或根本看不到表格。

在CTAS中有两个部分，SELECT部分可以是HiveQL支持的任何[SELECT语句](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Select)。CTAS的CREATE部分从SELECT部分获取生成的模式，并使用其他表格属性（如SerDe和存储格式）创建目标表。

CTAS有这些限制：

- 目标表不能是分区表。
- 目标表不能是外部表。
- 目标表不能是列表分段表。


##### 例如我要创建一个学生表student2  

要将每个人的学号+10 ，然后修改每个学生名为goodSD1、goodSD2……，如果为sex如果为01改为girl，02改为boy。

```
create table student2 
stored as textfile 
as 
select 
sno+10 sno,
concat('goodSD',
substr(sname,8,1))sname,
sage,
case sex when'01'then'girl' else 'boy' end as sex 
from student 
sort by sno,sname,sage,sex;
```

查看新创建的表

```
0: jdbc:hive2://localhost:10000> select * from student2;
+---------------+-----------------+----------------+---------------+
| student2.sno  | student2.sname  | student2.sage  | student2.sex  |
+---------------+-----------------+----------------+---------------+
| 201457507211  | goodSD1         | 18             | girl          |
| 201457507212  | goodSD2         | 19             | girl          |
| 201457507213  | goodSD3         | 18             | boy           |
| 201457507214  | goodSD3         | 18             | girl          |
| 201457507215  | goodSD4         | 19             | girl          |
| 201457507216  | goodSD5         | 18             | boy           |
+---------------+-----------------+----------------+---------------+
6 rows selected (0.35 seconds)
```

#### 2.4.3 用like新建表 （只复制表结构，不复制表数据）

创建一个新表student3，表结构与student一样

````
0: jdbc:hive2://localhost:10000> create table student3 like student;
No rows affected (0.261 seconds)
````

表结构

```
0: jdbc:hive2://localhost:10000> desc student3;
+-----------+------------+----------+
| col_name  | data_type  | comment  |
+-----------+------------+----------+
| sno       | bigint     |          |
| sname     | string     |          |
| sage      | int        |          |
| sex       | string     |          |
+-----------+------------+----------+
4 rows selected (0.383 seconds)
```

### 2.5 桶表

桶表是对数据进行哈希取值，然后放到不同文件中存储。

数据加载到桶表时，会对字段取hash值，然后与桶的数量取模。把数据放到对应的文件中。
物理上，每个桶就是表(或分区）目录里的一个文件，一个作业产生的桶(输出文件)和reduce任务个数相同

####  2.5.1 作用：

桶表专门用于抽样查询，是很专业性的，不是日常用来存储数据的表，需要抽样查询时，才创建和使用桶表。

#### 2.5.2  首先创建表格

```
create table bucket_t1
(id string)
clustered by (id) 
sorted by (id) 
into 10 buckets;
```

clustered by ：以哪个字段分桶，对id进行哈希取值

sorted by： 按照id字段排序

into10 buckets：分到10 个桶里。

#### 2.5.3 插入数据

这里有两种方式插入数据，一种是查询别的表，将数据放到创建的桶表里。另一种是直接load数据来，sqoop数据可以嘛？待测试。



##### a 利用insert-select 进行插入

首先创建一个number_tb的普通内部表，然后load本地数据（本地数据是999条随机数）

```
create table number_tb(id string);
load data local inpath'/root/hiveTest/number.txt' into table number_tb;
```

查询number_tb中的数据，并将数据插入到 桶表 bucket_t1中

```
insert overwrite table bucket_t1 select id from number_tb;
```

这时候会开启MapReduce任务。Reducer个数为表的桶数

并且在 bucket_t1桶表hdfs目录下会产生10个数据文件，如图：

![](https://shirukai.gitee.io/images/201711302044_593.png)

##### b 直接load data 

我们再创建一个桶表 名字为 bucket_t2

```
reate table bucket_t2(id string) clustered by (id) sorted by (id) into 10 buckets;
```



直接load本地数据会怎样？

```
0: jdbc:hive2://localhost:10000> load data local inpath '/root/hiveTest/number.txt' into table bucket_t2;
Error: Error while compiling statement: FAILED: SemanticException Please load into an intermediate table and use 'insert... select' to allow Hive to enforce bucketing. Load into bucketed tables are disabled for safety reasons. If you know what you are doing, please sethive.strict.checks.bucketing to false and that hive.mapred.mode is not set to 'strict' to proceed. Note that if you may get errors or incorrect results if you make a mistake while using some of the unsafe features. (state=42000,code=40000)

```

错误提示我们用insert...select方法去load data到bucket 表里。 所以现在不允许我们去load data 到桶表里了。不过人家也告诉我们了，如果我们真的想要LOAD data数据到桶表，可以设置strict.checks.bucketing to false

```
set hive.strict.checks.bucketing = false;
```

然后我们再load数据

```
load data local inpath '/root/hiveTest/number.txt' into table bucket_t2;
```

![](https://shirukai.gitee.io/images/201711302113_593.png)

在hdfs中对应的表数据目录下只有一个文件，并没有对数据进行分桶，所以这种插入数据的方法是错误的，官网默认也是不允许的。

那么sqoop数据可以吗？我们来测试一下。 经测试sqoop方法是不可以的。

### 2.6 倾斜表 Skewed Tables 

此功能可用于提高一列或多列具有[倾斜](https://cwiki.apache.org/confluence/display/Hive/Skewed+Join+Optimization)值的表的性能。通过指定经常出现的值（严重偏斜），Hive会自动将它们分割成单独的文件（或[列表](https://cwiki.apache.org/confluence/display/Hive/ListBucketing)中的[目录](https://cwiki.apache.org/confluence/display/Hive/ListBucketing)），并在查询期间考虑到这一点，以便跳过或包含整个文件（或目录的情况下[列表桶装](https://cwiki.apache.org/confluence/display/Hive/ListBucketing)），如果可能的话。

#### 创建倾斜表 

```
0: jdbc:hive2://localhost:10000> create table list_bucket_multiple(col1 string,col2 int,col3 string)
. . . . . . . . . . . . . . . .> skewed by (col1,col2) on (('s1',1),('s3',3),('s13',13),('s79',79));
```

### 2.7 临时表 

已经创建为临时表的表格只对当前会话可见。数据将存储在用户的暂存目录中，并在会话结束时被删除。

如果使用数据库中已存在的永久表的数据库/表名创建临时表，那么在该会话中，对该表的任何引用都将解析为临时表，而不是永久表。用户将无法访问该会话中的原始表，而不会删除临时表或将其重命名为非冲突的名称。

临时表具有以下限制：

- 分区列不受支持。
- 不支持创建索引



创建临时表 

```
create temporary table tmp_tb (key string,value string);
```

查看表结构

````
0: jdbc:hive2://localhost:10000> show create table tmp_tb;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TEMPORARY TABLE `tmp_tb`(                   |
|   `key` string,                                    |
|   `value` string)                                  |
| ROW FORMAT SERDE                                   |
|   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  |
| STORED AS INPUTFORMAT                              |
|   'org.apache.hadoop.mapred.TextInputFormat'       |
| OUTPUTFORMAT                                       |
|   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' |
| LOCATION                                           |
|   'hdfs://Master.Hadoop:9000/tmp/hive/root/4a5b13c3-6210-473a-963c-6355e45d04bf/_tmp_space.db/965fb4c8-dc6d-4a45-b7a1-05b79c6054bb' |
| TBLPROPERTIES (                                    |
| )                                                  |
+----------------------------------------------------+
13 rows selected (0.071 seconds)

````

 可以看出，表属性中的LOCATION指向的是hdfs中的一个临时文件。

### 2.8 约束

#### 2.8.1 主键约束 

```
0: jdbc:hive2://localhost:10000> create table pk(id1 integer,id2 integer,primary key (id1,id2) disable novalidate);
No rows affected (0.393 seconds)
```

#### 2.8.2 外键约束 

```
0: jdbc:hive2://localhost:10000> create table fk(id1 integer, id2 integer,
. . . . . . . . . . . . . . . .>   constraint c1 foreign key(id1, id2) references pk(id2, id1) disable novalidate);
No rows affected (0.278 seconds)
```

#### 2.9 删除表 

```
DROP TABLE [IF EXISTS] table_name [PURGE];     -- (Note: PURGE available in Hive 0.14.0 and later)
```

DROP TABLE删除此表的元数据和数据。如果配置了垃圾箱（并且未指定PURGE），则实际将数据移至.Trash / Current目录。元数据完全丢失。

删除EXTERNAL表时，表中的数据*不会*从文件系统中删除。

删除视图引用的表时，不会给出任何警告（视图将被视为无效，并且必须由用户删除或重新创建）。

否则，表格信息将从Metastore中删除，原始数据将被删除，就像“hadoop dfs -rm”一样。在许多情况下，这会导致表数据被移动到其主目录中用户的.Trash文件夹中; 错误地使用DROP TABLE的用户可以通过重新创建具有相同模式的表来恢复其丢失的数据，重新创建任何必要的分区，然后使用Hadoop手动将数据移回原位。这个解决方案随着时间的推移或者在安装过程中可能会发生变化，因为它依赖于底层实现。强烈建议用户不要反复丢弃表格

## 3 修改表 /分区 /列 

###  3.1 修改表 

#### 3.1.1 重命名表

```
ALTER TABLE table_name RENAME TO new_table_name;
```

例如：将test表重名名为test1

```
0: jdbc:hive2://localhost:10000> alter table test rename to test1;
No rows affected (0.519 seconds)
```

#### 3.1.2 修改表的属性 

```
ALTER TABLE table_name SET TBLPROPERTIES table_properties;
 
table_properties:
  : (property_name = property_value, property_name = property_value, ... )
```

您可以使用此语句将您自己的元数据添加到表中。目前last_modified_user，last_modified_time属性是由Hive自动添加和管理的。用户可以将自己的属性添加到此列表中。你可以做DESCRIBE EXTENDED TABLE来获得这个信息。

```
0: jdbc:hive2://localhost:10000> desc extended test1;
+-----------------------------+----------------------------------------------------+----------+
|          col_name           |                     data_type                      | comment  |
+-----------------------------+----------------------------------------------------+----------+
| id                          | int                                                |          |
| name                        | string                                             |          |
|                             | NULL                                               | NULL     |
| Detailed Table Information  | Table(tableName:test1, dbName:foreign_path_hivedb, owner:root, createTime:1513143808, lastAccessTime:0, retention:0, sd:StorageDescriptor(cols:[FieldSchema(name:id, type:int, comment:null), FieldSchema(name:name, type:string, comment:null)], location:hdfs://Master.Hadoop:9000/hiveLearn/foreign_path_hiveDB/test1, inputFormat:org.apache.hadoop.hive.ql.io.orc.OrcInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat, compressed:false, numBuckets:2, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.ql.io.orc.OrcSerde, parameters:{serialization.format=1}), bucketCols:[id], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), partitionKeys:[], parameters:{last_modified_time=1513236181, totalSize=1753, numRows=0, rawDataSize=0, numFiles=3, transient_lastDdlTime=1513236182, last_modified_by=root, transactional=true}, viewOriginalText:null, viewExpandedText:null, tableType:MANAGED_TABLE, rewriteEnabled:false) |          |
+-----------------------------+-
```

如我要修改这个表的描述

```
0: jdbc:hive2://localhost:10000> alter table test1 set tblproperties('comment' = 'this is a test table');
No rows affected (0.352 seconds)
```

#### 3.1.3 添加SerDe属性

```
ALTER TABLE table_name [PARTITION partition_spec] SET SERDE serde_class_name [WITH SERDEPROPERTIES serde_properties];
 
ALTER TABLE table_name [PARTITION partition_spec] SET SERDEPROPERTIES serde_properties;
 
serde_properties:
  : (property_name = property_value, property_name = property_value, ... )
```

SerDe属性在被Hive初始化时被传递给表的SerDe，以序列化和反序列化数据。因此，用户可以在这里存储自定义SerDe所需的任何信息。有关更多信息，请参阅开发人员指南中的[SerDe文档](https://cwiki.apache.org/confluence/display/Hive/SerDe)和[Hive SerDe](https://cwiki.apache.org/confluence/display/Hive/DeveloperGuide#DeveloperGuide-HiveSerDe)，有关在CREATE TABLE语句中设置表的SerDe和SERDEPROPERTIES的详细信息，请参阅上面的[行格式，存储格式和SerDe](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-RowFormat,StorageFormat,andSerDe)。

请注意这两个`property_name`和`property_value`必须加引号。

```
ALTER TABLE test1 SET SERDEPROPERTIES ('field.delim' = ',');
```

#### 3.1.4 改变表格存储属性

```
ALTER TABLE table_name CLUSTERED BY (col_name, col_name, ...) [SORTED BY (col_name, ...)]
  INTO num_buckets BUCKETS;
```

例：

创建一个普通的表

```
0: jdbc:hive2://localhost:10000> create table test2 (key string,value string);
No rows affected (1.069 seconds)
```

查看表属性

```
0: jdbc:hive2://localhost:10000> show create table test2;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `test2`(                              |
|   `key` string,                                    |
|   `value` string)                                  |
| ROW FORMAT SERDE                                   |
|   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  |
| STORED AS INPUTFORMAT                              |
|   'org.apache.hadoop.mapred.TextInputFormat'       |
| OUTPUTFORMAT                                       |
|   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' |
| LOCATION                                           |
|   'hdfs://Master.Hadoop:9000/hiveLearn/foreign_path_hiveDB/test2' |
| TBLPROPERTIES (                                    |
|   'transient_lastDdlTime'='1513236960')            |
+-------------------------------
```

修改表存储属性

```
0: jdbc:hive2://localhost:10000> alter table test2 clustered by (key) sorted by (key) into 2 buckets;
No rows affected (0.358 seconds)
```

查看修改后的属性

```
0: jdbc:hive2://localhost:10000> show create table test2;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `test2`(                              |
|   `key` string,                                    |
|   `value` string)                                  |
| CLUSTERED BY (                                     |
|   key)                                             |
| SORTED BY (                                        |
|   key ASC)                                         |
| INTO 2 BUCKETS                                     |
| ROW FORMAT SERDE                                   |
|   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  |
| STORED AS INPUTFORMAT                              |
|   'org.apache.hadoop.mapred.TextInputFormat'       |
| OUTPUTFORMAT                                       |
|   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' |
| LOCATION                                           |
|   'hdfs://Master.Hadoop:9000/hiveLearn/foreign_path_hiveDB/test2' |
| TBLPROPERTIES (                                    |
|   'last_modified_by'='root',                       |
|   'last_modified_time'='1513237030',               |
|   'transient_lastDdlTime'='1513237030')            |
+----------------------------------------------------+
20 rows selected (0.312 seconds)
```

#### 3.1.5修改表倾斜后存储为目录

##### 修改表倾斜

```
ALTER TABLE table_name SKEWED BY (col_name1, col_name2, ...)
  ON ([(col_name1_value, col_name2_value, ...) [, (col_name1_value, col_name2_value), ...]
  [STORED AS DIRECTORIES];
```

STORED AS DIRECTORIES选项确定[倾斜的](https://cwiki.apache.org/confluence/display/Hive/Skewed+Join+Optimization)表是否使用[列表分区](https://cwiki.apache.org/confluence/display/Hive/ListBucketing)功能，该功能会为倾斜的值创建子目录。

##### 修改表不倾斜

```
ALTER TABLE table_name NOT SKEWED;
```

NOT SKEWED选项使表格无偏斜，并关闭列表分段功能（因为列表分段表总是倾斜的）。这将影响在ALTER语句之后创建的分区，但对在ALTER语句之前创建的分区没有影响。

##### 修改表为不保存为目录 

```
ALTER TABLE table_name NOT STORED AS DIRECTORIES;
```

这将关闭列表bucketing功能，尽管表仍然倾斜。

##### 修改表的倾斜 位置

```
ALTER TABLE table_name SET SKEWED LOCATION (col_name1="location1" [, col_name2="location2", ...] );
```

这将更改列表分段的位置。

##### 3.1.6 修改表的约束 

表约束可以通过ALTER TABLE语句添加或删除。

```
ALTER TABLE table_name ADD CONSTRAINT constraint_name PRIMARY KEY (column, ...) DISABLE NOVALIDATE;
ALTER TABLE table_name ADD CONSTRAINT constraint_name FOREIGN KEY (column, ...) REFERENCES table_name(column, ...) DISABLE NOVALIDATE RELY;
ALTER TABLE table_name DROP CONSTRAINT constraint_name;
```

例如

```
0: jdbc:hive2://localhost:10000> alter table test1 add constraint test_pk primary key (id) disable novalidate;
No rows affected (2.762 seconds)
```

### 3.2 修改分区 

分区可以通过在ALTER TABLE语句中使用PARTITION子句添加，重命名，交换（移动），删除或（un）归档，如下所述。要使直接添加到HDFS的分区的Metastore知道，您可以使用Metastore检查命令（[MSCK ](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-RecoverPartitions(MSCKREPAIRTABLE))），或在Amazon EMR上使用ALTER TABLE的RECOVER PARTITIONS选项。请参阅下面的[Alter Either Table或Partition ](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-AlterEitherTableorPartition)以获取更多方法来更改分区。

#### 3.2.1 添加分区 

```
ALTER TABLE table_name ADD [IF NOT EXISTS] PARTITION partition_spec [LOCATION 'location'][, PARTITION partition_spec [LOCATION 'location'], ...];
 
partition_spec:
  : (partition_column = partition_col_value, partition_column = partition_col_value, ...)
```

您可以使用ALTER TABLE ADD PARTITION将分区添加到表中。分区值只有在字符串的情况下才能被引用。该位置必须是数据文件所在的目录。（ADD PARTITION更改表元数据，但不加载数据，如果分区位置中不存在数据，则查询不会返回任何结果。）如果表的partition_spec已存在，则会引发错误。您可以使用IF NOT EXISTS来跳过错误。

#### 3.2.2 重命名分区 

```
ALTER TABLE table_name PARTITION partition_spec RENAME TO PARTITION partition_spec;
```

此语句允许您更改分区列的值。其中一种用例是，您可以使用此语句来标准化旧版分区列值以符合其类型。在这种情况下，类型转换和规范化不会在旧的列值启用*partition_spec*甚至财产[hive.typecheck.on.insert](https://cwiki.apache.org/confluence/display/Hive/Configuration+Properties#ConfigurationProperties-hive.typecheck.on.insert)设置为true（默认值），它允许你在老指定字符串形式的任何遗留数据*partition_spec*。

#### 3.2.3 交换分区 

分区可以在表之间交换（移动）

```
-- Move partition from table_name_1 to table_name_2
ALTER TABLE table_name_2 EXCHANGE PARTITION (partition_spec) WITH TABLE table_name_1;
-- multiple partitions
ALTER TABLE table_name_2 EXCHANGE PARTITION (partition_spec, partition_spec2, ...) WITH TABLE table_name_1;
```

此语句允许您将分区中的数据从表移动到另一个具有相同模式但尚未拥有该分区的表。
有关此功能的更多详细信息，请参阅[Exchange分区](https://cwiki.apache.org/confluence/display/Hive/Exchange+Partition)和[HIVE-4095 ](https://issues.apache.org/jira/browse/HIVE-4095)。

#### 3.2.4 恢复分区（MSCK REPAIR TABLE）

Hive存储Metastore中每个表的分区列表。但是，如果直接将新分区添加到HDFS（例如通过使用`hadoop fs -put`命令），Metastore（因此Hive）将不会意识到这些分区，除非用户`ALTER TABLE table_name ADD PARTITION`在每个新添加的分区上运行命令。

但是，用户可以使用修复表选项运行Metastore检查命令：

```
MSCK REPAIR TABLE table_name;
```

这会将关于分区的元数据添加到Hive Metastore，以获取这些元数据尚不存在的分区。换句话说，它将添加存在于HDFS但不在Metastore中的任何分区。有关更多详细信息，请参阅[HIVE-874](https://issues.apache.org/jira/browse/HIVE-874)。当有大量未跟踪的分区时，可以批量运行MSCK REPAIR TABLE来避免OOME（内存不足错误）。通过为属性**hive.msck.repair.batch.size**提供配置的批处理大小，它可以在内部批处理中运行。该属性的默认值是零，这意味着它将一次执行所有的分区。

Amazon Elastic MapReduce（EMR）版本的Hive上的等价命令是：

````
ALTER TABLE table_name RECOVER PARTITIONS;
````

#### 3.2.5 删除分区  

```
ALTER TABLE table_name DROP [IF EXISTS] PARTITION partition_spec[, PARTITION partition_spec, ...]
  [IGNORE PROTECTION] [PURGE];  
```

您可以使用ALTER TABLE DROP PARTITION来删除表的分区。这将删除此分区的数据和元数据。如果配置了垃圾桶，则实际上将数据移动到.Trash / Current目录，除非指定了PURGE，但元数据完全丢失（请参阅上面的[丢弃表](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-DropTable)）。

对于受[NO_DROP CASCADE](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-AlterTable/PartitionProtections)保护的表，可以使用谓词IGNORE PROTECTION删除指定的分区或一组分区（例如，在两个Hadoop集群之间拆分表时）：

```
ALTER TABLE table_name DROP [IF EXISTS] PARTITION partition_spec IGNORE PROTECTION;
```

无论保护状态如何，上述命令都会删除该分区。

#### 3.2.6 归档分区 

```
ALTER TABLE table_name ARCHIVE PARTITION partition_spec;
ALTER TABLE table_name UNARCHIVE PARTITION partition_spec;
```

归档是将分区文件移动到Hadoop存档（HAR）中的功能。请注意，只有文件数量会减少; HAR不提供任何压缩。有关更多信息，请参阅[LanguageManual Archiving](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Archiving)

### 3.3 修改表或者分区  

#### 3.3.1修改表/分区文件格式 

```
ALTER TABLE table_name [PARTITION partition_spec] SET FILEFORMAT file_format;
```

#### 3.3.2 修改表/分区位置 

```
ALTER TABLE table_name [PARTITION partition_spec] SET LOCATION "new location";
```

#### 3.3.3修改表/分区TOUCH 

```

ALTER TABLE table_name TOUCH [PARTITION partition_spec];
```

TOUCH读取元数据，并将其写回。这有导致前/后执行挂钩的效果。一个示例用例是，如果您有一个挂钩，它会记录所有已修改的表/分区以及直接更改HDFS上的文件的外部脚本。由于脚本修改了配置单元之外的文件，修改将不会被挂钩记录。外部脚本可以调用TOUCH来启动钩子并将所述表或分区标记为已修改。

另外，如果我们合并可靠的最后修改时间，它可能会很有用。然后触摸也会更新那个时间。

请注意，如果TOUCH不存在，TOUCH不会创建表或分区。（请参见[创建表](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-CreateTable)）



#### 3.3.4 修改表/分区保护 

```
ALTER TABLE table_name [PARTITION partition_spec] ENABLE|DISABLE NO_DROP [CASCADE];
 
ALTER TABLE table_name [PARTITION partition_spec] ENABLE|DISABLE OFFLINE;
```

数据保护可以在表或分区级别进行设置。启用NO_DROP可防止[删除](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-DropPartitions)表。启用OFFLINE可防止查询表或分区中的数据，但仍可访问元数据。

如果表中的任何分区启用了NO_DROP，则该表也不能被丢弃。相反，如果一个表启用了NO_DROP，那么分区可能会被删除，但是NO_DROP CASCADE分区不能被删除，除非[drop partition命令](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-DropPartitions)指定了IGNORE PROTECTION 。

#### 3.3.5修改表/分区COMPACT 

```

```

