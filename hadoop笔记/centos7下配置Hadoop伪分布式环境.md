# Centos7下配置Hadoop伪分布式环境 

Centos 版本：7

Hadoop版本：2.7.4

Java版本：1.8



## 一、安装JDK 

官网下载jdk 1.8

http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

下载jdk-8u151-linux-x64.tar.gz并复制到 /usr/lib目录下

然后解压

```
tar -zxvf jdk-8u151-linux-x64.tar.gz
```

配置环境变量

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

## 二、配置ssh无密码登录 

yum安装openssh-server

```
yum install openssh-server
```

配置无密码登录

```
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
```

验证ssh

```
ssh shirukai.novalocal
```

## 三、关闭防火墙 

a.  查看防火墙状态

```
systemctl status firewalld
```

b.  查看开机是否启动防火墙服务

```
 systemctl is-enabled firewalld
```

c.  关闭防火墙

```
systemctl stop firewalld
systemctl status firewalld
```

d. 警用防火墙（系统启动时不启动防火墙）

```
systemctl disable firewalld
systemctl is-enabled firewalld
```

e. 确保setlinux关闭

```
setenforce 0
```

## 四、下载Hadoop2.7.4 

在usr目录下创建hadoop目录

```
cd /usr
mkdir hadoop
cd hadoop
```

下载hadoop

```
wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz
```

地址：

http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz

解压hadoop-2.7.4.tar.gz

```
tar -zxvf hadoop-2.7.4.tar.gz
```

在 hadoop目录下创建目录

```
mkdir /usr/hadoop/tmp 
mkdir /usr/hadoop/hdfs 
mkdir /usr/hadoop/hdfs/data 
mkdir /usr/hadoop/hdfs/name
```

## 五、配置Hadoop

### 1.配置系统环境变量 

```
vim /etc/profile
```

添加内容

```
#set hadoop path
export HADOOP_HOME=/usr/hadoop/hadoop-2.7.4
export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$PATH
```

#### 配置hosts 

查看当前的ip

```
ifconfig
//记住当前ip：10.110.13.243
```

查看当前主机名

```
[root@shirukai ~]# hostname
shirukai.novalocal
```

修改hosts 

/etc/hosts

```
vim hosts
```

修改内容

```
10.110.13.243  shirukai.novalocal
```



### 2.配置hadoop-env.sh

/usr/hadoop/hadoop-2.7.4/etc/hadoop

将java的环境变量配置到里面指定位置(大约在25行)

```
# The java implementation to use.
export JAVA_HOME=/usr/lib/jdk1.8.0_151
```

### 3.配置yarn-env.sh 

在大约26行位置

```
 25   echo "run java in $JAVA_HOME"
 26   JAVA_HOME=$JAVA_HOME
```

### 4.配置core-site.xml

```
<configuration>
 <property>
    <name>fs.default.name</name>
    <value>hdfs://0.0.0.0:9000</value>
    <description>HDFS的URI，文件系统://namenode标识:端口号</description>
</property>

<property>
    <name>hadoop.tmp.dir</name>
    <value>/usr/hadoop/tmp</value>
    <description>namenode上本地的hadoop临时文件夹</description>
</property>
</configuration>
```

### 5.配置hdfs-site.xml 

```
<configuration>
<property>
    <name>dfs.name.dir</name>
    <value>/usr/hadoop/hdfs/name</value>
    <description>namenode上存储hdfs名字空间元数据 </description>
</property>

<property>
    <name>dfs.data.dir</name>
    <value>/usr/hadoop/hdfs/data</value>
    <description>datanode上数据块的物理存储位置</description>
</property>

<property>
    <name>dfs.replication</name>
    <value>1</value>
    <description>副本个数，配置默认是3,应小于datanode机器数量</description>
</property>
</configuration>

```

### 6.配置mapred-site.xml 

```
<configuration>
<property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
</property>
</configuration>
```

### 7.配置yarn-site.xml 

```
<configuration>
<property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
</property>
<property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>0.0.0.0:8088</value>
</property>
</configuration>
</configuration>
```

### 8.修改slaves 

```
shirukai.novalocal
```

## 六、启动服务 

### 1.格式化namenode 

```
bin/hdfs namenode -format
```

### 2.启动namenode和datanode守护进程 

```
sbin/start-dfs.sh
```

### 3.启动Resourcemanager和NodeManager守护进程

```
sbin/start-yarn.sh
```

### 4.验证 

```
[root@shirukai logs]# jps
3584 SecondaryNameNode
3411 DataNode
3285 NameNode
3753 ResourceManager
5310 Jps
3855 NodeManager
```

浏览器输入

http://10.110.13.243:50070

http://10.110.13.243:8099