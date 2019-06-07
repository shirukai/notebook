# 创建DataFrame的几种方式

如要生成如下的DataFrame数据

```
+----+---+-----------+
|name|age|      phone|
+----+---+-----------+
|ming| 20|15552211521|
|hong| 19|13287994007|
| zhi| 21|15552211523|
+----+---+-----------+
```

### 第一种：通过Seq生成

```
val spark = SparkSession
  .builder()
  .appName(this.getClass.getSimpleName).master("local")
  .getOrCreate()

val df = spark.createDataFrame(Seq(
  ("ming", 20, 15552211521L),
  ("hong", 19, 13287994007L),
  ("zhi", 21, 15552211523L)
)) toDF("name", "age", "phone")

df.show()
```

### 第二种：读取Json文件生成

json文件内容

```
{"name":"ming","age":20,"phone":15552211521}
{"name":"hong", "age":19,"phone":13287994007}
{"name":"zhi", "age":21,"phone":15552211523}
```

代码

```
    val dfJson = spark.read.format("json").load("/Users/shirukai/Desktop/HollySys/Repository/sparkLearn/data/student.json")
    dfJson.show()
```

### 第三种：读取csv文件生成

csv文件

```
name,age,phone
ming,20,15552211521
hong,19,13287994007
zhi,21,15552211523
```

代码：

```
val dfCsv = spark.read.format("csv").option("header", true).load("/Users/shirukai/Desktop/HollySys/Repository/sparkLearn/data/students.csv")
dfCsv.show()
```

### 第四种：通过Json格式的RDD生成（弃用）

```
    val sc = spark.sparkContext
    import spark.implicits._
    val jsonRDD = sc.makeRDD(Array(
      "{\"name\":\"ming\",\"age\":20,\"phone\":15552211521}",
      "{\"name\":\"hong\", \"age\":19,\"phone\":13287994007}",
      "{\"name\":\"zhi\", \"age\":21,\"phone\":15552211523}"
    ))

    val jsonRddDf = spark.read.json(jsonRDD)
    jsonRddDf.show()
```



### 第五种：通过Json格式的DataSet生成

```
//第五种：通过Json格式的DataSet生成
val jsonDataSet = spark.createDataset(Array(
  "{\"name\":\"ming\",\"age\":20,\"phone\":15552211521}",
  "{\"name\":\"hong\", \"age\":19,\"phone\":13287994007}",
  "{\"name\":\"zhi\", \"age\":21,\"phone\":15552211523}"
))
val jsonDataSetDf = spark.read.json(jsonDataSet)

jsonDataSetDf.show()
```

### 第六种: 通过csv格式的DataSet生成

```
   val scvDataSet = spark.createDataset(Array(
      "ming,20,15552211521",
      "hong,19,13287994007",
      "zhi,21,15552211523"
    ))
    spark.read.csv(scvDataSet).toDF("name","age","phone").show()
```

### 第七种：动态创建schema

```
    val schema = StructType(List(
      StructField("name", StringType, true),
      StructField("age", IntegerType, true),
      StructField("phone", LongType, true)
    ))
    val dataList = new util.ArrayList[Row]()
    dataList.add(Row("ming",20,15552211521L))
    dataList.add(Row("hong",19,13287994007L))
    dataList.add(Row("zhi",21,15552211523L))
    spark.createDataFrame(dataList,schema).show()
```

### 第八种：通过jdbc创建

```
    //第八种：读取数据库（mysql）
    val options = new util.HashMap[String,String]()
    options.put("url", "jdbc:mysql://localhost:3306/spark")
    options.put("driver","com.mysql.jdbc.Driver")
    options.put("user","root")
    options.put("password","hollysys")
    options.put("dbtable","user")

    spark.read.format("jdbc").options(options).load().show()
```

### 完整代码

```
package com.hollysys.spark

import java.util

import org.apache.spark.sql.types._
import org.apache.spark.sql.{Row, SQLContext, SparkSession}

/**
  * Created by shirukai on 2018/7/17
  * 创建DataFrame的几种方式
  */
object CreateDataFrameTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName(this.getClass.getSimpleName).master("local")
      .getOrCreate()

    //第一种：通过Seq生成
    val df = spark.createDataFrame(Seq(
      ("ming", 20, 15552211521L),
      ("hong", 19, 13287994007L),
      ("zhi", 21, 15552211523L)
    )) toDF("name", "age", "phone")

    df.show()

    //第二种：通过读取Json文件生成
    val dfJson = spark.read.format("json").load("/Users/shirukai/Desktop/HollySys/Repository/sparkLearn/data/student.json")
    dfJson.show()

    //第三种：通过读取Csv文件生成
    val dfCsv = spark.read.format("csv").option("header", true).load("/Users/shirukai/Desktop/HollySys/Repository/sparkLearn/data/students.csv")
    dfCsv.show()

    //第四种：通过Json格式的RDD生成（弃用）
    val sc = spark.sparkContext
    import spark.implicits._
    val jsonRDD = sc.makeRDD(Array(
      "{\"name\":\"ming\",\"age\":20,\"phone\":15552211521}",
      "{\"name\":\"hong\", \"age\":19,\"phone\":13287994007}",
      "{\"name\":\"zhi\", \"age\":21,\"phone\":15552211523}"
    ))

    val jsonRddDf = spark.read.json(jsonRDD)
    jsonRddDf.show()

    //第五种：通过Json格式的DataSet生成
    val jsonDataSet = spark.createDataset(Array(
      "{\"name\":\"ming\",\"age\":20,\"phone\":15552211521}",
      "{\"name\":\"hong\", \"age\":19,\"phone\":13287994007}",
      "{\"name\":\"zhi\", \"age\":21,\"phone\":15552211523}"
    ))
    val jsonDataSetDf = spark.read.json(jsonDataSet)

    jsonDataSetDf.show()

    //第六种: 通过csv格式的DataSet生成
    val scvDataSet = spark.createDataset(Array(
      "ming,20,15552211521",
      "hong,19,13287994007",
      "zhi,21,15552211523"
    ))
    spark.read.csv(scvDataSet).toDF("name","age","phone").show()

    //第七种：动态创建schema
    val schema = StructType(List(
      StructField("name", StringType, true),
      StructField("age", IntegerType, true),
      StructField("phone", LongType, true)
    ))
    val dataList = new util.ArrayList[Row]()
    dataList.add(Row("ming",20,15552211521L))
    dataList.add(Row("hong",19,13287994007L))
    dataList.add(Row("zhi",21,15552211523L))
    spark.createDataFrame(dataList,schema).show()

    //第八种：读取数据库（mysql）
    val options = new util.HashMap[String,String]()
    options.put("url", "jdbc:mysql://localhost:3306/spark")
    options.put("driver","com.mysql.jdbc.Driver")
    options.put("user","root")
    options.put("password","hollysys")
    options.put("dbtable","user")

    spark.read.format("jdbc").options(options).load().show()

  }
}
```