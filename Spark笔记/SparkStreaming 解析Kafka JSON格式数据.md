# SparkStreaming 解析Kafka JSON格式数据

> 项目记录：在项目中，SparkStreaming整合Kafka时，通常Kafka发送的数据是以JSON字符串形式发送的，这里总结了五种SparkStreaming解析Kafka中JSON格式数据并转为DataFrame进行数据分析的方法。

需求：将如下JSON格式的数据

![](http://shirukai.gitee.io/images/9744009fbbabe64d3bdd00163d4067b3.jpg)

转成如下所示的DataFrame

![](http://shirukai.gitee.io/images/8f8edce3f9d84668c263502d633b8384.jpg)

## 1 使用Python脚本创建造数器

随机生成如上图所示的JSON格式的数据，并将它发送到Kafka。造数器脚本代码如下所示：

kafka_data_generator.py

```python
"""
造数器：向kafka发送json格式数据

数据格式如下所示：
{
    "namespace":"000001",
    "region"："Beijing",
    "id":"9d58f83e-fb3b-45d8-b7e4-13d33b0dd832",
    "valueType":"Float",
    "value":"48.5",
    "time":"2018-11-05 15:04:47"
}
"""
import uuid
import time
import random
from pykafka import KafkaClient
import json

sample_type = ['Float', 'String', 'Int']
sample_namespace = ['000000', '000001', '000002']
sample_region = ['Beijing', 'Shanghai', 'Jinan', 'Qingdao', 'Yantai', 'Hangzhou']
sample_id_info = [
    {'3f7e7feb-fce6-4421-8321-3ac7c712f57a': {'valueType': 'Float', 'region': 'Shanghai', 'namespace': '000001'}},
    {'42f3937e-301c-489e-976b-d18f47df626f': {'valueType': 'Float', 'region': 'Beijing', 'namespace': '000000'}},
    {'d61e5ac7-4357-4d48-a6d9-3e070927f087': {'valueType': 'Int', 'region': 'Beijing', 'namespace': '000000'}},
    {'ddfca6fe-baf5-4853-8463-465ddf8234b4': {'valueType': 'String', 'region': 'Hangzhou', 'namespace': '000001'}},
    {'15f7ef13-2100-464c-84d7-ce99d494f702': {'valueType': 'Int', 'region': 'Qingdao', 'namespace': '000001'}},
    {'abb43869-dd0b-4f43-ab9d-e4682cb9c844': {'valueType': 'Int', 'region': 'Beijing', 'namespace': '000000'}},
    {'b63c1a92-c76c-4db3-a8ac-66d67c9dc6e6': {'valueType': 'Int', 'region': 'Yantai', 'namespace': '000001'}},
    {'0cf781ae-8202-4986-8df5-7ca0b21c094e': {'valueType': 'String', 'region': 'Yantai', 'namespace': '000002'}},
    {'42073ecd-0f23-49d6-a8ba-a8cbee6446e3': {'valueType': 'Float', 'region': 'Beijing', 'namespace': '000000'}},
    {'bd1fc887-d980-4488-8b03-2254165da582': {'valueType': 'String', 'region': 'Shanghai', 'namespace': '000000'}},
    {'eec90363-48bc-44b7-90dd-f79288d34f39': {'valueType': 'String', 'region': 'Shanghai', 'namespace': '000002'}},
    {'fb15d27f-d2e3-4048-85b8-64f4faa526d1': {'valueType': 'Float', 'region': 'Jinan', 'namespace': '000001'}},
    {'c5a623fd-d67b-4d83-8b42-3345352b8db9': {'valueType': 'String', 'region': 'Qingdao', 'namespace': '000001'}},
    {'fee3ecb2-dd1a-4421-a8bd-cf8bc6648320': {'valueType': 'Float', 'region': 'Yantai', 'namespace': '000001'}},
    {'e62818ab-a42a-4342-be31-ba46e0ae7720': {'valueType': 'Float', 'region': 'Qingdao', 'namespace': '000001'}},
    {'83be5bdc-737c-4616-a576-a15a2c1a1684': {'valueType': 'String', 'region': 'Hangzhou', 'namespace': '000001'}},
    {'14dcd861-14eb-40f3-a556-e52013646e6d': {'valueType': 'String', 'region': 'Beijing', 'namespace': '000002'}},
    {'8117826d-4842-4907-b6eb-446fead74244': {'valueType': 'String', 'region': 'Beijing', 'namespace': '000001'}},
    {'fb23b254-a873-4fba-a17d-73fdccbfe768': {'valueType': 'Int', 'region': 'Yantai', 'namespace': '000000'}},
    {'0685c868-2f74-4f91-a531-772796b1c8a4': {'valueType': 'String', 'region': 'Shanghai', 'namespace': '000001'}}]


def generate_id_info(amount=20):
    """
    生成id 信息，只执行一次
    :return:
    [{
    "id":{
        "type":"Int",
        "region":"Hangzhou"
    }
    }]
    """
    return [{str(uuid.uuid4()): {"valueType": random.sample(sample_type, 1)[0],
                                 "region": random.sample(sample_region, 1)[0],
                                 "namespace": random.sample(sample_namespace, 1)[0]
                                 }} for i in range(amount)]


def random_value(value_type):
    value = "this is string value"
    if value_type == "Float":
        value = random.uniform(1, 100)
    if value_type == "Int":
        value = random.randint(1, 100)
    return value


def generate_data(id_info):
    data = dict()
    for _id, info in id_info.items():
        data = {"id": _id,
                "value": random_value(info['valueType']),
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                }
        data.update(info)
    return data


def random_data():
    return generate_data(random.sample(sample_id_info, 1)[0])


if __name__ == '__main__':
    client = KafkaClient(hosts="localhost:9092", zookeeper_hosts="localhost:2181")
    topic = client.topics[b"spark_streaming_kafka_json"]
    with topic.get_sync_producer() as producer:
        for i in range(1000):
            _random_data = json.dumps(random_data())
            producer.produce(bytes(_random_data, encoding="utf-8"))
            time.sleep(1)

```

查看kafka topic 中是否包含数据：

```shell
 sh kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic spark_streaming_kafka_json --from-beginning
```

![](http://shirukai.gitee.io/images/adf14b30503df314496556350c269b69.jpg)

## 2 Spark Streaming 处理JSON格式数据

### 2.1 方法一：处理JSON字符串为case class 生成RDD[case class] 然后直接转成DataFrame

思路：Spark Streaming从Kafka读到数据后，先通过自定义的handleMessage2CaseClass方法进行一次转换，将JSON字符串转换成指定格式的case class：[KafkaMessage]，然后通过foreachRDD拿到RDD[KafkaMessage]类型的的rdd，最后直接通过spark.createDataFrame(RDD[KafkaMessage])。思路来源如下图所示：

![](http://shirukai.gitee.io/images/9b6b3c5d0fccc94cc9e8f6679bab9121.jpg)

核心代码：

```scala
    /**
      * 方法一：处理JSON字符串为case class 生成RDD[case class] 然后直接转成DataFrame
      */
    stream.map(record => handleMessage2CaseClass(record.value())).foreachRDD(rdd => {
      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
      val df = spark.createDataFrame(rdd)
      df.show()
    })
```

handleMessage2CaseClass方法：

```scala
def handleMessage2CaseClass(jsonStr: String): KafkaMessage = {
    val gson = new Gson()
    gson.fromJson(jsonStr, classOf[KafkaMessage])
}
```

Case Class:

```scala
case class KafkaMessage(time: String, namespace: String, id: String, region: String, value: String, valueType: String)
```

依赖：

```xml
<!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.8.5</version>
</dependency>
```

### 2.2 方法二：处理JSON字符串为Tuple 生成RDD[Tuple] 然后转成DataFrame

思路：此方法的思路与方法一的思路相同，只不过不转为Case Class 而是转为Tuple，思路来源如下图所示：

![](http://shirukai.gitee.io/images/d45f80d7f3c8c5f4c044bbbbf84ff7f2.jpg)

核心代码：

```scala
    /**
      * 方法二：处理JSON字符串为Tuple 生成RDD[Tuple] 然后转成DataFrame
      */
    stream.map(record => handleMessage2Tuples(record.value())).foreachRDD(rdd => {
      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
      import spark.implicits._
      val df = rdd.toDF("id", "value", "time", "valueType", "region", "namespace")
      df.show()
    })
```

handleMessage2Tuples方法：

```scala
  def handleMessage2Tuples(jsonStr: String): (String, String, String, String, String, String) = {
    import scala.collection.JavaConverters._
    val list = JSON.parseObject(jsonStr, classOf[JLinkedHashMap[String, Object]]).asScala.values.map(x => String.valueOf(x)).toList
    list match {
      case List(v1, v2, v3, v4, v5, v6) => (v1, v2, v3, v4, v5, v6)
    }
  }
```

### 2.3  方法三：处理JSON字符串为Row 生成RDD[Row] 然后通过schema创建DataFrame

思路：SparkStreaming从kafka读到数据之后，先通过handlerMessage2Row自定义的方法，将JSON字符串转成Row类型，然后通过foreachRDD拿到RDD[Row]类型的RDD，最后通过Spark.createDataFrame(RDD[Row],Schema)生成DataFrame，思路来源：

![](http://shirukai.gitee.io/images/41fd698f5236a337b5d915ef95eef33c.jpg)

核心代码：

```scala
    /**
      * 方法三：处理JSON字符串为Row 生成RDD[Row] 然后通过schema创建DataFrame
      */
        val schema = StructType(List(
          StructField("id", StringType),
          StructField("value", StringType),
          StructField("time", StringType),
          StructField("valueType", StringType),
          StructField("region", StringType),
          StructField("namespace", StringType))
        )
        stream.map(record => handlerMessage2Row(record.value())).foreachRDD(rdd => {
          val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
          val df = spark.createDataFrame(rdd, schema)
          df.show()
        })
```

handlerMessage2Row方法：

```scala
  def handlerMessage2Row(jsonStr: String): Row = {
    import scala.collection.JavaConverters._
    val array = JSON.parseObject(jsonStr, classOf[JLinkedHashMap[String, Object]]).asScala.values.map(x => String.valueOf(x)).toArray
    Row(array: _*)
  }
```

### 2.4 方法四：直接将 RDD[String] 转成DataSet 然后通过schema转换

思路：直接通过foreachRDD拿到RDD[String]类型的RDD，然后通过spark.createDataSet(RDD[String])方法生成只含有一列value列的DataSet，然后通过Spark SQL 内置函数 from_json格式化json字符串，然后取每一列的值生成DataFrame。思路来源：

![](http://shirukai.gitee.io/images/8f9ba40ed2b982db9b72273b71e4f000.jpg)

![](http://shirukai.gitee.io/images/3c242f6f0484a338d49b38f098fa881e.jpg)

核心代码：

```scala
    /**
      * 方法四：直接将 RDD[String] 转成DataSet 然后通过schema转换
      */
        val schema = StructType(List(
          StructField("namespace", StringType),
          StructField("id", StringType),
          StructField("region", StringType),
          StructField("time", StringType),
          StructField("value", StringType),
          StructField("valueType", StringType))
        )
        stream.map(record => record.value()).foreachRDD(rdd => {
          val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
          import spark.implicits._
          val ds = spark.createDataset(rdd)
          ds.select(from_json('value.cast("string"), schema) as "value").select($"value.*").show()
        })

```



### 2.5 方法五：直接将 RDD[String] 转成DataSet 然后通过read.json转成DataFrame

思路：直接通过foreachRDD拿到RDD[String]类型的RDD,然后通过spark.createDataSet创建DataSet，最后通过spark.read.json(DataSet[String])方法来创建DataFrame。此方法代码量最小，不需要指定schema，不需要进行json转换。思路来源：

![](http://shirukai.gitee.io/images/ae82640fd0b83331b156df7e8969530d.jpg)

核心代码：

```scala
/**
  * 方法五：直接将 RDD[String] 转成DataSet 然后通过read.json转成DataFrame
  */
    stream.map(record => record.value()).foreachRDD(rdd => {
      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
      import spark.implicits._
      val df = spark.read.json(spark.createDataset(rdd))
      df.show()
    })
```

## 3 对生成的DataFrame进行分析

通过上面方法我们已经可以拿到一个如期所欲的DataFrame了，接下来就是使用Spark SQL 对数据进行分析处理。

### 3.1 需求1：将time列的时间由原来的2018-11-07 17:08:43字符串格式，转成：yyyyMMdd这种格式，生成新的列，并命名为day列。

实现代码：

```scala
  import org.apache.spark.sql.functions._
      import spark.implicits._
      df.select(date_format($"time".cast(DateType), "yyyyMMdd").as("day"), $"*").show()
```

结果：

![](http://shirukai.gitee.io/images/8324ef057225a8ce45e37c20e2ab60eb.jpg)

### 3.2 需求2：按照Day列和namespae列进行分区，并保存到文件。

实现代码：

```scala
df.write.mode(SaveMode.Append)
.partitionBy("namespace", "time")
.parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/Streaming")
```

结果：

![](http://shirukai.gitee.io/images/507741bef57ea98e32f314fbd6f9b682.jpg)

## 4 一些思考？

### 4.1 思考1：如果json格式为[]数组该如何处理？

上面我们处理的json字符串都是{}都是对象格式的，那么如果Kafka里的数据是以[]数组字符串的格式存储的，那么我们该如何处理呢？

这里暂且提供两种方法：

#### 4.1.1 第一种：通过handleMessage自定义方法处理JSON字符串为Array[case class]，然后通过flatmap展开，再通过foreachRDD拿到RDD[case class]格式的RDD，最后直接转成DataFrame。

handleMessage方法：

```scala
  def handleMessage(jsonStr: String): Array[KafkaMessage] = {
    val gson = new Gson()
    gson.fromJson(jsonStr, classOf[Array[KafkaMessage]])
  }
```

核心代码：

```scala
    /**
      * 补充：处理[]数组格式的json字符串，方法一：通过handleMessage自定义方法处理JSON字符串为Array[case class]，
      * 然后通过flatmap展开，再通过foreachRDD拿到RDD[case class]格式的RDD，最后直接转成DataFrame。
      */
    stream.map(record => handleMessage(record.value())).flatMap(x=>x).foreachRDD(rdd => {
      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
      val df = spark.createDataFrame(rdd)
      df.show()
    })
```

注意：这里不能直接使用flatMap(_)，需要使用flatMap(x=>x)。或者改成stream.map(_.value()).flatMap(handleMessage).foreachRDD(……）

#### 4.1.2 第二种：直接处理RDD[String]，创建DataSet，然后通过Spark SQL 内置函数from_json和指定的schema格式化json数据，然后再通过内置函数explode展开数组格式的json数据，最后通过select json中的每一个key，获得最终的DataFrame

核心代码：

```scala
    /**
      * 补充：处理[]数组格式的json字符串，方法二：第二种：直接处理RDD[String]，创建DataSet，
      * 然后通过Spark SQL 内置函数from_json和指定的schema格式化json数据，
      * 再通过内置函数explode展开数组格式的json数据，最后通过select json中的每一个key，获得最终的DataFrame
      */
    val schema = StructType(List(
      StructField("namespace", StringType),
      StructField("id", StringType),
      StructField("region", StringType),
      StructField("time", StringType),
      StructField("value", StringType),
      StructField("valueType", StringType))
    )
    stream.map(record => record.value()).foreachRDD(rdd => {
      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
      import spark.implicits._
      val ds = spark.createDataset(rdd)
      import org.apache.spark.sql.functions._
      val df = ds.select(from_json('value, ArrayType(schema)) as "value").select(explode('value)).select($"col.*")
      df.show()
    })
```

### 4.2 思考2：如果使用StructStreaming该如何处理json数据？

StructStreaming是一个结构式流，实际拿到的就是一个DataFrame，所以可以使用上面的第四种方法来解析json数据。

```scala
package com.hollysys.spark.streaming.kafkajson

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{date_format, from_json, struct}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._

/**
  * Created by shirukai on 2018/11/8
  * 使用Struct Streaming 处理 kafka中json格式的数据
  */
object HandleJSONDataByStructStreaming {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession
      .builder()
      .appName(this.getClass.getSimpleName)
      .master("local[2]")
      .getOrCreate()
    val source = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "spark_streaming_kafka_json")
      .option("startingOffsets", "earliest")
      .option("failOnDataLoss", "false")
      .load()
    import spark.implicits._
    val schema = StructType(List(
      StructField("id", StringType),
      StructField("value", StringType),
      StructField("time", StringType),
      StructField("valueType", StringType),
      StructField("region", StringType),
      StructField("namespace", StringType))
    )
    val data = source.select(from_json('value.cast("string"), schema) as "value").select($"value.*")
      .select(date_format($"time".cast(DateType), "yyyyMMdd").as("day"), $"*")
    val query = data
      .writeStream
      .format("parquet")
      .outputMode("Append")
      .option("checkpointLocation", "/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/checkpoint")
      .option("path", "/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/structstreaming")
      .trigger(Trigger.ProcessingTime(3000)).partitionBy("namespace", "day")
      .start()

    query.awaitTermination()
  }
}

```

结果：

![](http://shirukai.gitee.io/images/409a635f7c1adeef4b41bd39a3795218.jpg)

## 完整代码：

```scala
package com.hollysys.spark.streaming.kafkajson


import com.alibaba.fastjson.JSON
import com.google.gson.Gson
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.sql.{Row, SaveMode, SparkSession}
import org.apache.spark.sql.types._
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.{Seconds, StreamingContext}
import java.util.{LinkedHashMap => JLinkedHashMap}

/**
  * Created by shirukai on 2018/11/7
  * Spark Streaming 处理 kafka json格式数据,并转成DataFrame
  */
object JSONDataHandler {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local[2]").setAppName("JSONDataHandler")
    val ssc = new StreamingContext(conf, Seconds(2))

    val kafkaParams = Map[String, Object](
      "bootstrap.servers" -> "localhost:9092",
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "spark_streaming",
      "auto.offset.reset" -> "earliest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val topics = Array("spark_streaming_kafka_json")
    val stream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](topics, kafkaParams)
    )


    /**
      * 方法一：处理JSON字符串为case class 生成RDD[case class] 然后直接转成DataFrame
      */
    stream.map(record => handleMessage2CaseClass(record.value())).foreachRDD(rdd => {
      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
      val df = spark.createDataFrame(rdd)
      import org.apache.spark.sql.functions._
      import spark.implicits._
      df.select(date_format($"time".cast(DateType), "yyyyMMdd").as("day"), $"*")
        .write.mode(SaveMode.Append)
        .partitionBy("namespace", "day")
        .parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/Streaming")
    })


    /**
      * 方法二：处理JSON字符串为Tuple 生成RDD[Tuple] 然后转成DataFrame
      */
    //    stream.map(record => handleMessage2Tuples(record.value())).foreachRDD(rdd => {
    //      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
    //      import spark.implicits._
    //      val df = rdd.toDF("id", "value", "time", "valueType", "region", "namespace")
    //      df.show()
    //    })

    /**
      * 方法三：处理JSON字符串为Row 生成RDD[Row] 然后通过schema创建DataFrame
      */
    //        val schema = StructType(List(
    //          StructField("id", StringType),
    //          StructField("value", StringType),
    //          StructField("time", StringType),
    //          StructField("valueType", StringType),
    //          StructField("region", StringType),
    //          StructField("namespace", StringType))
    //        )
    //        stream.map(record => handlerMessage2Row(record.value())).foreachRDD(rdd => {
    //          val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
    //          val df = spark.createDataFrame(rdd, schema)
    //          df.show()
    //        })

    /**
      * 方法四：直接将 RDD[String] 转成DataSet 然后通过schema转换
      */
    //        val schema = StructType(List(
    //          StructField("namespace", StringType),
    //          StructField("id", StringType),
    //          StructField("region", StringType),
    //          StructField("time", StringType),
    //          StructField("value", StringType),
    //          StructField("valueType", StringType))
    //        )
    //        stream.map(record => record.value()).foreachRDD(rdd => {
    //          val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
    //          import spark.implicits._
    //          val ds = spark.createDataset(rdd)
    //          ds.select(from_json('value.cast("string"), schema) as "value").select($"value.*").show()
    //        })

    /**
      * 方法五：直接将 RDD[String] 转成DataSet 然后通过read.json转成DataFrame
      */
    //        stream.map(record => record.value()).foreachRDD(rdd => {
    //          val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
    //          import spark.implicits._
    //          val df = spark.read.json(spark.createDataset(rdd))
    //          df.show()
    //        })

    /**
      * 补充：处理[]数组格式的json字符串，方法一：通过handleMessage自定义方法处理JSON字符串为Array[case class]，
      * 然后通过flatmap展开，再通过foreachRDD拿到RDD[case class]格式的RDD，最后直接转成DataFrame。
      */
    //    stream.map(record => handleMessage(record.value())).flatMap(x=>x).foreachRDD(rdd => {
    //      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
    //      val df = spark.createDataFrame(rdd)
    //      df.show()
    //    })

    /**
      * 补充：处理[]数组格式的json字符串，方法二：第二种：直接处理RDD[String]，创建DataSet，
      * 然后通过Spark SQL 内置函数from_json和指定的schema格式化json数据，
      * 再通过内置函数explode展开数组格式的json数据，最后通过select json中的每一个key，获得最终的DataFrame
      */
    //    val schema = StructType(List(
    //      StructField("namespace", StringType),
    //      StructField("id", StringType),
    //      StructField("region", StringType),
    //      StructField("time", StringType),
    //      StructField("value", StringType),
    //      StructField("valueType", StringType))
    //    )
    //    stream.map(record => record.value()).foreachRDD(rdd => {
    //      val spark = SparkSession.builder().config(rdd.sparkContext.getConf).getOrCreate()
    //      import spark.implicits._
    //      val ds = spark.createDataset(rdd)
    //      import org.apache.spark.sql.functions._
    //      val df = ds.select(from_json('value, ArrayType(schema)) as "value").select(explode('value)).select($"col.*")
    //      df.show()
    //    })

    ssc.start()
    ssc.awaitTermination()
  }

  def handleMessage(jsonStr: String): Array[KafkaMessage] = {
    val gson = new Gson()
    gson.fromJson(jsonStr, classOf[Array[KafkaMessage]])
  }

  def handleMessage2CaseClass(jsonStr: String): KafkaMessage = {
    val gson = new Gson()
    gson.fromJson(jsonStr, classOf[KafkaMessage])
  }

  def handleMessage2Tuples(jsonStr: String): (String, String, String, String, String, String) = {
    import scala.collection.JavaConverters._
    val list = JSON.parseObject(jsonStr, classOf[JLinkedHashMap[String, Object]]).asScala.values.map(x => String.valueOf(x)).toList
    list match {
      case List(v1, v2, v3, v4, v5, v6) => (v1, v2, v3, v4, v5, v6)
    }
  }

  def handlerMessage2Row(jsonStr: String): Row = {
    import scala.collection.JavaConverters._
    val array = JSON.parseObject(jsonStr, classOf[JLinkedHashMap[String, Object]]).asScala.values.map(x => String.valueOf(x)).toArray
    Row(array: _*)
  }
}

case class KafkaMessage(time: String, namespace: String, id: String, region: String, value: String, valueType: String)

```



## 总结

目前只想到了上面五种方法，如果有其它思路后续会补上。对比这五种方法，不考虑性能问题，从代码量和灵活度来看，第五种方法是比较好的，因为不需要我们指定schema信息。其次是第一种，不过需要事先定义好case class。另外，在上面的前三种方法中，我们都用到了将json转换成不同对象的方法，但是第一种用的是谷歌的gson后两种用的是阿里的fastjson。是因为，创建DataFrame的时候只支持case class，而当我们使用fastjson的JSON.pares(jsonStr,classOf[KafkaMessage])时会报错，因为fastjson无法将json字符串转成case class对象。所以这里选用的gson。

