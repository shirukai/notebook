# SparkSQL基于DataSourceV2自定义数据源

> 版本说明：Spark 2.3
>
> 前言：之前在[SparkSQL数据源操作](https://shirukai.github.io/2018/09/17/SparkSQL%E6%95%B0%E6%8D%AE%E6%BA%90%E6%93%8D%E4%BD%9C/)文章中整理了一些SparkSQL内置数据源的使用，总的来说SparkSQL支持的数据源还是挺丰富的，但业务上可能不拘束于这几种数据源，比如将HBase作为SparkSQL的数据源，REST数据源等。这里主要讲一下在Spark2.3版本之后推出的DataSourceV2，基于DataSourceV2实现自定义数据源

# 1 DataSourceV1 VS DataSourceV2

自Spark1.3版本之后，引入了数据源API，我们可以实现自定义数据源。2.3版本之后又引入的新版API，关于V1与V2的区别以及使用可以参考https://blog.csdn.net/zjerryj/article/details/84922369与https://developer.ibm.com/code/2018/04/16/introducing-apache-spark-data-sources-api-v2/这两篇文章。这里简单的总结一下V1的缺点，以及V2的新特性。

## 1.1 DataSourceV1缺点

* 依赖上层API
* 难以添加新的优化算子
* 难以传递分区信息
* 缺少事务性的写操作
* 缺少列存储和流式计算支持

## 1.2 DataSourceV2优点

* DataSourceV2 API使用Java编写
* 不依赖于上层API（DataFrame/RDD）
* 易于扩展，可以添加新的优化，同时保持向后兼容
* 提供物理信息，如大小、分区等
* 支持Streamin Source/Sink
* 灵活、强大和事务性的写入API

## 1.3 Spark2.3中V2的功能

* 支持列扫描和行扫描
* 列裁剪和过滤条件下推
* 可以提供基本统计和数据分区
* 事务写入API
* 支持微批和连续的Streaming Source/Sink

# 2 基于DataSourceV2实现输入源

SparkSQL的DataSourceV2的实现与StructuredStreaming自定义数据源如出一辙，思想是一样的，但是具体实现有所不同，主要步骤如下：

第一步：继承DataSourceV2和ReadSupport创建XXXDataSource类，重写ReadSupport的creatReader方法，用来返回自定义的DataSourceReader类，如返回自定义XXXDataSourceReader实例

第二步：继承DataSourceReader创建XXXDataSourceReader类，重写DataSourceReader的readSchema方法用来返回数据源的schema，重写DataSourceReader的createDataReaderFactories用来返回多个自定义DataReaderFactory实例

第三步：继承DataReaderFactory创建DataReader工厂类，如XXXDataReaderFactory，重写DataReaderFactory的createDataReader方法，返回自定义DataRader实例

第四步：继承DataReader类创建自定义的DataReader，如XXXDataReader，重写DataReader的next()方法，用来告诉Spark是否有下条数据，用来触发get()方法，重写DataReader的get()方法获取数据，重写DataReader的close()方法用来关闭资源

## 2.1 继承DataSourceV2和ReadSupport创建XXXDataSource类

这里以创建CustomDataSourceV2类为例

### 2.1.1 创建CustomDataSourceV2类

```scala
/**
  * 创建DataSource提供类
  * 1.继承DataSourceV2向Spark注册数据源
  * 2.继承ReadSupport支持读数据
  */
class CustomDataSourceV2 extends DataSourceV2
  with ReadSupport {
      // todo
}
```

### 2.1.2 重写ReadSupport的createReader方法

该方法用来返回一个用户自定义的DataSourceReader实例

```scala
  /**
    * 创建Reader
    *
    * @param options 用户定义的options
    * @return 自定义的DataSourceReader
    */
  override def createReader(options: DataSourceOptions): DataSourceReader = new CustomDataSourceV2Reader(options)
```

## 2.2 继承DataSourceReader创建XXXDataSourceReader类

该类用来自定义DataSourceReader，需要继承DataSourceReader，并重写readSchema和createDataReaderFactories方法。

### 2.2.1 创建CustomDataSourceV2Reader类

```scala
/**
  * 自定义的DataSourceReader
  * 继承DataSourceReader
  * 重写readSchema方法用来生成schema
  * 重写createDataReaderFactories,用来根据条件，创建多个工厂实例
  *
  * @param options options
  */
class CustomDataSourceV2Reader(options: DataSourceOptions) extends DataSourceReader {
    // Override some functions
}
```

### 2.2.2 重写DataSourceReader的readSchema方法

该方法用来返回数据源的schema

```scala
/**
  * 生成schema
  *
  * @return schema
  */
override def readSchema(): StructType = ???
```

### 2.2.3 重写DataSourceReader的createDataReaderFactories方法

实现该方法，可以根据不同的条件，创建多个createDataReader工厂实例，用来并发获取数据？(暂且这么理解的，或者是按照分区获取数据？)

```scala
  /**
    * 创建DataReader工厂实例
    *
    * @return 多个工厂类实例
    */
  override def createDataReaderFactories(): util.List[DataReaderFactory[Row]] = {
    import collection.JavaConverters._
    Seq(
      new CustomDataSourceV2ReaderFactory().asInstanceOf[DataReaderFactory[Row]]
    ).asJava
  }
```

## 2.3 继承DataReaderFactory创建DataReader工厂类

该类是DataReader的工厂来，用来返回DataReader实例

### 2.3.1 创建CustomDataSourceV2Factory类

```scala
/**
  * 自定义DataReaderFactory类
  */
class CustomDataSourceV2ReaderFactory extends DataReaderFactory[Row] {
   // Override some functions
}

```

### 2.3.2 重写DataReaderFactory的createDataReader方法

该方法用来实例化自定义的DataReader

```scala
  /**
    * 重写createDataReader方法，用来实例化自定义的DataReader
    *
    * @return 自定义的DataReader
    */
  override def createDataReader(): DataReader[Row] = new CustomDataReader
```

## 2.4 继承DataReader类创建自定义的DataReader

该类为重点实现部分，用来自定义获取数据的方式

### 2.4.1 创建CustomDataReader类

```scala
/**
  * 自定义DataReader类
  */
class CustomDataReader extends DataReader[Row] {
    // Override some functions
}
```

### 2.4.2 重写CustomDataReader的next()方法

该方法返回一个布尔值，来告诉Spark是否含有下条数据，以便触发get()方法获取数据

```scala
  /**
    * 是否有下一条数据
    *
    * @return boolean
    */
  override def next(): Boolean = ???
```

### 2.4.3 重写CustomDataReader的get()方法

该方法用来获取数据，返回类型是在继承DataReader时指定的泛型

```scala
  /**
    * 获取数据
    * 当next为true时会调用get方法获取数据
    *
    * @return Row
    */
  override def get(): Row = ???
```

### 2.4.4 重写CustomDataReader的close()方法

该方法用来关闭相应的资源

```scala
  /**
    * 关闭资源
    */
  override def close(): Unit = ???
```

## 2.5 以REST为例，实现自定义的数据源

这里主要是从REST接口里获取JSON格式的数据，然后生成DataFrame数据源

### 2.5.1 创建RestDataSource类

```scala
class RestDataSource extends DataSourceV2 with ReadSupport with WriteSupport {

  override def createReader(options: DataSourceOptions): DataSourceReader =
    new RestDataSourceReader(
      options.get("url").get(),
      options.get("params").get(),
      options.get("xPath").get(),
      options.get("schema").get()
    )
}

```

### 2.5.2 创建RestDataSourceReader类

```scala
/**
  * 创建RestDataSourceReader
  *
  * @param url          REST服务的的api
  * @param params       请求需要的参数
  * @param xPath        JSON数据的xPath
  * @param schemaString 用户传入的schema字符串
  */
class RestDataSourceReader(url: String, params: String, xPath: String, schemaString: String)
  extends DataSourceReader {
  // 使用StructType.fromDDL方法将schema字符串转成StructType类型
  var requiredSchema: StructType = StructType.fromDDL(schemaString)

  /**
    * 生成schema
    *
    * @return schema
    */
  override def readSchema(): StructType = requiredSchema

  /**
    * 创建工厂类
    *
    * @return List[实例]
    */
  override def createDataReaderFactories(): util.List[DataReaderFactory[Row]] = {
    import collection.JavaConverters._
    Seq(
      new RestDataReaderFactory(url, params, xPath).asInstanceOf[DataReaderFactory[Row]]
    ).asJava
  }
}
```

### 2.5.3 创建RestDataReaderFactory

```scala
/**
  * RestDataReaderFactory工厂类
  *
  * @param url    REST服务的的api
  * @param params 请求需要的参数
  * @param xPath  JSON数据的xPath
  */
class RestDataReaderFactory(url: String, params: String, xPath: String) extends DataReaderFactory[Row] {
  override def createDataReader(): DataReader[Row] = new RestDataReader(url, params, xPath)
}
```

### 2.5.4 创建RestDataReader

```scala
/**
  * RestDataReader类
  *
  * @param url    REST服务的的api
  * @param params 请求需要的参数
  * @param xPath  JSON数据的xPath
  */
class RestDataReader(url: String, params: String, xPath: String) extends DataReader[Row] {
  // 使用Iterator模拟数据
  val data: Iterator[Seq[AnyRef]] = getIterator

  override def next(): Boolean = {
    data.hasNext
  }

  override def get(): Row = {
    val seq = data.next().map {
      // 浮点类型会自动转为BigDecimal，导致Spark无法转换
      case decimal: BigDecimal =>
        decimal.doubleValue()
      case x => x
    }
    Row(seq: _*)
  }

  override def close(): Unit = {
    println("close source")
  }

  def getIterator: Iterator[Seq[AnyRef]] = {
    import scala.collection.JavaConverters._
    val res: List[AnyRef] = RestDataSource.requestData(url, params, xPath)
    res.map(r => {
      r.asInstanceOf[JSONObject].asScala.values.toList
    }).toIterator
  }
}
```

### 2.5.5 测试RestDataSource

```scala
object RestDataSourceTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .master("local[2]")
      .appName(this.getClass.getSimpleName)
      .getOrCreate()

    val df = spark.read
      .format("com.hollysys.spark.sql.datasource.rest.RestDataSource")
      .option("url", "http://model-opcua-hollysysdigital-test.hiacloud.net.cn/aggquery/query/queryPointHistoryData")
      .option("params", "{\n    \"startTime\": \"1543887720000\",\n    \"endTime\": \"1543891320000\",\n    \"maxSizePerNode\": 1000,\n    \"nodes\": [\n        {\n            \"uri\": \"/SymLink-10000012030100000-device/5c174da007a54e0001035ddd\"\n        }\n    ]\n}")
      .option("xPath", "$.result.historyData")
      //`response` ARRAY<STRUCT<`historyData`:ARRAY<STRUCT<`s`:INT,`t`:LONG,`v`:FLOAT>>>>
      .option("schema", "`s` INT,`t` LONG,`v` DOUBLE")
      .load()
    df.printSchema()
    df.show(false)
 
  }
}
```

![](http://shirukai.gitee.io/images/30a68af718db1637780fd7e07ab711f9.jpg)

# 3 基于DataSourceV2实现输出源

基于DataSourceV2实现自定义的输出源，需要以下几个步骤：

第一步：继承DataSourceV2和WriteSupport创建XXXDataSource，重写createWriter方法用来返回自定义的DataSourceWriter

第二步：继承DataSourceWriter创建XXXDataSourceWriter类，重写createWriterFactory返回自定义的DataWriterFactory，重写commit方法，用来提交整个事务。重写abort方法，用来做事务回滚

第三步：继承DataWriterFactory创建XXXDataWriterFactory类，重写createWriter方法返回自定义的DataWriter

第四步：继承DataWriter创建XXXDataWriter类，重写write方法，用来将数据写出，重写commit方法用来提交事务，重写abort方法用来做事务回滚

## 3.1 继承DataSourceV和WriterSupport创建XXXDataSource类

### 3.1.1 创建CustomDataSourceV2类

```scala
/**
  * 创建DataSource提供类
  * 1.继承DataSourceV2向Spark注册数据源
  * 2.继承WriteSupport支持读数据
  */
class CustomDataSourceV2 extends DataSourceV2
  with WriteSupport {
      // todo
}
```

### 3.1.2 重写createWriter方法

```scala
  /**
    * 创建Writer
    *
    * @param jobId   jobId
    * @param schema  schema
    * @param mode    保存模式
    * @param options 用于定义的option
    * @return Optional[自定义的DataSourceWriter]
    */
  override def createWriter(jobId: String,
                            schema: StructType,
                            mode: SaveMode,
                            options: DataSourceOptions): Optional[DataSourceWriter] = Optional.of(new CustomDataSourceV2Writer)
```

## 3.2 继承DataSourceWriter创建XXXDataSourceWriter类

### 3.2.1 创建CustomDataSourceV2Writer

需要继承DataSourceWriter

```scala
/**
  * 自定义DataSourceWriter
  * 继承DataSourceWriter
  */
class CustomDataSourceV2Writer extends DataSourceWriter {
    // Override some functions
}
```

## 3.3 继承DataWriterFactory创建XXXDataWriterFactory类

### 3.3.1 创建CustomDataWriterFactory

```scala
class CustomDataWriterFactory extends DataWriterFactory[Row] {
    // Override some functions
}
```

### 3.3.2 重写createDataWriter方法

该方法返回一个自定义的DataWriter

```scala
  /**
    * 创建DataWriter
    *
    * @param partitionId   分区ID
    * @param attemptNumber 重试次数
    * @return DataWriter
    *         每个分区创建一个RestDataWriter实例
    */
  override def createDataWriter(partitionId: Int, attemptNumber: Int): DataWriter[Row] = ???
```

## 3.4 继承DataWriter创建XXXDataWriter类

### 3.4.1 创建CustomDataWriter类

```scala
class CustomDataWriter extends DataWriter[Row] {
	// Overrride some functions
}
```

### 3.4.2 重写write方法

该方法用来写出单条数据，每条数据都会触发该方法

```scala
/**
  * write
  *
  * @param record 单条记录
  *               每条记录都会触发该方法
  */
override def write(record: Row): Unit = ???
```

### 3.4.3 重写commit方法

该方法一般用于事务提交，每个分区触发一次

```scala
/**
    * commit
    *
    * @return commit message
    *         每个分区触发一次
    */
  override def commit(): WriterCommitMessage = ???
```

### 3.4.4 重写abort方法

该方法用于事务回滚，当write方法发生异常之后触发该方法

```scala

  /**
    * 回滚：当write发生异常时触发该方法
    */
  override def abort(): Unit = ???
```



# 4 完整代码

## 4.1 自定义DataSource示例代码：

```scala
package com.hollysys.spark.sql.datasource

import java.util
import java.util.Optional

import org.apache.spark.sql.{Row, SaveMode}
import org.apache.spark.sql.sources.v2.reader.{DataReader, DataReaderFactory, DataSourceReader}
import org.apache.spark.sql.sources.v2.writer.{DataSourceWriter, DataWriter, DataWriterFactory, WriterCommitMessage}
import org.apache.spark.sql.sources.v2.{DataSourceOptions, DataSourceV2, ReadSupport, WriteSupport}
import org.apache.spark.sql.types.StructType

/**
  * @author : shirukai
  * @date : 2019-01-30 10:37
  *       Spark SQL 基于DataSourceV2接口实现自定义数据源
  */

/**
  * 创建DataSource提供类
  * 1.继承DataSourceV2向Spark注册数据源
  * 2.继承ReadSupport支持读数据
  * 3.继承WriteSupport支持读数据
  */
class CustomDataSourceV2 extends DataSourceV2
  with ReadSupport
  with WriteSupport {

  /**
    * 创建Reader
    *
    * @param options 用户定义的options
    * @return 自定义的DataSourceReader
    */
  override def createReader(options: DataSourceOptions): DataSourceReader = new CustomDataSourceV2Reader(options)

  /**
    * 创建Writer
    *
    * @param jobId   jobId
    * @param schema  schema
    * @param mode    保存模式
    * @param options 用于定义的option
    * @return Optional[自定义的DataSourceWriter]
    */
  override def createWriter(jobId: String,
                            schema: StructType,
                            mode: SaveMode,
                            options: DataSourceOptions): Optional[DataSourceWriter] = Optional.of(new CustomDataSourceV2Writer)
}


/**
  * 自定义的DataSourceReader
  * 继承DataSourceReader
  * 重写readSchema方法用来生成schema
  * 重写createDataReaderFactories,用来根据条件，创建多个工厂实例
  *
  * @param options options
  */
class CustomDataSourceV2Reader(options: DataSourceOptions) extends DataSourceReader {
  /**
    * 生成schema
    *
    * @return schema
    */
  override def readSchema(): StructType = ???

  /**
    * 创建DataReader工厂实例
    *
    * @return 多个工厂类实例
    */
  override def createDataReaderFactories(): util.List[DataReaderFactory[Row]] = {
    import collection.JavaConverters._
    Seq(
      new CustomDataSourceV2ReaderFactory().asInstanceOf[DataReaderFactory[Row]]
    ).asJava
  }
}


/**
  * 自定义DataReaderFactory类
  */
class CustomDataSourceV2ReaderFactory extends DataReaderFactory[Row] {
  /**
    * 重写createDataReader方法，用来实例化自定义的DataReader
    *
    * @return 自定义的DataReader
    */
  override def createDataReader(): DataReader[Row] = new CustomDataReader
}


/**
  * 自定义DataReader类
  */
class CustomDataReader extends DataReader[Row] {
  /**
    * 是否有下一条数据
    *
    * @return boolean
    */
  override def next(): Boolean = ???

  /**
    * 获取数据
    * 当next为true时会调用get方法获取数据
    *
    * @return Row
    */
  override def get(): Row = ???

  /**
    * 关闭资源
    */
  override def close(): Unit = ???
}

/**
  * 自定义DataSourceWriter
  * 继承DataSourceWriter
  */
class CustomDataSourceV2Writer extends DataSourceWriter {
  /**
    * 创建WriterFactory
    *
    * @return 自定义的DataWriterFactory
    */
  override def createWriterFactory(): DataWriterFactory[Row] = ???

  /**
    * commit
    *
    * @param messages 所有分区提交的commit信息
    *                 触发一次
    */
  override def commit(messages: Array[WriterCommitMessage]): Unit = ???

  /** *
    * abort
    *
    * @param messages 当write异常时调用
    */
  override def abort(messages: Array[WriterCommitMessage]): Unit = ???
}

/**
  * DataWriterFactory工厂类
  */
class CustomDataWriterFactory extends DataWriterFactory[Row] {
  /**
    * 创建DataWriter
    *
    * @param partitionId   分区ID
    * @param attemptNumber 重试次数
    * @return DataWriter
    *         每个分区创建一个RestDataWriter实例
    */
  override def createDataWriter(partitionId: Int, attemptNumber: Int): DataWriter[Row] = ???
}
/**
  * DataWriter
  */
class CustomDataWriter extends DataWriter[Row] {
  /**
    * write
    *
    * @param record 单条记录
    *               每条记录都会触发该方法
    */
  override def write(record: Row): Unit = ???
  /**
    * commit
    *
    * @return commit message
    *         每个分区触发一次
    */
  override def commit(): WriterCommitMessage = ???


  /**
    * 回滚：当write发生异常时触发该方法
    */
  override def abort(): Unit = ???
}

```

## 4.2 自定义RestDataSource代码

```SCALA
package com.hollysys.spark.sql.datasource.rest

import java.math.BigDecimal
import java.util
import java.util.Optional

import com.alibaba.fastjson.{JSONArray, JSONObject, JSONPath}
import org.apache.http.client.fluent.Request
import org.apache.http.entity.ContentType
import org.apache.spark.sql.{Row, SaveMode, SparkSession}
import org.apache.spark.sql.sources.v2.reader.{DataReader, DataReaderFactory, DataSourceReader, SupportsPushDownRequiredColumns}
import org.apache.spark.sql.sources.v2.writer.{DataSourceWriter, DataWriter, DataWriterFactory, WriterCommitMessage}
import org.apache.spark.sql.sources.v2.{DataSourceOptions, DataSourceV2, ReadSupport, WriteSupport}
import org.apache.spark.sql.types.StructType

/**
  * @author : shirukai
  * @date : 2019-01-09 16:53
  *       基于Rest的Spark SQL DataSource
  */
class RestDataSource extends DataSourceV2 with ReadSupport with WriteSupport {

  override def createReader(options: DataSourceOptions): DataSourceReader =
    new RestDataSourceReader(
      options.get("url").get(),
      options.get("params").get(),
      options.get("xPath").get(),
      options.get("schema").get()
    )

  override def createWriter(jobId: String,
                            schema: StructType,
                            mode: SaveMode,
                            options: DataSourceOptions): Optional[DataSourceWriter] = Optional.of(new RestDataSourceWriter)
}

/**
  * 创建RestDataSourceReader
  *
  * @param url          REST服务的的api
  * @param params       请求需要的参数
  * @param xPath        JSON数据的xPath
  * @param schemaString 用户传入的schema字符串
  */
class RestDataSourceReader(url: String, params: String, xPath: String, schemaString: String)
  extends DataSourceReader {
  // 使用StructType.fromDDL方法将schema字符串转成StructType类型
  var requiredSchema: StructType = StructType.fromDDL(schemaString)

  /**
    * 生成schema
    *
    * @return schema
    */
  override def readSchema(): StructType = requiredSchema

  /**
    * 创建工厂类
    *
    * @return List[实例]
    */
  override def createDataReaderFactories(): util.List[DataReaderFactory[Row]] = {
    import collection.JavaConverters._
    Seq(
      new RestDataReaderFactory(url, params, xPath).asInstanceOf[DataReaderFactory[Row]]
    ).asJava
  }


}

/**
  * RestDataReaderFactory工厂类
  *
  * @param url    REST服务的的api
  * @param params 请求需要的参数
  * @param xPath  JSON数据的xPath
  */
class RestDataReaderFactory(url: String, params: String, xPath: String) extends DataReaderFactory[Row] {
  override def createDataReader(): DataReader[Row] = new RestDataReader(url, params, xPath)
}

/**
  * RestDataReader类
  *
  * @param url    REST服务的的api
  * @param params 请求需要的参数
  * @param xPath  JSON数据的xPath
  */
class RestDataReader(url: String, params: String, xPath: String) extends DataReader[Row] {
  // 使用Iterator模拟数据
  val data: Iterator[Seq[AnyRef]] = getIterator

  override def next(): Boolean = {
    data.hasNext
  }

  override def get(): Row = {
    val seq = data.next().map {
      // 浮点类型会自动转为BigDecimal，导致Spark无法转换
      case decimal: BigDecimal =>
        decimal.doubleValue()
      case x => x
    }
    Row(seq: _*)
  }

  override def close(): Unit = {
    println("close source")
  }

  def getIterator: Iterator[Seq[AnyRef]] = {
    import scala.collection.JavaConverters._
    val res: List[AnyRef] = RestDataSource.requestData(url, params, xPath)
    res.map(r => {
      r.asInstanceOf[JSONObject].asScala.values.toList
    }).toIterator
  }
}

/** *
  * RestDataSourceWriter
  */
class RestDataSourceWriter extends DataSourceWriter {
  /**
    * 创建RestDataWriter工厂类
    *
    * @return RestDataWriterFactory
    */
  override def createWriterFactory(): DataWriterFactory[Row] = new RestDataWriterFactory

  /**
    * commit
    *
    * @param messages 所有分区提交的commit信息
    *                 触发一次
    */
  override def commit(messages: Array[WriterCommitMessage]): Unit = ???

  /** *
    * abort
    *
    * @param messages 当write异常时调用
    */
  override def abort(messages: Array[WriterCommitMessage]): Unit = ???

}

/**
  * DataWriterFactory工厂类
  */
class RestDataWriterFactory extends DataWriterFactory[Row] {
  /**
    * 创建DataWriter
    *
    * @param partitionId   分区ID
    * @param attemptNumber 重试次数
    * @return DataWriter
    *         每个分区创建一个RestDataWriter实例
    */
  override def createDataWriter(partitionId: Int, attemptNumber: Int): DataWriter[Row] = new RestDataWriter(partitionId, attemptNumber)
}

/**
  * RestDataWriter
  *
  * @param partitionId   分区ID
  * @param attemptNumber 重试次数
  */
class RestDataWriter(partitionId: Int, attemptNumber: Int) extends DataWriter[Row] {
  /**
    * write
    *
    * @param record 单条记录
    *               每条记录都会触发该方法
    */
  override def write(record: Row): Unit = {

    println(record)
  }

  /**
    * commit
    *
    * @return commit message
    *         每个分区触发一次
    */
  override def commit(): WriterCommitMessage = {
    RestWriterCommitMessage(partitionId, attemptNumber)
  }

  /**
    * 回滚：当write发生异常时触发该方法
    */
  override def abort(): Unit = {
    println("abort 方法被出发了")
  }
}

case class RestWriterCommitMessage(partitionId: Int, attemptNumber: Int) extends WriterCommitMessage

object RestDataSource {
  def requestData(url: String, params: String, xPath: String): List[AnyRef] = {
    import scala.collection.JavaConverters._
    val response = Request.Post(url).bodyString(params, ContentType.APPLICATION_JSON).execute()
    JSONPath.read(response.returnContent().asString(), xPath)
      .asInstanceOf[JSONArray].asScala.toList
  }
}

object RestDataSourceTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .master("local[2]")
      .appName(this.getClass.getSimpleName)
      .getOrCreate()

    val df = spark.read
      .format("com.hollysys.spark.sql.datasource.rest.RestDataSource")
      .option("url", "http://model-opcua-hollysysdigital-test.hiacloud.net.cn/aggquery/query/queryPointHistoryData")
      .option("params", "{\n    \"startTime\": \"1543887720000\",\n    \"endTime\": \"1543891320000\",\n    \"maxSizePerNode\": 1000,\n    \"nodes\": [\n        {\n            \"uri\": \"/SymLink-10000012030100000-device/5c174da007a54e0001035ddd\"\n        }\n    ]\n}")
      .option("xPath", "$.result.historyData")
      //`response` ARRAY<STRUCT<`historyData`:ARRAY<STRUCT<`s`:INT,`t`:LONG,`v`:FLOAT>>>>
      .option("schema", "`s` INT,`t` LONG,`v` DOUBLE")
      .load()


    df.printSchema()
    df.show(false)
//    df.repartition(5).write.format("com.hollysys.spark.sql.datasource.rest.RestDataSource")
//      .save()
  }
}
```

