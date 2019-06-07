# Azkaban环境搭建 

## 一、环境准备

### 版本说明：

jdk:1.8.0_151

ant: 1.10.2

mysql:5.1

node:8.5.0

### 安装JDK

官网下载地址： http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

下载jdk-8u151-linux-x64.tar.gz并复制到 /usr/lib目录下重命名为java

解压

```
tar -zxvf jdk-8u151-linux-x64.tar.gz
```

配置环境变量

```
vim /etc/profile
```

添加如下内容

```
#set java enviroenment
export JAVA_HOME=/usr/lib/java
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

### 安装ANT

下载

```
wget http://mirrors.tuna.tsinghua.edu.cn/apache//ant/binaries/apache-ant-1.10.2-bin.tar.gz
```

解压

```
tar -zxvf apache-ant-1.10.2-bin.tar.gz
```

配置环境变量

```
export ANT_HOME=/usr/local/apache-ant-1.10.2
export PATH=$PATH:$ANT_HOME/bin
```



### 安装mysql

从mysql官网下载 yum repo配置文件

```
wget http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
```

安装yum repo 文件

```
rpm -ivh mysql57-community-release-el7-9.noarch.rpm
```

这时，mysql的yum源已经安装好了。

清理缓存并更新yum源

```
yum clean all
yum makecache
```

安装mysql

```
yum install mysql-community-server
```

启动mysql

```
service mysqld start
```

查看初始密码

```
grep 'temporary password' /var/log/mysqld.log
```

使用初始密码登录

```
mysql -u root -p //回车，然后输入上一步查到的初始密码
```

更改初始密码

```
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';
```

修改密码强度限制：https://www.cnblogs.com/ivictor/p/5142809.html

2.配置

创建一个名为azkaban的数据库

```
mysql> create database azkaban;
```

设置mysql的信息包大小，默认的太小，改大一点(允许上传较大压缩包)

修改/etc/my.cnf配置文件

```
 vi /etc/my.cnf
```

```
[mysqld]

...

max_allowed_packet=1024M
```

重启mysql

```
service mysqld restart
```

### 安装node

下载

```
wget https://nodejs.org/dist/v8.5.0/node-v8.5.0-linux-x64.tar.gz /usr/lib/node-v8.5.0-linux-x64.tar.gz
```

解压

```
tar zxvf node-v8.5.0-linux-x64.tar.gz
```

配置环境变量

```
export NODE_HOME="/usr/lib/node-v8.5.0-linux-x64"
export PATH=$PATH:$NODE_HOME/bin
```

使修改后的文件生效

```
source /etc/profile 或者 . /etc/profile
```

查看安装情况

```
node -v
npm -v
```

## 二、源码编译 

### 服务源码编译

参考博客：https://blog.csdn.net/zk673820543/article/details/76984947

#### 1.准备

在/usr目录下创建一个azkaban目录，并在zakaban下分别创建目录azkaban-app 、azkaban-package、  azkaban-source：安装目录、安装包目录、源码目录

```
mkdir -p azkaban/azkaban-apps azkaban/azkaban-package azkaban/azkaban-source
```

#### 2.下载服务源码 

地址: https://github.com/azkaban/azkaban/archive/3.43.0.tar.gz

进入azkaban-source 然后wget源码

```
 cd azkaban/azkaban-source
 wget https://github.com/azkaban/azkaban/archive/3.43.0.tar.gz
```

#### 3.build

下载后先解压

```
 tar -zxvf azkaban-3.43.0.tar.gz
```

然后编译并打包为tar包

```
 cd azkaban-3.43.0
 ./gradlew distTar
```

因为需要下载一些依赖，所以编译的过程有些慢

![](https://shirukai.gitee.io/images/201804131139_190.gif)

编译完成

![](https://shirukai.gitee.io/images/201804131153_714.png)

#### 4.将编译好的文件复制到安装包目录下

```
 cp /usr/azkaban/azkaban-source/azkaban-3.43.0/azkaban-*/build/distributions/*.tar.gz  /usr/azkaban/azkaban-package/
```

### 插件源码编译

参考博客：https://cloud.tencent.com/developer/article/1079139

#### 1.下载插件源码

```
git clone https://github.com/azkaban/azkaban-plugins.git
```

#### 2.安装编译所需的dustjs-linkedin

```
npm install -g less dustjs-linkedin
```

![](https://shirukai.gitee.io/images/201804131203_586.png)

#### 3.编译

```
cd azkaban-plugins-master
ant
```

编译完成：

![](https://shirukai.gitee.io/images/201804131326_694.png)

将编译后的文件复制到azkaban-package/plugins下

```
cp -r * ../../../azkaban-package/plugins/
```



#### 4.编译出错问题汇总

##### 没有安装java加密扩展导致的错误：

![](https://shirukai.gitee.io/images/201804131207_393.png)

解决：

下载jdk1.8版本的jce扩展jar包：http://ov1a6etyz.bkt.clouddn.com/201804131315_772.rar

将下载后jar包复制到/usr/lib/java/jre/lib/security目录下面

## 三、安装服务和插件

### 安装服务

#### 1.准备

将编译好的服务安装包解压

```
cd /usr/azkaban/azkaban-package/server
```

这里我们分别解压azkaban-db-0.1.0-SNAPSHOT.tar.gz、azkaban-web-server-0.1.0-SNAPSHOT.tar.gz、azkaban-exec-server-0.1.0-SNAPSHOT.tar.gz、azkaban-solo-server-0.1.0-SNAPSHOT.tar.gz

```
tar -zxvf azkaban-db-0.1.0-SNAPSHOT.tar.gz
tar -zxvf azkaban-web-server-0.1.0-SNAPSHOT.tar.gz
tar -zxvf azkaban-exec-server-0.1.0-SNAPSHOT.tar.gz
tar -zxvf azkaban-solo-server-0.1.0-SNAPSHOT.tar.gz
```

复制解压后安装包到安装目录/usr/azkaban/azkaban-apps

```
[root@quickstart server]# mv azkaban-db-0.1.0-SNAPSHOT ../../azkaban-apps/
[root@quickstart server]# mv azkaban-exec-server-0.1.0-SNAPSHOT ../../azkaban-apps/
[root@quickstart server]# mv azkaban-solo-server-0.1.0-SNAPSHOT ../../azkaban-apps/
[root@quickstart server]# mv azkaban-web-server-0.1.0-SNAPSHOT ../../azkaban-apps/
```

#### 1.Azkaban Web Server配置

##### 导入SQL

进入mysql

```
mysql -uroot -pcloudera
```

导入sql

```
use azkaban;
source /usr/azkaban/azkaban-apps/azkaban-db-0.1.0-SNAPSHOT/create-all-sql-0.1.0-SNAPSHOT.sql;
```

##### 生成keystore

进入/usr/azkaban/azkaban-apps/azkaban-web-server-0.1.0-SNAPSHOT目录

执行下面命令生成秘钥：

```
keytool -keystore keystore -alias jetty -genkey -keyalg RSA
```

![](https://shirukai.gitee.io/images/201804131346_640.png)

这里我们填写的密码为：azkaban

##### 配置conf/azkaban.properties

如果在azkaban-web-server-0.1.0-SNAPSHOT下没有conf目录，可以从azkaban-solo-server-0.1.0-SNAPSHOT下把conf目录拷贝过来。

```
cp -r /usr/azkaban/azkaban-apps/azkaban-solo-server-0.1.0-SNAPSHOT/conf/ /usr/azkaban/azkaban-apps/azkaban-web-server-0.1.0-SNAPSHOT/
```

修改配置

设置数据库

```
     17 database.type=mysql
     18 mysql.port=3306
     19 mysql.host=localhost
     20 mysql.database=azkaban
     21 mysql.user=root
     22 mysql.password=cloudera
     23 mysql.numconnections=100
```

![](https://shirukai.gitee.io/images/201804131354_437.png)

获取SSL的KeyStore

Azkaban使用SSL套接字连接器，这意味着密钥库必须可用。您可以按照[此链接](http://docs.codehaus.org/display/JETTY/How+to+configure+SSL)提供的步骤创建一个。

一旦创建了密钥库文件，Azkaban必须被赋予它的位置和密码。其中`azkaban.properties`，应覆盖以下属性。

```
jetty.port=8666 #修改端口号为8666
jetty.keystore=keystore
jetty.password=azkaban
jetty.keypassword=azkaban
jetty.truststore=keystore
jetty.trustpassword=azkaban
```

![](https://shirukai.gitee.io/images/201804131357_162.png)

##### 配置用户管理

用户管理的配置在/usr/azkaban/azkaban-apps/azkaban-web-server-0.1.0-SNAPSHOT/conf/azkaban-user.xml这个配置文件里。

内容如下，按需修改：

```
<azkaban-users>
  <user groups="azkaban" password="azkaban" roles="admin" username="azkaban"/>
  <user password="metrics" roles="metrics" username="metrics"/>

  <role name="admin" permissions="ADMIN"/>
  <role name="metrics" permissions="METRICS"/>
</azkaban-users>
~                        
```

运行web-server

```
bin/azkaban-web-start.sh
```

报错1：log4j的配置文件没有找到

![](https://shirukai.gitee.io/images/201804131403_611.png)

在conf目录下创建 log4j.properties文件，内容如下：

```
log4j.rootLogger=INFO,C
log4j.appender.C=org.apache.log4j.ConsoleAppender
log4j.appender.C.Target=System.err
log4j.appender.C.layout=org.apache.log4j.PatternLayout
log4j.appender.C.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n
```

重新启动，访问ip:8666地址：

![](https://shirukai.gitee.io/images/201804131407_782.png)

#### 2. Azkaban Executor Server配置

进入/usr/azkaban/azkaban-apps/azkaban-exec-server-0.1.0-SNAPSHOT目录，创建extlib目录

```
mkdir extlib
```

从hadoop目录将一下jar包复制到该目录下

![](https://shirukai.gitee.io/images/201804131429_648.png)

或者下载：http://ov1a6etyz.bkt.clouddn.com/201804131431_320.zip

##### 配置/usr/azkaban/azkaban-apps/azkaban-exec-server-0.1.0-SNAPSHOT/conf/azkaban.properties

如果没有conf目录，从web-server将该目录拷贝过来。

修改内容如下：

```
default.timezone.id=Asia/Shanghai
# Loader for projects
executor.global.properties=conf/global.properties
azkaban.project.dir=projects
default.timezone.id=Asia/Shanghai
# Loader for projects
executor.global.properties=conf/global.properties
azkaban.project.dir=projects
default.timezone.id=Asia/Shanghai
# Loader for projects
executor.global.properties=conf/global.properties
azkaban.project.dir=projects
#database.type=h2
#h2.path=./h2
#h2.create.tables=true
database.type=mysql
mysql.port=3306
mysql.host=localhost
mysql.database=azkaban
mysql.user=root
mysql.password=cloudera
mysql.numconnections=100
# Azkaban Executor settings
executor.maxThreads=50
executor.port=12321
executor.flow.threads=30
# mail settings
mail.sender=
mail.host=
# User facing web server configurations used to construct the user facing server URLs. They are useful when there is a reverse proxy between Azkaban web servers and users.
# enduser -> myazkabanhost:443 -> proxy -> localhost:8081
# when this parameters set then these parameters are used to generate email links.
# if these parameters are not set then jetty.hostname, and jetty.port(if ssl configured jetty.ssl.port) are used.
# azkaban.webserver.external_hostname=myazkabanhost.com
# azkaban.webserver.external_ssl_port=443
# azkaban.webserver.external_port=8081
job.failure.email=
job.success.email=
lockdown.create.projects=false
cache.directory=cache
# JMX stats
jetty.connector.stats=true
executor.connector.stats=true
# Azkaban plugin settings
azkaban.jobtype.plugin.dir=plugins/jobtypes
azkaban.webserver.url=http://192.168.162.128:8666
```

启动服务：

```
[root@quickstart azkaban-exec-server-0.1.0-SNAPSHOT]# bin/azkaban-executor-start.sh
```

### 安装插件

#### HDFS查看器插件

HDFS查看器插件应安装在AzkabanWebServer插件目录中，该目录在AzkabanWebServer的配置文件中指定

1.复制插件到webserver目录下：

```
cp /usr/azkaban/azkaban-package/plugins/hdfsviewer/packages/azkaban-hdfs-viewer-\$\{git.tag\}.tar.gz  /usr/azkaban/azkaban-apps/azkaban-web-server-0.1.0-SNAPSHOT/
```

2.在websever目录下创建plugins/viewer目录，并将复制过去的tar包解压，重命名为hdfs，复制到viewer下

```
mkdir -p plugins/viewer
tar -zxvf azkaban-hdfs-viewer-\$\{git.tag\}.tar.gz
```

3.修改配置文件

```
viewer.plugins=hdfs
```

4.将 Azkaban Executor Server 目录下的extlib目录复制到webserver目录下，否则启动的时候回报缺少jar包的错误，如下图所示：

![](https://shirukai.gitee.io/images/201804131505_419.png)

5.启动web服务：

![](https://shirukai.gitee.io/images/201804131506_908.png)

#### Job Type 插件

Azkaban有一套有限的内置作业类型来运行本地unix命令和简单的java程序。在大多数情况下，您需要安装额外的作业类型插件，例如hadoopJava，Pig，Hive，VoldemortBuildAndPush等。一些常见的插件包含在azkaban-jobtype存档中。

1.在/usr/azkaban/azkaban-apps/azkaban-exec-server-0.1.0-SNAPSHOT创建plugins目录

```
mkdir plugins
```

2.将编译好的job type插件复制到plugins目录下

```
cp -r /usr/azkaban/azkaban-package/plugins/jobtype/packages/azkaban-jobtype-\$\{git.tag\}.tar.gz  /usr/azkaban/azkaban-apps/azkaban-exec-server-0.1.0-SNAPSHOT/plugins/
```

3.解压tar并重命名为jobtypes

```
tar -zxvf azkaban-jobtype-\$\{git.tag\}.tar.gz
mv azkaban-jobtype-\$\{git.tag\}/ jobtypes
```

4.配置插件

/usr/azkaban/azkaban-apps/azkaban-exec-server-0.1.0-SNAPSHOT/plugins/jobtypes下修改commonprivate.properties

添加一下配置：

```
## hadoop security manager setting common to all hadoop jobs
hadoop.security.manager.class=azkaban.security.HadoopSecurityManager_H_1_0

## hadoop security related settings

# proxy.keytab.location=
# proxy.user=

# azkaban.should.proxy=true
# obtain.binary.token=true
# obtain.namenode.token=true
# obtain.jobtracker.token=true

# global classpath items for all jobs. e.g. hadoop-core jar, hadoop conf
jobtype.global.classpath=/usr/lib/hadoop/client-0.20/*:/usr/lib/hadoop-yarn/*

# global jvm args for all jobs. e.g. java.io.temp.dir, java.library.path
#jobtype.global.jvm.args=

# hadoop
hadoop.classpath=
hadoop.home=/usr/lib/hadoop
pig.home=/usr/lib/pig
hive.home=/usr/lib/hive
spark.home=/usr/lib/spark

# configs for jobtype security settings
execute.as.user=false
azkaban.native.lib=

```

## 四 、 相关拓展

### 关于权限管理

https://azkaban.readthedocs.io/en/latest/userManager.html

![](http://shirukai.gitee.io/images/3f221bb666864039e7363f6b593b8692.jpg)

看官网说明是要在配置文件里指定一个类，然后修改xml文件，用来配置用户权限，如果想要自定义用户权限的话，可以拓展修改azkaban.user.XmlUserManager类。

### 短信改造思路

https://blog.csdn.net/tracymkgld/article/details/19126087

