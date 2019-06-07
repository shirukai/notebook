#  配置Hadoop全分布式环境 

## 一、准备工作

### 准备三台虚机并保证能相互ping通 

| 序号   | IP地址            | 主机名           | 类型       | 用户名  |
| ---- | --------------- | ------------- | -------- | ---- |
| 1    | 192.168.162.177 | Master.Hadoop | NameNode | root |
| 2    | 192.168.162.155 | Slave1.Hadoop | DataNode | root |
| 3    | 192.168.162.166 | Slave2.Hadoop | DataNode | root |

### 主机名的修改：

```
vim /etc/hostname
```

按照一定的格式修改三台机器的主机名。

### 配置Hosts

```
vim /etc/hosts
```

### 添加映射到hosts文件 

```
192.168.162.177 Master.Hadoop
192.168.162.155 Slave1.Hadoop
192.168.162.166 Slave2.Hadoop
```

三台机器配置相同的hosts



## 二、关闭防火墙

1. ### 查看防火墙状态

```
systemctl status firewalld
```

2. ### 查看开机是否启动防火墙服务

```
 systemctl is-enabled firewalld
```

3. ### 关闭防火墙

```
systemctl stop firewalld
systemctl status firewalld
```

4. ### 警用防火墙（系统启动时不启动防火墙）

```
systemctl disable firewalld
systemctl is-enabled firewalld
```

5. ### 确保setlinux关闭

```
setenforce 0
```



## 三、免密登录 

首先虚机需要安装ssh如果没有安装，可以通过yum进行安装

```
yum install openssh-server
yum install openssh-clients
```

> 为什么要免密登录？

因为我们的nameNode与dataNode是在不同的主机上，我们需要主机间做互信，nameNode可以不用密码登录到dataNode。

### Master.Hadoop 

在master主机输入生成秘钥

```
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
```

将秘钥追加到authorized_keys 

```
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
```

然后利用scp将其复制到两个slave主机上

### Slave1

在Slave1主机上输入

```
scp root@Master.Hadoop:~/.ssh/id_dsa.pub ~/.ssh/master_dsa.pub

cat ~/.ssh/master_dsa.pub >> ~/.ssh/authorized_keys
```

### Slave2 

在Slave2主机输入

```
scp root@Master.Hadoop:~/.ssh/id_dsa.pub ~/.ssh/master_dsa.pub

cat ~/.ssh/master_dsa.pub >> ~/.ssh/authorized_keys
```

### 测试 

在master主机上连接两个主机，如果不需要密码，说明免密成功

```
ssh Stave1.Hadoop
exit
ssh Stave2.Hadoop
exit
```

## 四、配置JDK 

> 在master主机上配置jdk，然后scp到其他两台主机即可。

### 官网下载jdk 1.8 

http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

下载jdk-8u151-linux-x64.tar.gz并复制到 /usr/lib目录下

### 解压

```
tar -zxvf jdk-8u151-linux-x64.tar.gz
```

### 配置环境变量

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

### 验证jdk 

```
[root@shirukai ~]# java -version
java version "1.8.0_151"
Java(TM) SE Runtime Environment (build 1.8.0_151-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.151-b12, mixed mode)
```

### 将jdk目录发送到两台Slave主机

```
scp -r /usr/lib/java-1.8.0_151 root@Slave1.Hadoop:/usr/lib/
scp -r /usr/lib/java-1.8.0_151 root@Slave2.Hadoop:/usr/lib/
```

配置环境变量就不要统一发送了，每台机子单独配置，方法跟master一样。

## 五、下载Hadoop(master主机)

> 注意：这里同样只在master主机下载，并配置，然后利用scp发送到其他两台slave主机上

### 在usr目录下创建hadoop目录

```
cd /usr
mkdir hadoop
cd hadoop
```

### 下载hadoop

```
wget http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz
```

地址：

http://mirror.bit.edu.cn/apache/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz

解压hadoop-2.7.4.tar.gz

```
tar -zxvf hadoop-2.7.4.tar.gz
```

### 在 hadoop目录下创建目录 

```
mkdir /usr/hadoop/tmp 
mkdir /usr/hadoop/hdfs 
mkdir /usr/hadoop/hdfs/data 
mkdir /usr/hadoop/hdfs/name
```

## 六、配置Hadoop

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

### 2.配置hadoop-env.sh

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
    <value>hdfs://Master.Hadoop:9000</value>
    <description>HDFS的URI，文件系统://namenode标识:端口号</description>
</property>

<property>
    <name>hadoop.tmp.dir</name>
    <value>/usr/hadoop/tmp</value>
    <description>namenode上本地的hadoop临时文件夹</description>
</property>
<property>
   <name>io.file.buffer.size</name>
   <value>131073</value>
</property>
</configuration>
```

### 5.配置hdfs-site.xml

```
<configuration>
<property>
    <name>dfs.name.dir</name>
    <value>file:/usr/hadoop/hdfs/name</value>
    <description>namenode上存储hdfs名字空间元数据 </description>
</property>

<property>
    <name>dfs.data.dir</name>
    <value>file:/usr/hadoop/hdfs/data</value>
    <description>datanode上数据块的物理存储位置</description>
</property>
<property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>master.hadoop:9001</value>
</property>
<property>
    <name>dfs.replication</name>
    <value>2</value>
    <description>副本个数，配置默认是3,应小于datanode机器数量</description>
</property>
    <property>
         <name>dfs.webhdfs.enabled</name>
         <value>true</value>
    </property>
    <property>
         <name>dfs.permissions</name>
         <value>false</value>
    </property>
</configuration>

```

### 6.配置mapred-site.xml(这个文件没有需要创建)

```
<configuration>
<property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
          <property>
                  <name>mapreduce.jobhistory.address</name>
                  <value>Master.Hadoop:10020</value>
          </property>
          <property>
                <name>mapreduce.jobhistory.webapp.address</name>
                <value>Master.Hadoop:19888</value>
       </property>
</property>
</configuration>
```

### 7.配置yarn-site.xml

```
<configuration>

<!-- Site specific YARN configuration properties -->
<property>
  <name>yarn.resourcemanager.address</name>
  <value>Master.Hadoop:18040</value>
</property>
<property>
  <name>yarn.resourcemanager.scheduler.address</name>
  <value>Master.Hadoop:18030</value>
</property>
<property>
  <name>yarn.resourcemanager.webapp.address</name>
  <value>Master.Hadoop:18088</value>
</property>
<property>
  <name>yarn.resourcemanager.resource-tracker.address</name>
  <value>Master.Hadoop:18025</value>
</property>
<property>
  <name>yarn.resourcemanager.admin.address</name>
  <value>Master.Hadoop:18141</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>

```

### 8.添加 masters文件 

```
192.168.162.177
```

### 9.修改slaves

```
192.168.162.155
192.168.162.166
```

### 10.将配置后的hadoop利用scp发送到两台slave主机上 

#### 发送给slave1 

```
scp -r /usr/hadoop root@Slave1.Hadoop:/usr/
```

#### 发送给slave2 

```
scp -r /usr/hadoop root@Slave2.Hadoop:/usr/
```

### 11.配置另外两台slave的Hadoop环境变量

分别编辑vim /etc/profile然后添加如下内容：

```
#set hadoop path
export HADOOP_HOME=/usr/hadoop/hadoop-2.7.4
export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$PATH
```

## 七、启动服务  

只在master主机上启动服务即可

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

## 八、测试服务 

### 在master主机输入jps查看进程 

```
[root@Master ~]# jps
1328 SecondaryNameNode
1141 NameNode
1813 Jps
1478 ResourceManager
```

### 在slave1主机输入jps 

```
[root@Slave1 ~]# jps
2500 NodeManager
2392 DataNode
2634 Jps
```

### 在slave2 主机输入jps 

```
[root@Slave2 ~]# jps
2583 NodeManager
2473 DataNode
2715 Jps
```

### 访问Master.Hadoop：50070即 192.168.162.177:50070查看集群状况 

