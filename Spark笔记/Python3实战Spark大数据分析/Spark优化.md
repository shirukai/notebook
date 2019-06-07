# Spjark优化

## 1 HistoryServer配置及使用

官网地址：http://spark.apache.org/docs/latest/monitoring.html

### 1.1 开启HistoryServer

要想开启spark的HistoryServer只需要修改$SPARK_HOME/conf/spark-defaults.conf文件，将spark.eventLog.enabled设置为true。

首先将spark-defaults.conf.template 重名为 spark-defaults.conf

```shell
cp spark-defaults.conf.template spark-defaults.conf
```

然后修改内容如下：

```properties
spark.eventLog.enabled           true
spark.eventLog.dir               hdfs://localhost:9000/directory
```

开启spark日志，并制定日志路径

### 1.2 设置SPARK_HISTORY_OPTS

开启HistorySever之后需要设置SPARK_HISTORY_OPTS相关参数，如设置端口号（spark.history.ui.port）、设置logDir（spark.history.fs.logDirectory）

修改$SPARK_HOME/conf/spark-env.sh文件，内容为：

```
SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs://localhost:9000/directory"
```

### 1.3 启动HisoryServer服务

在$SPARK_HOME/sbin/下启动

```shell
sh start-history-server.sh
```

![](http://shirukai.gitee.io/images/71257b7bef47d924c3dee375c9d5d0ed.jpg)

## 2 序列化

官网：http://spark.apache.org/docs/latest/tuning.html#data-serialization

## 3 内存管理

官网：http://spark.apache.org/docs/latest/tuning.html#memory-tuning

spark内存用于计算和存储两方面

## 4 广播变量

官网：http://spark.apache.org/docs/latest/tuning.html#broadcasting-large-variables

```python
>>> broadcastVar = sc.broadcast([1, 2, 3])
<pyspark.broadcast.Broadcast object at 0x102789f10>

>>> broadcastVar.value
[1, 2, 3]
```

## 5 数据本地化

官网：http://spark.apache.org/docs/latest/tuning.html#data-locality

移动计算

## 6 项目性能优化

* 并行度：spark.sql.shuffle.partitions
* 分区字段类型推测：spark.sql.sources.partitionColumnTypeInference.enabled