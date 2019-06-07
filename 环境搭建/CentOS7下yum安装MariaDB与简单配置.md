# CentOS7下yum安装MariaDB与简单配置

开始之前要确保已经安装yum并且配置好相关的源。

## 一、 安装命令：


```
yum -y install mariadb mariadb-server
```
## 二、启动MariaDB


```
systemctl start mariadb
```

## 三、 设置开机启动


```
systemctl enable mariadb
```
## 四、相关配置

```
mysql_secure_installation
```

### 1. 设置密码


```
Enter current password for root (enter for none): #直接回车就行
Set root password? [Y/n] y # 设置密码
New password: 
Re-enter new password: 


Remove anonymous users? [Y/n] # 是否删除匿名用户，删除就行

Disallow root login remotely? [Y/n] n # 是否禁止root远程登录，N

Remove test database and access to it? [Y/n] #  是否删除测试表，Y

Reload privilege tables now? [Y/n] # 是否重新加载权限表，Y


Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!

```
### 2. 登录


```
mysql -uroot -proot
```


### 3. 配置MariaDB的字符集


#### a. 查看数据库字符集


```
show variables like "%character%";show variables like "%collation%";
```

显示如下

```
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | latin1                     |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | latin1                     |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set (0.00 sec)

+----------------------+-------------------+
| Variable_name        | Value             |
+----------------------+-------------------+
| collation_connection | utf8_general_ci   |
| collation_database   | latin1_swedish_ci |
| collation_server     | latin1_swedish_ci |
+----------------------+-------------------+

```



#### b.修改文件/etc/my.cnf文件

```
vi /etc/my.cnf
```

在[mysqld]标签下添加

```
init_connect='SET collation_connection = utf8_unicode_ci' 
init_connect='SET NAMES utf8' 
character-set-server=utf8 
collation-server=utf8_unicode_ci 
skip-character-set-client-handshake
```
#### c.修改文件 /etc/my.cnf.d/client.cnf


```
vi /etc/my.cnf.d/client.cnf
```
在[client]中添加

```
default-character-set=utf8
```

#### d. 修改文件/etc/my.cnf.d/mysql-clients.cnf

```
vi /etc/my.cnf.d/mysql-clients.cnf
```
在[mysql]中添加

```
default-character-set=utf8
```
####  e.重启MariaDB

```
systemctl restart mariadb
```

####  f.查看修改后的字符集
进入数据库


```
mysql -uroot -proot
```

```
show variables like "%character%";show variables like "%collation%";
```


```
MariaDB [(none)]> show variables like "%character%";show variables like "%collation%";
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8                       |
| character_set_connection | utf8                       |
| character_set_database   | utf8                       |
| character_set_filesystem | binary                     |
| character_set_results    | utf8                       |
| character_set_server     | utf8                       |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+
8 rows in set (0.00 sec)

+----------------------+-----------------+
| Variable_name        | Value           |
+----------------------+-----------------+
| collation_connection | utf8_unicode_ci |
| collation_database   | utf8_unicode_ci |
| collation_server     | utf8_unicode_ci |
+----------------------+-----------------+
3 rows in set (0.00 sec)
```
### 4. 添加用户，设置权限

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

参考文章：

[CentOS 7.0 使用 yum 安装 MariaDB 与 MariaDB 的简单配置](http://www.linuxidc.com/Linux/2016-03/128880.htm)