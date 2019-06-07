## RDD 

概念：

一个只读且分区的数据集

RDD的优势：

高效容错

可以控制数据的分区来优化计算性能

并行处理

提供了丰富的操作数据的api

可以显示的将任何类型的中间结果存储在内存中

## RDD的五个主要特性

```
 * Internally, each RDD is characterized by five main properties:
 *
 *  - A list of partitions 一系列的分区/分片
 *  - A function for computing each split 一个用于计算每一个分区的函数
 *  - A list of dependencies on other RDDs 一些列依赖
 *  - Optionally, a Partitioner for key-value RDDs (e.g. to say that the RDD is hash-partitioned) 分区器
 *  - Optionally, a list of preferred locations to compute each split on (e.g. block locations for
 *    an HDFS file) 数据在哪优先把作业调度到数据所在的节点进行计算：移动数据不如移动计算
```



## 深入查看RDD的五个抽象API

源码：

```scala
/**
 * :: DeveloperApi ::
 * Implemented by subclasses to compute a given partition.
  *
  * 在一个task上下文中计算某一个分区的数据得到一个Iterator
 */
@DeveloperApi
def compute(split: Partition, context: TaskContext): Iterator[T]

/**
 * Implemented by subclasses to return the set of partitions in this RDD. This method will only
 * be called once, so it is safe to implement a time-consuming computation in it.
 *
 * The partitions in this array must satisfy the following property:
 *   `rdd.partitions.zipWithIndex.forall { case (partition, index) => partition.index == index }`
  *   获取RDD的分区列表,用于并行计算
 */
protected def getPartitions: Array[Partition]

/**
 * Implemented by subclasses to return how this RDD depends on parent RDDs. This method will only
 * be called once, so it is safe to implement a time-consuming computation in it.
  * 获取依赖列表
 */
protected def getDependencies: Seq[Dependency[_]] = deps

/**
 * Optionally overridden by subclasses to specify placement preferences.
  * 获取RDD某一个分区的数据存储在哪一个机器上
 */
protected def getPreferredLocations(split: Partition): Seq[String] = Nil

/** Optionally overridden by subclasses to specify how they are partitioned.
  * 分区器
  * */
@transient val partitioner: Option[Partitioner] = None
```

## RDD的创建方式

1. 从一个稳定的存储系统中，比如HDFS文件
2. 从一个存在的RDD上可以创建一个RDD
3. 从内存中已存在的序列列表中

```scala
package com.hollysys.spark

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Created by shirukai on 2018/6/21
  */
object RDDCreationTest {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName(this.getClass.toString).setMaster("local")
    val sc = new SparkContext(conf)

    //创建RDD的方法
    //1.从一个稳定的存储系统中，比如hdfs文件，或者本地文件系统
    val hdfsFileRDD = sc.textFile("hdfs://cdh-master:8020//user/root/srk/words.txt")
    hdfsFileRDD.count()

    //2.从一个已经存在的RDD中，即RDD的transformation api
    val mapRDD = hdfsFileRDD.map(x => x + "test")
    mapRDD.count()

    //3.从一个已经存在于内存中的列表，可以指定分区
    val listRDD = sc.parallelize[Int](Seq(1,2,3,3,4),2)
    listRDD.collect()
    //查看哪个分区有哪些元素
    listRDD.glom().collect()
    //创建一个range RDD 从0到10步长为2，分区个数是4个
    val rangeRDD = sc.range(0,10,2,4)
    rangeRDD.collect()
    /**
      * res7: Array[Long] = Array(0, 2, 4, 6, 8)
      * */

    //与parallelize一样,makeRDD可以指定存储的机器
    val makeRDD = sc.makeRDD(Seq(1,2,3,3,4),2)
    makeRDD.collect()
  }
}
```

## Parallelize



## RDD Dependency

窄依赖：父亲RDD的一个分区的数据只能被子RDD的一个分区消费

宽依赖：父亲RDD的一个分区的数据同时被子RDD的多个分区消费

## RDD分区

从存储系统创建RDD的分区不需要分区

非key-value RDD分区不需要分区

key-value需要分区

### HashPartitioner

partitionBy(newHashPartitioner(2))

### HashPartitioner性能优化

![](https://shirukai.gitee.io/images/6a6801dd01f8fd5cdd1db05d51af86a9.jpg)

两个知识点：

对RDD预分区会提高计算性能

是否保留父RDD的分区器



### RangePartitioner原理

将可以排序的key分到几个大概相等的范围分区中的一个分区汇中

比如一个有10个分区的RDD[(Int,String)]需要按照RangePartitioner重分区为3个分区：

分区一接收>=0且<=10的key的数据

分区二接收>10且<=30的key的数据

分区三接收>30的key的数据

#### 实现步骤如下：

1. 对每一个分区进行数据采样并计算每一个采样到的数据的权重
2. 根据采样到的数据和权重计算每一个分区的最大的key值
3. 用需要分区的key和上面计算得到的每一个分区最大的key值对比决定这个key所在的分区



### 自定义Partitioner

如果key为url，我们希望域名相同的key进入到同一个分区

我们自定义DomainNamePartitioner

```scala
package com.hollysys.spark

import java.net.URL

import org.apache.spark.{HashPartitioner, Partitioner, SparkContext}

/**
  * Created by shirukai on 2018/6/21
  */

class DomainNamePartitioner(val numParts: Int) extends Partitioner {


  //分多少分区
  override def numPartitions: Int = numParts

  //获取分区
  override def getPartition(key: Any): Int = {
    val domain = new URL(key.toString).getHost
        val code = (domain.hashCode % numParts)
        if (code < 0) {
          code + numParts
        } else {
          code
        }
  }

  override def equals(obj: scala.Any): Boolean = obj match {
    case dnp: DomainNamePartitioner =>
      dnp.numParts == numParts
    case _ => false
  }

  //override def hashCode(): Int = numParts
}

object DomainNamePartitioner {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local", this.getClass.getSimpleName)
    val urlRDD = sc.makeRDD(Seq(("http://baidu.com/test", 2), ("http://baidu.com/index", 2),
      ("http://ali.com/index", 3), ("http://ali.com/bigdata", 4), ("http://baidu.com/change", 3)))
    urlRDD.glom().collect()
    //Array(Array((http://baidu.com/test,2), (http://baidu.com/index,2)),
    // Array((http://hollysys.com/index,3), (http://hollysys.com/bigdata,4), (http://baidu.com/change,3)))
    val hashPartitionedRDD = urlRDD.partitionBy(new HashPartitioner(2))
    hashPartitionedRDD.glom().collect()
    //Array(Array(),
    // Array((http://hollysys.com/index,3), (http://hollysys.com/bigdata,4), (http://baidu.com/change,3), (http://baidu.com/test,2), (http://baidu.com/index,2)))

    val domainNamePartitionedRDD = urlRDD.partitionBy(new DomainNamePartitioner(2))
    val a = domainNamePartitionedRDD.glom().collect()
    println(a)
  }
}
```

### Hash 与Range两种Partitioner对比

![](https://shirukai.gitee.io/images/1ebc29e107ca59af9ab55218ff75516f.jpg)

### coalesce使用场景

改变RDD的分区数

```scala
package com.hollysys.spark

import org.apache.spark.SparkContext

/**
  * Created by shirukai on 2018/6/21
  */
object CoalesceTest {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local",this.getClass.getSimpleName)
    //创建一个RDD，并设置分区数为1000个
    val hdfsFileRDD = sc.textFile("hdfs://cdh-master:8020//user/root/srk/words.txt",1000)
    //查看 hdfsFileRDD的分区数是否为1000
    hdfsFileRDD.partitions.size

    //我们通过coalesce来降低分区数量的目的是：
    //分区太多，每个分区的数据量太少，导致太多的task，我们想介绍task的数量，所以要降低分区数
    //第一个参数表示我们期望的分区数
    //第二个参数表示是否需要经过shuffle来达到我们的分区数
    val coalesceRDD = hdfsFileRDD.coalesce(100,false)
    coalesceRDD.partitions.size
  }
}
```



场景一：将一个含有100个分区的RDD的分区降为10个

APi: hdfsFileRDD.coalesce(10,false)

场景二：将一个含有10个分区的RDD的分区数升为100个

Api: hdfsFileRDD.coalesce(100,false) 不会增

场景三：将一个含有1000个分区的RDD的分区数降为2个

Api：hdfsFileRDD.coalesce(2,true)

场景四：将一个含有10个分区的RDD的分区数升为100个

Api：hdfsFileRDD.coalesce(100,true)

#### hdfsFileRDD.repartition(100) ==hdfsFileRDD.coalesce(100,true)

## 单类型RDD操作API

### RDD基本transformation api 介绍

#### map、flatmap、filter、mapPartitions、mapPatitonWithIndexRDD

```scala
package com.hollysys.spark

import org.apache.spark.SparkContext

/**
  * Created by shirukai on 2018/6/21
  */
object MapApiTest {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local", this.getClass.getSimpleName)
    val listRDD = sc.parallelize(Seq(1, 2, 3, 3, 4), 2)

    val mapRDD = listRDD.map(x => x + 2)
    mapRDD.collect
    //Array(3, 4, 5, 5, 6)
    val users = listRDD.map(x => {
      if (x < 3) User("小于3", x) else User("大于3", x)
    })
    //res0: Array[User] = Array(User(小于3,1), User(小于3,2), User(大于3,3), User(大于3,3), User(大于3,4))


    //scala中的map和flatmap的区别
    val l = List(List(1, 2, 3), List(2, 3, 4))
    l.map(x => x.toString())
    //res0: List[String] = List(List(1, 2, 3), List(2, 3, 4))
    l.flatMap(x => x)
    //res1: List[Int] = List(1, 2, 3, 2, 3, 4)
    0.to(3)
    //res2: scala.collection.immutable.Range.Inclusive = Range(0, 1, 2, 3)

    //spark中的flatMap
    val flatMapRDD = listRDD.flatMap(x => x.to(3))
    flatMapRDD.collect()
    //res3: Array[Int] = Array(1, 2, 3, 2, 3, 3, 3)

    val filterRDD = listRDD.filter(x => x != 1)
    filterRDD.collect()
    //res4: Array[Int] = Array(2, 3, 3, 4)


    //将rdd的每一个分区的数据转成一个数组，进而将所有的分区数据转成一个二维数组
    val glomRDD = listRDD.glom()
    glomRDD.collect()
    //res5: Array[Array[Int]] = Array(Array(1, 2), Array(3, 3, 4))

    val mapPartitionRDD = listRDD.mapPartitions(iterator => {
      iterator.map(x => x + 1)
    })
    mapPartitionRDD.collect()
    //res0: Array[Int] = Array(2, 3, 4, 4, 5)

    val mapPatitonWithIndexRDD = listRDD.mapPartitionsWithIndex((index, iterator) => {
      iterator.map(x => x + index)
    })
    mapPatitonWithIndexRDD.collect()

    mapPartitionRDD.saveAsTextFile("hdfs://localhost:9000/output")

  }
}

case class User(userId: String, amount: Int)
```

### 采样API介绍

#### sample(false,0.1)

![](https://shirukai.gitee.io/images/2e6fc8237adb859ce64b30c7f72b814d.jpg)

```
sample(withReplacement:boolean,fraction:double,seed:Long)
```

有放回采样，无放回采样

如果withReplacement=true的话表示有放回的抽样，采用泊松抽样算法实现

如果withReplacement=false的话表示无返回的抽样，采用伯努利抽样算法实现

fraction表示每一个元素被抽为样本的概率，并不是表示需要抽取的数据量的因子

seed 种子，每一个分区采样的随机种子

#### takeSample(false,5)

![](https://shirukai.gitee.io/images/8f793f2233a15b6ce6466991f698c804.jpg)

#### randomSplit(Array(0.2,0.4,0.4))

```scala
package com.hollysys.spark

import org.apache.spark.{SparkConf, SparkContext}

/**
  * Created by shirukai on 2018/6/22
  * 抽样api测试
  */
object SampleApiTest {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName(this.getClass.getSimpleName).setMaster("local")
    val sc = new SparkContext(conf)
    val listRDD = sc.parallelize(Seq(1, 2, 3, 3), 2)

    //第一个参数为withReplacenment
    //如果withReplacement=true的话表示又放回的抽样，采用泊松抽样算法实现
    //如果withReplacement=false的话表示无放回抽样，采用伯努利抽样算法实现

    //第二个参数为：fraction，表示每一个元素被抽取为样本的概率，并不是表示需要抽取的数据量的因子
    //比如从100个数据中抽样，fraction=0.2，并不是表示需要抽取100*0.2=20个数据，
    //而是100个元素的被抽取为样本的概率为0.2；样本的大小并不是固定的，而是服从二项分布
    //当withReplacement=true的时候，fraction>=0
    //当withReplacement=false的时候，0<fraction<1

    //第三个参数为：reed表示生成随机数的种子，即根据这个reed为rdd的每一个分区生成一个随机种子
    val sampleRDD = listRDD.sample(false, 0.5, 100)
    sampleRDD.glom().collect()
    //Array[Array[Int]] = Array(Array(1), Array(3))

    //按照权重对RDD进行随机抽样切分，有几个权重，就切分成几个RDD
    val splitRDD = listRDD.randomSplit(Array(0.2, 0.8))
    splitRDD.size
    splitRDD(0).glom().collect()
    //res3: Array[Array[Int]] = Array(Array(), Array())
    splitRDD(1).glom().collect()
    //res4: Array[Array[Int]] = Array(Array(1, 2), Array(3, 3))
    


    //随机抽取指定数量的样本数据
    listRDD.takeSample(false, 1, 100)
    //res1: Array[Int] = Array(1)

  }
} 
```

### 分层采样API

分层采样：将数据根据不同的特征组成不同的组，然后按特定条件从不同的组中获取样本并重新组成新的数组。

![](https://shirukai.gitee.io/images/fa2719a2ce0d4a6777cebf84ad31f1b4.jpg)

对于一个键值RDD，key用于分类，value可以使任意的值

然后我们通过fractions参数定义分类条件和采样几率

因此fracions参数定义一个Map[K,Double]类型，其中key是键值的分层条件，Double是满足条件的key条件的采样比例



#### sampleBykey

#### sampleByKeyExact

```scala
    val pairRDD = sc.parallelize[(Int, Int)](Seq(
      (1, 2), (3, 4), (3, 6), (5, 6)
    ), 4)
    pairRDD.collect()
    //Array[(Int, Int)] = Array((1,2), (3,4), (3,6), (5,6))


    //分层采样
    val fractions = Map(1 -> 0.3, 3 -> 0.6, 5 -> 0.3)

    val sampleByKeyRDD = pairRDD.sampleByKey(true, fractions)
    sampleByKeyRDD.glom().collect()
    //Array[Array[(Int, Int)]] = Array(Array((1,2)), Array(), Array(), Array((5,6)))

    val sampleByKeyExacRDD = pairRDD.sampleByKeyExact(true, fractions)
    sampleByKeyExacRDD.glom().collect()

    //res1: Array[Array[(Int, Int)]] = Array(Array((1,2)), Array(), Array((3,6), (3,6)), Array((5,6))
  
```



sampleBykey 和sampleByKeyExact的区别

sampleBykey并不对过滤全量数据。因此只得到近似值

sampleByKeyExtra会对全量数据做采样计算，因此耗费大量的计算资源，但是结果会更准确



### pipe的使用方式及其特点

执行python或者sh脚本，然后生成新的脚本

```scala
package com.hollysys.spark

import org.apache.spark.SparkContext

/**
  * Created by shirukai on 2018/6/27
  */
object pipeTest {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local", this.getClass.getSimpleName)

    val dataRDD = sc.parallelize(List("hi", "hello", "how", "are", "you"), 2)

    //运行进程需要的环境变量
    val env = Map("env" -> "test-env")

    def printPipeContext(func: String => Unit): Unit = {
      val tastkContextData = "this is task context data per partition"
      func(tastkContextData)
    }

    def printRDDElement(ele: String, func: String => Unit): Unit = {
      if (ele == "hello") {
        func("dog")
      } else func(ele)
    }


    val pipeRDD = dataRDD.pipe(Seq("sh", "/Users/shirukai/Desktop/HollySys/Repository/sparkLearn/src/main/resource/echo.sh"),
      env, printPipeContext, printRDDElement, false)

    pipeRDD.glom().collect()

  }
}
```



### RDD基本操作-action

foreach、foreachPartition、collect、take、first、top、max、min

![](https://shirukai.gitee.io/images/5f36509b23712374ed4d5f60d97061d5.jpg)

```scala
package com.hollysys.spark

import org.apache.spark.SparkContext

/**
  * Created by shirukai on 2018/6/27
  */
object BaseActionApiTest {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local", this.getClass.getSimpleName)

    val listRDD = sc.parallelize[Int](Seq(1, 2, 4, 3, 3, 6), 2)

    listRDD.collect()
    //res6: Array[Int] = Array(1, 2, 4, 3, 3, 6)

    listRDD.take(2)
    //res7: Array[Int] = Array(1, 2)

    listRDD.top(2)
    //res8: Array[Int] = Array(6, 4)

    listRDD.first()
    //res9: Int = 1

    listRDD.min()
    //res10: Int = 1

    listRDD.max()
    //res11: Int = 6

    listRDD.takeOrdered(2)
    //res12: Array[Int] = Array(1, 2)


    listRDD.reduce((x, y) => x + y)
    //res13: Int = 19


    listRDD.treeReduce((x, y) => x + y)
    //res14: Int = 19

    listRDD.fold(0)((x, y) => x + y)
    //res15: Int = 19


  }
}

class MyOrdering extends Ordering[Int] {
  override def compare(x: Int, y: Int): Int = {
    x - y
  }
}
```
## key-value类型RDD操作API

```scala
package com.hollysys.spark

import org.apache.spark.SparkContext

/**
  * Created by shirukai on 2018/6/28
  */
object KeyValueCreationTest {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local", this.getClass.getSimpleName)

    val kvPairRDD = sc.parallelize(Seq(
      ("key1", "value1"),
      ("key2", "value2"),
      ("key3", "value3")
    ))
    kvPairRDD.collect()
    //res0: Array[(String, String)] = Array((key1,value1), (key2,value2), (key3,value3))


    val personSeqRDD = sc.parallelize(Seq(
      User("jeffy", 30),
      User("kkk", 20),
      User("jeffy", 30),
      User("kkk", 30)
    ))

    //将RDD变成二元组类型的RDD
    val keyByRDD = personSeqRDD.keyBy(_.userId)
    keyByRDD.collect()
    //res1: Array[(String, User)] = Array((jeffy,User(jeffy,30)), (kkk,User(kkk,20)), (jeffy,User(jeffy,30)), (kkk,User(kkk,30)))

    //等价于
    val keyRDD2 = personSeqRDD.map(user => (user.userId, user))
    keyRDD2.collect()

    val groupByRDD = personSeqRDD.groupBy(_.userId)
    groupByRDD.collect()
    //res3: Array[(String, Iterable[User])] = Array((jeffy,CompactBuffer(User(jeffy,30), User(jeffy,30))), (kkk,CompactBuffer(User(kkk,20), User(kkk,30))))

    
  }
}

case class User(userId: String, amount: Int)
```



### combineByKey 

前三个参数：

![](https://shirukai.gitee.io/images/30196730509fd3fc3c441f8b7256085a.jpg)

```scala
package com.hollysys.spark

import org.apache.spark.SparkContext

import scala.reflect.ClassTag

/**
  * Created by shirukai on 2018/6/28
  */
object CombineByKeyApiTest {
  def test[C: ClassTag]() = {
    println(reflect.classTag[C].runtimeClass.getName)
  }

  def main(args: Array[String]): Unit = {
    test[String]()
    val sc = new SparkContext("local", this.getClass.getSimpleName)

    val pairStrRDD = sc.parallelize[(String, Int)](Seq(
      ("coffee", 1),
      ("coffee", 2),
      ("panda", 3),
      ("coffee", 9)
    ))

    /**
      *
      * 功能：对pairStrRDD这个RDD统计每一个相同key对用的所有value值的累加值以及这个key出现的次数
      * 需要的三个参数
      *
      * createCombiner：V=>C, ==>Int -> (Int,Int)
      * mergeValue:(C,V)=>C, ==>((Int,Int),Int) -> (Int,Int)
      * mergeCombiners:(C,C) =>C ==> ((Int,Int),(Int,Int)) ->(Int,Int)
      *
      */
    def createCombiner = (value: Int) => (value, 1)

    def mergeValue = (acc: (Int, Int), value: Int) => (acc._1 + value, acc._2 + 1)

    def mergeCombiners = (acc1: (Int, Int), acc2: (Int, Int)) => (acc1._1 + acc2._1, acc1._2 + acc2._2)


    val testCombineByKeyRDD =
      pairStrRDD.combineByKey(createCombiner, mergeValue, mergeCombiners)

    testCombineByKeyRDD.collect()

  }
}
```

#### 参数：partitioner

![](https://shirukai.gitee.io/images/ef88defa9389a1d0e4e7ff4124c85129.jpg)

#### 参数：mapSideCombine

![](https://shirukai.gitee.io/images/159e52e42fdcedf115b348df0acbda73.jpg)

#### 参数：serializer

![](https://shirukai.gitee.io/images/d3f0587d725d62219a32322b7bb07a9a.jpg)



### 基于conmbineByKey实现的api详解

aggregateByKey、reduceByKey(distinct是利用reduceByKey实现的)、foldByKey、groupByKey（groupBy是利用groupByKey实现的）

以上api都是基于combineByKey实现的，只是参数不同而已。



