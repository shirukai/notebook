# Spark读写Elasticsearch

> 版本说明

Spark:2.3.1

Elasticsearch: elasticsearch-6.4.0

## 1 Scala环境下Spark读写Elasticsearch

### 1.1 依赖包

#### 1.1.1 Spark依赖

```xml
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.11</artifactId>
    <version>${spark.version}</version>
    <exclusions>
        <exclusion>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

#### 1.1.2 Elasticeach依赖

```xml
<!--elasticsearch-->
<dependency>
    <groupId>org.elasticsearch</groupId>
    <artifactId>elasticsearch-hadoop</artifactId>
    <version>6.4.0</version>
</dependency>
```

### 1.2 RDD读写ES

使用RDD读写ES，主要是使用了SparkContext()的esRDD()和saveToEs()两个方法。但是这个两个方法需要引入es的包之后才有

```scala
import org.elasticsearch.spark._
```

#### 1.2.1 写数据到ES

在这之前先写一个case class 用于创建RDD

```scala
case class Course(name: String, credit: Int)
```

```scala
 val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local")
    conf.set("es.nodes", "192.168.1.188")
    conf.set("es.port", "9200")
    conf.set("es.index.auto.create", "true")
    val sc = new SparkContext(conf)
 	//rdd写es
    val courseRdd = sc.makeRDD(Seq(Course("Hadoop", 4), Course("Spark", 3), Course("Kafka", 4)))
    courseRdd.saveToEs("/course/rdd")
    
```

#### 1.2.2 从ES读数据

```scala
 //rdd读es
    val esCourseRdd = sc.esRDD("/course/rdd")
    esCourseRdd.foreach(c => {
      println(c.toString())
    })
    /**
      * (vNHejmUBdoXqZPoSocAx,Map(name -> Kafka, credit -> 4))
      * (u9HejmUBdoXqZPoSocAx,Map(name -> Spark, credit -> 3))
      * (utHejmUBdoXqZPoSocAx,Map(name -> Hadoop, credit -> 4))
      */

```

### 1.3 DataFrame读写ES

如果想使用spark sql读写ES同样需要引入es的包

```scala
    import org.elasticsearch.spark.sql._
```

#### 1.3.1 DataFrame写数据到ES

```scala
  //dataframe写es
    val df = spark.read.format("csv").option("header", true).option("inferSchema", true).load("hdfs://192.168.1.188:9000/data/Beijing_2017_HourlyPM25_created20170803.csv")
    df.select("Year", "Month", "Day", "Hour", "Value").saveToEs("/csv/dataframe")
  
```

#### 1.3.2 DataFrame从ES读数据

```scala
//dataframe读es
    val esDf = spark.esDF("/csv/dataframe")
    esDf.show()

    /**
      * +---+----+-----+-----+----+
      * |Day|Hour|Month|Value|Year|
      * +---+----+-----+-----+----+
      * |  1|   0|    1|  505|2017|
      * |  1|   2|    1|  466|2017|
      * |  1|  14|    1|  596|2017|
      * |  1|  17|    1|  522|2017|
      * |  1|  21|    1|  452|2017|
      * |  2|   1|    1|  466|2017|
      * |  2|   7|    1|   93|2017|
      * |  2|   8|    1|   27|2017|
      * |  2|   9|    1|   17|2017|
      * |  2|  13|    1|  251|2017|
      * |  2|  16|    1|  251|2017|
      * |  3|   2|    1|  341|2017|
      * |  3|   8|    1|  365|2017|
      * |  3|   9|    1|  361|2017|
      * |  3|  21|    1|  542|2017|
      * |  3|  22|    1|  548|2017|
      * |  4|   3|    1|  590|2017|
      * |  4|   6|    1|  482|2017|
      * |  4|  17|    1|  323|2017|
      * |  4|  22|    1|  369|2017|
      * +---+----+-----+-----+----+
      */
```

### 1.4 完整代码

```scala
package com.hollysys.spark.elasticsearch

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession

/**
  * Created by shirukai on 2018/8/31
  * spark 读写ES
  */
object EsTest {
  def main(args: Array[String]): Unit = {
    import org.elasticsearch.spark._
    import org.elasticsearch.spark.sql._
    val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local")
    conf.set("es.nodes", "192.168.1.188")
    conf.set("es.port", "9200")
    conf.set("es.index.auto.create", "true")
    val sc = new SparkContext(conf)
    val spark = SparkSession.builder.config(conf).getOrCreate()


    //rdd写es
    val courseRdd = sc.makeRDD(Seq(Course("Hadoop", 4), Course("Spark", 3), Course("Kafka", 4)))
    courseRdd.saveToEs("/course/rdd")

    //rdd读es
    val esCourseRdd = sc.esRDD("/course/rdd")
    esCourseRdd.foreach(c => {
      println(c.toString())
    })
    /**
      * (vNHejmUBdoXqZPoSocAx,Map(name -> Kafka, credit -> 4))
      * (u9HejmUBdoXqZPoSocAx,Map(name -> Spark, credit -> 3))
      * (utHejmUBdoXqZPoSocAx,Map(name -> Hadoop, credit -> 4))
      */

    //dataframe写es
    val df = spark.read.format("csv").option("header", true).option("inferSchema", true).load("hdfs://192.168.1.188:9000/data/Beijing_2017_HourlyPM25_created20170803.csv")
    df.select("Year", "Month", "Day", "Hour", "Value").saveToEs("/csv/dataframe")
    //dataframe读es
    val esDf = spark.esDF("/csv/dataframe")
    esDf.show()

    /**
      * +---+----+-----+-----+----+
      * |Day|Hour|Month|Value|Year|
      * +---+----+-----+-----+----+
      * |  1|   0|    1|  505|2017|
      * |  1|   2|    1|  466|2017|
      * |  1|  14|    1|  596|2017|
      * |  1|  17|    1|  522|2017|
      * |  1|  21|    1|  452|2017|
      * |  2|   1|    1|  466|2017|
      * |  2|   7|    1|   93|2017|
      * |  2|   8|    1|   27|2017|
      * |  2|   9|    1|   17|2017|
      * |  2|  13|    1|  251|2017|
      * |  2|  16|    1|  251|2017|
      * |  3|   2|    1|  341|2017|
      * |  3|   8|    1|  365|2017|
      * |  3|   9|    1|  361|2017|
      * |  3|  21|    1|  542|2017|
      * |  3|  22|    1|  548|2017|
      * |  4|   3|    1|  590|2017|
      * |  4|   6|    1|  482|2017|
      * |  4|  17|    1|  323|2017|
      * |  4|  22|    1|  369|2017|
      * +---+----+-----+-----+----+
      */
  }

}

case class Course(name: String, credit: Int)

```

## 2 pyspark写数据到Elasticsearch

使用pyspark写数据到Elasticsearch主要是利用的写入外部数据源，需要org.elasticsearch.spark.sql相关的jar包

### 2.1 下载相关jar包

使用pyspark写数据到es需要依赖elasticsearch-spark-20_2.11.jar包，可以到maven仓库下载。

下载地址：http://mvnrepository.com/artifact/org.elasticsearch/elasticsearch-spark-20_2.11/6.4.0

### 2.2 pyspark中使用

pyspark2es.py

```python
# encoding: utf-8
"""
Created by shirukai on 2018/8/31
"""
from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName("pyspark2es").getOrCreate()
    data = [
        (1, "Kafka"),
        (2, "Spark"),
        (3, "Hadoop")
    ]
    df = spark.createDataFrame(data, schema=['id', 'name'])
    df.write.format("org.elasticsearch.spark.sql").option("es.nodes", "192.168.1.196:9200").mode("overwrite").save(
        "pyspark2es/python")
    spark.stop()

```

使用spark-submit提交任务

```shell
bin/spark-submit --master local --jars /Users/shirukai/apps/spark-2.3.1/jars/elasticsearch-spark-20_2.11-6.4.0.jar  /Users/shirukai/apps/spark-2.3.1/script/pyspark2es.py
```



