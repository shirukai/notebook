# hive学习之修改表、分区、列 

查看已有表：

```
0: jdbc:hive2://localhost:10000> show tables;
+----------------------+
|       tab_name       |
+----------------------+
| bucket_table         |
| external_student     |
| partition_table      |
| person               |
| sample_data          |
| student              |
| student1             |
| student4             |
| t1                   |
| t2                   |
| t3                   |
| test1                |
| test_partition       |
| testhivedrivertable  |
| user                 |
| user1                |
| user2                |

```

### 重命名表

将 test_partition 表重名为t_partition

```
0: jdbc:hive2://localhost:10000> alter table test_partition rename to t_partition;
No rows affected (0.287 seconds)
```

### 查看表属性 

```
0: jdbc:hive2://localhost:10000> desc extended t_partition;
+-----------------------------+----------------------------------------------------+-----------------------+
|          col_name           |                     data_type                      |        comment        |
+-----------------------------+----------------------------------------------------+-----------------------+
| sid                         | int                                                |                       |
| sname                       | string                                             |                       |
| sex                         | string                                             |                       |
| stest                       | string                                             |                       |
|                             | NULL                                               | NULL                  |
| # Partition Information     | NULL                                               | NULL                  |
| # col_name                  | data_type                                          | comment               |
|                             | NULL                                               | NULL                  |
| sex                         | string                                             |                       |
| stest                       | string                                             |                       |
|                             | NULL                                               | NULL                  |
| Detailed Table Information  | Table(tableName:t_partition, dbName:default, owner:root, createTime:1511916391, lastAccessTime:0, retention:0, sd:StorageDescriptor(cols:[FieldSchema(name:sid, type:int, comment:null), FieldSchema(name:sname, type:string, comment:null), FieldSchema(name:sex, type:string, comment:null), FieldSchema(name:stest, type:string, comment:null)], location:hdfs://Master.Hadoop:9000/user/hive/warehouse/t_partition, inputFormat:org.apache.hadoop.mapred.TextInputFormat, outputFormat:org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat, compressed:false, numBuckets:-1, serdeInfo:SerDeInfo(name:null, serializationLib:org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, parameters:{serialization.format=1}), bucketCols:[], sortCols:[], parameters:{}, skewedInfo:SkewedInfo(skewedColNames:[], skewedColValues:[], skewedColValueLocationMaps:{}), storedAsSubDirectories:false), partitionKeys:[FieldSchema(name:sex, type:string, comment:null), FieldSchema(name:stest, type:string, comment:null)], parameters:{last_modified_time=1511918377, totalSize=0, numRows=0, rawDataSize=0, createTime=111, COLUMN_STATS_ACCURATE={"BASIC_STATS":"true"}, numFiles=0, numPartitions=0, transient_lastDdlTime=1511918377, comment=111, last_modified_by=root}, viewOriginalText:null, viewExpandedText:null, tableType:MANAGED_TABLE, rewriteEnabled:false) |                       |
+-----------------------------+----------------------------------------------------+-----------------------+
```



### 修改表属性

```
ALTER TABLE t_partition SET TBLPROPERTIES('createTime' = '111'); 
```



### 分区操作 

http://blog.csdn.net/skywalker_only/article/details/30224309

#### 新增分区

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

#### 现在我们需要新增一个分区gender=S，空分区无数据。

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

#### 删除分区 

删除分区，会将我们的元数据、以及hdfs文件中的数据一起删除。

```
0: jdbc:hive2://localhost:10000> alter table partition_table drop partition(gender='S');
No rows affected (0.316 seconds)
```

![](https://shirukai.gitee.io/images/201711291011_47.png)

hdfs中的数据也被删除了。

#### 现在我们要新建一个分区，并将hdfs中已经存在的一个目录，及里面的数据加载到这个表分区里 

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



#### 重命名分区 

```
0: jdbc:hive2://localhost:10000> alter table partition_table partition(gender='M') rename to partition(gender='S');
No rows affected (0.57 seconds)
```



### 修改列名/类型/位置/注释

下面的语句允许修改列名称、列类型、列注释、列位置。该语句仅修改Hive元数据，不会触动表中的数据，用户需要确定实际的数据布局符合元数据的定义。

```
ALTER TABLE table_name CHANGE [COLUMN] col_old_name col_new_name column_type [COMMENTcol_comment] [FIRST|(AFTER column_name)] 
```



修改sid 为sage

```
0: jdbc:hive2://localhost:10000> alter table partition_table change sid sage int first;
No rows affected (0.33 seconds)
0: jdbc:hive2://localhost:10000> desc partition_table;
+--------------------------+-----------------------+-----------------------+
|         col_name         |       data_type       |        comment        |
+--------------------------+-----------------------+-----------------------+
| sage                     | int                   |                       |
| name                     | string                |                       |
| gender                   | string                |                       |
|                          | NULL                  | NULL                  |
| # Partition Information  | NULL                  | NULL                  |
| # col_name               | data_type             | comment               |
|                          | NULL                  | NULL                  |
| gender                   | string                |                       |
+--------------------------+-----------------------+-----------------------+
8 rows selected (0.253 seconds)

```



### 增加/替换列

```
ALTER TABLE table_name ADD|REPLACE COLUMNS (col_name data_type[COMMENT col_comment], ...)  
```



新增列

```
0: jdbc:hive2://localhost:10000> alter table partition_table add columns(key int, value string);
No rows affected (0.306 seconds)
0: jdbc:hive2://localhost:10000> desc partition_table;
+--------------------------+-----------------------+-----------------------+
|         col_name         |       data_type       |        comment        |
+--------------------------+-----------------------+-----------------------+
| sage                     | int                   |                       |
| name                     | string                |                       |
| key                      | int                   |                       |
| value                    | string                |                       |
| gender                   | string                |                       |
|                          | NULL                  | NULL                  |
| # Partition Information  | NULL                  | NULL                  |
| # col_name               | data_type             | comment               |
|                          | NULL                  | NULL                  |
| gender                   | string                |                       |
+--------------------------+-----------------------+-----------------------+
10 rows selected (0.231 seconds)

```

利用replace columns来删除列如：

删除key value这两列

```
0: jdbc:hive2://localhost:10000> alter table partition_table replace columns(sage int , name string);
No rows affected (0.347 seconds)
```

