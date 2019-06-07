# CentOS下部署zookeeper集群

版本：zookeeper-3.4.13

## 1 环境准备

### 1.1 准备三台机器

机器信息如下：

| hostname          | ip              | 端口           |
| ----------------- | --------------- | -------------- |
| master.hadoop.com | 192.168.162.180 | 2181/2881/3881 |
| slave1.hadoop.com | 192.168.162.181 | 2181/2881/3881 |
| slave2.hadoop.com | 192.168.162.182 | 2181/2881/3881 |

按照上面信息分别修改hostname

```
vi /etc/hostname 
```

并修改hosts

```
vi /etc/hosts
```

内容如下：

```
192.168.162.180 master.hadoop.com
192.168.162.181 slave1.hadoop.com
192.168.162.182 slave2.hadoop.com
```

### 1.2 安装JDK

#### 1.2.1 官网下载jdk 1.8 

http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

下载jdk-8u151-linux-x64.tar.gz并复制到 /usr/lib目录下

#### 1.2.2 解压

```
tar -zxvf jdk-8u151-linux-x64.tar.gz
```

#### 1.2.3 配置环境变量

```
vim /etc/profile
```

添加如下内容

```
#set java enviroenment
export JAVA_HOME=/usr/lib/jdk1.8.0_151
export PATH=$JAVA_HOME/bin:$PATH
```

使环境变量生效

```
. /etc/profile
```

验证jdk

```
[root@shirukai ~]# java -version
java version "1.8.0_151"
Java(TM) SE Runtime Environment (build 1.8.0_151-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.151-b12, mixed mode)
```

#### 1.2.4 将jdk目录发送到两台Agent主机

```
scp -r /usr/lib/java-1.8.0_151 root@slave1.hadoop.com:/usr/lib/
scp -r /usr/lib/java-1.8.0_151 root@slave2.hadoop.com:/usr/lib/
```

配置环境变量就不要统一发送了，每台机子单独配置，方法跟Service主机一样。

### 1.3 关闭防火墙

#### 1.3.1 停止防火墙

```
systemctl stop firewalld
systemctl status firewalld
```

#### 1.3.2 禁用防火墙（系统启动时不启动防火墙）

```
systemctl disable firewalld
systemctl is-enabled firewalld
```

#### 1.3.3 确保setlinux关闭

临时关闭

```
setenforce 0
```

永久关闭

修改/etc/selinux/config文件中设置SELINUX=disabled ，然后重启服务器

## 2 安装zookeeper

### 2.1 下载zookeeper

下载地址：http://mirrors.shu.edu.cn/apache/zookeeper/zookeeper-3.4.13/zookeeper-3.4.13.tar.gz

```
wget http://mirrors.shu.edu.cn/apache/zookeeper/zookeeper-3.4.13/zookeeper-3.4.13.tar.gz
```

解压zookeeper

```
tar -zxvf zookeeper-3.4.13.tar.gz
```

移动到/root/apps下重命名为zookeeper

```
mv zookeeper-3.4.13 /root/apps/zookeeper
```

### 2.2 修改配置文件

以下操作只在master主机上进行，完成后将zookeeper目录scp到其它两台机子

#### 2.2.1 创建数据目录和日志目录

进入zookeeper目录

```
cd zookeeper
```

创建 data和logs目录

```
mkdir data logs
```

#### 2.2.2 修改配置

##### 2.2.2.1 进入conf目录

```
cd conf
```

##### 2.2.2.2 将zoo_sample.cfg文件重命名为zoo.cfg

```
mv zoo_sample.cfg zoo.cfg
```

##### 2.2.2.3 修改zoo.cfg

```
vi zoo.cfg
```

##### 2.2.2.4 修改内容如下：

```
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/root/apps/zookeeper/data
dataLogDir=/root/apps/zookeeper/logs
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
server.1=master.hadoop.com:2881:3881
server.2=slave1.hadoop.com:2881:3881
server.3=slave2.hadoop.com:2881:3881
```

##### 2.2.2.5 参数说明：

tickTime=2000

> tickTime这个时间是作为Zookeeper服务器之间或客户端之间维持心跳的时间间隔，也就是每个tickTime时间就会发送一次心跳

initLimit=10

> initLimit 这个配置项是用来皮质zookeeper接收客户端（Leader 或Follwer）初始化连接时最长能忍受多少个心跳时间间隔数。当已经超过10个心跳时间长度后zookeeper服务器还没有收到客户端的返回信息，那么表名这个客户端连接失败，总的时间长度就是10*2000=20秒

syncLimit=5 

>syncLimit这个配置项标识Leader与Follower之间发送消息,请求和应答时间长度,最长不能超过多少个tickTime的时间长度,总的时间长度就是5*2000=10秒 

dataDir=/root/apps/zookeeper/data

>dataDir顾名思义就是Zookeeper保存数据的目录,默认情况下Zookeeper将写数据的日志文件也保存在这个目录里。 

clientPort=2181 

> clientPort这个端口就是客户端（应用程序）连接Zookeeper服务器的端口,Zookeeper会监听这个端口接受客户端的访问请求。 

server.A=B：C：D 

> A是一个数字,表示这个是第几号服务器；
>
> B是这个服务器的IP地址（或者是与IP地址做了映射的主机名）；
>
> C第一个端口用来集群成员的信息交换,表示这个服务器与集群中的Leader服务器交换信息的端口；
>
> D是在leader挂掉时专门用来进行选举leader所用的端口。

##### 2.2.2.6 创建myid文件

在/root/apps/zookeeper/data目录下创建一个myid文件

```
cd /root/apps/zookeeper/data
vi myid
```

内容为1，其它两台分别为2，3

### 2.3 主机分发

在master主机上将修改后的zookeeper文件夹分发到其它两台主机上

```
scp -r /root/apps/zookeeper/ slave1.hadoop.com:/root/apps/
scp -r /root/apps/zookeeper/ slave2.hadoop.com:/root/apps/
```

然后只需要修改/root/apps/zookeeper/data/myid文件，分别为2 ，3即可

### 2.4 启动zookeeper

分别在三台主机上执行以下命令：

```
sh /root/apps/zookeeper/bin/zkServer.sh start
```

查看状态

```
sh /root/apps/zookeeper/bin/zkServer.sh status
```

停止服务

```
sh /root/apps/zookeeper/bin/zkServer.sh stop
```