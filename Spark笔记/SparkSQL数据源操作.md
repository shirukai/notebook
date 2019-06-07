# SparkSQL数据源操作

> 版本说明： spark-2.3.0

SparkSQL支持很多数据源，我们可以使用Spark内置的数据源，目前Spark支持的数据源有：json，parquet，jdbc，orc，libsvm，csv，text。也可以指定自定义的数据源，只需要在读取数据源的时候，指定数据源的全名。在https://spark-packages.org/这个网站，我们可以获取到更多的第三方的数据源。

官网文档：http://spark.apache.org/docs/latest/sql-programming-guide.html#data-sources

收藏笔记：https://blog.csdn.net/wsdc0521/article/details/50011349

## 1 JSON数据源

### 1.1 以json格式写入

先手动生成一个DataFrame，然后以json格式写入文件

```scala
import spark.implicits._
val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
df.show()
//以json格式写入文件
df.write.format("json").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/json")
```

保存数据时，可以指定SaveMode，如:

```scala
df.write.format("json").mode("errorifexists").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/json")
```

这里指定了SaveMode为errorifexists也就是如果文件已经存在，就报错，这种保存模式也是系统默认的。常见的SaveMode有：

| SaveMode      | 描述                                                         |
| ------------- | ------------------------------------------------------------ |
| errorifexists | 默认，如果文件存在报错                                       |
| append        | 将DataFrame保存到数据源时，如果数据/表已存在，则DataFrame的内容应附加到现有数据。 |
| overwrite     | 覆盖模式意味着在将DataFrame保存到数据源时，如果数据/表已经存在，则预期现有数据将被DataFrame的内容覆盖。 |
| ignore        | 忽略模式意味着在将DataFrame保存到数据源时，如果数据已存在，则预期保存操作不会保存DataFrame的内容并且不会更改现有数据。这与`CREATE TABLE IF NOT EXISTS`SQL中的类似。 |

### 1.2 以json格式读取

读取上面我们写入的json文件

```json
  //读取json数据源
    val jsonDF = spark.read.format("json").load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/json")
    jsonDF.show()
    /**
      * +---+----+-----------+
      * |age|name|      phone|
      * +---+----+-----------+
      * | 20|Ming|15552211521|
      * | 19|hong|13287994007|
      * | 21| zhi|15552211523|
      * +---+----+-----------+
      */
```

## 2 CSV数据源

### 2.1 以csv格式写入

手动生成一个DataFrame然后以csv格式写入文件

```scala
import spark.implicits._
val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
df.show()
//以csv格式写入文件
df.write.format("csv").mode("overwrite").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/csv")
```

### 2.2 以csv格式读取

读取我们上面写入的csv文件

```scala
 //读取csv数据源
    val csvDF = spark.read.format("csv").options(Map("sep"->",","inferSchema"->"true","header"->"true")).load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/csv")
    csvDF.show()
```

在读取csv文件时我们可以指定option参数：

| Option      | 描述                                                         |
| ----------- | ------------------------------------------------------------ |
| sep         | 分隔符，csv文件数据之间的分隔符                              |
| inferSchema | 推测schema，默认为false，不推测schema所有数据类型将都为String |
| header      | 是否包含表头，默认为false                                    |

## 3 Text数据源

### 3.1 以Text格式写入

将手动生成的DataFrame以text格式写入文件

```scala
 import spark.implicits._
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()
    val textDF = df.map(_.toSeq.foldLeft("")(_+","+_).substring(1))
    //以text格式写入文件
    textDF.write.format("text").mode("overwrite").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/text")

```

写入text格式时，要求我们的DataFrame只有一列，否则会报如下错误：

![](http://shirukai.gitee.io/images/8e24c4deef04f2f96954208e6b4652d7.jpg)

### 3.2 以Text格式读取，并转为DataFrame

Spark SQL 读取text文件，只有一列，这是我们可以通过进一步的处理，转化为以“,”分割的多列DataFrame

```scala
//读取text文件
val text = spark.read.format("text").load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/text")
text.show()
lazy val first = textDF.first()
val numAttrs = first.split(",").length
import org.apache.spark.sql.functions._
var newDF = textDF.withColumn("splitCols", split($"value", ","))
0.until(numAttrs).foreach(x => {
  newDF = newDF.withColumn("col" + "_" + x, $"splitCols".getItem(x))
})
newDF.show()

/**
  * +-------------------+--------------------+-----+-----+-----------+
  * |              value|           splitCols|col_0|col_1|      col_2|
  * +-------------------+--------------------+-----+-----+-----------+
  * |Ming,20,15552211521|[Ming, 20, 155522...| Ming|   20|15552211521|
  * |hong,19,13287994007|[hong, 19, 132879...| hong|   19|13287994007|
  * | zhi,21,15552211523|[zhi, 21, 1555221...|  zhi|   21|15552211523|
  * +-------------------+--------------------+-----+-----+-----------+
  */
```

## 4 Parquet数据源

Spark 默认的数据源操作为Parquet格式，也就是说，当我们read或者write的时候，不指定数据源类型，Spark默认会使用Parquet格式来处理。

### 4.1 以Parquet格式写入

```scala
import spark.implicits._
//从内存中创建一个DataFrame
val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
df.show()
//以Parquet的格式写入
df.write.format("parquet").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet")
```

### 4.2 以Parquet格式读取

```scala
//读取Parquet
val parquetDF = spark.read.format("parquet").load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet")
parquetDF.printSchema()

/**
  * root
  * |-- name: string (nullable = true)
  * |-- age: integer (nullable = true)
  * |-- phone: long (nullable = true)
  */
```

### 4.3 模式合并

官网的例子：

```scala
 // Create a simple DataFrame, store into a partition directory
    val squaresDF = spark.sparkContext.makeRDD(1 to 5).map(i => (i, i * i)).toDF("value", "square")
    squaresDF.write.parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet/test_table/key=1")

    // Create another DataFrame in a new partition directory,
    // adding a new column and dropping an existing column
    val cubesDF = spark.sparkContext.makeRDD(6 to 10).map(i => (i, i * i * i)).toDF("value", "cube")
    cubesDF.write.parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet/test_table/key=2")

    // Read the partitioned table
    val mergedDF = spark.read.option("mergeSchema", "true").parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet/test_table")
    mergedDF.printSchema()

    /***
      * root
      * |-- value: integer (nullable = true)
      * |-- square: integer (nullable = true)
      * |-- cube: integer (nullable = true)
      * |-- key: integer (nullable = true)
      */
```



## 5 JDBC数据源

### 5.1 以JDBC数据源写入

```scala
import spark.implicits._
//从内存中创建一个DataFrame
val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
df.show()
val connectionProperties = new Properties()
connectionProperties.put("user", "root")
connectionProperties.put("password", "hollysys")
//写入mysql数据库
df.write.jdbc("jdbc:mysql://localhost:3306/springboot?useSSL=false&characterEncoding=utf-8","spark_people",connectionProperties)
```

执行后会在数据库中，自动创建表，并将数据写入到表中：

![](http://shirukai.gitee.io/images/d6d171fea218376e624e0d65e2d21e9b.jpg)

### 5.2 以JDBC数据源读取

使用Spark读取我们上面写入数据库表中的数据

```scala
//读取mysql数据库表数据
val mysqlDF = spark.read.jdbc("jdbc:mysql://localhost:3306/springboot?useSSL=false&characterEncoding=utf-8","spark_people",connectionProperties)
mysqlDF.show()

/**
  * +----+---+-----------+
  * |name|age|      phone|
  * +----+---+-----------+
  * |Ming| 20|15552211521|
  * |hong| 19|13287994007|
  * | zhi| 21|15552211523|
  * +----+---+-----------+
  */
```

完整代码：

```scala
package com.hollysys.spark.sql

import java.util.Properties

import org.apache.spark.sql.SparkSession

/**
  * Created by shirukai on 2018/9/11
  * Spark SQL 对数据源操作
  */
object DataSourceApp {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName(this.getClass.getSimpleName).master("local").getOrCreate()
    jsonExample(spark)
    //csvExample(spark)
    //textExample(spark)
    //parquetExample(spark)
    //jdbcExample(spark)
  }

  def jsonExample(spark: SparkSession): Unit = {
    import spark.implicits._
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()
    //以json格式写入文件
    df.write.format("json").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/json")

    //读取json数据源
    val jsonDF = spark.read.format("json").load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/json")
    jsonDF.printSchema()
    jsonDF.show()

    /**
      * +---+----+-----------+
      * |age|name|      phone|
      * +---+----+-----------+
      * | 20|Ming|15552211521|
      * | 19|hong|13287994007|
      * | 21| zhi|15552211523|
      * +---+----+-----------+
      */
  }

  def csvExample(spark: SparkSession): Unit = {
    import spark.implicits._
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()
    //以csv格式写入文件
    df.write.format("csv").mode("overwrite").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/csv")
    //读取csv数据源
    val csvDF = spark.read.format("csv").options(Map("sep" -> ";", "inferSchema" -> "true", "header" -> "true")).load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/csv")
    csvDF.show()
  }

  def textExample(spark: SparkSession): Unit = {
    import spark.implicits._
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()
    val textDF = df.map(_.toSeq.foldLeft("")(_ + "," + _).substring(1))
    //以text格式写入文件
    textDF.write.format("text").mode("overwrite").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/text")
    //读取text文件
    val text = spark.read.format("text").load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/text")
    text.show()
    lazy val first = textDF.first()
    val numAttrs = first.split(",").length
    import org.apache.spark.sql.functions._
    var newDF = textDF.withColumn("splitCols", split($"value", ","))
    0.until(numAttrs).foreach(x => {
      newDF = newDF.withColumn("col" + "_" + x, $"splitCols".getItem(x))
    })
    newDF.show()

    /**
      * +-------------------+--------------------+-----+-----+-----------+
      * |              value|           splitCols|col_0|col_1|      col_2|
      * +-------------------+--------------------+-----+-----+-----------+
      * |Ming,20,15552211521|[Ming, 20, 155522...| Ming|   20|15552211521|
      * |hong,19,13287994007|[hong, 19, 132879...| hong|   19|13287994007|
      * | zhi,21,15552211523|[zhi, 21, 1555221...|  zhi|   21|15552211523|
      * +-------------------+--------------------+-----+-----+-----------+
      */
  }

  def parquetExample(spark: SparkSession): Unit = {
    import spark.implicits._
    //从内存中创建一个DataFrame
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()
    //以Parquet的格式写入
    df.write.format("parquet").mode("overwrite").save("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet")

    //读取Parquet
    val parquetDF = spark.read.format("parquet").load("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet")
    parquetDF.printSchema()

    /**
      * root
      * |-- name: string (nullable = true)
      * |-- age: integer (nullable = true)
      * |-- phone: long (nullable = true)
      */

    // Create a simple DataFrame, store into a partition directory
    val squaresDF = spark.sparkContext.makeRDD(1 to 5).map(i => (i, i * i)).toDF("value", "square")
    squaresDF.write.parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet/test_table/key=1")

    // Create another DataFrame in a new partition directory,
    // adding a new column and dropping an existing column
    val cubesDF = spark.sparkContext.makeRDD(6 to 10).map(i => (i, i * i * i)).toDF("value", "cube")
    cubesDF.write.parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet/test_table/key=2")

    // Read the partitioned table
    val mergedDF = spark.read.option("mergeSchema", "true").parquet("/Users/shirukai/Desktop/HollySys/Repository/learn-demo-spark/data/parquet/test_table")
    mergedDF.printSchema()

    /** *
      * root
      * |-- value: integer (nullable = true)
      * |-- square: integer (nullable = true)
      * |-- cube: integer (nullable = true)
      * |-- key: integer (nullable = true)
      */
  }

  def jdbcExample(spark: SparkSession): Unit = {
    import spark.implicits._
    //从内存中创建一个DataFrame
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()
    val connectionProperties = new Properties()
    connectionProperties.put("user", "root")
    connectionProperties.put("password", "hollysys")
    //写入mysql数据库
    df.write.mode("overwrite").jdbc("jdbc:mysql://localhost:3306/springboot?useSSL=false&characterEncoding=utf-8", "spark_people", connectionProperties)

    //读取mysql数据库表数据
    val mysqlDF = spark.read.jdbc("jdbc:mysql://localhost:3306/springboot?useSSL=false&characterEncoding=utf-8", "spark_people", connectionProperties)
    mysqlDF.show()

    /**
      * +----+---+-----------+
      * |name|age|      phone|
      * +----+---+-----------+
      * |Ming| 20|15552211521|
      * |hong| 19|13287994007|
      * | zhi| 21|15552211523|
      * +----+---+-----------+
      */

  }
}
```