# centos下安装mysql 5.7

Cenos7默认数据库是mariaDB，所以yum install mysql 会自动安装mariaDB。所以我们要想在centos7下安装mysql，首先要配置mysql的源。



### 1. 从mysql官网下载 yum repo配置文件  

```
wget http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
```

### 2. 安装yum repo 文件  

```
rpm -ivh mysql57-community-release-el7-9.noarch.rpm
```

这时，mysql的yum源已经安装好了。

### 3. 清理缓存并更新yum源 

```
yum clean all
yum makecache
```

### 4. 安装mysql 

```
yum install mysql-community-server
```



### 5. 启动mysql 

```
service mysqld start
```



### 6. 查看初始密码 

```
grep 'temporary password' /var/log/mysqld.log
```



### 7.使用初始密码登录 

```
mysql -u root -p //回车，然后输入上一步查到的初始密码
```



### 8.更改初始密码 

```
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';
```

修改密码强度限制：https://www.cnblogs.com/ivictor/p/5142809.html

### 9. 添加用户，设置权限

#### a.创建用户命令

```
MariaDB [(none)]> create user inspur@localhost identified by 'inspur';

```

#### b. 授权

```
grant all privileges on *.* to inspur@'localhost' identified by 'inspur';

```

#### b.授予外网登录权限

```
grant all privileges on *.* to root@'%' identified by 'inspur';

```



