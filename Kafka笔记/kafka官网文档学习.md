# Kafka学习 

## 介绍 

#### kafka是一个分布式流式数据平台，具备以下三个特点：

- 类似消息系统，提供事件流的发布和订阅，即具备数据注入功能
- 存储时间流数据的几点具有故障容错的特点，即具备数据存储功能
- 能够对实时的事件流进行流式地处理和分析，即具备流处理功能

#### kafka通常用户两大类应用：

* 构建可在系统或应用程序之间可靠获取数据的实时流数据管道
* 构建实时流应用程序，用户转换或相应数据流

#### 与kafka相关的概念： 

* kafka作为一个集群运行在一台或多台可以跨越多个数据中心的服务器上
* kafka集群在称为主题的类别中存储记录流
* 每个记录有一个键，一个值和一个时间戳组成


#### kafka有四个核心API：

**Producer API** 允许应用程序发布记录流到一个或者多个kafka的topic

**Consumer API** 允许应用程序订阅一个或多个topic，并处理所产生的对他们记录的数据流

**Streams API** 允许应用程序充当流处理器，从一个或多个topic消费输入流，并产生一个输出流到一个或多个主题，有效的变换输入流到输出流

**Connector API** 允许构建和运行kafka主题连接到现有的应用程序或数据系统中重用生产者或消费者。例如，连接到关系型数据库的连接器可能会捕获对表的买个更改。

![](https://shirukai.gitee.io/images/201803271507_36.png)

## Topics（主题） 和 Logs（日志） 

> 主题是记录发布的类别或提要名称。kafka的主题总是多用户的;也就是说，一个主题可以有零个、一个或多个订阅了写入它的数据的消费者

对于每一个主题，kafka集群都维护一个这样的分区日志：

![](https://shirukai.gitee.io/images/201803271512_908.png)

每个分区都是一个有序的、不可变的记录序列，它被不断地附加到一个结构化的提交日志中。分区中的记录都被分配了一个顺序的id号，称为偏移量，它惟一地标识分区内的每条记录。

kafka的集群可以持续地保存所有已发布的记录——不管它们是否被消费——使用可配置的保留期。例如，如果保留策略被设置为两天，那么在记录发布后的两天内，它将被用于消费，之后将被丢弃以腾出空间。kafka的性能在数据大小方面是有效的，所以长期存储数据并不是问题。

![](https://shirukai.gitee.io/images/201803271514_346.png)

实际上，在每个消费者的基础上保留的元数据是日志中消费者的偏移量或位置。这个偏移量由使用者控制：一般来说，消费者会在读取记录时线性地增加它的偏移量，但是，事实上，由于这个位置是由使用者控制的，它可以按照它喜欢的任何顺序使用记录。例如，消费者可以重新设置旧的偏移量，以重新处理过去的数据，或者跳过最近的记录，开始从“当前”开始消费。

这一功能的结合意味着kafka的消费者非常便宜——他们可以在不影响集群或其他消费者的情况下，也可以不受影响。例如，您可以使用我们的命令行工具来“tail”任何主题的内容，而不需要改变任何现有使用者所消耗的内容。

日志中的分区有几个用途。首先，它们允许日志扩展到可以容纳单个服务器的大小。每个单独的分区必须适合承载它的服务器，但是一个主题可能有多个分区，因此它可以处理任意数量的数据。第二，它们是并行的单元——更多的是关于这一点。

## Distribution（分配）

日志的分区分布在kafka集群中的服务器上，每个服务器处理数据和请求共享分区。每个分区都在可配置数量的服务器上进行复制，以实现容错。

每个分区都有一个充当“领导者”的服务器，以及充当“追随者”的零个或多个服务器。领导者处理所有对该分区的读写请求，而关注者被动地复制领导者。如果领导者失败了，他的一个追随者将自动成为新的领导者。每个服务器都充当某些分区的领导者和其他人的关注者，因此负载在集群中很好地平衡。

## Geo-Replication（地域复制）

Kafka MirrorMaker为您的集群提供了地理复制支持。使用MirrorMaker，消息可以跨多个数据中心或云区域复制。您可以在主动/被动场景中使用它进行备份和恢复;或者在主动/主动方案中，将数据与用户更接近，或者支持数据本地需求。

## Producers 

生产者将数据发布到他们选择的主题。生产者负责选择将哪个记录分配给主题中的哪个分区。这可以以循环方式完成，只是为了平衡负载，或者可以根据某种语义分区功能（例如基于记录中的某个键）完成。更多关于在第二次使用分区！

## Consumers 

消费者用*消费者组*名称标记自己，并且发布到主题的每个记录都被传送到每个订阅消费者组中的一个消费者实例。消费者实例可以在单独的进程中或在单独的机器上。

如果所有消费者实例具有相同的消费者组，则记录将有效地在消费者实例上进行负载均衡。

如果所有消费者实例具有不同的消费者组，则每条记录都将广播给所有消费者进程。

两个服务器Kafka集群托管四个分区（P0-P3）和两个消费者组。消费者组A有两个消费者实例，而组B有四个消费者实例。

然而，更常见的是，我们发现话题的消费者群体很少，每个“逻辑用户”都有一个。每个组由许多消费者实例组成，具有可扩展性和容错性。这只不过是发布 - 订阅语义，订阅者是一群消费者而不是一个进程。

在Kafka中实现消费的方式是将日志中的分区划分为消费者实例，以便每个实例在任何时间点都是“公平分享”分区的独占消费者。这个维护组中成员资格的过程是由Kafka协议动态处理的。如果新实例加入该组，则他们将接管来自该组的其他成员的一些分区; 如果一个实例死亡，其分区将分配给其余实例。

kafka只提供一个分*区内*记录的总顺序，而不是主题中不同分区之间的顺序。按分区排序与按键分区数据的能力相结合，足以满足大多数应用程序的需求。但是，如果您需要全部订单而不是记录，则可以通过仅有一个分区的主题来实现，但这意味着每个消费者组只有一个消费者进程。

## Multi-tenancy(多租户)

您可以将Kafka部署为多租户解决方案。通过配置哪些主题可以产生或使用数据来启用多租户。还有配额操作支持。管理员可以根据请求定义和执行配额以控制客户端使用的代理资源。有关更多信息，请参阅[安全性文档](https://kafka.apache.org/documentation/#security)。

## Guarantees 担保 

在一个高层次的kafka提供以下保证：

- 由制作者发送到特定主题分区的消息将按照它们发送的顺序附加。也就是说，如果记录M1由同一个生产者作为记录M2发送，并且M1被首先发送，则M1将具有比M2更低的偏移并且出现在日志中较早的地方。
- 消费者实例按照它们存储在日志中的顺序查看记录。
- 对于具有复制因子N的主题，我们将容忍多达N-1个服务器的故障，而不会丢失任何提交给日志的记录。

有关这些保证的更多详细信息在文档的设计部分给出。

## kafka作为消息系统

kafka的流概念如何与传统的企业消息传递系统相比较？

消息传统上有两种模式：[排队](http://en.wikipedia.org/wiki/Message_queue)和[发布 - 订阅](http://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)。在队列中，消费者池可以从服务器读取，并且每条记录都会转到其中的一个; 在发布 - 订阅记录被广播给所有消费者。这两种模式都有优势和劣势。排队的优势在于它允许您将多个用户实例中的数据处理分开，从而扩展您的处理。不幸的是，队列不是多用户的 - 一旦一个进程读取数据消失了。发布 - 订阅允许您将数据广播到多个进程，但无法进行扩展处理，因为每条消息都发送给每个订阅者。

kafka的消费群体概念概括了这两个概念。与队列一样，消费者组允许您将一系列流程（消费者组成员）的处理分开。与发布 - 订阅一样，kafka允许您向多个消费者群体广播消息。

kafka模式的优点是每个主题都有这些属性 - 它可以扩展处理，也可以是多用户 - 不需要选择其中一个。

Kafka也比传统的消息系统有更强大的订单保证。

传统队列在服务器上按顺序保留记录，并且如果多个使用者从队列中消耗，则服务器按照它们存储的顺序提交记录。但是，尽管服务器按顺序提交记录，但记录会异步传送给消费者，因此它们可能会针对不同的消费者按顺序到达。这实际上意味着在并行消耗的情况下记录的排序会丢失。消息传递系统通常具有“排他消费者”的概念，只允许一个进程从队列中消费，但这当然意味着处理中没有并行性。

kafka做得更好。通过在主题内部有一个并行概念 - 分区概念，Kafka能够在消费者流程池中提供订单保证和负载均衡。这是通过将主题中的分区分配给使用者组中的使用者来实现的，以便每个分区仅由组中的一位使用者使用。通过这样做，我们确保消费者是该分区的唯一读者，并按顺序使用数据。由于有很多分区，这仍然可以平衡许多消费者实例的负载。但请注意，消费者组中的消费者实例不能多于分区。

## kafka作为存储系统 

任何允许发布消息与消费消息分离的消息队列都可以充当存储系统的空中消息。kafka的不同之处在于它是一个非常好的存储系统。

写入Kafka的数据写入磁盘并进行复制以实现容错。Kafka允许生产者等待确认，以便在完全复制之前写入不被认为是完整的，并且即使写入的服务器失败也能保证写入持续。

Kafka磁盘结构使用的规模很大 - 无论您在服务器上有50 KB还是50 TB的持久性数据，Kafka都会执行相同的操作。

由于把存储的重视，并允许客户控制自己的读取位置的结果，你能想到kafka作为一种特殊用途的分布式文件系统，致力于高性能，低延迟提交日志存储，复制和传播。

## 用于流处理的Kafka 

仅读取，写入和存储数据流是不够的，目的是启用流的实时处理。

在Kafka中，流处理器是指从输入主题获取连续数据流，对该输入执行一些处理并生成连续数据流以输出主题的任何内容。

例如，零售应用程序可能会接受销售和装运的输入流，并输出一系列重新排序和对这些数据计算出的价格调整。

可以直接使用生产者API和消费者API进行简单的处理。然而，对于更复杂的转换，Kafka提供了完全集成的[Streams API](http://kafka.apache.org/documentation/streams)。这允许构建应用程序进行非平凡的处理，从而计算聚合关闭流或将流连接在一起。

这个工具有助于解决这类应用程序面临的难题：处理无序数据，重新处理代码更改的输入，执行有状态的计算等。

流API基于Kafka提供的核心原语构建：它使用生产者API和消费者API输入，使用Kafka进行有状态存储，并在流处理器实例之间使用相同的组机制来实现容错。

## 把碎片放在一起 

消息传递，存储和流处理的这种组合可能看起来很不寻常，但对于Kafka作为流式传输平台的角色来说，这是非常重要的。

像HDFS这样的分布式文件系统允许存储用于批处理的静态文件。有效地，这样的系统允许存储和处理过去的*历史*数据。

传统的企业消息传递系统允许处理订阅后将来的消息。以这种方式构建的应用程序处理将来的数据。

Kafka结合了这两种功能，而且这两种组合对于Kafka用作流式传输应用平台和流式数据管道都非常重要。

通过将存储和低延迟订阅相结合，流式应用可以以相同的方式处理过去和未来的数据。这是一个单一的应用程序可以处理历史的，存储的数据，而不是在它达到最后一个记录时结束，它可以在将来的数据到达时继续处理。这是流处理的一般概念，包括批处理以及消息驱动的应用程序。

同样，对于流式数据流水线，订阅实时事件的组合使得可以将Kafka用于非常低延迟的流水线; 但可靠地存储数据的能力可以将其用于必须保证数据交付的关键数据，或者与只能定期加载数据的离线系统集成，或者可能在较长时间内停机进行维护。流处理设施可以在数据到达时进行转换。

## 在shell 命令行对kafka进行操作 

### 创建一个topic

我们用一个分区和一个副本创建一个名为“srktest"的主题

```
/usr/lib/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

查看主题列表

```
/usr/lib/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181
```

也可以将代理设置为在发布不存在的主题时自动创建主题，而不是手动创建主题。

### 发送消息 

Kafka附带一个命令行客户端，它将从文件或标准输入中获取输入，并将其作为消息发送到Kafka集群。默认情况下，每行将作为单独的消息发送。

运行生产者，然后在控制台中输入几条消息发送到服务器

```
[root@localhost ~]# /usr/lib/kafka/bin/kafka-console-producer.sh --broker-list 192.168.1.88:9092 --topic srktest
>This is my first kafka's message from shell client
>haha is ok?
```

### 启动消费者 

kafka也有一个命令行消费者，将消息转储到标准输出。

```
[root@localhost ~]# /usr/lib/kafka/bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.88:9092 --topic srktest --from-beginning
This is my first kafka's message from shell client
haha is ok?
```

如果您将上述每个命令都在不同的终端中运行，那么您现在应该能够将消息键入生产者终端，并将它们显示在消费者终端中。

所有的命令行工具都有其他选项; 在没有参数的情况下运行该命令将显示更详细地记录它们的使用信息。

### 设置多代理集群 

在单机环境下扩展kafka的节点，组成集群

首先我们为每个代理创建一个配置文件

```
cp config/server.properties config/server-1.properties
cp config/server.properties config/server-2.properties
```

现在编辑这些新文件并设置下列属性：

```
config/server-1.properties:
    broker.id=1
    listeners=PLAINTEXT://:9093
    log.dir=/tmp/kafka-logs-1
 
config/server-2.properties:
    broker.id=2
    listeners=PLAINTEXT://:9094
    log.dir=/tmp/kafka-logs-2
```

该`broker.id`属性是群集中每个节点的唯一且永久的名称。我们必须覆盖端口和日志目录，因为我们在同一台机器上运行这些端口和日志目录，并且我们希望让所有代理都试图在同一个端口注册或覆盖彼此的数据。

我们已经有Zookeeper和我们的单个节点，所以我们只需要启动两个新节点：

```
> bin/kafka-server-start.sh config/server-1.properties &
...
> bin/kafka-server-start.sh config/server-2.properties &
...
```

现在创建一个复制因子为三的新主题

```
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicate-topic
```

好吧，但现在我们有一个集群，我们怎么知道哪个经纪人在做什么？要查看运行“describe”命令：

```
bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic  my-replicate-topic
Topic:my-replicate-topic	PartitionCount:1	ReplicationFactor:3	Configs:
	Topic: my-replicate-topic	Partition: 0	Leader: 0	Replicas: 0,1,3	Isr: 0,1,3
```

这里是对输出的解释，第一行给出所有分区的摘要，每个附加行提供有关一个分区的信息，由于我们只有一个分区，所以只有一行数据。

* leader 是负责给定分区的所有读写操作的节点，每个节点将成为分区随机选择部分的领导者
* replicas 是复制此分区的日志的节点列表，无论是不是领导者，是不是还存活着
* isr ”是一组“同步”副本。这是复制品列表的子集，目前活着并被引导到领导者身边。




## java客户端操作kafka 

### pox依赖 

```
		<dependency>
			<groupId>org.apache.kafka</groupId>
			<artifactId>kafka-clients</artifactId>
			<version>0.11.0.0</version>
		</dependency>
```



### 发送消息 

````
        Properties props = new Properties();
        props.put("bootstrap.servers", "192.168.1.188:9092");//kakfa 服务
        props.put("acks", "all");、//leader 需要等待所有备份都成功写入日志
        props.put("retries", 0);//重试次数
        props.put("batch.size", 16384);
        props.put("linger.ms", 1);
        props.put("buffer.memory", 33554432);
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");//key的序列化方式
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");//value的序列化方式
        Producer<String, String> producer = new KafkaProducer<String, String>(props);
        for (int i = 0; i < 100; i++)
            producer.send(new ProducerRecord<String, String>("srktest", "client" + i, "this message from client" + i));
        producer.close();
````

### 接受消息 

```
        Properties props = new Properties();
        props.put("bootstrap.servers", "192.168.1.188:9092");
        props.put("group.id", "srk");
        props.put("enable.auto.commit", "false");
        props.put("auto.offset.reset", "earliest");
        props.put("auto.commit.interval.ms", "1000");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(props);
        consumer.subscribe(Arrays.asList("srktest"));
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(100);
            for (ConsumerRecord<String, String> record : records)
                System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
        }
```



### Producer配置说明

| 名称                                  | 说明                                                         | 类型                      | 默认值                                                       | 有效值       | 重要性 |
| ------------------------------------- | ------------------------------------------------------------ | ------------------------- | ------------------------------------------------------------ | ------------ | ------ |
| bootstrap.servers                     | 用于建立与kafka集群连接的host/port组。数据将会在所有servers上均衡加载，不管哪些server是指定用于bootstrapping。这个列表仅仅影响初始化的hosts（用于发现全部的servers）。这个列表格式：host1:port1,host2:port2,…因为这些server仅仅是用于初始化的连接，以发现集群所有成员关系（可能会动态的变化），这个列表不需要包含所有的servers（你可能想要不止一个server，尽管这样，可能某个server宕机了）。如果没有server在这个列表出现，则发送数据会一直失败，直到列表可用。 | list                      |                                                              |              | 高     |
| acks                                  | producer需要server接收到数据之后发出的确认接收的信号，此项配置就是指procuder需要多少个这样的确认信号。此配置实际上代表了数据备份的可用性。以下设置为常用选项：（1）acks=0： 设置为0表示producer不需要等待任何确认收到的信息。副本将立即加到socket buffer并认为已经发送。没有任何保障可以保证此种情况下server已经成功接收数据，同时重试配置不会发生作用（因为客户端不知道是否失败）回馈的offset会总是设置为-1；（2）acks=1： 这意味着至少要等待leader已经成功将数据写入本地log，但是并没有等待所有follower是否成功写入。这种情况下，如果follower没有成功备份数据，而此时leader又挂掉，则消息会丢失。（3）acks=all： 这意味着leader需要等待所有备份都成功写入日志，这种策略会保证只要有一个备份存活就不会丢失数据。这是最强的保证。， | string                    | -1                                                           | [all -1 0 1] | 高     |
| key.serializer                        | key的序列化方式，若是没有设置，同serializer.class            | 实现Serializer接口的class |                                                              |              | 高     |
| value.serializer                      | value序列化类方式                                            | 实现Serializer接口的class |                                                              |              | 高     |
| buffer.memory                         | producer可以用来缓存数据的内存大小。如果数据产生速度大于向broker发送的速度，producer会阻塞或者抛出异常，以“block.on.buffer.full”来表明。这项设置将和producer能够使用的总内存相关，但并不是一个硬性的限制，因为不是producer使用的所有内存都是用于缓存。一些额外的内存会用于压缩（如果引入压缩机制），同样还有一些用于维护请求。 | long                      | 33554432                                                     |              | 高     |
| compression.type                      | producer用于压缩数据的压缩类型。默认是无压缩。正确的选项值是none、gzip、snappy。压缩最好用于批量处理，批量处理消息越多，压缩性能越好 | string                    | none                                                         |              | 高     |
| retries                               | 设置大于0的值将使客户端重新发送任何数据，一旦这些数据发送失败。注意，这些重试与客户端接收到发送错误时的重试没有什么不同。允许重试将潜在的改变数据的顺序，如果这两个消息记录都是发送到同一个partition，则第一个消息失败第二个发送成功，则第二条消息会比第一条消息出现要早。 | int                       | 0                                                            |              | 高     |
| batch.size                            | producer将试图批处理消息记录，以减少请求次数。这将改善client与server之间的性能。这项配置控制默认的批量处理消息字节数。不会试图处理大于这个字节数的消息字节数。发送到brokers的请求将包含多个批量处理，其中会包含对每个partition的一个请求。较小的批量处理数值比较少用，并且可能降低吞吐量（0则会仅用批量处理）。较大的批量处理数值将会浪费更多内存空间，这样就需要分配特定批量处理数值的内存大小。 | int                       | 16384                                                        |              | 高     |
| client.id                             | 当向server发出请求时，这个字符串会发送给server。目的是能够追踪请求源头，以此来允许ip/port许可列表之外的一些应用可以发送信息。这项应用可以设置任意字符串，因为没有任何功能性的目的，除了记录和跟踪 | string                    | “”                                                           |              | 中     |
| connections.max.idle.ms               | 关闭连接空闲时间                                             | long                      | 540000                                                       |              | 中     |
| linger.ms                             | producer组将会汇总任何在请求与发送之间到达的消息记录一个单独批量的请求。通常来说，这只有在记录产生速度大于发送速度的时候才能发生。然而，在某些条件下，客户端将希望降低请求的数量，甚至降低到中等负载一下。这项设置将通过增加小的延迟来完成–即，不是立即发送一条记录，producer将会等待给定的延迟时间以允许其他消息记录发送，这些消息记录可以批量处理。这可以认为是TCP种Nagle的算法类似。这项设置设定了批量处理的更高的延迟边界：一旦我们获得某个partition的batch.size，他将会立即发送而不顾这项设置，然而如果我们获得消息字节数比这项设置要小的多，我们需要“linger”特定的时间以获取更多的消息。 这个设置默认为0，即没有延迟。设定linger.ms=5，例如，将会减少请求数目，但是同时会增加5ms的延迟。 | long                      | 0                                                            |              | 中     |
| max.block.ms                          | 控制block的时长,当buffer空间不够或者metadata丢失时产生block  | long                      | 60000                                                        |              | 中     |
| max.request.size                      | 请求的最大字节数。这也是对最大记录尺寸的有效覆盖。注意：server具有自己对消息记录尺寸的覆盖，这些尺寸和这个设置不同。此项设置将会限制producer每次批量发送请求的数目，以防发出巨量的请求。 | int                       | 1048576                                                      |              | 中     |
| partitioner.class                     | 分区类                                                       | 实现Partitioner 的class   | class org.apache.kafka.clients.producer.internals.DefaultPartitioner |              | 中     |
| receive.buffer.bytes                  | socket的接收缓存空间大小,当阅读数据时使用                    | int                       | 32768                                                        |              | 中     |
| request.timeout.ms                    | 客户端将等待请求的响应的最大时间,如果在这个时间内没有收到响应，客户端将重发请求;超过重试次数将抛异常 | int                       | 3000                                                         |              | 中     |
| send.buffer.bytes                     | 发送数据时的缓存空间大小                                     | int                       | 131072                                                       |              | 中     |
| timeout.ms                            | 此配置选项控制server等待来自followers的确认的最大时间。如果确认的请求数目在此时间内没有实现，则会返回一个错误。这个超时限制是以server端度量的，没有包含请求的网络延迟 | int                       | 30000                                                        |              | 中     |
| max.in.flight.requests.per.connection | kafka可以在一个connection中发送多个请求，叫作一个flight,这样可以减少开销，但是如果产生错误，可能会造成数据的发送顺序改变,默认是5 (修改） | int                       | 5                                                            |              | 低     |
| metadata.fetch.timeout.ms             | 是指我们所获取的一些元素据的第一个时间数据。元素据包含：topic，host，partitions。此项配置是指当等待元素据fetch成功完成所需要的时间，否则会跑出异常给客户端 | long                      | 60000                                                        |              | 低     |
| metadata.max.age.ms                   | 以微秒为单位的时间，是在我们强制更新metadata的时间间隔。即使我们没有看到任何partition leadership改变。 | long                      | 300000                                                       |              | 低     |
| metric.reporters                      | 类的列表，用于衡量指标。实现MetricReporter接口，将允许增加一些类，这些类在新的衡量指标产生时就会改变。JmxReporter总会包含用于注册JMX统计 | list                      | none                                                         |              | 低     |
| metrics.num.samples                   | 用于维护metrics的样本数                                      | int                       | 2                                                            |              | 低     |
| metrics.sample.window.ms              | metrics系统维护可配置的样本数量，在一个可修正的window size。这项配置配置了窗口大小，例如。我们可能在30s的期间维护两个样本。当一个窗口推出后，我们会擦除并重写最老的窗口 | long                      | 30000                                                        |              | 低     |
| reconnect.backoff.ms                  | 连接失败时，当我们重新连接时的等待时间。这避免了客户端反复重连 | long                      | 10                                                           |              | 低     |
| retry.backoff.ms                      | 在试图重试失败的produce请求之前的等待时间。避免陷入发送-失败的死循环中 | long                      | 100                                                          |              |        |

### 