# SparkStreaming 整合多种数据源

SparkStreaming可以处理多种数据源，比如从socket里获取数据流，从文件系统获取数据流，从Flume获取数据流、从Kafka里获取数据流等。

需要注意的是：

* SparkStreaming 在处理socket、flume、kafka、Kinesis数据源的时候，本地模式下不能用以local、或者local[1]运行，因为需要启动一个线程运行Receivers来接收数据。读取文件系统的时候，不需要启动Receivers，所以在处理文件系统数据源的时候，不需要设置多个线程。
* 将逻辑扩展到在集群上运行，分配给Spark Streaming应用程序的核心数必须大于接收器数。否则系统将接收数据，但无法处理数据。

详细的介绍可以参考官网：http://spark.apache.org/docs/latest/streaming-programming-guide.html#input-dstreams-and-receivers。

本笔记主要记录一下Spark Steaming处理Socket、文件系统、Flume、Kafka等多种数据源。

## 1 Socket Stream

本小节，将以SparkStreaming处理Socket数据为例，实现简单的WordCount、并将执行结果写入到MySQL、进行有状态的词频统计即统计单词包括之前的数据一共出现的次数、使用Transform api进行黑名单过滤操作、最后整合Spark SQL 使用 DataFrame进行词频统计等。

### 1.1 处理Socket Stream进行简单的WordCount

NetworkWordCount.scala

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/16
  * Spark Streaming 处理Socket 数据
  * nc -lk 9999
  */
object NetworkWordCount {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("NetworkWordCount").setMaster("local[2]")
    /**
      * 创建StreamingContext需要两个参数，SparkConf 和 batch interval
      */
    val ssc = new StreamingContext(conf, Seconds(2))

    // 从socket中获取数据
    val lines = ssc.socketTextStream("localhost", 9999)

    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
    wordCounts.print()

    ssc.start()
    ssc.awaitTermination()
  }
}
```

效果：

![](http://shirukai.gitee.io/images/77c4ad7584a7b4d06c63faded3405b54.gif)

### 1.2 将处理结果写到MySQL里

官网：http://spark.apache.org/docs/latest/streaming-programming-guide.html#design-patterns-for-using-foreachrdd

将数据写入MySQL我们需要使用foreachRDD去遍历RDD，然后RDD的数据写入到MySQL。

```scala
package com.hollysys.spark.streaming

import java.sql.{Connection, DriverManager}

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/16
  * 将统计结果写到MySQL中
  *
  * 创建MySQL表：
  * create table wordcount(word varchar(50) default null,wordcount int(10) default null);
  */
object ResultWriteMySQL {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(5))

    val lines = ssc.socketTextStream("localhost", 9999)

    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map((_, 1)).reduceByKey(_ + _)
    wordCounts.foreachRDD(rdd => {

      rdd.foreachPartition(iterator => {
        val connection = createConnection()
        iterator.foreach(record => {
          val sql = "insert into wordcount(word,wordcount) values ('" + record._1 + "','" + record._2 + "')"
          connection.createStatement().execute(sql)
        })
      })
    })
    ssc.start()
    ssc.awaitTermination()
  }

  /**
    * 获取数据库连接
    * @return
    */
  def createConnection(): Connection = {
    DriverManager.getConnection("jdbc:mysql://localhost:3306/spark?useSSL=false&characterEncoding=utf-8&user=root&password=hollysys")
  }
}

```

### 1.3 进行有状态的WordCount

应用场景：统计单词一种出现的次数

官网：http://spark.apache.org/docs/latest/streaming-programming-guide.html#updatestatebykey-operation

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/16
  * 使用Spark Streaming 完成有状态统计
  */
object StatefulWordCount {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(5))
    // 如果使用了stateful的算子，必须要设置checkpoint
    // 在生产环境中，建议大家把checkpoint设置到HDFS的某个文件夹中
    ssc.checkpoint("data/checkpoint")
    val lines = ssc.socketTextStream("localhost", 9999)

    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map((_, 1)).updateStateByKey(updateFunction)
    wordCounts.print()

    ssc.start()
    ssc.awaitTermination()
  }

  def updateFunction(currentValue: Seq[Int], previousValue: Option[Int]): Option[Int] = {
    val current = currentValue.sum
    val pre = previousValue.getOrElse(0)
    Some(current + pre)
  }
}
```

### 1.4 利用Transform进行黑名单过滤

官网地址：http://spark.apache.org/docs/latest/streaming-programming-guide.html#transform-operation

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/16
  * 黑名单过滤
  */
object TransformApp {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("NetworkWordCount").setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(2))
    /**
      * 创建StreamingContext需要两个参数，SparkConf 和 batch interval
      */
    val lines = ssc.socketTextStream("localhost", 9999)
    /**
      * 构建黑名单
      */
    val blacks = List("zs", "ls")
    val blacksRDD = ssc.sparkContext.parallelize(blacks).map((_, true))

    val res = lines.map(x => (x.split(",")(1), x)).transform(rdd => {
      rdd.leftOuterJoin(blacksRDD).filter(!_._2._2.getOrElse(false))
        .map(_._2._1)
    })
    res.print()
    ssc.start()
    ssc.awaitTermination()
  }
}
```

### 1.5 使用Spark SQL 处理数据

官网地址：http://spark.apache.org/docs/latest/streaming-programming-guide.html#dataframe-and-sql-operations

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/16
  * 黑名单过滤
  */
object TransformApp {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("NetworkWordCount").setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(2))
    /**
      * 创建StreamingContext需要两个参数，SparkConf 和 batch interval
      */
    val lines = ssc.socketTextStream("localhost", 9999)
    /**
      * 构建黑名单
      */
    val blacks = List("zs", "ls")
    val blacksRDD = ssc.sparkContext.parallelize(blacks).map((_, true))

    val res = lines.map(x => (x.split(",")(1), x)).transform(rdd => {
      rdd.leftOuterJoin(blacksRDD).filter(!_._2._2.getOrElse(false))
        .map(_._2._1)
    })
    res.print()
    ssc.start()
    ssc.awaitTermination()
  }
}
```

## 2 File Stream

SparkStreaming也可以使用文件系统作为数据源。本地文件系统、或者hdfs都可以。

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/16
  * 使用Spark Streaming 处理文件系统（local/hdfs）的数据
  */
object FileWordCount {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(5))

    val lines = ssc.textFileStream("file:///Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/text")
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
    wordCounts.print()

    ssc.start()
    ssc.awaitTermination()

  }
}

```

## 3 Flume Stream

### 3.1 方式一：Push方式整合Flume Agent

官网：http://spark.apache.org/docs/latest/streaming-flume-integration.html

Flume 推送数据到SparkStreaming。这时SparkStreaming需要启动一个Avro代理的接受器来接受数据。实现流程为：Flume 设置一个netcat-source，经过memory-channel，然后使用avro-sink发送数据，最后spark streaming接受数据然后处理。

#### 3.1.1 配置Flume Agent

我们需要配置一个Flume Agent 用来收集收集数据然后发送给Spark Streaming。

Flume Agent的配置选型为：netcat-source --> memory-channel --> avro-sink

在$FLUME_HOME/conf 下创建flume-push-spark.conf 

```shell
vi $FLUME_HOME/conf/flume-push-spark.conf 
```

内容如下：

```
flume2spark.sources = netcat-source
flume2spark.sinks = avro-sink
flume2spark.channels = memory-channel

# Describe/configure the source
# sources类型
flume2spark.sources.netcat-source.type = netcat
flume2spark.sources.netcat-source.bind = localhost
flume2spark.sources.netcat-source.port = 9090

flume2spark.sinks.avro-sink.type = avro
flume2spark.sinks.avro-sink.hostname = localhost
flume2spark.sinks.avro-sink.port = 9999

flume2spark.channels.memory-channel.type = memory
flume2spark.channels.memory-channel.capacity = 1000
flume2spark.channels.memory-channel.transactionCapacity = 100

flume2spark.sources.netcat-source.channels = memory-channel
flume2spark.sinks.avro-sink.channel = memory-channel
```

#### 3.1.2 Spark Streaming 代码开发

##### 3.1.2.1 引入依赖

这里我们的spark.version版本为2.3.0

```xml
<!--Spark Streaming flume-->
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-streaming-flume_2.11</artifactId>
    <version>${spark.version}</version>
</dependency>
```

##### 3.1.2.2 代码开发

创建FlumePushWordCount.scala

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.flume._

/**
  * Created by shirukai on 2018/10/17
  * Spark Streaming 整合Flume，Flume push 数据到Spark Streaming
  */
object FlumePushWordCount {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("NetworkWordCount").setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(5))

    val flumeData = FlumeUtils.createStream(ssc, "localhost", 9999)
    val result = flumeData.map(x => new String(x.event.getBody.array()).trim).flatMap(_.split(" ")).map((_, 1)).reduceByKey(_ + _)
    result.print()
    ssc.start()
    ssc.awaitTermination()
  }
}
```

#### 3.1.3 IDEA 启动运行测试

代码开发完成后，我们可以在IDEA里直接启动测试，这里我们需要先启动Spark Streaming 的应用程序，然后再启动Flume 的Agent。

##### 3.1.3.1 启动Spark Streaming应用

启动我们编写好的Spark Streaming应用的main方法。

![](http://shirukai.gitee.io/images/db512b418e34c8ce8fc5d992cb819103.jpg)



##### 3.1.3.2 启动Flume Agent

启动我们上面创建的Flume Agent

```shell
flume-ng agent \
--name flume2spark \
--conf-file /Users/shirukai/apps/flume-1.8.0/conf/flume-push-spark.conf \
-Dflume.root.logger=INFO,console
```

![](http://shirukai.gitee.io/images/db5f31f3d47b02d8f31af51f3ae3eb70.jpg)

##### 3.1.3.3 使用telnet发送数据

```shell
telnet localhost 9090
```

![](http://shirukai.gitee.io/images/06c4edc1016d2ba68a8ebc947417cc6f.jpg)

执行结果：

![](http://shirukai.gitee.io/images/c6293077f7bed7fc1bce67f76656ba9a.jpg)



#### 3.1.4 以部署的方式运行测试

上面我们使用IDEA直接运行main方法测试了我们的应用程序，下面来记录一下如何以部署的形式运行应用程序。

![](http://shirukai.gitee.io/images/9fecc182bfd607004fe24e0e0501d165.jpg)

通过官方文档我们可以看出，在使用SBT或者Maven打包项目的时候，我们需要把spark-streaming-flume_2.11及其依赖也打包到应用程序的JAR中，对于Python的应用程序在spark-submit的时候通过制定--packages来指定依赖包。接下来将演示两种方式加载依赖，一种是把依赖打包到JAR中，另一种是在提交应用程序时指定依赖包。如果不引入依赖会报如下错误：

![](http://shirukai.gitee.io/images/2310f00714fc004d1a667995326eaff7.jpg)

##### 3.1.4.1 将依赖打包到JAR中

我们可以通过maven的打包插件，将spark-streaming-flume_2.11打包到应用程序的JAR中。可以通过如下配置：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>2.4.3</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <artifactSet>
                    <includes>
                        <include>com.alibaba:fastjson</include>
                        <include>org.apache.spark:spark-streaming-flume_2.11</include>
                        <include>org.apache.flume:flume-ng-core</include>
                        <include>org.apache.flume:flume-ng-sdk</include>
                    </includes>
                </artifactSet>
            </configuration>
        </execution>
    </executions>
</plugin>
```

经测试，需要打包spark-streaming-flume_2.11、flume-ng-core\flume-ng-sdk这三个依赖包。否则回报错。

将项目打包

```shell
 mvn package -DskipTests
```

执行命令后我们会在项目的target目录下得到一个learn-demo-spark-1.0-SNAPSHOT.jar的JAR。

使用spark-submit 提交应用

```shell
spark-submit --master local --class com.hollysys.spark.streaming.FlumePushWordCount /Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/target/learn-demo-spark-1.0-SNAPSHOT.jar

```

##### 3.1.4.2 在提交应用是指定依赖

```shell
spark-submit --master local[2] --packages org.apache.spark:spark-streaming-flume_2.11:2.3.0 --class com.hollysys.spark.streaming.FlumePushWordCount /Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/target/learn-demo-spark-1.0-SNAPSHOT.jar

```

注意：如果遇到下载依赖包报错的情况， 可以到maven仓库里先把之前下载好的包删掉。

### 3.2 方式二：Pull方式整合Flume Agent

官网：http://spark.apache.org/docs/latest/streaming-flume-integration.html#approach-2-pull-based-approach-using-a-custom-sink

Flume 将数据发送到spark-sink，然后Spark Streaming 从spark-sink上拉取数据。

#### 3.2.1 配置Flume Agent

我们需要配置一个Flume Agent 用来收集收集数据然后发送给spark-sink。

Flume Agent的配置选型为：netcat-source --> memory-channel --> spark-sink

在$FLUME_HOME/conf 下创建flume-pull-spark.conf 

```shell
vi $FLUME_HOME/conf/flume-pull-spark.conf 
```

内容如下：

```
flume2spark.sources = netcat-source
flume2spark.sinks = spark-sink
flume2spark.channels = memory-channel

# Describe/configure the source
# sources类型
flume2spark.sources.netcat-source.type = netcat
flume2spark.sources.netcat-source.bind = localhost
flume2spark.sources.netcat-source.port = 9090

flume2spark.sinks.spark-sink.type = org.apache.spark.streaming.flume.sink.SparkSink
flume2spark.sinks.spark-sink.hostname = localhost
flume2spark.sinks.spark-sink.port = 9999

flume2spark.channels.memory-channel.type = memory
flume2spark.channels.memory-channel.capacity = 1000
flume2spark.channels.memory-channel.transactionCapacity = 100

flume2spark.sources.netcat-source.channels = memory-channel
flume2spark.sinks.spark-sink.channel = memory-channel
```

##### 重要！重要！重要！

为了避免下面过程中出现的错误，在这里需要将Flume依赖的jar包放到$FLUME_HOME/lib下，可以参考官网

![](http://shirukai.gitee.io/images/5dc2686a69bad9303f79664a1c25b02b.jpg)

#### 3.2.2 Spark Streaming 代码开发

##### 3.2.2.1 引入依赖

```xml
<!--Spark Streaming flume sink-->
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-streaming-flume-sink_2.11</artifactId>
    <version>${spark.version}</version>
</dependency>

<!--commons lang3-->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.7</version>
</dependency>
```

##### 3.2.2.2 代码开发

创建FlumePullWordCount.scala

```scala
package com.hollysys.spark.streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.flume._
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/17
  * Spark Streaming 整合Flume，Spark Streaming 从flume pull 数据
  */
object FlumePullWordCount {
  def main(args: Array[String]): Unit = {
//    if(args.length !=2){
//      System.err.println("Usage: FlumePushWordCount <hostname> <port>")
//      System.exit(1)
//    }
    val conf = new SparkConf().setAppName("FlumePullWordCount").setMaster("local[2]")
    val ssc = new StreamingContext(conf, Seconds(5))

    val flumeData = FlumeUtils.createPollingStream(ssc,"localhost",9999)
    val result = flumeData.map(x => new String(x.event.getBody.array()).trim).flatMap(_.split(" ")).map((_, 1)).reduceByKey(_ + _)
    result.print()
    ssc.start()
    ssc.awaitTermination()
  }
}

```

#### 3.2.3 IDEA 启动运行测试

代码开发完成后，我们可以在IDEA里直接启动测试，这里我们需要先启动Flume 的Agent，然后再启动Spark Streaming 的应用程序。与Push方式相反。

##### 3.2.3.1 启动Flume Agent 

```shell
flume-ng agent \
--name flume2spark \
--conf-file /Users/shirukai/apps/flume-1.8.0/conf/flume-pull-spark.conf \
-Dflume.root.logger=INFO,console
```

这时候会报如下错误：

![](http://shirukai.gitee.io/images/bfa02ec843a0861b632bc92c06fe7be2.jpg)

根据报错信息可以看出，我们的flume使用了spark-sink，但是没有找到org.apache.spark.streaming.flume.sink.SparkSink这个类，这时需要将依赖的spark-streaming-flume-sink_2.11.jar包复制到$FLUME_HOME/lib下。

关于如何下载jar包：

可以到https://mvnrepository.com/artifact/org.apache.spark/spark-streaming-flume-sink_2.11/2.3.0 maven仓库下载。

下载完成之后，将jar移动到$FLUME_HOME/lib下，然后重新启动。

```shell
mv spark-streaming-flume-sink_2.11-2.3.0.jar /Users/shirukai/apps/flume-1.8.0/lib/
```

##### 3.2.3.2 启动Spark Streaming 应用

![](http://shirukai.gitee.io/images/82cb3a99648325489d570948868ab4fc.jpg)

当spark streaming应用启动的时候，Flume Agent回报如下错误，原因是因为我们需要导入相应的jar包。

https://mvnrepository.com/artifact/org.scala-lang/scala-library/2.11.8

![](http://shirukai.gitee.io/images/e94c0a539016ccb4414decd500d6640d.jpg)

删除之前的版本，替换成最新下载的2.11.8

https://mvnrepository.com/artifact/org.apache.commons/commons-lang3/3.5

![](http://shirukai.gitee.io/images/7effd41259c316866f8de1cad2d7b9e2.jpg)

##### 3.2.3.3 使用telnet 发送数据

```shell
telnet localhost 9090
```

![](http://shirukai.gitee.io/images/336a603da04615bf2bfc45bdd620d577.gif)

## 4 Kafka Stream

官网：http://spark.apache.org/docs/latest/streaming-kafka-0-10-integration.html

### 4.1  Spark Streaming 代码开发

#### 4.1.1 引入依赖

```xml
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-streaming-kafka-0-10_2.11</artifactId>
    <version>2.3.0</version>
</dependency>
```

#### 3.1.2 代码开发

```scala
package com.hollysys.spark.streaming

import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.{Seconds, StreamingContext}

/**
  * Created by shirukai on 2018/10/29
  * Spark Streaming 整合Kafka 进行词频统计
  */
object KafkaDirectWordCount {
  def main(args: Array[String]): Unit = {
    if (args.length != 2) {
      System.err.println("Usage:KafkaDirectWordCount <brokers> <topics>")
      System.exit(1)
    }
    val Array(servers, topics) = args


    val conf = new SparkConf().setMaster("local[2]").setAppName("NetworkWordCount")
    val ssc = new StreamingContext(conf, Seconds(5))


    //val spark = SparkSession.builder().getOrCreate()
    val kafkaParams = Map[String, Object](
      "bootstrap.servers" -> servers,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "spark_streaming",
      "auto.offset.reset" -> "earliest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )


    val topicSet = topics.split(",").toSet
    val message = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](topicSet, kafkaParams)
    )
    message.map(_.value()).flatMap(_.split(" ")).map((_, 1)).reduceByKey(_ + _).print()

    ssc.start()
    ssc.awaitTermination()

  }
}
```

### 4.2 运行测试

#### 4.2.1 启动Kafka

##### 启动zookeeper

```shell
sh $ZK_HOME/bin/zkServer.sh start
```

##### 启动kafka

```shell
sh $KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
```

##### 创建topic

```shell
sh $KAFKA_HOME/bin/kafka-topics.sh --create  --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafka_streaming_topic
```

##### 查看topic

```shell
sh $KAFKA_HOME/bin/kafka_topics.sh --list --zookeeper localhost:2181
```

##### 使用kafka console producer 发送消息

```shell
sh $KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka_streaming_topic
```

#### 4.2.2 启动应用

![](http://shirukai.gitee.io/images/f3e7bea4b79c41ad4ec8fabdb443b19f.jpg)



![](http://shirukai.gitee.io/images/8b7138f6dd7617714f3b698133c976b7.jpg)

## 5 实战：获取应用日志，并进行实时分析

需求描述：通过Flume收集应用程序产生的日志，然后Flume将日志发送到kafka消息队里，最后Spark Streaming 分析 kafka里的数据，判断是否为WARN或者ERROR类日志，并打印输出。

实现思路：应用 通过log4j Appender 将日志信息发送给Flume，Flume使用Avro Souce接收数据，经过Memory Channel 通过 Kafka Sink 发送给Kafka，最后SparkStreaming进行数据处理，如下图所示：

![](http://shirukai.gitee.io/images/879aa5d452e2f9ddec377c6c3eb7b01b.jpg)

### 5.1 配置 Kafka

##### 启动zookeeper

```shell
sh $ZK_HOME/bin/zkServer.sh start
```

##### 启动kafka

```shell
sh $KAFKA_HOME/bin/kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
```

##### 创建topic:log-streaming

```shell
sh $KAFKA_HOME/bin/kafka-topics.sh --create  --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic log-streami
```

##### 查看topic

```shell
sh $KAFKA_HOME/bin/kafka_topics.sh --list --zookeeper localhost:2181
```

### 5.2 配置Flume Angent

在FLUME_HOME/conf/下创建log-angent.conf的配置文件，内容如下：

```properties
log-angent.sources = avro-source
log-angent.sinks = kafka-sink
log-angent.channels = memory-channel

log-angent.sources.avro-source.type = avro
log-angent.sources.avro-source.bind = localhost
log-angent.sources.avro-source.port = 9999

log-angent.sinks.kafka-sink.type = org.apache.flume.sink.kafka.KafkaSink
log-angent.sinks.kafka-sink.kafka.topic = log-streaming
log-angent.sinks.kafka-sink.kafka.bootstrap.servers = localhost:9092

log-angent.channels.memory-channel.type = memory
log-angent.channels.memory-channel.capacity = 1000
log-angent.channels.memory-channel.transactionCapacity = 100

log-angent.sources.avro-source.channels = memory-channel
log-angent.sinks.kafka-sink.channel = memory-channel
```

启动 Flume Agent

```
flume-ng agent --conf $FLUME_HOME/conf --conf-file $FLUME_HOME/conf/log-angent.conf --name log-angent
```

### 5.3 Application 整合Log4j Appender

想要收集应用里的日志，Flume官网提供了一个Log4j Appender的类用来收集应用的日志。需要我们在应用中整合Log4j Appender。官网地址：http://flume.apache.org/FlumeUserGuide.html#load-balancing-log4j-appender

#### 5.3.1 修改日志配置

修改应用中resources目录下的log4j.properties配置文件，添加如下内容：

```properties
log4j.appender.flume = org.apache.flume.clients.log4jappender.Log4jAppender
log4j.appender.flume.Hostname = localhost
log4j.appender.flume.Port = 9999
log4j.appender.flume.UnsafeMode = true
```

然后在log4j.rootCategory添加flume

```properties
log4j.rootCategory=INFO, console,flume
```

#### 5.3.2 添加log4j-appender依赖

添加log4j-appender依赖，否则会报如下错误：

![](http://shirukai.gitee.io/images/fea51c589b694c2afb4fb3261eb45a28.jpg)

依赖：

```xml
<!--flume log4j appender-->
<dependency>
    <groupId>org.apache.flume.flume-ng-clients</groupId>
    <artifactId>flume-ng-log4jappender</artifactId>
    <version>1.8.0</version>
</dependency>
```

#### 5.3.3 模拟日志生成

创建LogGenerator类，模拟日志生成，并没10条数据产生一条错误日志。

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Created by shirukai on 2018/10/30
 * 模拟产生日志
 */
public class LogGenerator {
    public static void main(String[] args) throws Exception {
        Logger LOG = LoggerFactory.getLogger(LogGenerator.class);
        int index = 0;
        while (true) {

            Thread.sleep(1000);
            if (index % 10 == 0) {
                LOG.error("value:{}", index);
            } else {
                LOG.info("value:{}", index);
            }
            index++;
        }
    }
}
```

### 5.4 开发Spark Streaming应用

创建Spark Streaming应用，用来处理kafka数据。如下所示：KafkaLogHandler

```scala
package com.hollysys.spark.streaming

import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent

/**
  * Created by shirukai on 2018/10/31
  * 处理kafka里log数据
  */
object KafkaLogHandler {
  def main(args: Array[String]): Unit = {
    if (args.length != 2) {
      System.err.println("Usage:KafkaDirectWordCount <brokers> <topics>")
      System.exit(1)
    }
    val Array(servers, topics) = args


    val conf = new SparkConf().setMaster("local[2]").setAppName("KafkaLogHandler")
    val ssc = new StreamingContext(conf, Seconds(5))


    //val spark = SparkSession.builder().getOrCreate()
    val kafkaParams = Map[String, Object](
      "bootstrap.servers" -> servers,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "spark_streaming",
      "auto.offset.reset" -> "earliest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )


    val topicSet = topics.split(",").toSet
    val message = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](topicSet, kafkaParams)
    )
    message.map(_.value()).foreachRDD(rdd => rdd.foreach(println))

    ssc.start()
    ssc.awaitTermination()
  }
}

```

### 5.5 启动测试

#### 5.5.1 启动日志模拟器

![](http://shirukai.gitee.io/images/cdb573682e7241a41bc24407f754a856.jpg)

#### 5.5.2 启动Spark Streaming 应用

![](http://shirukai.gitee.io/images/7da66cfb235ce3d3bd1b8290cba5cae4.jpg)