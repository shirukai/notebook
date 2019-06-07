# SparkSQL 操作Hive表

> 版本说明：
>
> Hadoop: 2.7.6
>
> Spark: 2.3.0
>
> Hive: 3.0.0

要想SparkSQL能后读到hive的元数据，需要将hive的配置文件hive-site.xml拷贝到Spark的conf目录下。另外，需要将mysql的jar包分别拷到hive的lib目录下和spark的jars目录下。简易下载高版本的jar包，避免不必要的错误。

## 1 创建Hive表

进入hive命令行。创建一个以","作为分隔符的表，表名为hive_people，分别包含name、age、phone字段。建表语句如下所示：

```shell
hive> create table hive_people
    > (name string,age int, phone bigint)
    > row format delimited fields terminated by ',';
OK
Time taken: 0.125 seconds
```

查看我们的表结构

```shell
hive> desc hive_people;
OK
name                	string              	                    
age                 	int                 	                    
phone               	bigint              	                    
Time taken: 0.069 seconds, Fetched: 3 row(s)
```

加载本地数据到hive表

假如我们有一个people.txt文件，文件内容如下：

```
Ming,20,15552211521
hong,19,13287994007
zhi,21,15552211523
```

将上述的文件里的数据加载到hive表中：

```shell
hive> load data local inpath '/Users/shirukai/people.txt' into table hive_people;
Loading data to table default.hive_people
OK
Time taken: 0.25 seconds
```

查看表数据：

```
hive> select * from hive_people;
OK
Ming	20	15552211521
hong	19	13287994007
zhi	21	15552211523
Time taken: 0.14 seconds, Fetched: 3 row(s)
```

统计表中有多少条记录

```shell
hive> select count(0) from hive_people;
Query ID = shirukai_20180913112654_df58f6be-164f-4ef7-be57-133e36b0153f
Total jobs = 1
Launching Job 1 out of 1
Number of reduce tasks determined at compile time: 1
In order to change the average load for a reducer (in bytes):
  set hive.exec.reducers.bytes.per.reducer=<number>
In order to limit the maximum number of reducers:
  set hive.exec.reducers.max=<number>
In order to set a constant number of reducers:
  set mapreduce.job.reduces=<number>
Job running in-process (local Hadoop)
2018-09-13 11:26:56,520 Stage-1 map = 100%,  reduce = 100%
Ended Job = job_local1874426855_0002
MapReduce Jobs Launched: 
Stage-Stage-1:  HDFS Read: 472 HDFS Write: 236 SUCCESS
Total MapReduce CPU Time Spent: 0 msec
OK
3
Time taken: 1.719 seconds, Fetched: 1 row(s)
```

从上面信息可以看出，当我们执行count这句SQL的时候，hive实际上是执行了一次MapReduce作业。

## 2 Spark SQL 操作Hive表

如上，我们已经创建了一张hive表，并且在hive表中插入了一些数据，并执行了count统计操作。接下来，使用SparkSQL来操作hive表。以下将在spark-shell里进行操作。

打开spark-shell

```shell
spark-shell
2018-09-13 11:31:00 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Spark context Web UI available at http://192.168.1.42:4040
Spark context available as 'sc' (master = local[*], app id = local-1536809469802).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.3.1
      /_/
         
Using Scala version 2.11.8 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_171)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 
```

查看所有表

```shell
scala> spark.sql("show tables").show()
2018-09-13 11:41:40 WARN  ObjectStore:568 - Failed to get database global_temp, returning NoSuchObjectException
+--------+-----------+-----------+
|database|  tableName|isTemporary|
+--------+-----------+-----------+
| default|hive_people|      false|
+--------+-----------+-----------+
```

从上面我们可以看出，我们在hive 里创建的表，通过Spark SQL给读取数来了，接下来，我们来查看一下hive_people表里的数据

```shell
scala> spark.sql("select * from hive_people").show()
+----+---+-----------+
|name|age|      phone|
+----+---+-----------+
|Ming| 20|15552211521|
|hong| 19|13287994007|
| zhi| 21|15552211523|
+----+---+-----------+
```

或者

```shell
scala> spark.table("hive_people").show()
+----+---+-----------+
|name|age|      phone|
+----+---+-----------+
|Ming| 20|15552211521|
|hong| 19|13287994007|
| zhi| 21|15552211523|
+----+---+-----------+
```

统计条数：

```shell
scala> spark.sql("select * from hive_people").count()
res2: Long = 3
```

按照年龄分组统计

```shell
scala> spark.sql("select age, count(1) as mount from hive_people where group by age").show()
+---+-----+
|age|mount|
+---+-----+
| 20|    1|
| 19|    1|
| 21|    1|
+---+-----+
```

将上面的结果写入people_age_count表里

```shell
scala> spark.sql("select age, count(1) as mount from hive_people where group by age").write.saveAsTable("people_age_count")
2018-09-13 11:53:23 WARN  ShellBasedUnixGroupsMapping:87 - got exception trying to get groups for user hdfs: id: hdfs: no such user
id: hdfs: no such user
```

查看表是否被保存了：

```shell
scala> spark.sql("show tables").show()
+--------+----------------+-----------+
|database|       tableName|isTemporary|
+--------+----------------+-----------+
| default|     hive_people|      false|
| default|people_age_count|      false|
+--------+----------------+-----------+
```

使用hive查看刚刚创建的表：

```shell
hive>show tables;
OK
hive_people
people_age_count
Time taken: 0.902 seconds, Fetched: 2 row(s)
```

设置shuffle分区

```shell
scala> spark.sqlContext.setConf("spark.sql.shuffle.partitions","10")

scala> spark.sql("select age, count(1) as mount from hive_people where group by age").show()
+---+-----+
|age|mount|
+---+-----+
| 20|    1|
| 21|    1|
| 19|    1|
+---+-----+
```

