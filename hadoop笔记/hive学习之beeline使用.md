# hive学习之beeline使用 

官网文档：

https://cwiki.apache.org/confluence/display/Hive/HiveServer2+Clients#HiveServer2Clients-ConnectionURLs

## 什么是Beeline？

HiveServer2支持与HiveServer2一起使用的命令shell Beeline。这是一个基于SQLLine CLI的JDBC客户端。

Beeline shell既可以在嵌入模式下工作，也可以在远程模式下工作。在嵌入式模式下，它运行嵌入式Hive（类似于[Hive CLI](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Cli)），而远程模式则是通过Thrift连接到单独的HiveServer2进程。从[Hive 0.14](https://issues.apache.org/jira/browse/HIVE-7615)开始，当Beeline与HiveServer2一起使用时，它还会打印来自HiveServer2的日志消息，以便执行到STDERR的查询。建议将远程HiveServer2模式用于生产，因为它更安全，不需要为用户授予直接的HDFS / Metastore访问权限。

> 在远程模式下，HiveServer2只接受有效的Thrift调用 - 即使在HTTP模式下，消息体也包含Thrift有效负载



## 举例 

进入Beeline

```
beeline
```

连接jdbc

```
beeline> !connect jdbc:hive2://localhost:10000 root root

Connecting to jdbc:hive2://localhost:10000
Connected to: Apache Hive (version 2.3.2)
Driver: Hive JDBC (version 2.3.2)
Transaction isolation: TRANSACTION_REPEATABLE_READ
0: jdbc:hive2://localhost:10000> 
```

执行show tables 操作

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
| testhivedrivertable  |
| user                 |
| user1                |
| user2                |
+----------------------+
16 rows selected (0.606 seconds)
```

设置 输出格式 

```
beeline --outputformat=[table/vertical/xmlattr/xmlelements/csv/tsv/dsv/csv2/tsv2]
```

例如设置 beeline --outputformat=xmlattr

```
[root@Master ~]# beeline --outputformat=xmlattr
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/lib/apache-hive-2.3.2-bin/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/hadoop/hadoop-2.7.4/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Beeline version 2.3.2 by Apache Hive
beeline> !connect jdbc:hive2://localhost:10000 root root
Connecting to jdbc:hive2://localhost:10000
Connected to: Apache Hive (version 2.3.2)
Driver: Hive JDBC (version 2.3.2)
Transaction isolation: TRANSACTION_REPEATABLE_READ
0: jdbc:hive2://localhost:10000> select * from user1;
<resultset>
  <result user1.user="root" user1.password="*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"/>
  <result user1.user="root" user1.password="*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"/>
  <result user1.user="root" user1.password="*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"/>
  <result user1.user="root" user1.password="*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"/>
  <result user1.user="root" user1.password="*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B"/>
</resultset>
5 rows selected (0.546 seconds)
0: jdbc:hive2://localhost:10000> 

```

