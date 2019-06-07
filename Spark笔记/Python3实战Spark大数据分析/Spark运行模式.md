# Spark运行模式

官网说明：http://spark.apache.org/docs/latest/submitting-applications.html

目前spark支持的运行模式主要有Local、Standalone、Mesos、YARN、Kubernetes。这里主要记录spark在Local、Standalone、YARN环境下运行。

假如目前我们有一个简单的wordcount应用，将分别在以下环境中运行。

wordcount.py，文件路径：/Users/shirukai/Desktop/HollySys/Repository/learn-demo-pyspark/wordcount.py

```python
"""
Created by shirukai on 2018/8/28
"""
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    input = [
        'This tutorial provides a quick introduction to using Spark. We will first introduce the API through Spark’s interactive shell (in Python or Scala), then show how to write applications in Java, Scala, and Python.',
        'To follow along with this guide, first download a packaged release of Spark from the Spark website. Since we won’t be using HDFS, you can download a package for any version of Hadoop.',
        'Note that, before Spark 2.0, the main programming interface of Spark was the Resilient Distributed Dataset (RDD). After Spark 2.0, RDDs are replaced by Dataset, which is strongly-typed like an RDD, but with richer optimizations under the hood. The RDD interface is still supported, and you can get a more complete reference at the RDD programming guide. However, we highly recommend you to switch to use Dataset, which has better performance than RDD. See the SQL programming guide to get more information about Dataset.']
    words = sc.parallelize(input) \
        .map(lambda line: line.replace(". ", " ").replace(", ", " ").rstrip(".")) \
        .flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .map(lambda x: (x[1], x[0])) \
        .sortByKey(False) \
        .map(lambda x: (x[1], x[0]))
    print(words.take(3))

```

## 1 Local模式

Local模式主要是在开发测试应用的时候使用。

### 1.1 使用spark-submit的本地模式提交应用

进入spark-home

```shell
cd $SPARK_HOME
```

提交应用

```shell
./bin/spark-submit\
 --master local[2]\
 --name spark-local\
 /Users/shirukai/Desktop/HollySys/Repository/learn-demo-pyspark/wordcount.py
```

--master:指定运行模式

--name:指定应用名字

路径

### 1.2 Lcoal Master URL说明

| Master URL | Meaning               |
| ---------- | --------------------- |
| local      | 运行在一个线程上      |
| local[K]   | 运行在K个线程上       |
| local[K,F] | K个线程，最大F次失败  |
| local[*]   | 最大线程              |
| local[*,F] | 最大线程，最大F次失败 |



## 2 Standalone模式

### 2.1 启动spark集群

修改 $SPARK_HOME/conf/slaves,将所节点的hostname添加到此文件中。

```shell
sh $SPARK_HOME/sbin/start-all.sh 
```

jps 查看进程

```shell
shirukaideMacBook-Pro:conf shirukai$ jps
1633 Master
1676 Worker
```

服务启动后，我们可以访问spark的WebUI ，正常的地址为hostname:8080,这里我的端口改为18080，访问localhost:18080

![](http://shirukai.gitee.io/images/9386090d6ad81573e502323d9dcd6b42.jpg)

### 2.2 在Standalone模式下启动pyspark交互式进程

由上图可以看出，我们的master的url为：spark://shirukaideMacBook-Pro.local:7077

进入spark-home

```shell
cd $SPARK_HOME
```

启动pyspark

```shell
./bin/pyspark --master spark://shirukaideMacBook-Pro.local:7077
```

启动后，可以在web界面上，看到，我们已经启动的交互式应用

![](http://shirukai.gitee.io/images/081dcd6dd8fcc9f29181d9f493cbf813.jpg)

这时候我们可以查看应用详情：

![](http://shirukai.gitee.io/images/5baca29dcb9e305b797363ea4e952cd2.gif)

因为我们没有进行任何操作，所以我们的详情里的内容是空的，接下在，我们在pyspark里，进行交互性操作

```shell
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.3.1
      /_/

Using Python version 3.6.4 (default, Jan 16 2018 12:04:33)
SparkSession available as 'spark'.
>>> data=[1,2,3,4,5]
>>> rdd=sc.p
sc.parallelize(        sc.pickleFile(         sc.profiler_collector  sc.pythonExec          sc.pythonVer           
>>> rdd=sc.parallelize(data)
>>> rdd.collect()
[1, 2, 3, 4, 5]                                                                 
>>> 
```

刷新应用详情页面，发现我们有详情生成

![](http://shirukai.gitee.io/images/38201ffcea7681804f57a3c3c1e4cd2b.jpg)

### 2.3 使用spark-submit的Standalone模式提交应用

进入spark-home

```shell
cd $SPARK_HOME
```

提交应用

```shell
./bin/spark-submit\
 --master spark://shirukaideMacBook-Pro.local:7077\
 --name spark-standalone\
 /Users/shirukai/Desktop/HollySys/Repository/learn-demo-pyspark/wordcount.py
```

![](http://shirukai.gitee.io/images/e2e679c9499a87cbd12849a6c85d6b3d.jpg)

注意：如果使用standalone模式，而且节点数大于1的时候，如果使用本地文件测试，必须要本证每个节点都要有相同的文件。

## 3 YARN 模式

大多数都使用Spark on YARN模式，它是把Spark当做客户端，把作业提交到YARN上执行，不需要spark集群（不需要启动spark的master、和worker）

### 3.1 使用spark-submit的YARN模式提交应用

#### 3.1.1 在提交应用之前，需要启动hadoop集群。

```shell
shirukaideMacBook-Pro:~ shirukai$ jps
2625 NameNode
2706 DataNode
3011 NodeManager
3032 Jps
2810 SecondaryNameNode
2923 ResourceManager
1326 SparkSubmit
```

我们可以看出我们YARN的ResourceManager和NodeManager已经启动。进入YARN的WebUI查看，http://localhost:8088/cluster

![](http://shirukai.gitee.io/images/698680434226a8bb43964b861e304354.jpg)

由上图可以看出目前没有YARN的资源分配给spark。

#### 3.1.2 提交应用

进入spark-home

```shell
cd $SPARK_HOME
```

提交应用

```shell
./bin/spark-submit\
 --master yarn\
 --name spark-yarn\
 /Users/shirukai/Desktop/HollySys/Repository/learn-demo-pyspark/wordcount.py
```

报错：

![](http://shirukai.gitee.io/images/01b123c43dfa5c1fd4645cf8f1762bc6.jpg)

从错误信息中可以看出，我们的worker的python版本跟driver的Python版本不一致，这时候需要我们设置环境变量。PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON，修改$SPARK_HOME/conf/spark-env.sh文件，在其中添加如下内容，指定一下python环境：

```shell
export PYSPARK_PYTHON=/Users/shirukai/anaconda3/bin/python
export PYSPARK_DRIVER_PYTHON=/Users/shirukai/anaconda3/bin/python
```

然后再次启动，执行成功，查看YARN的界面

![](http://shirukai.gitee.io/images/9d84c666e7c2a06d96b3438acfca798a.jpg)

#### 3.1.3 deploy-mode

--master yarn-client 或者 --master yarn-cluster

yarn支持client（默认）和cluster模式：dirver运行在哪里

client：提交作业的进程是不能停止的，否则作业就挂了

cluster：提交完作业，那么提交作业端就可以断开了，因为driver是运行在am里的。

#### 3.1.4 使用YARN查看application日志

例如我们的applicationId为：application_1535511788876_0002

```shell
yarn logs -applicationId application_1535511788876_0002
```

发现报错：

```shell
18/08/29 11:31:40 INFO client.RMProxy: Connecting to ResourceManager at /0.0.0.0:8032
18/08/29 11:31:40 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
/tmp/logs/hdfs/logs/application_1535511788876_0002 does not exist.
Log aggregation has not completed or is not enabled.
```

原因是我们的日志聚合功能没有开启，需要设置Yarn的JobHistory：//todo

#### 思考：

如何规避如下问题：

Neither spark.yarn.jars nor spark.yarn.archive is set, falling back to uploading libraries under SPARK_HOME.