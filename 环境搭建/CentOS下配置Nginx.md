# CentOS下配置Nginx 

官网：https://nginx.org/en/download.html

## 一、编译安装

1.下载源码 

```
wget https://nginx.org/download/nginx-1.13.10.tar.gz
```

2.解压

```
tar -zxvf nginx-1.13.10.tar.gz
```

3.编译安装

进入目录

```
cd nginx-1.13.10
```

配置

```
./configure
```

编译

```
make
make install
```

查找安装路径

```
whereis nginx
```

由于环境问题可能出现的错误异常：



![](https://shirukai.gitee.io/images/201803290947_293.png)

解决方法：

```
yum -y install pcre-devel
```



![](https://shirukai.gitee.io/images/201803290955_558.png)

```
yum install -y zlib-devel
```

### 安装脚本

````
#! /bin/bash
download_url=https://nginx.org/download/nginx-1.13.10.tar.gz
file_name=${download_url##*/}
file_dir=${file_name%.tar.gz*}
# download nginx
wget ${download_url}
# 解压
tar -zxvf ${file_name}
# 切入目录
cd ${file_dir}
# 编译安装
./configure
make
make install
# 查看路径
whereis nginx
````



## 二、基本操作 

### 启动、停止nginx 

```
cd /usr/local/nginx/sbin
./nginx  #启动
./nginx -s stop # 强制停止，相当于kill进程
./nginx -s quit # 等待进程任务处理完结束
./nginx -s reload #重新加载配置
```

### 查询进程

```
ps aux |grep nginx
```

### 重启 nginx 

#### 1先停止再启动 

```
./nginx -s quit
./nginx
```

#### 2重新加载配置文件

当nginx配置文件nginx.conf修改后，要想让配置生效需要重启 nginx，使用`-s reload`不用先停止 ngin x再启动 nginx 即可将配置信息在 nginx 中生效，如下：

```
./niginx -s reload
```

### 开机自启动

即在`rc.local`增加启动代码就可以了。

```
vi /etc/rc.local
```

增加一行 `/usr/local/nginx/sbin/nginx`
设置执行权限：

```
chmod 755 rc.local
```

## 三、部署静态页面 

修改 /usr/local/nginx/conf下的nginx.conf文件

添加server

    server {
         listen      80; 
         server_name localhost;
         root /www/equip-warning-web/theme/templates/equip-warning-web/; # 静态页面路径
         index alarmInfoQuery.html;
         location ~* ^.+\.(jpg|jpeg|gif|png|ico|css|js|pdf|txt|ttf|woff2|woff){
         root /www/equip-warning-web/theme/;#加载静态资源
         }
       }
## 四、解决跨域问题 

修改 /usr/local/nginx/conf下的nginx.conf文件

添加server

```
   server {
         listen 8090;
         server_name localhost;
         location / {
         proxy_pass http://192.168.66.159:18188;
         add_header 'Access-Control-Allow-Origin' '*';
         if ($request_method = 'OPTIONS') {  
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            #
            # Custom headers and headers various browsers *should* be OK with but aren't
            #
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
            #
            # Tell client that this pre-flight info is valid for 20 days
            #
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }
        if ($request_method = 'POST') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }
        if ($request_method = 'GET') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
        }
        }
    }
```