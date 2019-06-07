linux环境下编译安装grafana并实现汉化

前言：目前实现汉化的方案很笨拙，需要对源码里的模板文件，以及js里用的显示数据进行一一汉化。所以在这里记录一下汉化以及编译安装的过程。

## 一、配置运行环境 

* go语言环境

* node环境

* git

  ### 安装go语言环境 

  利用yum安装go

  ```
  yum install go
  ```

  yum会自动处理go需要的环境依赖

  ​

  ### 安装 node.js 

  1. 下载安装包 [版本地址](https://nodejs.org/dist/)
  2. ​

  ```
  wget https://nodejs.org/dist/v8.5.0/node-v8.5.0-linux-x64.tar.gz
  ```
  3.解压

  ```
  tar zxvf node-v8.5.0-linux-x64.tar.gz
  ```
  4. 配置环境变量/etc/profile

  ```
  export NODE_HOME="/root/node-v8.5.0-linux-x64"
  export PATH=$PATH:$NODE_HOME/bin
  ```
  5. 使修改后的文件生效
  ```
  source /etc/profile
  ```
  6. 查看安装情况


  ```
  node -v
  npm -v
  ```
  ### 安装 git 

  ```
  yum install git
  ```

## 二、git 项目源码

创建项目目录并相应的设置路径（或使用默认的Go工作区目录）

```
export GOPATH=`pwd`
go get github.com/grafana/grafana
```

## 三、构建后端 

```
cd $GOPATH/src/github.com/grafana/grafana
go run build.go setup
go run build.go build    
```

### 四、构建前端 

```
npm install -g yarn
yarn install --pure-lockfile
npm run build
```

在这里注意 运行yarn install --pure-lockfile的时候可能会报如下错误：

![111](C:/Users/shirukai/Desktop/img/111.png)

原因是虚拟机里没有安装bzip2所以下载的文件解压不了，所以执行如下命令：

```
yum install bzip2
```

### 五、运行Grafana 

```
./bin/grafana-server
```

## 六、汉化 

grafana的模板资源主要是在源码的public下，修改相应的html文件以及js文件就可以汉化