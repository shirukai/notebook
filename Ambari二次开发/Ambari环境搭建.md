# Ambari安装部署

## 一、准备工作

### 准备三台虚机并保证能相互ping通

| 序号   | IP地址            | 主机名               | 类型      | 用户名  |
| ---- | --------------- | ----------------- | ------- | ---- |
| 1    | 192.168.162.167 | iop167.ambari.com | service | root |
| 2    | 192.168.162.168 | iop168.ambari.com | agent   | root |
| 3    | 192.168.162.169 | iop169.ambari.com | agent   | root |

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
192.168.162.167 iop167.ambari.com iop167
192.168.162.168 iop168.ambari.com iop168
192.168.162.169 iop169.ambari.com iop169
```

**三台机器配置相同的hosts**



## 二、关闭防火墙

1. ### 查看防火墙状态

```
systemctl status firewalld
```

1. ### 查看开机是否启动防火墙服务

```
 systemctl is-enabled firewalld
```

1. ### 关闭防火墙

```
systemctl stop firewalld
systemctl status firewalld
```

1. ### 警用防火墙（系统启动时不启动防火墙）

```
systemctl disable firewalld
systemctl is-enabled firewalld
```

1. ### 确保setlinux关闭

   临时关闭

```
setenforce 0
```

永久关闭

修改/etc/selinux/config文件中设置SELINUX=disabled ，然后重启服务器

## 三、免密登录

首先虚机需要安装ssh如果没有安装，可以通过yum进行安装

```
yum install openssh-server
yum install openssh-clients
```

### iop167.ambari.com

在master主机输入生成秘钥

```
ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
```

将秘钥追加到authorized_keys 

```
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
```

然后利用scp将其复制到两个slave主机上

### iop168.ambari.com

在agent1主机上输入

```
scp root@iop167.ambari.com:~/.ssh/id_dsa.pub ~/.ssh/master_dsa.pub

cat ~/.ssh/master_dsa.pub >> ~/.ssh/authorized_keys
```

### iop169.ambari.com

在agent2主机输入

```
scp root@iop167.ambari.com:~/.ssh/id_dsa.pub ~/.ssh/master_dsa.pub

cat ~/.ssh/master_dsa.pub >> ~/.ssh/authorized_keys
```

### 测试

在master主机上连接两个主机，如果不需要密码，说明免密成功

```
ssh iop168.ambari.com
exit
ssh iop169.ambari.com
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

### 将jdk目录发送到两台Agent主机

```
scp -r /usr/lib/java-1.8.0_151 root@Slave1.Hadoop:/usr/lib/
scp -r /usr/lib/java-1.8.0_151 root@Slave2.Hadoop:/usr/lib/
```

配置环境变量就不要统一发送了，每台机子单独配置，方法跟Service主机一样。

## 五、配置本地源

安装本地源的目的，是为了方式在安装ambari的过程总由于网络原因造成安装失败。在linux配置yum本地源的笔记中，有详细讲到。

ambari2.6源地址：https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.0.0/bk_ambari-installation/content/download_the_ambari_repo_lnx7.html

## 六、安装mysql 

在server节点安装ambari server 之前 首先需要安装mysql数据库

```
yum -y install mysql-community-server
yum -y install mysql-connector-java


systemctl enable mysqld.service
systemctl restart mysqld.service

```

运行` mysql_secure_installation` 进行安全配置，会执行如下几个设置：

```
（1）为root用户设置密码；
（2）删除匿名账号；
（3）取消root用户远程登录；
（4）删除test库和对test库的访问权限；
（5）刷新授权表使修改生效。
```

设置root用户密码为root,新增ambari用户并设置权限

```
mysql -uroot -proot
CREATE USER 'ambari'@'%' IDENTIFIED BY 'ambari';
GRANT ALL PRIVILEGES ON *.* TO 'ambari'@'%';
CREATE USER 'ambari'@'localhost' IDENTIFIED BY 'ambari';
GRANT ALL PRIVILEGES ON *.* TO 'ambari'@'localhost';
CREATE USER 'ambari'@'iop167.ambai.com' IDENTIFIED BY 'ambari'; //本地主机名
GRANT ALL PRIVILEGES ON *.* TO 'ambari'@'iop167.ambai.com'; //本地主机名
FLUSH PRIVILEGES;
```

使用ambari用户登录，创建ambari数据库

```
mysql -uambari -pambari
CREATE DATABASE ambari;
```

## 七、安装配置ambari-server

### 安装

```
yum -y install ambari-server
```

### 配置 

```
[root@iop167 /]# ambari-server setup
Using python  /usr/bin/python
Setup ambari-server
Checking SELinux...
SELinux status is 'disabled'
Customize user account for ambari-server daemon [y/n] (n)? y
Enter user account for ambari-server daemon (root):root
Adjusting ambari-server permissions and ownership...
Checking firewall status...
Checking JDK...
Do you want to change Oracle JDK [y/n] (n)? y
[1] Oracle JDK 1.8 + Java Cryptography Extension (JCE) Policy Files 8
[2] Oracle JDK 1.7 + Java Cryptography Extension (JCE) Policy Files 7
[3] Custom JDK
==============================================================================
Enter choice (1): /usr/lib/jdk1.8.0_151
Invalid number.
[1] Oracle JDK 1.8 + Java Cryptography Extension (JCE) Policy Files 8
[2] Oracle JDK 1.7 + Java Cryptography Extension (JCE) Policy Files 7
[3] Custom JDK
==============================================================================
Enter choice (1): 3
WARNING: JDK must be installed on all hosts and JAVA_HOME must be valid on all hosts.
WARNING: JCE Policy files are required for configuring Kerberos security. If you plan to use Kerberos,please make sure JCE Unlimited Strength Jurisdiction Policy Files are valid on all hosts.
Path to JAVA_HOME: /usr/lib/jdk1.8.0_151
Validating JDK on Ambari Server...done.
Completing setup...
Configuring database...
Enter advanced database configuration [y/n] (n)? y
Configuring database...
==============================================================================
Choose one of the following options:
[1] - PostgreSQL (Embedded)
[2] - Oracle
[3] - MySQL / MariaDB
[4] - PostgreSQL
[5] - Microsoft SQL Server (Tech Preview)
[6] - SQL Anywhere
[7] - BDB
==============================================================================
Enter choice (3): 3
Hostname (localhost): 
Port (3306): 
Database name (ambari): 
Username (ambari): 
Enter Database Password (bigdata): 
Re-enter password: 
Configuring ambari database...
Configuring remote database connection properties...
WARNING: Before starting Ambari Server, you must run the following DDL against the database to create the schema: /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
Proceed with configuring remote database connection properties [y/n] (y)? y
Extracting system views...
ambari-admin-2.5.1.0.159.jar
...........
Adjusting ambari-server permissions and ownership...
Ambari Server 'setup' completed successfully.
```

### 执行SQL语句 

```
mysql -uambari -pambari
use ambari
source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
```



### 修改Ambari源配置文件 

只保留相应操作系统版本，其他删除，baseurl改为对应本地地址即可。

```
cd /var/lib/ambari-server/resources/stacks/HDP/2.6/repos/
```

修改 repoinfo.xml文件

```
[root@iop167 repos]# vim repoinfo.xml 

<?xml version="1.0"?>
<reposinfo>
  <os family="redhat7">
    <repo>
      <baseurl>http://10.110.18.58:81/CentOS-7/HDP</baseurl>
      <repoid>HDP</repoid>
      <reponame>HDP</reponame>
    </repo>
    <repo>
      <baseurl>http://10.110.18.58:81/CentOS-7/HDP-UTILS</baseurl>
      <repoid>HDP-UTILS</repoid>
      <reponame>HDP-UTILS</reponame>
    </repo>
    <repo>
      <baseurl>http://10.110.18.58:81/CentOS-7/HDP-INSPUR</baseurl>
      <repoid>HDP-INSPUR</repoid>
      <reponame>HDP-INSPUR</reponame>
    </repo>
    <repo>
      <baseurl>http://10.110.18.58:81/CentOS-7/HDF</baseurl>
      <repoid>HDF</repoid>
      <reponame>HDF</reponame>
    </repo>
  </os>
</reposinfo>
```

### 启动ambari

```
ambari-server start
```



