# Spark SQL 内置函数

> 版本说明：spark-2.3.0

SparkSQL内置函数官网API：http://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.sql.functions%24

CSDN博主整理的内置函数：https://blog.csdn.net/liam08/article/details/79663018

平常在使用mysql的时候，我们在写SQL的时候会使用到MySQL为我们提供的一些内置函数，如数函数：求绝对值abs()、平方根sqrt()等，还有其它的字符函数、日期函数、聚合函数等等。使我们利用这些内置函数能够快速实现我们的业务逻辑。在SparkSQL里其实也为我们提供了近两百多种内置函数，我们通过

```scla
import org.apache.spark.sql.functions._
```

导入内置函数包，来使用。也可以在SQL语句中直接使用。SparkSQL内置函数分类：聚合函数、集合函数、日期函数、数学函数、混杂函数、非聚合函数、排序函数、字符串函数、UDF函数和窗口函数这10类函数。



## 1 内置函数的使用

使用内置函数的方式有两种，一种是通过编程的方式的使用，另一种是通过SQL的方式使用。

例如：我们有如下数据，想要使用SparkSQL内置函数lower()来将名字全部转为小写

```
+----+---+-----------+
|name|age|      phone|
+----+---+-----------+
|Ming| 20|15552211521|
|hong| 19|13287994007|
| zhi| 21|15552211523|
+----+---+-----------+
```

以编程的方式使用内置函数

```scala
import org.apache.spark.sql.functions._
df.select(lower(col("name")).as("name"), col("age"), col("phone")).show()
```

以SQL的方式使用

```scala
df.createOrReplaceTempView("people")
spark.sql("select lower(name) as name,age,phone from people").show()
```

## 2 UDF函数的使用

有的时候，SparkSQL提供的内置函数无法满足我们的业务的时候，我们可以使用过UDF函数来自定义我们的实现逻辑。例如：需要对上面的数据添加一列id，要求id的生成是name+随机生成的uuid+phone。这时候我们可以使用UDF自定义函数实现。如下所示：

```scala
//根据name和phone生成组合，并加上一段uud生成唯一表示id
def idGenerator(name: String, phone: Long): String = {
  name + "-" + UUID.randomUUID().toString + "-" + phone.toString
}
//生成udf函数
val idGeneratorUDF = udf(idGenerator _)
//加入隐式转换
import spark.implicits._
df.withColumn("id", idGeneratorUDF($"name", $"phone")).show()
```

也可以这样写：

```scala
//加入隐式转换
import spark.implicits._
//根据name和phone生成组合，并加上一段uud生成唯一表示id
def idGenerator(name: String, phone: Long): String = {
  name + "-" + UUID.randomUUID().toString + "-" + phone.toString
}
//注册udf函数
spark.udf.register("idGenerator",idGenerator _)
//使用idGenerator
df.withColumn("id",callUDF("idGenerator",$"name",$"phone")).show()
```

结果都是一样的：

```
+----+---+-----------+--------------------+
|name|age|      phone|                  id|
+----+---+-----------+--------------------+
|Ming| 20|15552211521|Ming-9b87d4d5-91d...|
|hong| 19|13287994007|hong-7a91f7d8-66a...|
| zhi| 21|15552211523|zhi-f005859c-4516...|
+----+---+-----------+--------------------+
```

同样，我们可以将我们自定义的UDF函数注册到SparkSQL里，然后用SQL实现

```scala
//将自定义函数注册到SparkSQL里
spark.udf.register("idGeneratorUDF",idGeneratorUDF)
//创建临时表
df.createOrReplaceTempView("people")
//使用sql查询
spark.sql("select idGeneratorUDF(name,phone) as id,name,age,phone from people").show()
```

结果：

```
+--------------------+----+---+-----------+
|                  id|name|age|      phone|
+--------------------+----+---+-----------+
|Ming-5e9b6efb-bac...|Ming| 20|15552211521|
|hong-a3f6d67b-a20...|hong| 19|13287994007|
|zhi-7038c0c6-6086...| zhi| 21|15552211523|
+--------------------+----+---+-----------+
```

注意：上面加入import spark.implicits._隐式转换是为了方便使用$"列名"来代替col("列名")

完整代码：

```scala
package com.hollysys.spark.sql

import java.util.UUID
import org.apache.spark.sql.SparkSession

/**
  * Created by shirukai on 2018/9/11
  * spark sql 内置函数
  */
object SparkSQLFunctionApp {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName(this.getClass.getSimpleName).master("local").getOrCreate()
    import org.apache.spark.sql.functions._
    //加入隐式转换: 本例子里可以使用toDF方法和$"列名"代替col("列名")
    import spark.implicits._
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L)).toDF("name", "age", "phone")
    df.show()

    /**
      * +----+---+-----------+
      * |name|age|      phone|
      * +----+---+-----------+
      * |Ming| 20|15552211521|
      * |hong| 19|13287994007|
      * | zhi| 21|15552211523|
      * +----+---+-----------+
      */
    //1 使用内置函数将所有名字都转为小写
    //1.1 编程的方式：
    df.select(lower($"name").as("name"), $"age", $"phone").show()

    /**
      * +----+---+-----------+
      * |name|age|      phone|
      * +----+---+-----------+
      * |ming| 20|15552211521|
      * |hong| 19|13287994007|
      * | zhi| 21|15552211523|
      * +----+---+-----------+
      */
    //1.2 SQL的方式
    //注册表
    df.createOrReplaceTempView("people")
    spark.sql("select lower(name) as name,age,phone from people").show()

    /**
      * +----+---+-----------+
      * |name|age|      phone|
      * +----+---+-----------+
      * |ming| 20|15552211521|
      * |hong| 19|13287994007|
      * | zhi| 21|15552211523|
      * +----+---+-----------+
      */

    //2 UDF函数的使用
    //2.1 直接使用
    //根据name和phone生成组合，并加上一段uud生成唯一表示id
    def idGenerator(name: String, phone: Long): String = {
      name + "-" + UUID.randomUUID().toString + "-" + phone.toString
    }

    //生成udf函数
    val idGeneratorUDF = udf(idGenerator _)
    df.withColumn("id", idGeneratorUDF($"name", $"phone")).show()

    /**
      * +----+---+-----------+--------------------+
      * |name|age|      phone|                  id|
      * +----+---+-----------+--------------------+
      * |Ming| 20|15552211521|Ming-74338e40-548...|
      * |hong| 19|13287994007|hong-4f058f2b-9d3...|
      * | zhi| 21|15552211523|zhi-f42bea86-a9cf...|
      * +----+---+-----------+--------------------+
      */
    //将自定义函数注册到SparkSQL里
    spark.udf.register("idGeneratorUDF", idGeneratorUDF)
    //创建临时表
    df.createOrReplaceTempView("people")
    //使用sql查询
    spark.sql("select idGeneratorUDF(name,phone) as id,name,age,phone from people").show()

    /**
      * +----+---+-----------+--------------------+
      * |name|age|      phone|                  id|
      * +----+---+-----------+--------------------+
      * |Ming| 20|15552211521|Ming-74338e40-548...|
      * |hong| 19|13287994007|hong-4f058f2b-9d3...|
      * | zhi| 21|15552211523|zhi-f42bea86-a9cf...|
      * +----+---+-----------+--------------------+
      */
    //2.2 通过callUDF使用
    //注册udf函数
    spark.udf.register("idGenerator", idGenerator _)
    //使用idGenerator
    df.withColumn("id", callUDF("idGenerator", $"name", $"phone")).show()

    /**
      * +----+---+-----------+--------------------+
      * |name|age|      phone|                  id|
      * +----+---+-----------+--------------------+
      * |Ming| 20|15552211521|Ming-74338e40-548...|
      * |hong| 19|13287994007|hong-4f058f2b-9d3...|
      * | zhi| 21|15552211523|zhi-f42bea86-a9cf...|
      * +----+---+-----------+--------------------+
      */
    //创建临时表
    df.createOrReplaceTempView("people")
    //使用sql查询
    spark.sql("select idGenerator(name,phone) as id,name,age,phone from people").show()

    /**
      * +--------------------+----+---+-----------+
      * |                  id|name|age|      phone|
      * +--------------------+----+---+-----------+
      * |Ming-d4236bac-e21...|Ming| 20|15552211521|
      * |hong-bff84c0d-67d...|hong| 19|13287994007|
      * |zhi-aa0174b0-c8b3...| zhi| 21|15552211523|
      * +--------------------+----+---+-----------+
      */
  }
}

```

