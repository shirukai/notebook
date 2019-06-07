# Dockder常用操作及技巧

## 1 Dockerfile

Dockerfile常用命令：https://www.jianshu.com/p/10ed530766af

官网介绍：https://docs.docker.com/engine/reference/builder/#usage

### 1.1 Flask 服务Dockerfile

```dockerfile
FROM python:3

ARG SERVER_PORT=18666
MAINTAINER shirukai "shirukai@hollysys.net"
# set work dir
WORKDIR hiacloud-analytics-api

# copy server files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# expose server port
EXPOSE ${SERVER_PORT}

# set time zone
ENV TZ Asia/Shanghai
#COPY localtime /etc/localtime

# start flask service when the container starts
CMD python main.py
```

### 1.2 Springboot 服务Dockerfile

```dockerfile
FROM anapsix/alpine-java:8u172b11_jdk

MAINTAINER shirukai shirukai@hollysys.net
EXPOSE 8080

ADD target/demo-0.0.1-SNAPSHOT.jar /
WORKDIR /learn-demo-springboot

RUN chmod +x /learn-demo-springboot/*.sh

ENV TZ Asia/Shanghai
CMD [ "./start.sh" ]
```



## 2 常用命令

### 2.1 镜像相关

#### 使用Dockerfile创建镜像：docker build -t  REPOSITORY:TAG .

```shell
docker build -t hiacloud-analytics-api:v1 .
```

#### 查看本地仓库的镜像：docker images

```shell
shirukaiimac:hiacloud-analytics-api shirukai$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
python              3                   1e80caffd59e        3 weeks ago         923MB
centos              7                   75835a67d134        2 months ago        200MB
```

#### 拉取远程仓库镜像：docker pull REPOSITORY:TAG

```shell
docker pull registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api:v1
```

#### 将本地镜像推送到远程仓库：docker push REPOSITORY:TAG

##### 将已有的镜像推送到远程仓库

A 先将已有镜像打标签:docker tag IMAGE_ID REPOSITORY:TAG

例如这里我的远程仓库地址为registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api，版本设置为v1

```shell
docker tag ad029e5c5fe0 registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api:v1
```

B 登录远程仓库：docker login --username=USERNAME REPOSITORY_REGOIN

例如这里的远程仓库为阿里的，我的账号是308899573@qq.com，仓库区域用的是北京地区的registry.cn-beijing.aliyuncs.com

```shell
docker login --username=308899573@qq.com registry.cn-beijing.aliyuncs.com
```

C 推送镜像到远程仓库：docker push  REPOSITORY:TAG

```shell
docker push registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api:v1
```

##### 使用Dockerfile构建新的镜像然后推送到远程仓库

A 构建新的镜像：docker build -t REPOSITORY:TAG

```shell 
docker build -t registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api:v1
```

B 登录远程仓库：docker login --username=USERNAME REPOSITORY_REGOIN

例如这里的远程仓库为阿里的，我的账号是308899573@qq.com，仓库区域用的是北京地区的registry.cn-beijing.aliyuncs.com

```shell
docker login --username=308899573@qq.com registry.cn-beijing.aliyuncs.com
```

C 推送镜像到远程仓库：docker push  REPOSITORY:TAG

```shell
docker push registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api:v1
```

#### 删除镜像：docker rmi [参数] IMAGE_ID/ REPOSITORY:TAG

##### 根据仓库名和版本删除镜像：docker rmi REPOSITORY:TAG

```shell
docker rmi registry.cn-beijing.aliyuncs.com/shirukai/hiacloud-analytics-api:v1
```

##### 根据镜像ID删除镜像： docker rmi IMAGE_ID

```shell
docker rmi ad029e5c5fe0
```

##### 强制删除：docker rmi -f IMAGE_ID

```shell
docker rmi -f ad029e5c5fe0
```

### 2.2 容器相关

#### 启动容器 ：docker run [params]  REPOSITORY:TAG

##### 启动容器并绑定端口映： docker run -itd -p OUT_PORT:IN_PORT REPOSITORY:TAG

```shell
docker run -itd -p 18666:18666 hiacloud-analytics-api:v1
```

#### 查看正在运行的容器：docker ps

```shell
docker ps
```

#### 查看正在运行容器的日志：docker logs -f CONTAINER_ID

```shell
docker logs -f aa7dc31fce42
```

#### 列出所有容器:docker container list

```shell
docker container list
```

#### 进入正在运行的容器:docker exec -it CONTAINER_ID /bin/bash

```shell
docker exec -it a563f04c5947 /bin/bash
```

#### 停止容器：docker stop CONTAINER_ID

```shell
docker stop a563f04c5947
```

## k8s常用命令

