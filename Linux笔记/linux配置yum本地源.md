# linux配置yum本地源

> 往往安装某些软件时，依赖的东西太多，或者网络原因，容易造成软件安装失败，这时候我们可以配置yum本地源，将需要的软件的rpm包同步到本地，然后使用本地源。例如安装ambari的时候，我们通常把ambari的安装源同步到本地，然后安装。



## 1 安装httpd 

 Httpd是由ASF（apache software foundation）维护的开源项目之一 也是目前最为流行的web服务器之一 目前有三个维护版本 分别为2.1 2.2 2.4 特性丰富：高度模块化的设计 出色的稳定性 支持OSD 丰富的第三方插件。

```
yum -y install httpd.x86_64
```



## 2.同步网络源

将网络源利用工具同步到本地，这里以同步ambari源为例子

### 2.1 安装wget 

```
yum -y install wget.x86_64
```

### 2.2下载ambari2.6.0的源到/etc/yum.repos.d/目录下

```
wget -nv http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.6.0.0/ambari.repo -O /etc/yum.repos.d/ambari.repo
```

### 2.3 查看源列表 

```
yum repolist
```

### 2.4 安装yum-utils 

```
yum -y install yum-utils
```

### 2.5同步源

```
reposync -r ambari-2.6.0.0
```

### 2.6 复制源文件到/var/www/html/目录下 

执行同步命令之后，会得到一个目录，将这个目录移动到/var/www/html/下

```
mv /etc/yum.repos.d/ambari-2.6.0.0 /var/www/html/
```

## 3使用createrepo创建本地源

### 3.1安装createrepo 

```
yum -y install createrepo
```

### 3.2切换到/var/www/html/ambari-2.6.0.0目录下 

```
cd /var/www/html/ambari-2.6.0.0/
```

### 3.3创建本地源

```
createrepo .
```

## 4其他源安装

安装本地源的原理是一样的，就是把网络源的rpm安装包同步或者下载到本地的某个目录下，然后安装httpd服务，将存放已下下载rpm包的目录移动到/var/www/html目录下。然后创建本地源。我们就可以使用这个源了。

### 5 重启httpd服务 

````
systemctl restart httpd.service
````

