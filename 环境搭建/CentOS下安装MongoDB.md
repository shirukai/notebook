# CentOS下安装MongoDB

MongoDB 是一个基于分布式文件存储的数据库。由 C++ 语言编写。旨在为 WEB 应用提供可扩展的高性能数据存储解决方案。

MongoDB 是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。

## 1 下载安装

官网提供windows、Linux、OSX系统环境下的安装包，这里主要是记录一下在Linux下的安装。首先到官网下载最新的安装包。这里下载的是4.0.1版本的。

官网地址：https://www.mongodb.com/

4.0.1版本适合CentOS系统的下载地址：https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.1.tgz

![](https://shirukai.gitee.io/images/09a40de52e03bf9fb92744a55303d0d4.gif)

### 1.1 在CentOS中，我们使用wget下载安装包。

```
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.1.tgz
```

![](https://shirukai.gitee.io/images/e0a221aba30bbdfac5d993b5ce98ce8c.jpg)

### 1.2 解压并修改相关配置

1.2.1 解压

```
tar -zxvf mongodb-linux-x86_64-4.0.1.tgz
```

#### 1.2.2 重命名为mongodb

```
mv mongodb-linux-x86_64-4.0.1 mongodb
```

#### 1.2.3 创建文件:db用来存放数据库、logs用来存放日志

```
cd mongodb
mkdir db logs
```

#### 1.2.4 添加配置文件

```
cd bin
vi mongodb.conf
```

内容如下：

```
dbpath=/root/apps/mongodb/db
logpath=/root/apps/mongodb/logs/mongodb.log
port=27017
fork=true
nohttpinterface=true
```

参数解释：

```
dbpath: 数据库存放位置
logpath：日志存放位置
port：监听端口
fork：是否后台运行
nohttpinterface：是否关闭http接口
```

#### 1.2.5 绑定ip和配置文件

```
./mongod --bind_ip 192.168.162.128 -f mongodb.conf
```

发现报错：

![](https://shirukai.gitee.io/images/16439e50f92b11fef26e6b55a2701ebe.jpg)

原因：https://stackoverflow.com/questions/48020445/error-parsing-ini-config-file-unrecognised-option-nohttpinterface

我们把配置文件中的nohttpinterface=true去掉

报错：

![](https://shirukai.gitee.io/images/a0ad511a23fff76a05812d11e2aae095.jpg)

解决方法：

删除db目录下的mongod.lock文件

然后以修复的方式启动

```
bin/mongod -f /root/apps/mongodb/bin/mongodb.conf --repair
```

#### 1.2.6 开机启动

```
vi /etc/rc.d/rc.local
```

添加如下内容：

```
/root/apps/mongodb/bin/mongod --bind_ip 192.168.162.128 -f /root/apps/mongodb/bin/mongodb.conf
```

#### 1.2.7 自动安装脚本

```
#! /bin/bash
download_url=https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.1.tgz
file_name=${download_url##*/}
file_dir=${file_name%.tgz*}
now_path=$(pwd)
dbpath=dbpath=${now_path}/${file_dir}/db
logpath=logpath=${now_path}/${file_dir}/logs/mongodb.log
fork=fork=true
port=port=27017
ipaddr=$(ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\1", "g", $2)}')
# download
wget $download_url

# untgz
tar -zxvf $file_name

# cd 
cd $file_dir

# mkdir
mkdir db logs

echo $dbpath >> bin/mongodb.conf
echo $logpath >> bin/mongodb.conf
echo $fork >> bin/mongodb.conf
echo $port >> bin/mongodb.conf

#bind
binpath=${now_path}/${file_dir}/bin
${binpath}/mongod --bind_ip ${ipaddr} -f ${binpath}/mongodb.conf

#开机启动
echo ${binpath}/mongod --bind_ip ${ipaddr} -f ${binpath}/mongodb.conf >> /etc/rc.d/rc.local

```

## 2 连接使用

进入数据库

```
./mongo 192.168.162.128
```

查看数据列表

```
show dbs;
```

查看版本

```
db.version()
```

客户端下载：https://www.robomongo.org/download