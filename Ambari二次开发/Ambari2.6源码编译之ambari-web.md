# Ambari编译之ambari-web

## 1.准备 

### 1.1下载源码 

#### 安装wget

```
yum -y install wget
```

#### 下载源码

将源码下载到/opt目录下

```
wget http://www.apache.org/dist/ambari/ambari-2.6.0/apache-ambari-2.6.0-src.tar.gz -O /opt/apache-ambari-2.6.0-src.tar.gz
```

### 1.2配置编译环境

#### 1.2.1安装node.js

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

#### 1.2.2安装bzip2

```
yum install bzip2
```

## 2.编译

### 2.1 npm安装依赖

#### 2.1.1切换到ambari-web目录下

```
cd /opt/apache-ambari-2.6.0-src/ambari-web
```

#### 2.1.2安装依赖

注意：安装依赖的时候有phantomjs，需要翻墙才能下载，而且需要系统安装bzip2。npm安装依赖的过程可能会很慢，最好在网络良好的环境下下载。

```
npm install
```

### 2.2 安装brunch

```
npm install -g brunch
```

### 2.3 编译 

```
brunch build
```

### 2.4 实时监控编译 

```
brunch watch #缩写 brunch w
```

## 3.软链接 

建立软链接的目的，是方便实时编译，编译后直接在ambri上显示编译后的效果。

### 3.1备份源文件

切换到/usr/lib/ambari-server

```
cd /usr/lib/ambari-server
```

备份web

```
mv web web.bak
```

### 3.2建立软链接 

```
ln -s /opt/apache-ambari-2.6.0-src/ambari-web/public web
```

## 4.启动测试 

在ambari-web下执行实时编译

```
brunch w
```

重启ambari-server

```
ambari-server restart
```



补充：可能需要的环境

##### 安装yarn

yarn 与npm一样，是一个包管理工具。

下载yarn的rpm包仓库

```
wget https://dl.yarnpkg.com/rpm/yarn.repo -O /etc/yum.repos.d/yarn.repo
```

配置NodeSource仓库

```
curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
```

yum安装

```
yum install yarn
```

#### 