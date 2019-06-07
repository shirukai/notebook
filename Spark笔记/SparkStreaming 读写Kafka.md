# Spark/Streaming 读写Kafka

> 版本说明

kafka：2.12-2.0.0

spark：

```xml
<spark.version>2.3.0</spark.version>
```

scala依赖包：

```xml
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-streaming-kafka-0-10_2.11</artifactId>
    <version>${spark.version}</version>
</dependency>
```

java 依赖包：

```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>2.0.0</version>
</dependency>
```

## 1 Spark 写数据到Kafka

Spark写数据到kafka，只是将原生写法进行lazy val包装，然后使用广播变量的形式，将KafkaProducer广播到每一个Executor。实现内容如下：

### 1.1 包装KafkaProducer

KafkaSink.scala

```scala
package com.hollysys.spark.kafka

import java.util.concurrent.Future
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord, RecordMetadata}
/**
  * Created by shirukai on 2018/8/31
  * kafka producer（借鉴网络）
  */
class KafkaSink[K, V](createProducer: () => KafkaProducer[K, V]) extends Serializable {
  /* This is the key idea that allows us to work around running into
     NotSerializableExceptions. */
  lazy val producer = createProducer()

  def send(topic: String, key: K, value: V): Future[RecordMetadata] =
    producer.send(new ProducerRecord[K, V](topic, key, value))

  def send(topic: String, value: V): Future[RecordMetadata] =
    producer.send(new ProducerRecord[K, V](topic, value))
}

object KafkaSink {

  import scala.collection.JavaConversions._

  def apply[K, V](config: Map[String, Object]): KafkaSink[K, V] = {
    val createProducerFunc = () => {
      val producer = new KafkaProducer[K, V](config)
      sys.addShutdownHook {
        // Ensure that, on executor JVM shutdown, the Kafka producer sends
        // any buffered messages to Kafka before shutting down.
        producer.close()
      }
      producer
    }
    new KafkaSink(createProducerFunc)
  }

  def apply[K, V](config: java.util.Properties): KafkaSink[K, V] = apply(config.toMap)
}
```

### 1.2 Spark向Kafka发送数据

KafkaTest.scala

```scala
package com.hollysys.spark.kafka

import java.util.Properties

import org.apache.kafka.common.serialization.StringSerializer
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.sql.SparkSession

/**
  * Created by shirukai on 2018/8/31
  */
object KafkaTest {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local")
    val sc = new SparkContext(conf)
    val spark = SparkSession.builder.config(conf).getOrCreate()
    // 广播KafkaSink
    val kafkaProducer: Broadcast[KafkaSink[String, String]] = {
      val kafkaProducerConfig = {
        val p = new Properties()
        p.setProperty("bootstrap.servers", "localhost:9092")
        p.setProperty("key.serializer", classOf[StringSerializer].getName)
        p.setProperty("value.serializer", classOf[StringSerializer].getName)
        p
      }
      sc.broadcast(KafkaSink[String, String](kafkaProducerConfig))
    }
    //读取数据
    val df = spark.read.format("csv").option("header", true).option("inferSchema", true).load("hdfs://192.168.1.188:9000/data/Beijing_2017_HourlyPM25_created20170803.csv")
    df.foreach(row => {
      Thread.sleep(1000)
      printf("send data:" + row.toString())
      kafkaProducer.value.send("spark_kafka", System.currentTimeMillis().toString, row.toString())
    })
  }
}
```

## 2 Spark Streaming 从Kafka读取数据

```scala
package com.hollysys.streaming

import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent

/**
  * Created by shirukai on 2018/8/23
  */
object SparkStreamingTest {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local[2]").setAppName("NetworkWordCount")
    val ssc = new StreamingContext(conf, Seconds(2))
    val kafkaParams = Map[String, Object](
      "bootstrap.servers" -> "localhost:9092",
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "spark_streaming",
      "auto.offset.reset" -> "earliest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val topics = Array("Streaming")
    val stream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](topics, kafkaParams)
    )

    stream.map(record => (record.key, record.value()))
    stream.foreachRDD(rdd => {
      rdd.foreach(data=>{
        println(data.key())
        println(data.value())
      })
    })
    ssc.start()
    ssc.awaitTermination()
  }
}
```

