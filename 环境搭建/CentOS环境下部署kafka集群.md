# CentOS下部署kakfa集群

zookeeper版本：zookeeper-3.4.13

kakfa版本：kafka_2.11-2.0.0

## 1 环境准备

在已有zookeeper集群上，部署kakfa集群。每个节点上部署一个broker

zookeeper集群主机信息如下：

| hostname          | ip              | 端口           |
| ----------------- | --------------- | -------------- |
| master.hadoop.com | 192.168.162.180 | 2181/2881/3881 |
| slave1.hadoop.com | 192.168.162.181 | 2181/2881/3881 |
| slave2.hadoop.com | 192.168.162.182 | 2181/2881/3881 |

## 2 安装kafka

### 2.1 下载kafka

下载地址：http://mirrors.hust.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz

```
wget http://mirrors.hust.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz
```

解压kafka

```
tar -zxvf kafka_2.11-2.0.0.tgz
```

移动到/root/apps下并重命名kafka

```
mv kafka_2.11-2.0.0 /root/apps/kafka
```

### 2.2 修改配置文件

以下操作只在master主机上进行，完成后将kafka目录scp到其它两台机子

#### 2.2.1 创建日志目录

进入kafka目录

```
cd /root/apps/kafka
```

在此目录创建kafkalogs目录用来存放kafka的日志数据

```
mkdir kafkalogs
```

#### 2.2.2 修改配置文件

```
vi /config/server.properties
```

修改配置说明

```properties
broker.id=0 # 设置broker.id为0,其它两个节点需修改为1，2
listeners=PLAINTEXT://:9092 #监听端口为9092
advertised.listeners=PLAINTEXT://master.hadoop.com:9092 # 设置hostname
log.dirs=/root/apps/kafka/kafkalogs # 日志数据储存位置
zookeeper.connect=master.hadoop.com:2181,slave1.hadoop.com:2181,slave2.hadoop.com:2181 # zookeeper的ip和端口
```

### 2.3 主机分发

在master主机上将修改后的kafka文件夹分发到其它两台主机上,并修改配置文件中的broker.id 和hostname

```
scp -r /root/apps/kafka/ slave1.hadoop.com:/root/apps/
scp -r /root/apps/kafka/ slave2.hadoop.com:/root/apps/
```

### 2.4 启动kafka

启动kakfa之前，先启动zookeeper。然后再启动kafka

```
sh /root/apps/kafka/bin/kafka-server-start.sh -daemon /root/apps/kafka/config/server.properties
```

启动脚本

```shell
#!/bin/bash
#master
echo 'start master zookeeper'
sh /root/apps/zookeeper/bin/zkServer.sh start
echo 'start slave1 zookeeper'
ssh root@slave1.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/zookeeper/bin/zkServer.sh start
exit
eeooff
echo 'start slave2 zookeeper'
ssh root@slave2.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/zookeeper/bin/zkServer.sh start
exit
eeooff
echo 'start mastet kafka'
sh /root/apps/kafka/bin/kafka-server-start.sh -daemon /root/apps/kafka/config/server.properties
echo 'start slave1 kafka'
ssh root@slave1.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/kafka/bin/kafka-server-start.sh -daemon /root/apps/kafka/config/server.properties
exit
eeooff
echo 'start slave2 kafka'
ssh root@slave2.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/kafka/bin/kafka-server-start.sh -daemon /root/apps/kafka/config/server.properties
exit
eeooff
```

停止脚本

```shell
#!/bin/bash
# stop kafka
echo 'stop master kafka'
sh /root/apps/kafka/bin/kafka-server-stop.sh
echo 'stop slave1 kafka'
ssh root@slave1.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/kafka/bin/kafka-server-stop.sh
exit
eeooff
echo 'stop slave2 kafka'
ssh root@slave2.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/kafka/bin/kafka-server-stop.sh
exit
eeooff
# stop zookeeper
echo 'stop master zookeeper'
sh /root/apps/zookeeper/bin/zkServer.sh stop
echo 'stop slave1 zookeeper'
ssh root@slave1.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/zookeeper/bin/zkServer.sh stop
exit
eeooff
echo 'stop slave2 zookeeper'
ssh root@slave2.hadoop.com > /dev/null 2>&1 << eeooff
sh /root/apps/zookeeper/bin/zkServer.sh stop
exit
eeooff
```

## 3 补充：Kafka 单节点部署

### 3.1 kafka单节点单broker部署

单节点，单broker部署与上面集群部署的单个节点的配置差不多。

#### 3.1.1 下载安装包

下载地址：http://mirrors.hust.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz

```
wget http://mirrors.hust.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz
```

#### 3.1.2 解压kafka

```
tar -zxvf kafka_2.11-2.0.0.tgz
```

#### 3.1.3 移动到/root/apps下并重命名kafka

```
mv kafka_2.11-2.0.0 /root/apps/kafka
```

#### 3.2.4 修改配置文件

##### 创建日志目录

进入kafka目录

```
cd /root/apps/kafka
```

在此目录创建kafkalogs目录用来存放kafka的日志数据

```
mkdir kafkalogs
```

##### 修改配置文件

```
vi /config/server.properties
```

修改配置说明

```properties
broker.id=0 
listeners=PLAINTEXT://:9092 #监听端口为9092
advertised.listeners=PLAINTEXT://localhost:9092 # 设置hostname
log.dirs=/root/apps/kafka/kafkalogs # 日志数据储存位置
zookeeper.connect=localhost:2181
```

### 3.2 kafka 单节点多broker部署

单节点多broker的核心是通过修改server.properties配置文件，来实现多broker。

#### 3.2.1 配置文件修改

复制server.properties为server-1.properties、server-2.properties、server-3.properties三个文件

```shell
cd $KAFKA_HOME/config/
cp server.properties server-1.properties
cp server.properties server-2.properties
cp server.properties server-3.properties
```

并分别修改三个配置文件的broker.id=为1、2、3 监听端口为9093、9094、9095 日志目录为/root/apps/kafka/kafkalogs-1、/root/apps/kafka/kafkalogs-2、/root/apps/kafka/kafkalogs-3

server-1.properties的修改内容

```properties
broker.id=1
listeners=PLAINTEXT://:9093 #监听端口为9093
advertised.listeners=PLAINTEXT://localhost:9093 # 设置hostname
log.dirs=/root/apps/kafka/kafkalogs-1 # 日志数据储存位置
zookeeper.connect=localhost:2181
```

server-2.properties的修改内容

```properties
broker.id=2
listeners=PLAINTEXT://:9094 #监听端口为9094
advertised.listeners=PLAINTEXT://localhost:9094 # 设置hostname
log.dirs=/root/apps/kafka/kafkalogs-2 # 日志数据储存位置
zookeeper.connect=localhost:2181
```

server-3.properties的修改内容

```properties
broker.id=3
listeners=PLAINTEXT://:9095 #监听端口为9095
advertised.listeners=PLAINTEXT://localhost:9095 # 设置hostname
log.dirs=/root/apps/kafka/kafkalogs-3 # 日志数据储存位置
zookeeper.connect=localhost:2181
```

#### 3.2.2 启动kafka服务

```
kafka-server-start.sh -daemon /Users/shirukai/apps/kafka/config/server-1.properties 
kafka-server-start.sh -daemon /Users/shirukai/apps/kafka/config/server-2.properties 
kafka-server-start.sh -daemon /Users/shirukai/apps/kafka/config/server-3.properties 
```

## 4 kafka 命令行操作

### 4.1 启动kafka

```shell
kafka-server-start.sh -daemon /Users/shirukai/apps/kafka/config/server.properties 
```

### 4.2 topic相关操作

#### 4.2.1 创建topic

```shell
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic srk-test 
```

--create 表示创建分区

--zookeeper 指定zookeeper的地址

--replication-factor  设置副本系数为1

--partitions 设置分区为1

--topic 设置topic名字为srk-test

![](http://shirukai.gitee.io/images/77ff89aebaf028625b070340e1caebaa.jpg)

#### 4.2.2 查看topic列表

需要指定zookeeper地址

```shell
kafka-topics.sh --list --zookeeper localhost:2181
```

结果：

```shell
shirukaideMacBook-Pro:kafka shirukai$ kafka-topics.sh --list --zookeeper localhost:2181
srk-test
```

#### 4.2.3 查看topic描述信息

查看所有topic的描述信息

```shell
kafka-topics.sh --describe --zookeeper localhost:2181
```

查看指定topic的描述信息

```shell
kafka-topics.sh --describe --zookeeper localhost:2181 --topic srk-test
```

### 4.4 发送消息

```shell
kafka-console-producer.sh --broker-list localhost:9092 --topic srk-test
```

### 4.5 消费消息

```shell
shirukai$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic srk-test --from-beginnig
```

--from-beginnig 代表从头开始消费，之前的数据也能消费到。

![](http://shirukai.gitee.io/images/87b718d2c71125656f9f5891ea470842.gif)





