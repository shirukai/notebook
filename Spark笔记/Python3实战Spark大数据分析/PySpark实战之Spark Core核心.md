# ySpark实战之Spark Core核心

## 1 RDD常用操作

RDD操作有两种：Transformation和Action

Transformation：从一个已有的RDD中创建一个新的RDD

Action：执行计算，返回一个结果

### 1.1 Transformations算子

| Transformation                                            | Meaning                                                      |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| map(func)                                                 | 遍历已有的RDD中的每个元素，并应用func函数，生成新的RDD返回。 |
| filter(func)                                              | 应用func函数过滤已有RDD的每个元素，生成新的RDD返回。         |
| flatMap(func)                                             | 与map类似，但每个输入项可以映射到0个或更多输出项（因此func应该返回Seq而不是单个项。 |
| mapPartitions(func)                                       | 与map类似，但在RDD的每个分区（块）上单独运行，因此当在类型T的RDD上运行时，func必须是Iterator <T> => Iterator <U>类型。 |
| mapPartitionsWithIndex(func)                              | 与mapPartitions类似，但也为func提供了表示分区索引的整数值，因此当在类型T的RDD上运行时，func必须是类型（Int,Iterator <T>）=> Iterator <U>。 |
| sample(withReplacement, fraction, seed)                   | 使用给定的随机数生成器种子，在有或没有替换的情况下对数据的一小部分进行采样。 |
| union(otherDataset)                                       | 返回一个新数据集，其中包含源数据集和参数中元素的并集。       |
| intersection(otherDataset)                                | 返回包含源数据集和参数中元素交集的新RDD。                    |
| distinct([numPartitions]))                                | 返回包含源数据集的不同元素的新数据集。                       |
| groupByKey([numPartitions])                               | 在（K，V）对的数据集上调用时，返回（K，Iterable <V>）对的数据集，注意：如果要对每个键执行聚合（例如总和或平均值）进行分组，则使用reduceByKey或aggregateByKey将产生更好的性能。<br/>注意：默认情况下，输出中的并行级别取决于父RDD的分区数。 您可以传递可选的numPartitions参数来设置不同数量的任务。 |
| reduceByKey(func, [numPartitions])                        | 当调用（K，V）对的数据集时，返回（K，V）对的数据集，其中使用给定的reduce函数func聚合每个键的值，该函数必须是类型（V，V）=> V.与groupByKey类似，reduce任务的数量可通过可选的第二个参数进行配置。 |
| aggregateByKey(zeroValue)(seqOp, combOp, [numPartitions]) | 当调用（K，V）对的数据集时，返回（K，U）对的数据集，其中使用给定的组合函数和中性“零”值聚合每个键的值。 允许与输入值类型不同的聚合值类型，同时避免不必要的分配。 与groupByKey类似，reduce任务的数量可通过可选的第二个参数进行配置。 |
| sortByKey([ascending], [numPartitions])                   | 当调用K实现Ordered的（K，V）对数据集时，返回按键升序或降序排序的（K，V）对的数据集，如布尔升序参数中所指定。 |
| join(otherDataset, [numPartitions])                       | 当调用类型（K，V）和（K，W）的数据集时，返回（K，（V，W））对的数据集以及每个键的所有元素对。 通过leftOuterJoin，rightOuterJoin和fullOuterJoin支持外连接。 |
| cogroup(otherDataset, [numPartitions])                    | 当调用类型（K，V）和（K，W）的数据集时，返回（K，（Iterable <V>，Iterable <W>））元组的数据集。 此操作也称为groupWith。 |
| cartesian(otherDataset)                                   | 当调用类型T和U的数据集时，返回（T，U）对的数据集（所有元素对）。 |
| pipe(command, [envVars])                                  | 通过shell命令管道RDD的每个分区，例如， 一个Perl或bash脚本。 RDD元素被写入进程的stdin，并且输出到其stdout的行将作为字符串的RDD返回。 |
| coalesce(numPartitions)                                   | 将RDD中的分区数减少为numPartitions。 过滤大型数据集后，可以更有效地运行操作。 |
| repartition(numPartitions)                                | 随机重新调整RDD中的数据以创建更多或更少的分区并在它们之间进行平衡。 这总是随机播放网络上的所有数据。 |
| repartitionAndSortWithinPartitions(partitioner)           | 根据给定的分区重新分区RDD，并在每个生成的分区中按键对记录进行排序。 这比调用重新分区然后在每个分区内排序更有效，因为它可以将排序推送到shuffle机器中。 |
### 1.2 Actions算子

| Action                                   | Meaning                                                      |
| ---------------------------------------- | ------------------------------------------------------------ |
| reduce(func)                             | 使用函数func（它接受两个参数并返回一个）来聚合数据集的元素。 该函数应该是可交换的和关联的，以便可以并行正确计算。 |
| collect()                                | 在驱动程序中将数据集的所有元素作为数组返回。 在过滤器或其他返回足够小的数据子集的操作之后，这通常很有用。 |
| count()                                  | 返回数据集中的元素数。                                       |
| first()                                  | 返回数据集的第一个元素（类似于take(1)）。                    |
| take(n)                                  | 返回包含数据集的前n个元素的数组。                            |
| takeSample(withReplacement, num, [seed]) | 返回一个数组，其中包含数据集的num个元素的随机样本，有或没有替换，可选地预先指定随机数生成器种子。 |
| takeOrdered(n, [ordering])               | 使用自然顺序或自定义比较器返回RDD的前n个元素。               |
| saveAsTextFile(path)                     | 将数据集的元素作为文本文件（或文本文件集）写入本地文件系统，HDFS或任何其他Hadoop支持的文件系统的给定目录中。 Spark将在每个元素上调用toString，将其转换为文件中的一行文本。 |
| saveAsSequenceFile(path(Java and Scala)  | 将数据集的元素作为Hadoop SequenceFile写入本地文件系统，HDFS或任何其他Hadoop支持的文件系统中的给定路径中。 这可以在实现Hadoop的Writable接口的键值对的RDD上使用。 在Scala中，它也可以在可隐式转换为Writable的类型上使用（Spark包括基本类型的转换，如Int，Double，String等）。 |
| saveAsObjectFile(path) (Java and Scala)  | 使用Java序列化以简单格式编写数据集的元素，然后可以使用SparkContext.objectFile（）加载。 |
| countByKey()                             | 仅适用于类型（K，V）的RDD。 返回（K，Int）对的散列映射以及每个键的计数。 |
| foreach(func)                            | 在数据集的每个元素上运行函数func。 这通常用于副作用，例如更新累加器或与外部存储系统交互。注意：在foreach（）之外修改除累加器之外的变量可能会导致未定义的行为。 有关详细信息，请参阅了解闭包。 |

### 1.3 常用算子

#### 1.3.1 map

map(func):将func函数作用到数据集的每一个元素上，生成一个新的数据集返回。

```python
        data = [1, 2, 3, 4, 5]
        rdd1 = sc.parallelize(data)
        rdd2 = rdd1.map(lambda x: x * 2)
        print(rdd2.collect())
        """
        [2, 4, 6, 8, 10]
        """
```

#### 1.3.2 filter

filter(func): 选出所有func返回值为ture的元素，生成一个新的分布式的数据集返回

```python
data = [1, 2, 3, 4, 5]
rdd1 = sc.parallelize(data)
map_rdd = rdd1.map(lambda x: x * 2)
filter_rdd = map_rdd.filter(lambda x: x > 5)
print(filter_rdd.collect())
"""
[6, 8, 10]
"""
```

#### 1.3.3 flatMap

flatMap(func) 输入的item能够被map到0或者多个items输出，返回值是一个Sequence

```python
data = ['hello spark', 'hello world', 'hello world']
rdd = sc.parallelize(data)
print(rdd.flatMap(lambda line: line.split(" ")).collect())
"""
['hello', 'spark', 'hello', 'world', 'hello', 'world']
"""
```

#### 1.3.4 groupByKey

把相同key的数据分发到一起

```python
data = ['hello spark', 'hello world', 'hello world']
rdd = sc.parallelize(data)
mapRdd = rdd.flatMap(lambda line: line.split(" ")).map(lambda x: (x, 1))
groupRdd = mapRdd.groupByKey()
print(groupRdd.collect())
"""
[('hello', <pyspark.resultiterable.ResultIterable object at 0x10b94ea20>), ('spark', <pyspark.resultiterable.ResultIterable object at 0x10b94ee10>), ('world', <pyspark.resultiterable.ResultIterable object at 0x10b94ef60>)]
"""
print(groupRdd.map(lambda x: {x[0]: list(x[1])}).collect())
"""
[{'hello': [1, 1, 1]}, {'spark': [1]}, {'world': [1, 1]}]
"""
```

#### 1.3.5 reduceByKey

把相同的key的数据分发到一起并进行相应的计算

```python
data = ['hello spark', 'hello world', 'hello world']
rdd = sc.parallelize(data)
mapRdd = rdd.flatMap(lambda line: line.split(" ")).map(lambda x: (x, 1))
reduceByKeyRdd = mapRdd.reduceByKey(lambda a, b: a + b)
print(reduceByKeyRdd.collect())
"""
[('hello', 3), ('spark', 1), ('world', 2)]
"""
```

#### 1.3.6 sortByKey

根据key排序

```python
data = ['hello spark', 'hello world', 'hello world']
rdd = sc.parallelize(data)
mapRdd = rdd.flatMap(lambda line: line.split(" ")).map(lambda x: (x, 1))
reduceByKeyRdd = mapRdd.reduceByKey(lambda a, b: a + b)
print(reduceByKeyRdd.map(lambda x: (x[1], x[0])).sortByKey(True).map(lambda x: (x[1], x[0])).collect())
"""
[('spark', 1), ('world', 2), ('hello', 3)]
"""
```

#### 1.3.7 union

返回一个新数据集，其中包含源数据集和参数中元素的并集。

```python
a = sc.parallelize([1,2,3])
b = sc.parallelize([3,4,5])
print(a.union(b).collect())
"""
[1, 2, 3, 3, 4, 5]
"""
```

#### 1.3.8 distinct

去重

```python
a = sc.parallelize([1,2,3])
b = sc.parallelize([3,4,5])
unionRdd = a.union(b)
print(unionRdd.distinct().collect())
"""
[2, 4, 1, 3, 5]
"""
```

#### 1.3.9 join

inner join

outer join:left/right/full

```python
a = sc.parallelize([("A", "a1"), ("C", "c1"), ("D", "d1"), ("F", "f1"), ("F", "f2")])
b = sc.parallelize([("A", "a2"), ("C", "c2"), ("C", "c3"), ("E", "e1")])
print(a.join(b).collect())
"""
[('C', ('c1', 'c2')), ('C', ('c1', 'c3')), ('A', ('a1', 'a2'))]
"""
```

### 1.3.10 reduce

```python
data = [1, 2, 3, 4, 5, 6, 7, 8]
rdd = sc.parallelize(data)
print(rdd.reduce(lambda x, b: x + b))
"""
36
"""
```

## 2 词频统计

#### 开发步骤分析：

文本内容的每一行转成一个个的单词 flatmap

单词==> (单词，1) map

把所有相同单词的计数相加得到最终的结果 reduceByKey

```python
conf = SparkConf().setMaster("local").setAppName("spark0827")
sc = SparkContext(conf=conf)
input = "file:///Users/shirukai/Desktop/HollySys/Repository/learn-demo-pyspark/data/words.txt"
output = "file:///Users/shirukai/Desktop/HollySys/Repository/learn-demo-pyspark/data/output"
words = sc.textFile(input).map(lambda line: line.replace(". ", " ").replace(", ", " ").rstrip(".")).flatMap(
    lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
words.saveAsTextFile(output)
sc.stop()
```

## 3 核心概述

http://spark.apache.org/docs/latest/cluster-overview.html

### 3.1 相关术语

Application：基于Spark的应用程序 = 1 driver + executors

Driver program：The process running the main() function of the application and creating the SparkContext

Cluster manager：An external service for acquiring resources on the cluster (e.g. standalone manager, Mesos, YARN)

Deploy mode：Distinguishes where the driver process runs. In "cluster" mode, the framework launches the driver inside of the cluster. In "client" mode, the submitter launches the driver outside of the cluster.

Worker node：Any node that can run application code in the cluster

Executor：A process launched for an application on a worker node, that runs tasks and keeps data in memory or disk storage across them. Each application has its own executors.

Task：A unit of work that will be sent to one executor

Job： A parallel computation consisting of multiple tasks that gets spawned in response to a Spark action (e.g. `save`, `collect`); you'll see this term used in the driver's logs.一个action对应一个job

Stage：Each job gets divided into smaller sets of tasks called *stages* that depend on each other (similar to the map and reduce stages in MapReduce); you'll see this term used in the driver's logs.一个stage的边界往往是从某个地方取数据开始，到shuffle的结束。

### 3.1 运行架构及注意事项

![](http://spark.apache.org/docs/latest/img/cluster-overview.png)

关于这个体系结构有几个有用的注意事项：
每个应用程序都有自己的执行器进程，这些进程在整个应用程序期间都处于待机状态，并在多个线程中运行任务。这样做的好处是，在调度侧（每个驱动程序都调度自己的任务）和执行侧（来自不同应用程序的任务在不同的JVM中运行）将应用程序彼此隔离。然而，这也意味着如果不将数据写入外部存储系统，数据就不能在不同的Spark应用程序（SparkContext的实例）之间共享。
Snice是底层集群管理器的不可知论者。只要它能够获取执行器进程，并且这些进程彼此通信，那么即使在也支持其他应用程序（例如，Mesos/YARN）的集群管理器上运行它就相对容易。
驱动程序必须在其整个生命周期中侦听并接受来自其执行器的传入连接（例如，请参阅网络配置部分中的spark...port）。因此，驱动程序必须是从工人节点网络可寻址的。
因为驱动程序在集群上调度任务，所以应该在接近工作节点的地方运行，最好是在相同的局域网上。如果希望远程向集群发送请求，最好向驱动程序打开RPC，让它从附近提交操作，而不是在远离工作节点的地方运行驱动程序。

## 4 spark缓存

http://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-persistence

### 4.1 缓存描述

Spark中最重要的功能之一是在内存中跨操作持久化（或缓存）数据集。当持久化RDD时，每个节点都将其计算的任何分区存储在内存中，并在数据集（或从中派生的数据集）上的其他操作中重用它们。这允许未来的行动要快得多（通常超过10倍）。缓存是迭代算法和快速交互使用的关键工具。

可以使用它的持久persist()或cach()方法标记RDD。当执行第一个action操作时，它将被保存在节点上的内存中。Spark的缓存是容错的——如果RDD的任何分区丢失，它将使用最初创建它的转换自动重新计算。

此外，每个持久化RDD可以使用不同的存储级别来存储，例如，允许您将数据集保存在磁盘上，将其保存在内存中，也可以作为序列化的Java对象（以节省空间），将其复制到节点上。这些级别是通过将StorageLevel对象（Scala、Java、Python）传递到Sturiar()来设置的。cache()方法是使用默认存储级别的简写，即StorageLevel.MEMORY_ONLY（在内存中存储反序列化对象）。

| Storage Level                         | Meaning                                                      |
| ------------------------------------- | ------------------------------------------------------------ |
| MEMORY_ONLY                           | 将RDD存储为JVM中的反序列化Java对象。如果RDD不适合内存，某些分区将不会被缓存，并且将在需要时重新计算。这是默认级别。 |
| MEMORY_AND_DISK                       | 将RDD存储为JVM中的反序列化Java对象。如果RDD不适用于内存，则存储到磁盘，并在需要时从那里读取它们。 |
| MEMORY_ONLY_SER  (Java and Scala)     | 将RDD存储为序列化的Java对象（每个分区的一个字节数组）。这通常比反序列化对象更加节省空间，尤其是在使用快速序列化器时，但是读取时需要更多的CPU。 |
| MEMORY_AND_DISK_SER  (Java and Scala) | 类似于MEMORY_ONLY_SER，但是将不适合内存的分区溢出到磁盘中，而不是在每次需要时动态地重新计算它们。 |
| DISK_ONLY                             | 只在磁盘上存储RDD分区。                                      |
| MEMORY_ONLY_2, MEMORY_AND_DISK_2, etc | 与上面的级别相同，但是在两个群集节点上复制每个分区。         |
| OFF_HEAP (experimental)               | 类似于MexyyOnLySysServer，但将数据存储在堆内存中。这需要启用堆堆内存。 |

cache/persist和其他的tranformation操作一样都是lazy模式，没有遇到action是不会提交作业到spark上运行的。

如果一个RDD在后续的计算中可能会被使用到，那么建议cache

cache底层调用的是persist方法，传入的参数是：StorageLevel.MEMORY_ONLY

```python
def cache(self):
    """
    Persist this RDD with the default storage level (C{MEMORY_ONLY}).
    """
    self.is_cached = True
    self.persist(StorageLevel.MEMORY_ONLY)
    return self
```

移除缓存：unpersist()

### 4.2 选择缓存策略的依据

Spark的存储级别是为了在内存使用和CPU效率之间提供不同的权衡。我们建议通过以下过程来选择一个：

* 如果您的RDDs与默认存储级别（MeimyIyOnLead）适配，那么就把它们保留下来。这是CPU效率最高的选项，允许RDDs上的操作尽可能快地运行。

* 如果没有，请尝试使用MEMORY_ONLY_SER并选择一个快速序列化库来使对象更加节省空间，但是访问速度仍然相当快。（java、scala）

* 不要写数据到磁盘，除非计算数据集的函数是昂贵的，否则它们会过滤大量数据。否则，重新计算分区可能与从磁盘读取一样快。

* 如果需要快速故障恢复（例如，如果使用spark来服务Web应用程序的请求），则使用复制的存储级别。所有存储级别都通过重新计算丢失的数据来提供完全的容错性，但是复制的数据允许您在RDD上继续运行任务，而不必等待重新计算丢失的分区。

## 5 Spark Lineage机制

RDD之间的依赖关系：Lineage

### 5.1 Spark Dependency

窄依赖：一个父RDD的partition之多被子RDD使用一次

![](http://shirukai.gitee.io/images/d38dff1f7082e9abbd9680fbea190d88.jpg)

宽依赖：一个父RDD的partition会被子RDD的partition使用多次，有shuffle

![](http://shirukai.gitee.io/images/1960c4779e1db5bb335d7c993fe78afd.jpg)



