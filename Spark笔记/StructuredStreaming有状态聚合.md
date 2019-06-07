# StructuredStreaming有状态聚合

>版本说明：Spark2.3

为保证多个Batch之间能够进行有状态的计算，SparkStreaming在1.6版本之前就引入了updateStateByKey的状态管理机制，在1.6之后又引入了mapWithState的状态管理机制。关于SparkStreaming的updateStateByKey和mapWithState的以查看[《Spark-Streaming 状态管理应用优化之路》](https://blog.csdn.net/struggle3014/article/details/79792695)。StructuredStreaming原本就是有状态的计算，这里我主要记录一下在StructuredStreaming里可以自定义状态操作的算子。

# 1 关于StructuredStreaming有状态操作算子

在StructuredStreaming里主要提供了两种自定义状态操作算子：mapGroupWithState和flatMapGroupWithState，可以帮助我们进行自定义的有状态的计算。这两个算法需要在KeyValueGroupedDataSet后使用，即在groupByKey之后使用这两个方法。下面将分别介绍一下mapGroupWithState和flatMapGroupWithState算子的使用

# 2 mapGroupWithState

参考：https://jaceklaskowski.gitbooks.io/spark-structured-streaming/spark-sql-streaming-KeyValueGroupedDataset-mapGroupsWithState.html

mapGroupWithState源码如下：

```scala
def mapGroupsWithState[S: Encoder, U: Encoder](
    func: (K, Iterator[V], GroupState[S]) => U): Dataset[U]

def mapGroupsWithState[S: Encoder, U: Encoder](
      timeoutConf: GroupStateTimeout)(
      func: (K, Iterator[V], GroupState[S]) => U): Dataset[U]
```

以第一种传参为例，需要我们传入一个函数(K, Iterator[V], GroupState[S]) => U): Dataset[U]，第一个参数为key,groupByKey中的那个key，类型与Key一致。第二个参数为values，当前key组下的所有数据，类型是Iterator[V]。第三个参数为组状态，类型是GroupState[S]。返回值是个U，DataSet中的单条数据。例如下面的函数：

```scala
  case class Word(time: Long, word: String)
  type State = mutable.ListBuffer[Word]    

	def mapGroupWithStateFunc(key: String, values: Iterator[Word], state: GroupState[State]): Word = {
      // 获取状态
      val historyState = state.getOption.getOrElse(mutable.ListBuffer[Word]())
      val valueList = values.toList
      println(s"Key为 $key 的历史状态：$historyState")
      println(s"Key为 $key 的当前数据：$valueList")
      valueList.foreach(w => {
        historyState += w
      })
      state.update(historyState)
      historyState.last
    }
```

完整代码：

```scala
package com.hollysys.spark.structured.usecase

import java.util.UUID

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.{GroupStateTimeout, OutputMode}
import org.apache.spark.sql.types.TimestampType

import scala.collection.mutable

/**
  * Created by shirukai on 2019-02-28 18:05
  * 使用mapGroupWithState进行有状态聚合操作
  */
object MapGroupsWithStateTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder
      .master("local[2]")
      .appName("MapGroupsWithStateTest")
      .getOrCreate()
    import spark.implicits._
    val lines = spark.
      readStream
      .format("socket")
      .option("host", "localhost")
      .option("port", "9090")
      .load
      .as[String]

    import org.apache.spark.sql.streaming.GroupState

    def mapGroupWithStateFunc(key: String, values: Iterator[Word], state: GroupState[State]): Word = {
      // 获取状态
      val historyState = state.getOption.getOrElse(mutable.ListBuffer[Word]())
      val valueList = values.toList
      println(s"Key为 $key 的历史状态：$historyState")
      println(s"Key为 $key 的当前数据：$valueList")
      valueList.foreach(w => {
        historyState += w
      })
      state.update(historyState)
      historyState.last
    }


    val df = lines.as[String].flatMap(line => {
      val lineSplits = line.split("[|]")
      lineSplits.flatMap(item => {
        val itemSplits = item.split(":")
        val t = itemSplits(0).toLong
        itemSplits(1).split(" ").map(word => (t, word))
      })
    }).toDF("time", "word").select($"time".cast(TimestampType), $"word").as[Word]
      .groupByKey(_.word)
//      .mapGroupsWithState(mapGroupWithStateFunc _)
    .mapGroupsWithState(timeoutConf = GroupStateTimeout.ProcessingTimeTimeout)(func = mapGroupWithStateFunc)
    val query = df
      .writeStream
      .format("console")
      .outputMode(OutputMode.Update)
      // 是否压缩显示
      .option("truncate", value = false)
      // 显示条数
      .option("numRows", 30)
      .option("checkpointLocation", "/tmp/temporary-" + UUID.randomUUID.toString)
      .start()

    query.awaitTermination()
  }

  case class Word(time: Long, word: String)

  type State = mutable.ListBuffer[Word]
  //  type State = mutable.TreeMap[String,Long]
  //  implicit val State: Encoder[State] = org.apache.spark.sql.Encoders.kryo[State]
}

```

我们可以使用Socket终端进行验证：nc -lk 9090

发送数据：1551326520:cat dog|1551326580:dog dog

```
Key为 cat 的历史状态：ListBuffer()
Key为 dog 的历史状态：ListBuffer()
Key为 cat 的当前数据：List(Word(1551326520,cat))
Key为 dog 的当前数据：List(Word(1551326520,dog), Word(1551326580,dog), Word(1551326580,dog))
-------------------------------------------
Batch: 0
-------------------------------------------
+----------+----+
|time      |word|
+----------+----+
|1551326580|dog |
|1551326520|cat |
+----------+----+
```

再发送数据：1551326520:cat dog|1551326580:dog dog

```
Key为 dog 的历史状态：ListBuffer(Word(1551326520,dog), Word(1551326580,dog), Word(1551326580,dog))
Key为 dog 的当前数据：List(Word(1551326520,dog), Word(1551326580,dog), Word(1551326580,dog))
Key为 cat 的历史状态：ListBuffer(Word(1551326520,cat))
Key为 cat 的当前数据：List(Word(1551326520,cat))
-------------------------------------------
Batch: 1
-------------------------------------------
+----------+----+
|time      |word|
+----------+----+
|1551326580|dog |
|1551326520|cat |
+----------+----+
```

# 3 flatMapGroupWithState

参考：https://jaceklaskowski.gitbooks.io/spark-structured-streaming/spark-sql-streaming-KeyValueGroupedDataset-flatMapGroupsWithState.html

flatMapGroupWithState与mapGroupWithState类似，区别有点像map和flatmap。上面我们可以看到mapGroupWithState回返回一条记录，而这里我们将的flatMapGroupWithState可以返回多条记录。

```scala
flatMapGroupsWithState[S: Encoder, U: Encoder](
  outputMode: OutputMode,
  timeoutConf: GroupStateTimeout)(
  func: (K, Iterator[V], GroupState[S]) => Iterator[U]): Dataset[U]
```

注意：flatMapGroupWithState函数仅可以在Append和Update输出模式下使用

说明：

outputMode：输出模式，通过OutputMode.Append设置

timeoutConf：状态过期设置，通过GroupStateTimeout.NoTimeout设置

func：自定义函数

func函数参数说明：

K,为groupByKey中的key的类型，该key将以参数的形式传入

V key分组下的所有数据类型，这些数据Iterator[V]将以参数的形式传入

S自定义状态的存储类型

U 自定义返回类型

上面说到flatMapGroupWithState与mapGroupWithState类似，这里对上面mapGroupWithState自定义的函数进行稍加修改，只改一下返回值类型即可。如下所示：

```scala
def mapGroupWithStateFunc(key: String, values: Iterator[Word], state: GroupState[State]): Iterator[Word] = {
  // 获取状态
  val historyState = state.getOption.getOrElse(mutable.ListBuffer[Word]())
  val valueList = values.toList
  println(s"Key为 $key 的历史状态：$historyState")
  println(s"Key为 $key 的当前数据：$valueList")
  valueList.foreach(w => {
    historyState += w
  })
  state.update(historyState)
  historyState.iterator
}
```

除此之外我们还要指定一个下数据的输出模式：

```scala
      .groupByKey(_.word)
      //      .mapGroupsWithState(mapGroupWithStateFunc _)
      .flatMapGroupsWithState(
      outputMode = OutputMode.Update(),
      timeoutConf = GroupStateTimeout.ProcessingTimeTimeout)(func = mapGroupWithStateFunc)
```

完整代码：

```scala
package com.hollysys.spark.structured.usecase

import java.util.UUID

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.streaming.{GroupStateTimeout, OutputMode}
import org.apache.spark.sql.types.TimestampType

import scala.collection.mutable

/**
  * Created by shirukai on 2019-02-28 18:05
  * 使用flatMapGroupWithState进行有状态聚合操作
  */
object FlatMapGroupsWithStateTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder
      .master("local[2]")
      .appName("MapGroupsWithStateTest")
      .getOrCreate()
    import spark.implicits._
    val lines = spark.
      readStream
      .format("socket")
      .option("host", "localhost")
      .option("port", "9090")
      .load
      .as[String]

    import org.apache.spark.sql.streaming.GroupState

    def mapGroupWithStateFunc(key: String, values: Iterator[Word], state: GroupState[State]): Iterator[Word] = {
      // 获取状态
      val historyState = state.getOption.getOrElse(mutable.ListBuffer[Word]())
      val valueList = values.toList
      println(s"Key为 $key 的历史状态：$historyState")
      println(s"Key为 $key 的当前数据：$valueList")
      valueList.foreach(w => {
        historyState += w
      })
      state.update(historyState)
      historyState.iterator
    }


    val df = lines.as[String].flatMap(line => {
      val lineSplits = line.split("[|]")
      lineSplits.flatMap(item => {
        val itemSplits = item.split(":")
        val t = itemSplits(0).toLong
        itemSplits(1).split(" ").map(word => (t, word))
      })
    }).toDF("time", "word").select($"time".cast(TimestampType), $"word").as[Word]
      .groupByKey(_.word)
      //      .mapGroupsWithState(mapGroupWithStateFunc _)
      .flatMapGroupsWithState(
      outputMode = OutputMode.Update(),
      timeoutConf = GroupStateTimeout.ProcessingTimeTimeout)(func = mapGroupWithStateFunc)
    val query = df
      .writeStream
      .format("console")
      .outputMode(OutputMode.Update)
      // 是否压缩显示
      .option("truncate", value = false)
      // 显示条数
      .option("numRows", 30)
      .option("checkpointLocation", "/tmp/temporary-" + UUID.randomUUID.toString)
      .start()

    query.awaitTermination()
  }

  case class Word(time: Long, word: String)

  type State = mutable.ListBuffer[Word]
  //  type State = mutable.TreeMap[String,Long]
  //  implicit val State: Encoder[State] = org.apache.spark.sql.Encoders.kryo[State]
}

```

我们可以使用Socket终端进行验证：nc -lk 9090

发送数据：1551326520:cat dog|1551326580:dog dog

```
Key为 dog 的历史状态：ListBuffer()
Key为 dog 的当前数据：List(Word(1551326520,dog), Word(1551326580,dog), Word(1551326580,dog))
Key为 cat 的历史状态：ListBuffer()
Key为 cat 的当前数据：List(Word(1551326520,cat))
-------------------------------------------
Batch: 0
-------------------------------------------
+----------+----+
|time      |word|
+----------+----+
|1551326520|dog |
|1551326580|dog |
|1551326580|dog |
|1551326520|cat |
+----------+----+

```

再发送数据：1551326520:cat dog|1551326580:dog dog

```
Key为 dog 的历史状态：ListBuffer(Word(1551326520,dog), Word(1551326580,dog), Word(1551326580,dog))
Key为 dog 的当前数据：List(Word(1551326520,dog), Word(1551326580,dog), Word(1551326580,dog))
Key为 cat 的历史状态：ListBuffer(Word(1551326520,cat))
Key为 cat 的当前数据：List(Word(1551326520,cat))
-------------------------------------------
Batch: 1
-------------------------------------------
+----------+----+
|time      |word|
+----------+----+
|1551326520|dog |
|1551326580|dog |
|1551326580|dog |
|1551326520|dog |
|1551326580|dog |
|1551326580|dog |
|1551326520|cat |
|1551326520|cat |
+----------+----+
```

# 4 注意

有时候我么你状态里需要一个有序的集合，如TreeMap、TreeSet等。经过测试scala里的TreeMap和TreeSet没法使用。错误信息：https://stackoverflow.com/questions/53159151/spark-catalyst-flatmapgroupswithstate-group-state-with-sorted-collection 。而java中的TreeMap也没发直接使用，我么你可以通过Encoder后再使用，如下所示：

```scala
  type State = util.TreeMap[String,Long]
  implicit val State: Encoder[State] = org.apache.spark.sql.Encoders.kryo[State]
```

