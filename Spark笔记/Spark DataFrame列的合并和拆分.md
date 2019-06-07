# Spark DataFrame 列的合并与拆分

> 版本说明：Spark-2.3.0

使用Spark SQL在对数据进行处理的过程中，可能会遇到对一列数据拆分为多列，或者把多列数据合并为一列。这里记录一下目前想到的对DataFrame列数据进行合并和拆分的几种方法。

## 1 DataFrame列数据的合并

例如：我们有如下数据，想要将三列数据合并为一列，并以“,”分割

```
+----+---+-----------+
|name|age|      phone|
+----+---+-----------+
|Ming| 20|15552211521|
|hong| 19|13287994007|
| zhi| 21|15552211523|
+----+---+-----------+
```

### 1.1 使用map方法重写

使用map方法重写就是将DataFrame使用map取值之后，然后使用toSeq方法转成Seq格式，最后使用Seq的foldLeft方法拼接数据，并返回，如下所示：

```scala
//方法1：利用map重写
    val separator = ","
    df.map(_.toSeq.foldLeft("")(_ + separator + _).substring(1)).show()

    /**
      * +-------------------+
      * |              value|
      * +-------------------+
      * |Ming,20,15552211521|
      * |hong,19,13287994007|
      * | zhi,21,15552211523|
      * +-------------------+
      */
```

### 1.2 使用内置函数concat_ws

合并多列数据也可以使用SparkSQL的内置函数concat_ws()

```java
 //方法2： 使用内置函数 concat_ws
    import org.apache.spark.sql.functions._
    df.select(concat_ws(separator, $"name", $"age", $"phone").cast(StringType).as("value")).show()

    /**
      * +-------------------+
      * |              value|
      * +-------------------+
      * |Ming,20,15552211521|
      * |hong,19,13287994007|
      * | zhi,21,15552211523|
      * +-------------------+
      */
```

### 1.3 使用自定义UDF函数

自己编写UDF函数，实现多列合并

```scala
    //方法3：使用自定义UDF函数

    // 编写udf函数
    def mergeCols(row: Row): String = {
      row.toSeq.foldLeft("")(_ + separator + _).substring(1)
    }

    val mergeColsUDF = udf(mergeCols _)
    df.select(mergeColsUDF(struct($"name", $"age", $"phone")).as("value")).show()
```

完整代码：

```scala
package com.hollysys.spark.sql

import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.types.StringType

/**
  * Created by shirukai on 2018/9/12
  * DataFrame 合并列
  */
object MergeColsTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName(this.getClass.getSimpleName)
      .master("local")
      .getOrCreate()

    //从内存创建一组DataFrame数据
    import spark.implicits._
    val df = Seq(("Ming", 20, 15552211521L), ("hong", 19, 13287994007L), ("zhi", 21, 15552211523L))
      .toDF("name", "age", "phone")
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
    //方法1：利用map重写
    val separator = ","
    df.map(_.toSeq.foldLeft("")(_ + separator + _).substring(1)).show()

    /**
      * +-------------------+
      * |              value|
      * +-------------------+
      * |Ming,20,15552211521|
      * |hong,19,13287994007|
      * | zhi,21,15552211523|
      * +-------------------+
      */
    //方法2： 使用内置函数 concat_ws
    import org.apache.spark.sql.functions._
    df.select(concat_ws(separator, $"name", $"age", $"phone").cast(StringType).as("value")).show()

    /**
      * +-------------------+
      * |              value|
      * +-------------------+
      * |Ming,20,15552211521|
      * |hong,19,13287994007|
      * | zhi,21,15552211523|
      * +-------------------+
      */
    //方法3：使用自定义UDF函数

    // 编写udf函数
    def mergeCols(row: Row): String = {
      row.toSeq.foldLeft("")(_ + separator + _).substring(1)
    }

    val mergeColsUDF = udf(mergeCols _)
    df.select(mergeColsUDF(struct($"name", $"age", $"phone")).as("value")).show()

    /**
      * /**
      * * +-------------------+
      * * |              value|
      * * +-------------------+
      * * |Ming,20,15552211521|
      * * |hong,19,13287994007|
      * * | zhi,21,15552211523|
      * * +-------------------+
      **/
      */
      spark.stop()
  }
}

```



## 2 DataFrame列数据的拆分

上面我们将DataFrame的多列数据合并为一列如下所示，有时候我们也需要将单列数据，以某种拆分规则，将一列拆分为多列。下面提供几种将一列拆分为多列的方法。

```
+-------------------+
|              value|
+-------------------+
|Ming,20,15552211521|
|hong,19,13287994007|
| zhi,21,15552211523|
+-------------------+
```

### 2.1 使用内置函数split，然后遍历添加列

该方法，先利用内置函数split将单列的数据拆分，然后遍历使用getItem(角标)方法获取拆分后的数据，依次使用withColumn方法添加新列，代码如下所示：

```scala
    //方法1： 使用内置函数split，然后遍历添加列
    val separator = ","
    lazy val first = df.first()

    val numAttrs = first.toString().split(separator).length
    val attrs = Array.tabulate(numAttrs)(n => "col_" + n)
    //按指定分隔符拆分value列，生成splitCols列
    var newDF = df.withColumn("splitCols", split($"value", separator))
    attrs.zipWithIndex.foreach(x => {
      newDF = newDF.withColumn(x._1, $"splitCols".getItem(x._2))
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

### 2.2 使用UDF函数创建多列数据，然后合并

该方法是使用udf函数，生成多个列，然后合并到原来的数据。该方法参考了VectorDisassembler（与spark ml官网提供的VectorAssembler相反），这是一个第三方的spark ml向量拆分算法，该方法github地址：https://github.com/jamesbconner/VectorDisassembler。代码如下所示：

```scala
//方法2：使用udf函数创建多列，然后合并
    val attributes: Array[Attribute] = {
      val numAttrs = first.toString().split(separator).length
      //生成attributes
      Array.tabulate(numAttrs)(i => NumericAttribute.defaultAttr.withName("value" + "_" + i))
    }
    //创建多列数据
    val fieldCols = attributes.zipWithIndex.map(x => {
      val assembleFunc = udf {
        str: String =>
          str.split(separator)(x._2)
      }
      assembleFunc(df("value").cast(StringType)).as(x._1.name.get, x._1.toMetadata())
    })
    //合并数据
    df.select(col("*") +: fieldCols: _*).show()

    /**
      * +-------------------+-------+-------+-----------+
      * |              value|value_0|value_1|    value_2|
      * +-------------------+-------+-------+-----------+
      * |Ming,20,15552211521|   Ming|     20|15552211521|
      * |hong,19,13287994007|   hong|     19|13287994007|
      * | zhi,21,15552211523|    zhi|     21|15552211523|
      * +-------------------+-------+-------+-----------+
      */
```

完整代码：

```scala
package com.hollysys.spark.sql

import org.apache.spark.ml.attribute.{Attribute, NumericAttribute}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.StringType

/**
  * Created by shirukai on 2018/9/12
  * 拆分列
  */
object SplitColTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName(this.getClass.getSimpleName)
      .master("local")
      .getOrCreate()

    //从内存中创建DataFrame
    import spark.implicits._
    val df = Seq("Ming,20,15552211521", "hong,19,13287994007", "zhi,21,15552211523")
      .toDF("value")
    df.show()

    /**
      * +-------------------+
      * |              value|
      * +-------------------+
      * |Ming,20,15552211521|
      * |hong,19,13287994007|
      * | zhi,21,15552211523|
      * +-------------------+
      */

    import org.apache.spark.sql.functions._
    //方法1： 使用内置函数split，然后遍历添加列
    val separator = ","
    lazy val first = df.first()

    val numAttrs = first.toString().split(separator).length
    val attrs = Array.tabulate(numAttrs)(n => "col_" + n)
    //按指定分隔符拆分value列，生成splitCols列
    var newDF = df.withColumn("splitCols", split($"value", separator))
    attrs.zipWithIndex.foreach(x => {
      newDF = newDF.withColumn(x._1, $"splitCols".getItem(x._2))
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

    //方法2：使用udf函数创建多列，然后合并
    val attributes: Array[Attribute] = {
      val numAttrs = first.toString().split(separator).length
      //生成attributes
      Array.tabulate(numAttrs)(i => NumericAttribute.defaultAttr.withName("value" + "_" + i))
    }
    //创建多列数据
    val fieldCols = attributes.zipWithIndex.map(x => {
      val assembleFunc = udf {
        str: String =>
          str.split(separator)(x._2)
      }
      assembleFunc(df("value").cast(StringType)).as(x._1.name.get, x._1.toMetadata())
    })
    //合并数据
    df.select(col("*") +: fieldCols: _*).show()

    /**
      * +-------------------+-------+-------+-----------+
      * |              value|value_0|value_1|    value_2|
      * +-------------------+-------+-------+-----------+
      * |Ming,20,15552211521|   Ming|     20|15552211521|
      * |hong,19,13287994007|   hong|     19|13287994007|
      * | zhi,21,15552211523|    zhi|     21|15552211523|
      * +-------------------+-------+-------+-----------+
      */
       spark.stop()
  }
}

```

