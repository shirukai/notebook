# Flume的简单安装和使用

> 版本说明：
>
> Flume:1.8.0
>
> Java:1.8.0
>
> 官网地址：http://flume.apache.org/

## 1 Flume的安装

在安装Flume之前，确保已经安装过Java JDK 1.8以上。

### 1.1 下载安装包

从Flume官网下载安装包，下载地址：http://mirror.bit.edu.cn/apache/flume/1.8.0/apache-flume-1.8.0-bin.tar.gz

```shell
wget http://mirror.bit.edu.cn/apache/flume/1.8.0/apache-flume-1.8.0-bin.tar.gz
```

### 1.2 解压安装包

解压下载的安装包

```shell
tar -zxvf apache-flume-1.8.0-bin.tar.gz
```

并重名为flume-1.8.0

```shell
mv apache-flume-1.8.0-bin.tar.gz flume-1.8.0
```

### 1.3 配置环境变量

将Flume添加到环境变量里

```shell
vi ~/.bash_profile
```

添加内容如下：

```shell
export FLUME_HOME=/Users/shirukai/apps/flume-1.8.0
export PATH=$FLUME_HOME/bin:$PATH
```

### 1.4 修改Flume配置

修改Flume的配置，将JAVA_HOME添加到环境配置中

进入Flume安装目录

```shell
cd $FLUME_HOME/conf/
```

复制 flume-env.sh.template 并重名为 flume-env.sh

```shell
cp flume-env.sh.template flume-env.sh
```

完成之后查看Flume版本

```shell
shirukaideMacBook-Pro:conf shirukai$ flume-ng version
Flume 1.8.0
Source code repository: https://git-wip-us.apache.org/repos/asf/flume.git
Revision: 99f591994468633fc6f8701c5fc53e0214b6da4f
Compiled by denes on Fri Sep 15 14:58:00 CEST 2017
From source with checksum fbb44c8c8fb63a49be0a59e27316833d
shirukaideMacBook-Pro:conf shirukai$ vi ~/.bash_profile 
```

## 2 Flume的简单使用

使用Flume的关键就是写配置文件：

A) 配置Source

B) 配置Channel

C) 配置Sink

D) 把以上三个组件串起来

### 2.1 从指定网络端口采集数据输出到控制台

官网例子：http://flume.apache.org/FlumeUserGuide.html#a-simple-example

使用的是Agent类型为netcat

关于netcat参数：

http://flume.apache.org/FlumeUserGuide.html#netcat-tcp-source

a1: agent名称

r1: source的名称

k1: sink的名称

c1: channel的名称

#### 2.1.1 在$FLUME_HOME/conf下创建example.conf配置文件

```shell
vi $FLUME_HOME/conf/example.conf
```

内容如下：

```properties
# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
# sources类型
a1.sources.r1.type = netcat 
# 绑定ip
a1.sources.r1.bind = localhost
# 绑定端口
a1.sources.r1.port = 9999

# Describe the sink
# 将日志输出到控制台
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
# channel类型为内存
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

#### 2.1.2 启动Agent

```shell
flume-ng agent \
--name a1 \
--conf $FLUME_HOME/conf/ \
--conf-file example.conf \
-Dflume.root.logger=INFO,console
```

参数说明：

--name agent的名字

--conf 配置文件的目录

--conf-file 配置文件名

-Dflume.root.logger logger属性

#### 2.1.3 使用telnet进行测试

```shell
telnet 0.0.0.0 9999
```

![](http://shirukai.gitee.io/images/0eaf5b935203d714c55e6bb40da6e08c.gif)

```
Event: { headers:{} body: 6B 61 66 6B 61 0D                               kafka. }
```

Event 是Flume数据传输的基本单元

Event = 可选的header + byte array 

### 2.2 监控一个文件实时采集新增的数据输出到控制台

Agent选型：exec source + memory channel + logger sink

angent类型为：exec source

官网地址:http://flume.apache.org/FlumeUserGuide.html#exec-source

#### 2.2.1 在$FLUME_HOME/conf下创建example-exec.conf配置文件

```shell
vi $FLUME_HOME/conf/example-exec.conf
```

内容如下：

```properties
# example.conf: A single-node Flume configuration

# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
# sources类型
a1.sources.r1.type = exec 
# 绑定命令
a1.sources.r1.command = tail -f /Users/shirukai/data.log
# 指定shell
a1.sources.r1.shell = /bin/sh -c

# Describe the sink
# 将日志输出到控制台
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
# channel类型为内存
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

#### 2.2.2 启动Agent

```shell
flume-ng agent \
--name a1 \
--conf $FLUME_HOME/conf/ \
--conf-file example-exec.conf \
-Dflume.root.logger=INFO,console
```

#### 2.2.3 向/Users/shirukai/data.log追加内容

```shell
shirukaideMacBook-Pro:~ shirukai$ echo hello >> data.log 
```

![](http://shirukai.gitee.io/images/f81a0e2585636cc6eba23d8d050dd13d.gif)

### 2.3 将A服务器上的日志实时采集到B服务器

#### 2.3.1 设计思路

将A服务器上的日志通过exec source 收集起来，经过memory channel 然后通过avro sink 发送到B服务器上。

B服务器通过avro source 接收数据，经过memory channel 然后通过 logger sink 将信息打印到控制台上，如下图所示

![](http://shirukai.gitee.io/images/00db23449ff20e4da7203d8e2becc586.jpg)

这里通过再一台机器上不同的的Agent来模拟两台服务器。将设两个Agent的名字分别为：agent1、agent2，技术选型如下：

agent1：exec source + memory channel + avro sink

agent2: avro source + memory channel + avor sink 

#### 2.3.2 创建agent1的配置文件：exec-memory-avro-agent1.conf

创建文件：

```shell
vi $FLUME_HOME/conf/exec-memory-avro-agent1.conf
```

内容如下:

```properties
agent1.sources = exec-source
agent1.sinks = avro-sink
agent1.channels = memory-channel

# Describe/configure the source
# sources类型
agent1.sources.exec-source.type = exec
agent1.sources.exec-source.command = tail -f /Users/shirukai/data.log
agent1.sources.exec-source.shell = /bin/sh -c

agent1.sinks.avro-sink.type = logger
        
agent1.channels.memory-channel.type = memory
agent1.channels.memory-channel.capacity = 1000
agent1.channels.memory-channel.transactionCapacity = 100

agent1.sources.exec-source.channels = memory-channel
agent1.sinks.avro-sink.channel = memory-channel
```



#### 2.3.3 创建agent2的配置文件：avro-memory-logger-agent2.conf

创建文件：

```shell
vi $FLUME_HOME/conf/avro-memory-logger-agent2.conf
```

内容如下:

```properties
agent2.sources = avro-source
agent2.sinks = logger-sink
agent2.channels = memory-channel

agent2.sources.avro-source.type = avro 
agent2.sources.avro-source.bind = localhost
agent2.sources.avro-source.port = 9999

agent2.sinks.logger-sink.type = logger

agent2.channels.memory-channel.type = memory
agent2.channels.memory-channel.capacity = 1000
agent2.channels.memory-channel.transactionCapacity = 100

agent2.sources.avro-source.channels = memory-channel
agent2.sinks.logger-sink.channel = memory-channel
```

#### 2.3.4 启动Agent测试

启动agent2：

```shell
flume-ng agent \
--name agent2 \
--conf $FLUME_HOME/conf/ \
--conf-file avro-memory-logger-agent2.conf \
-Dflume.root.logger=INFO,console
```

启动agent1：

```shell
flume-ng agent \
--name agent1 \
--conf $FLUME_HOME/conf/ \
--conf-file exec-memory-avro-agent1.conf \
-Dflume.root.logger=INFO,console
```

测试

![](http://shirukai.gitee.io/images/f128b2c335c8d6e847fad46fee5cbaa7.gif)



### 2.4 将A服务器上的日志实时采集到B服务器然后将数据发送到Kafka

#### 2.4.1 设计思路

上面一个例子，我们实现了将A服务器商的日志，实时采集到B服务器，B服务器将信息打印到控制台上。这里我们对2.3的例子进行改造，将B服务器接收的信息发送到kafka上。这时候就要用到flume的kafka Sink，官网地址：http://flume.apache.org/FlumeUserGuide.html#kafka-sink

整个流程如下图所示：

![](http://shirukai.gitee.io/images/f8ea83fbc65e76a9cab932eb7bf14f37.jpg)

#### 2.4.2 环境准备

确保已经启动kafka，kafka版本为[kafka_2.12-2.0.0.tgz](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.0.0/kafka_2.12-2.0.0.tgz)，服务地址localhost:9092

#### 2.4.3 创建agent

在上面2.3例子的基础上，我们可以继续使用agent1的配合文件，然后在agent2的基础上，创建agent3的配置文件 avro-memory-kafka-agent3.conf。

创建文件avro-memory-kafka-agent3.conf

```shell
vi avro-memory-kafka-agent3.conf
```

内容如下：

```shell
agent3.sources = avro-source
agent3.sinks = kafka-sink
agent3.channels = memory-channel

agent3.sources.avro-source.type = avro 
agent3.sources.avro-source.bind = localhost
agent3.sources.avro-source.port = 9999

agent3.sinks.kafka-sink.type = org.apache.flume.sink.kafka.KafkaSink
agent3.sinks.kafka-sink.kafka.topic = flume-test
agent3.sinks.kafka-sink.kafka.bootstrap.servers = localhost:9092

agent3.channels.memory-channel.type = memory
agent3.channels.memory-channel.capacity = 1000
agent3.channels.memory-channel.transactionCapacity = 100

agent3.sources.avro-source.channels = memory-channel
agent3.sinks.kafka-sink.channel = memory-channel
```

#### 2.4.4 使用Java 客户端来读取Kafka

上面我们可以通过flume将信息发送到kafka里，现在需要使用Java来写一个客户端Kafka consumer 来消费数据。

FlumeMessageConsumer.java

```java
package com.springboot.demo.kafka;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.Arrays;
import java.util.Properties;

/**
 * Created by shirukai on 2018/10/15
 */
public class FlumeMessageConsumer {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        //五位数
        props.put("group.id", "123456");
        props.put("enable.auto.commit", "false");
        props.put("auto.offset.reset", "earliest");
        props.put("auto.commit.interval.ms", "1000");

        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList("flume-test"));
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
        while (true) {
            for (ConsumerRecord<String, String> record : records) {
                System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
            }
        }
    }
}
```

#### 2.4.5 启动测试

##### 启动Kafka

```shell
 sh /Users/shirukai/apps/kafka/bin/kafka-server-start.sh -daemon /Users/shirukai/apps/kafka/config/server.properties
```

##### 启动kafka consumer

执行FlumeMessageConsumer类的 main 方法

##### 启动Agent3

```shell
flume-ng agent \
--name agent3 \
--conf-file /Users/shirukai/apps/flume-1.8.0/conf/avro-memory-kafka-agent3.conf \
-Dflume.root.logger=INFO,console
```

##### 启动Agent1

```shell
flume-ng agent \
--name agent1 \
--conf-file /Users/shirukai/apps/flume-1.8.0/conf/exec-memory-avro-agent1.conf \
-Dflume.root.logger=INFO,console
```

![](http://shirukai.gitee.io/images/7b17bf6fdf2fd0d0d1b0fcf1517424ce.gif)