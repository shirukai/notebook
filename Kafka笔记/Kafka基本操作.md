# 启动kafka服务器
* 需要启动zookeeper，因为kafka会将topic信息写入zookeeper的brokers目录；
* config/server.properties文件至少需要配置zookeeper信息；
* 通过 
```
bin/kafka-server-start.sh -daemon config/server.properties 
```
启动kafka。

> -daemon表示在后台运行。

# 关闭kafka服务器
* bin目录提供了一个关闭脚本，但好像有问题；
* 可以通过 kill -s TERM $pid 来关闭。

> $pid表示kafka服务器进程编号。

# 创建topic
```
bin/kafka-topics.sh --create --zookeeper master:2181 --replication-factor 1 --partitions 1 --topic test
```
> topic创建成功后，在zookeeper中创建/brokers/topics/test目录，此目录下包括主题的分区信息。并在/tmp/kafka-logs(**默认**)创建test对应的目录，如test-0，表示第一个分区。

# 查看topic
```
bin/kafka-topics.sh --list --zookeeper master:2181
```
# 删除topic
```
bin/kafka-topics.sh --delete --zookeeper master:2181 --topic test
```
> 该操作只是将test主题标志为已删除状态，通过将topic放到zookeeper的/admin/delete_topics目录。如需彻底删除，需要从zookeeper中删除/brokers/topics/test及/admin/delete_topics/test目录，并且需要从/tmp/kafka-logs目录将test对应的目录删除，否则，重建该topic后，会发现topic标记为已删除状态。**若只是恢复处于删除状态的topic，可直接从/admin/delete_topics删除topic目录即可。也就是说，kafka通过zookeeper的这个目录来表示topic的删除状态。**
**在server.properties文件中，将delete.topic.enable=true**可以保证删除主题及相关目录。

# 发送消息
```
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```
> 然后就可以在控制台中输入消息了。

# 接收消息
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```
> 将收到producer发送的消息。新本[0.10.1]版中，consumer是直连broker，而老版是连zookeeper。