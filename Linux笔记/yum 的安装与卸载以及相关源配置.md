# yum 的安装与卸载以及相关源配置

>系统版本

```
[root@localhost ~]# uname -r
3.10.0-514.el7.x86_64

```

## 一、yum源卸载

1. 查看yum组件

```
[root@localhost ~]# rpm -qa yum
yum-3.4.3-150.el7.centos.noarch

```
2. 卸载和yum有关的所有组件


```
rpm -qa | grep yum | xargs rpm -e --nodeps
```
3. 再次查看


```
[root@localhost ~]#  rpm -qa yum

```
没有相关信息说明卸载成功。

## 二、安装
### 1. 安装wget
下载 rpm文件
http://mirrors.163.com/centos/7/os/x86_64/Packages/wget-1.14-15.el7.x86_64.rpm

安装

```
rpm -ivh wget-1.14-13.el7.x86_64.rpm 

```

### 2. 安装yum

1. 下载yum依赖包
http://mirrors.163.com/centos/7/os/x86_64/Packages/


```
 wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-3.4.3-154.el7.centos.noarch.rpm
 
 wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-metadata-parser-1.1.4-10.el7.x86_64.rpm
 
 wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.31-42.el7.noarch.rpm

```


2. 安装
```
rpm -ivh yum-*  --nodeps --force
```

## 三、配置源
切换到目录：/etc/yum.repos.d/


### 1.备份之前的源文件
#### a. 新建目录

```
mkdir centos.repo.back
mv *.repo centos.repo.back
```

### 2. 下载源文件：
#### a. 163源：
http://mirrors.163.com/.help/centos.html

centos7：

```
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo
```

#### b. 阿里源：
http://mirrors.aliyun.com/help/centos?spm=5176.bbsr150321.0.0.d6ykiD


centos7：

```
wget http://mirrors.aliyun.com/repo/Centos-7.repo
```

### 3.生成缓存

```
yum clean all
yum makecache
```
## 四、yum使用

### 常用指令
1.用YUM安装软件包命令：yum install ~

2.用YUM删除软件包命令：yum remove ~

```
      1.使用YUM查找软件包
      命令：yum search ~
      2.列出所有可安装的软件包
      命令：yum list
      3.列出所有可更新的软件包
      命令：yum list updates
      4.列出所有已安装的软件包
      命令：yum list installed
      5.列出所有已安装但不在Yum Repository內的软件包
      命令：yum list extras
      6.列出所指定软件包
      命令：yum list～
      7.使用YUM获取软件包信息
      命令：yum info～
      8.列出所有软件包的信息
      命令：yum info
      9.列出所有可更新的软件包信息
      命令：yum info updates
      10.列出所有已安裝的软件包信息
      命令：yum info installed
      11.列出所有已安裝但不在Yum Repository內的软件包信息
      命令：yum info extras
      12.列出软件包提供哪些文件
      命令：yump rovides~
```

参考文章：

[yum安装与卸载软件常见命令](http://www.linuxidc.com/Linux/2016-05/131702.htm)


[CentOS下yum的安装及配置](http://blog.csdn.net/to_baidu/article/details/52583854)
