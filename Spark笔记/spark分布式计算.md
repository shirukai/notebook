# Spark 分布式计算

## 概述

### 分布式计算：

在每一个block所在的机器针对block数据进行计算，将结果汇总到计算master。

原则：移动计算而尽可能少的移动数据

其实就是将单台机器上的计算扩展多台机器上进行计算

### spark分布式计算：

##### 计算是怎么并行计算的？

每一个block数据块就是一个分区计算的输入数据集，对每一个block计算都是可以同时进行的，这样就达到了并行计算的目的。对于按照相同key来聚合（相同的key必须在同一个分区中）的步骤，可以根据数据的特点对数据进行重新分区。

##### 每一步的计算怎么理解？

计算之前，我们会给每一步定义一个计算函数，每一步计算都是将这个自定义函数应用到每一条数据中，然后得到计算的结果数据。

##### 如果在计算第四步的时候，有某个计算任务由于网络原因等挂掉了，怎么办？

重新从其依赖的第一步和第二步以及第三步计算得出第四步需要的数据

##### 数据的分区方式是什么样的？

对于一开始计算的时候，读取文件的时候，文件的每一个block就是一个分区，当然我们也可以设置成2个block一个分区，对于key-value类型的数据的分区我们可以根据key按照某种规则来进行分区。比如按照key的hash值来分区。

##### 在计算伊始读取分区数据的时候，会发生从其他机器节点通过网络传输读取数据吗？

可能会发生，但是需要尽量避免。我们需要遵循移动计算而不移动数据的原则。每一个数据块都包含了它所在的机器的信息，我们需要提供这个数据块所在的机器，然后将计算任务发送到对应的机器上来执行，这个就是计算任务的本地性。

##### 每一步出现的数据都是一份存储吗？

不是，数据的存储只有一份，就是一开始的数据存储，在shuffle的时候们会有中间临时数据的存储。

## RDD（Resilient Distributed Datasets）

弹性分布式数据集，一个只读且分区的数据集

### RDD都会有以下特性：

1.一个分区列表，用于并行计算没每个分区对应这个一个原子数据集，作为这个分区计算的数据输入

2.计算这个RDD某个分区数据（这个分区数据是由父亲RDD对应分区计算出来的）函数

3.一个依赖列表，这个rdd依赖的父rdd是哪些（在计算的时候可以通过这个依赖来容错）

4.这个rdd的分区元数据信息，其实就是该RDD怎么分区的，比如某个rdd是通过hash partitioner得到的

5.分区数据的存储地址，用来计算任务的本地特性

6.spark的计算是“流”式计算

#### 创建RDD的三种方式：

##### 方式一：从存储在存储系统汇总的数据来创建，比如：

```
val inputRdd = sc.newAPIHadoopFile("hdfs://cdh-master:8020/hiaAnalyticsService/000000/hiaDataFiles/word.txt")
```

##### 方式二：可以基于一个已经保存的RDD来创建一个RDD比如：

```
val words = inputRdd.flatMap(_._2.toString.split(","))
```

##### 方式三：可以基于一个已经在spark内存中的列表数据来创建一个RDD，比如：

```
val numbers = sc.parallelize(Seq(1,2,3.4))
```



### RDD api 概述1

```scala
import org.apache.hadoop.io.{LongWritable,Text}
import org.apache.hadoop.mapred.TextInputFormat
import org.apache.spark.rdd.RDD
```


```scala
val inputRdd:RDD[(LongWritable,Text)] = 
sc.hadoopFile("hdfs://cdh-master:8020//user/root/srk/words.txt",classOf[TextInputFormat], classOf[LongWritable], classOf[Text])
```


```scala
inputRdd.partitions.size
```


    2


```scala
inputRdd.dependencies
```


    List()


```scala
inputRdd.partitioner
```


    None


```scala
val words:RDD[String] = inputRdd.flatMap(_._2.toString.split(" "))
```


```scala
words.partitions.size
```


```scala
words.dependencies
```


    List(org.apache.spark.OneToOneDependency@7217a263)


```scala
words.dependencies.map(_.rdd)
```


    List(hdfs://cdh-master:8020//user/root/srk/words.txt HadoopRDD[0] at hadoopFile at <console>:23)


```scala
words.partitioner
```


    None


```scala
val wordCount:RDD[(String,Int)] = words.map(word=>(word,1))
```


```scala
wordCount.dependencies
```


    List(org.apache.spark.OneToOneDependency@66ed5e20)


```scala
wordCount.dependencies.map(_.rdd)
```


    List(MapPartitionsRDD[1] at flatMap at <console>:24)


```scala
import org.apache.spark.HashPartitioner
```


```scala
val counts:RDD[(String,Int)] = wordCount.reduceByKey(new HashPartitioner(2),(x,y)=>x+y)
```


```scala
counts.partitioner
```


    Some(org.apache.spark.HashPartitioner@2)


```scala
counts.saveAsTextFile("hdfs://cdh-master:8020//user/root/srk/wordCount")
```
### RDD api 概述2

非触发计算 称为转换api

触发计算的 称为 动作api: savaAsTextFile

缓存api:persist() 和cache()

清理缓存：unpersist()

### Spark分布内存

#### 什么是分布式内存?

##### 第一个层面：

集群计算资源的管理

其实道理和分布式存储是一样的，只不过分布式存储是管理整个集群的所有slave的磁盘的大小，那么分布式内存则是管理整个集群汇总每台机器的内存大小。

##### 第二个层面：

单个应用计算master对计算资源的管理

每个应用先申请需要的计算资源，然后在申请到资源的节点上启动计算服务，这个服务同时负责对在这个节点上申请到的资源进行管理，并且使用资源的时候需要向计算master汇报。



##### Shuffle过程spark是基于内存的？

##### 而MapReduce是基于磁盘的？是这样的嘛？

不是的，MapReduce 是基于磁盘的，没错。但是spark不完全基于内存，spark的shuffle中间结果也是需要写入文件的，只是对内存的利用比较充分而已。



##### 大数据中间结果数据的复用场景

一种是迭代式计算应用

一种是交互性数据挖掘应用

以上两种应用存大量的中间结果数据复用的场景



##### 各种框架对中间结果复用的处理

MapReduce 以及Dryad等，将中间结果写到分布式文件系统中，需要磁盘IO

Pregel和HaLoop等奖一些特定的中间结果数据隐式的存储在分布式内存中

spark可以将任何类型的中间结果数据显示的调用api存储在分布式内存中



##### spark 调用RDD中的rdd.persist（StorageLevel.MEMORY_ONLY）方法来缓存种鸽中间rdd数据结果

```
val points = spark.textFile(……).map(paresPoint).persist()
var w = //random inital vector
for(i<-1 to ITERATIONS){
    val gradient = points.map{
        ……
    }
}
```

## Spark组件概述

![](https://shirukai.gitee.io/images/b5a6838837648031c846e7795d337cdf.jpg)

先记住结论：

1.spark sql将Dataset的api翻译成RDD api 来达到计算目的

2.spark ml是利用Dataset的api和RDD api来达到计算目的

3.spark mllib是利用RDD api来达到计算目的

4.spark Streaming将DStream的api翻译成RDD api来达到计算目的

5.spark graphx是利用RDD api以及扩展RDD来达到计算目的

### Spark core

![](https://shirukai.gitee.io/images/37b18c8ecc9f86306c207e173629d1b9.jpg)



* Security是安全组件，Serializer是序列化组件，rpc是远程调用组件，这些组件都是基础的组件
* RDD是所有计算的基础，如果想构建一个业务计算的话，先构建RDD链，这个链可以用RDD中的api在计算master中来构建
* deploy负责spark分布式计算集群的初始化，以及每次分布式计算任务的提交
* 有了RDD链后，可以通过scheduler来分解task，并且将这些task分发到相应的机器上执行
* 执行task时需要集群资源的，计算master是需要从资源master中申请资源的，这部分会有一个集群资源管理模块来干这个活
* 每一个task都是在某台机器上的某个Executor中执行的
* 在task的运行过程中，可能会涉及到中间数据的存储，这个有starage组件来完成
* task的运行需要内存，内存的管理有memory来完成
* 当一个task需要其他机器上的数据作为输入的时候，就需要shuffle来完成

### Spark Sql

目的：主要解决结构化数据处理的问题以达到关系型数据处理

定义：结构化数据就是带有schema的数据，如下图所示：

![](https://shirukai.gitee.io/images/99fc1dd30e0dece5f9a718e13e7c8503.jpg)



##### 带上schema的好处：

1. 让编程者可以用sql语句来处理数据
2. 让编程者尅利用schema信息来优化数据的存储
3. 使spark sql 可以根据schema信息对数据处理进行优化，比如code generation

##### spark sql 支持两种查询处理方式，一种是sql形式，一种是DataFrame api code的形式

##### 示例：

```
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("sparkSql").master("local").getOrCreate()
    val df = spark.read.json("data/person.json")
    df.show()

    /**
      * +----+-------+
      * | age|   name|
      * +----+-------+
      * |null|Michael|
      * |  30|   Andy|
      * |  19| Justin|
      * +----+-------+
      */
    df.createOrReplaceTempView("person")
    import spark.implicits._
    //使用spark sql方式
    val sqlDF = spark.sql("SELECT age, name FROM person where age > 21")
    sqlDF.show()

    /**
      * +---+----+
      * |age|name|
      * +---+----+
      * | 30|Andy|
      * +---+----+
      */
    //使用 DF api的方式
    val filterAgeDf = df.filter($"age" > 21)
    filterAgeDf.show()

    /**
      * +---+----+
      * |age|name|
      * +---+----+
      * | 30|Andy|
      * +---+----+
      */
  }
```



#### 大数据应用的特点：

1. 需要从各种各样的数据源抽取创幻数据：spark sql 通过catalyst解决多数据源抽取数据的问题
2. 关系型数据的查询，比如用sql
3. 对查询出来的数据做复杂的机器学习或者图计算
4. 在实际情况中，一个应用中关系型数据的查询处理与复杂的程序算法一般都是结合起来使用的

#### catalyst

定义扩展点：

扩展点一：数据源

* 很简单就可以实现半结构化数据的schema的推测，比如JSON
* 可以使用spark sql联合查询多个数据源，然后处理数据

扩展点二：数据类型的自定义，使的很容易为机器学习冷雨中的向量自定义数据类型

性能优化：

很方便的添加优化性能的组件，比如code generation



#### spark sql的初衷

1. 使得编程者从关系型处理中受益，比如直接sql处理以及优化关系型数据的存储
2. 使得sql使用者可以很简单调用spark中复杂的算法包，比如机器学习

#### DataFram的提出

1. 通过dataFram的api使得惯性处理和程序性处理的集成更加紧密
2. 包含了一个扩展性很强的优化器-catalyst，可以控制code generation，还可以定义扩展点等

#### Dataset的提出

1. 强类型
2. 可以支持自定义强大的lambda函数
3. DataFrame是类型为Row的DataSet，即Dataset[Row]
4. 可以将Dataset理解成带有schema的RDD

## Spark streaming

### DStream （Discretized Stream）特点

一个依赖父DStream的列表

一个生成RDD的时间间隔

一个生成RDD的函数

### Spark Streaming的特点

Streaming实时接收到的数据是存储在spark的分布式内存中

streaming的处理流程和RDD批处理非常类似，只是数据的输入形式不一样而已

streaming的底层数据的计算最终还是调用RDD的api来实现的

streaming除了支持处理每隔一段时间的实时数据，还支持处理每隔一段时间一个window的数据

#### 容错

某个节点失败的恢复机制

某个节点计算很慢的恢复机制

#### 现有系统怎么解决上面的容错问题？

1. replication即每一个计算节点都有两份拷贝（数据和计算逻辑）且两个节点之间需要保证接收到的消息的顺序是一致的。
2. upsteam backup 即每一个节点保留接收到数据的一份拷贝，当这个节点失败的时候，一个备用机器来代替失败的节点，集群将失败节点上的数据发送给备用机器进行恢复
3. 以上两种方案都只能解决么某个节点失败的容错，解决不了某个计算节点很慢的问题

#### spark streaming解决容错

某个节点失败的恢复机制：RDD根据其依赖可以重新进行计算失败的节点的任务

某个节点计算很慢的恢复机制：可以利用spark的task调度过程中task推测机制来解决