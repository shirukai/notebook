# SparkML特征向量合并和拆分

VectorAssembler（特征向量合并）是spark ml包里提供的算法， 但是对于向量拆分，官方没有听方法，这里从GitHub上看到一个向量拆分的算法，一起贴出来学习研究。

## VectorAssembler（特征向量合并）

摘录官网翻译：

VectorAssembler 是将给定的一系列的列合并到单个向量列中的transformer。它可以将原始特征和不同特征transformers（转换器）生成的特征合并为单个特征向量，来训练ML模型，如逻辑回归和决策树等机器学习算法。

VectorAssembler可以接受一下的输入类型：所有值类型、布尔类型、向量类型。输入列的值将按指定顺序依次添加到一个向量中。

### Example

假设我们有一个 **DataFrame** 包含 **id**, **hour**, **mobile**, **userFeatures**以及**clicked** 列：

```
id | hour | mobile | userFeatures     | clicked
----|------|--------|------------------|---------
 0  | 18   | 1.0    | [0.0, 10.0, 0.5] | 1.0
```

**userFeatures** 是一个包含3个用户特征的特征列，我们希望将 **hour**, **mobile** 以及 **userFeatures** 组合为一个单一特征向量叫做 **features，**并将其用于预测是否点击。如果我们设置 **VectorAssembler** 的输入列为 **hour** , **mobile** 以及**userFeatures**，输出列为 **features**，转换后我们应该得到以下结果：

```
id | hour | mobile | userFeatures     | clicked | features
----|------|--------|------------------|---------|-----------------------------
 0  | 18   | 1.0    | [0.0, 10.0, 0.5] | 1.0     | [18.0, 1.0, 0.0, 10.0, 0.5]
```

代码：

```
package com.hollysys.ml.featureSelectors.vectorAssembler

import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.ml.linalg.Vectors
import org.apache.spark.sql.SparkSession

/**
  * Created by shirukai on 2018/6/29
  */
object VectorAssemblerLearn {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName(this.getClass.getSimpleName).master("local")
      .getOrCreate()
    val dataset = spark.createDataFrame(
      Seq((0, 18, 1.0, Vectors.dense(0.0, 10.0, 0.5), 1.0))
    ).toDF("id", "hour", "mobile", "userFeatures", "clicked")

    val assembler = new VectorAssembler()
      .setInputCols(Array("hour", "mobile", "userFeatures"))
      .setOutputCol("features")

    val output = assembler.transform(dataset)

    output.select("features").show()

    /**
      * +---+----+------+--------------+-------+--------------------+
      * | id|hour|mobile|  userFeatures|clicked|            features|
      * +---+----+------+--------------+-------+--------------------+
      * |  0|  18|   1.0|[0.0,10.0,0.5]|    1.0|[18.0,1.0,0.0,10....|
      */

  }
```

## VectorDisassembler（特征向量拆分）

VectorDisassembler与VectorAssembler相反，是非spark ml算法。可以从GitHub上获取源码：https://github.com/jamesbconner/VectorDisassembler

下面将如下格式向量拆分

```
+--------------------+
|            features|
+--------------------+
|[18.0,1.0,0.0,10....|
+--------------------+
```

代码：

```
val disassembler = new VectorDisassembler().setInputCol("features")
disassembler.transform(output.select("features")).show()

/**
  * +--------------------+----+------+--------------+--------------+--------------+
  * |            features|hour|mobile|userFeatures_0|userFeatures_1|userFeatures_2|
  * +--------------------+----+------+--------------+--------------+--------------+
  * |[18.0,1.0,0.0,10....|18.0|   1.0|           0.0|          10.0|           0.5|
  * +--------------------+----+------+--------------+--------------+--------------+
  */
```