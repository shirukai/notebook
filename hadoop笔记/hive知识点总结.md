# hive 知识点 

## 1.制表符

创建表的时候设置制表符

```
create table emp
(empno int,
ename string,
job string,mgr int,
hiredate date, 
sal float,
comm float,
deptno int)
row format delimited fields terminated by ",";
```

如何查看hive表的制表符？

```
0: jdbc:hive2://localhost:10000> show create table emp;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `emp`(                                |
|   `empno` int,                                     |
|   `ename` string,                                  |
|   `job` string,                                    |
|   `mgr` int,                                       |
|   `hiredate` date,                                 |
|   `sal` float,                                     |
|   `comm` float,                                    |
|   `deptno` int)                                    |
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
|   'hdfs://Master.Hadoop:9000/user/hive/warehouse/emp' |
| TBLPROPERTIES (                                    |
|   'field.delim'=',',                               |
|   'last_modified_by'='root',                       |
|   'last_modified_time'='1511938450',               |
|   'transient_lastDdlTime'='1511938450')            |
+----------------------------------------------------+
25 rows selected (0.255 seconds)

```

### 修改表的制表符？

通过设置SERDEPROPERTIES的属性来更改导入数据的时候的制表符。

例如：

创建一个名为tab1的表，里面有两个字段，一个是name string类型、另一个是 age int类型，并且创建表的时候给设定了以“,”为制表符，创建语句如下：

```
create table tab1
(name string, age int) 
row format delimited fields terminated by ",";
```

创建完成后，我们来查看表结构 

```
0: jdbc:hive2://localhost:10000> show create table tab1;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `tab1`(                               |
|   `name` string,                                   |
|   `age` int)                                       |
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
|   'hdfs://Master.Hadoop:9000/user/hive/warehouse/tab1' |
| TBLPROPERTIES (                                    |
|   'transient_lastDdlTime'='1513065940')            |
+----------------------------------------------------+
16 rows selected (0.352 seconds)
```

可以看出 这个表的'field.delim'=',',  所以我们需要导入以逗号分割的数据，才能正确显示。

所以，我们先来导入以逗号分割的数据：

```
shirukai,19
licuiping,18
```

导入语句：(如果需要重写表中数据可以用 overwrite into table 表名的语法来导入数据)

```
load data local inpath '/root/hiveTest/tab1.txt' into table tab1;
```

查看表数据：

```
0: jdbc:hive2://localhost:10000> select * from tab1;
+------------+-----------+
| tab1.name  | tab1.age  |
+------------+-----------+
| shirukai   | 19        |
| licuiping  | 18        |
+------------+-----------+

```

如果导入“：”分割的数据会怎样？

```
shirukai:18
licuiping:18
```

```
0: jdbc:hive2://localhost:10000> load data local inpath '/root/hiveTest/tab2.txt' overwrite into table tab1;
```

查看表：

```
0: jdbc:hive2://localhost:10000> select * from tab1;
+---------------+-----------+
|   tab1.name   | tab1.age  |
+---------------+-----------+
| shirukai:18   | NULL      |
| licuiping:18  | NULL      |
+---------------+-----------+
2 rows selected (0.211 seconds)
```

#### 修改制表符 

首先我们再创建一个表tab2，字段以及属性跟tab1一样。

```
create table tab2 like tab1;
```

创建完成后，我们来查看表结构

```
0: jdbc:hive2://localhost:10000> show create table tab2;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `tab2`(                               |
|   `name` string,                                   |
|   `age` int)                                       |
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
|   'hdfs://Master.Hadoop:9000/user/hive/warehouse/tab2' |
| TBLPROPERTIES (                                    |
|   'transient_lastDdlTime'='1513068637')            |
+----------------------------------------------------+
16 rows selected (0.174 seconds)
```



这时我们来修改tab2的制表符 

```
0: jdbc:hive2://localhost:10000> alter table tab2 set SERDEPROPERTIES ('field.delim'=':');
```

查看修改后的表结构

```
0: jdbc:hive2://localhost:10000> show create table tab2;
+----------------------------------------------------+
|                   createtab_stmt                   |
+----------------------------------------------------+
| CREATE TABLE `tab2`(                               |
|   `name` string,                                   |
|   `age` int)                                       |
| ROW FORMAT SERDE                                   |
|   'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'  |
| WITH SERDEPROPERTIES (                             |
|   'field.delim'=':',                               |
|   'serialization.format'=',')                      |
| STORED AS INPUTFORMAT                              |
|   'org.apache.hadoop.mapred.TextInputFormat'       |
| OUTPUTFORMAT                                       |
|   'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' |
| LOCATION                                           |
|   'hdfs://Master.Hadoop:9000/user/hive/warehouse/tab2' |
| TBLPROPERTIES (                                    |
|   'last_modified_by'='root',                       |
|   'last_modified_time'='1513068827',               |
|   'transient_lastDdlTime'='1513068827')            |
+----------------------------------------------------+
18 rows selected (0.186 seconds)

```



然后导入以":"分割的数据

```
0: jdbc:hive2://localhost:10000> load data local inpath '/root/hiveTest/tab2.txt' into table tab2;
No rows affected (0.887 seconds)
```

查看数据 

```
0: jdbc:hive2://localhost:10000> select * from tab2;
+------------+-----------+
| tab2.name  | tab2.age  |
+------------+-----------+
| shirukai   | 18        |
| licuiping  | 18        |
+------------+-----------+
2 rows selected (0.219 seconds)
```



## 删除表数据

首先我们来复制一个表，用来做删除测试

```
0: jdbc:hive2://localhost:10000> create table test_student as select sno,sname,sage,sex from student;
WARNING: Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
No rows affected (49.172 seconds)
```

查看数据 

```
0: jdbc:hive2://localhost:10000> select * from test_student;
+-------------------+---------------------+--------------------+-------------------+
| test_student.sno  | test_student.sname  | test_student.sage  | test_student.sex  |
+-------------------+---------------------+--------------------+-------------------+
| 201457507201      | student1            | 18                 | 01                |
| 201457507202      | student2            | 19                 | 01                |
| 201457507203      | student3            | 18                 | 02                |
| 201457507204      | student3            | 18                 | 01                |
| 201457507205      | student4            | 19                 | 01                |
| 201457507206      | student5            | 18                 | 02                |
+-------------------+---------------------+--------------------+-------------------+
6 rows selected (0.224 seconds)

```

现在想要删除sname=student1的数据

```
0: jdbc:hive2://localhost:10000> delete from test_student where sname='student1';
Error: Error while compiling statement: FAILED: SemanticException [Error 10294]: Attempt to do update or delete using transaction manager that does not support these operations. (state=42000,code=10294)
```

报错，提示当前使用的事务管理器不支持这些这些操作。

通过设置临时参数、或者修改配置文件来解决这个问题。

##### 设置临时变量(只对当前会话生效)

```
set hive.auto.convert.join.noconditionaltask.size = 10000000; set hive.support.concurrency = true; set hive.enforce.bucketing = true; set hive.exec.dynamic.partition.mode = nonstrict; set hive.txn.manager = org.apache.hadoop.hive.ql.lockmgr.DbTxnManager; set hive.compactor.initiator.on = true;
```

##### 或者修改配置文件

```
<property>
<name>hive.enforce.bucketing</name>
<value>true</value>
</property>
<property>
<name>hive.exec.dynamic.partition.mode</name>
<value>nonstrict</value>
</property>
<property>
<name>hive.txn.manager</name>
<value>org.apache.hadoop.hive.ql.lockmgr.DbTxnManager</value>
</property>
<property>
<name>hive.compactor.initiator.on</name>
<value>true</value>
</property>
<property>
<name>hive.compactor.worker.threads</name>
<value>1</value>
</property>
<property>
<name>hive.in.test</name>
<value>true</value>
</property>
<property>
<name>hive.auto.convert.join.noconditionaltask.size</name>
<value>10000000</value>
</property>
<property>
<name>hive.support.concurrency </name>
<value>true</value>
</property>
```



然后执行删除操作

```
0: jdbc:hive2://localhost:10000> delete from test_student where sname='student1';
Error: Error while compiling statement: FAILED: SemanticException [Error 10297]: Attempt to do update or delete on table foreign_path_hivedb.test_student that does not use an AcidOutputFormat or is not bucketed (state=42000,code=10297)
```

仍然报错，提示当前表没有使用AcidOutputFormat或者不是桶表，网上查到确实如此，而且目前只有ORCFileformat支持AcidOutputFormat，不仅如此建表时必须指定参数('transactional' = true)。



##### 于是重新按照要求建表，并导入数据。 

先删除之前的表

```
0: jdbc:hive2://localhost:10000> drop table test_student;
No rows affected (0.286 seconds)
```

重新创建表，设置为桶表，并设置参数('transactional' = true)

```
0: jdbc:hive2://localhost:10000> create table test_student(sno bigint,sname string,sage int,sex string)clustered by(sno) into 2 buckets stored as orc TBLPROPERTIES('transactional'='true');
No rows affected (0.247 seconds)
```

向表中插入数据

```
0: jdbc:hive2://localhost:10000> insert into table test_student  select sno,sname,sage,sex from student;
WARNING: Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
No rows affected (88.172 seconds)
```

查看表数据

```
0: jdbc:hive2://localhost:10000> select * from test_student;
+-------------------+---------------------+--------------------+-------------------+
| test_student.sno  | test_student.sname  | test_student.sage  | test_student.sex  |
+-------------------+---------------------+--------------------+-------------------+
| 201457507201      | student1            | 18                 | 01                |
| 201457507202      | student2            | 19                 | 01                |
| 201457507203      | student3            | 18                 | 02                |
| 201457507204      | student3            | 18                 | 01                |
| 201457507205      | student4            | 19                 | 01                |
| 201457507206      | student5            | 18                 | 02                |
+-------------------+---------------------+--------------------+-------------------+
6 rows selected (0.82 seconds)
```

然后按条件删除数据

```
0: jdbc:hive2://localhost:10000> delete from test_student where sname='student1';
WARNING: Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
No rows affected (284.526 seconds)
```



##### 删除数据的其他方法 

1. 通过数据重写，插入空数据，就可以清空表数据了。

```
insert overwrite table tab2 select name,age form tab2 where age=20;
```

2. 也可以用truncate清空表数据

```
0: jdbc:hive2://localhost:10000> truncate table dynamic_par_tb;
No rows affected (0.551 seconds)
```

