# CentOS7下yum安装oracle

## 一、安装前环境准备

### 1. VMware 搭建centos7 的虚机
配置好网络IP为192.168.162.155
### 2. 下载Oracle11g安装文件


```
linux.x64_11gR2_database_1of2.zip
linux.x64_11gR2_database_2of2.zip

```
百度云：

链接：http://pan.baidu.com/s/1gf1oJJH 密码：1ivl

### 3. 通过shell工具连接虚机然后上传至/home 目录


```
-rw-r--r--. 1 root   root     1239269270 Sep 23 19:25 linux.x64_11gR2_database_1of2.zip
-rw-r--r--. 1 root   root     1111416131 Sep 23 19:25 linux.x64_11gR2_database_2of2.zip
```

## 二、安装前操作系统准备

### 1. 使用root用户登录linux
### 2. yum安装unzip软件，用来解压上传的oracle安装文件

```
[root@localhost ~]#yum install unzip –y
```
### 3.解压oracle安装程序

```
[root@localhost ~]# cd /home
[root@localhost home]# unzip linux.x64_11gR2_database_1of2.zip
[root@localhost home]# unzip linux.x64_11gR2_database_2of2.zip
```
>解压完成后，机会在/home目录下生成一个database文件夹，里面就是oracle安装文件

### 4. yum安装vim软件，用于编辑配置文件

```
[root@localhost ~]#yum install vim -y
```

### 5. 在/etc/hosts文件中添加主机名
a. 查看主机名


```
[root@localhost ~]#hostname
localhost.localdomain
```
b. 添加到hosts文件中

```
[root@localhost ~]# vim /etc/hosts
```

```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.162.155 loaclhost.localdomain

```
### 6. 关掉selinux

```
[root@localhost ~]# vim /etc/selinux/config
```
设置 ELINUX=disabled

使配置文件生效

```
[root@localhost ~]# setenforce 0
```
### 7.关闭防火墙,以免安装过程中发生不必要的错误


```
[root@localhost ~]# service iptables stop

[root@localhost ~]# systemctl stop firewalld

[root@localhost ~]# systemctl disable firewalld
```
### 8. 安装oracle 11g依赖包


```
[root@localhost ~]# yum install gcc make binutils gcc-c++ compat-libstdc++-33elfutils-libelf-devel elfutils-libelf-devel-static ksh libaio libaio-develnumactl-devel sysstat unixODBC unixODBC-devel pcre-devel –y

```
### 9. 添加安装用户和组

```
[root@localhost ~]# groupadd oinstall

[root@localhost ~]# groupadd dba

[root@localhost ~]# useradd -g oinstall -G dba oracle

[root@localhost ~]# passwd oracle

[root@localhost ~]# id oracle

uid=1001(oracle) gid=1001(oinstall) 组=1001(oinstall),1002(dba)
```
### 10. 修改内核参数配置文件

```
[root@localhost ~]# vim /etc/sysctl.conf
```


```
# For more information, see sysctl.conf(5) and sysctl.d(5).
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.shmall = 2097152
kernel.shmmax = 536870912
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 9000 65500
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576


```
其中kernel.shmmax = 536870912为本机物理内存（1G）的一半，单位为byte

查看配置是否生效


```
[root@loaclhost ~]# sysctl -p
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.shmall = 2097152
kernel.shmmax = 536870912
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 9000 65500
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576

```
### 11.修改用户的限制文件


```
[root@localhost ~]# vim /etc/security/limits.conf
```
添加如下内容
```
#@student        -       maxlogins       4
oracle           soft    nproc           2047

oracle           hard    nproc           16384

oracle           soft    nofile          1024

oracle           hard    nofile         65536

oracle           soft    stack           10240

```

### 12.修改用户验证选项（root用户）

```
[root@localhost ~]# vim /etc/pam.d/login
```

添加如下内容：
```
session required  /lib64/security/pam_limits.so
session required   pam_limits.so

```
### 13.创建oracle安装目录和设置文件权限


```
[root@localhost ~]# mkdir -p /data/oracle/product/11.2.0

[root@localhost ~]# mkdir /data/oracle/oradata

[root@localhost ~]# mkdir /data/oracle/inventory

[root@localhost ~]# mkdir /data/oracle/fast_recovery_area

[root@localhost ~]# chown -R oracle:oinstall /data/oracle

[root@localhost ~]# chmod -R 777 /data/oracle
```
### 14.以oracle用户登录系统,设置oracle用户环境变量


```
[root@localhost ~]# su - oracle
[oracle@localhost ~]$  vim .bash_profile
```

添加如下内容：


```
ORACLE_BASE=/data/oracle; export ORACLE_BASE
ORACLE_HOME=$ORACLE_BASE/product/11.2.0; export ORACLE_HOME
NLS_LANG=SIMPLIFIED CHINESE_CHINA.ZHS16GBK; export NLS_LANG
ORACLE_SID=ds; export ORACLE_SID
PATH=$PATH:$ORACLE_HOME/bin:$ORACLE_HOME/jdk/bin:/sbin;
export PATH
BIN=$ORACLE_HOME/bin; export BIN
LD_LIBRARY_PATH=$ORACLE_HOME/lib; export LD_LIBRARY_PATH
export LANG=en_US.UTF-8
```
注意，ORACLE_SID=ds与创建的数据库实例名称一致，否则数据库启动后无法访问。


配置完后使用命令使配置生效


```
[oracle@localhost ~]$ source .bash_profile
#使用echo $ORACLE_BASE  
    或者  
    echo $ORACLE_HOME 
#查看配置的信息是否生效，如果正确的话是和你的配置是一致的
```
退出在登录，使得环境变量的配置生效


```
exit

su - oracle

env | grep ORA
```


```
[oracle@loaclhost ~]$ env |grep ORA
ORACLE_SID=ds
ORACLE_BASE=/data/oracle
ORACLE_HOME=/data/oracle/product/11.2.0

```
### 15.安装前的最后准备--编辑静默安装响应文件

a. 将响应文件复制到oracle用户家目录 即/home/oracle


```
[oracle@localhost ~]$ cp -R /home/database/response/ .
[oracle@localhost ~]$ ll
总用量 0
drwxr-xr-x. 2 oracle oinstall 58 5月  12 20:15 response
```

b. 编辑相应文件

```
[oracle@localhost ~]$ cd response/

[oracle@localhost response]$ vim db_install.rsp
```
oracle.install.option=INSTALL_DB_SWONLY

ORACLE_HOSTNAME=localhost

UNIX_GROUP_NAME=oinstall

INVENTORY_LOCATION=/data/oracle/inventory

SELECTED_LANGUAGES=en,zh_CN

ORACLE_HOME=/data/oracle/product/11.2.0

ORACLE_BASE=/data/oracle

oracle.install.db.InstallEdition=EE

oracle.install.db.DBA_GROUP=dba

oracle.install.db.OPER_GROUP=dba

DECLINE_SECURITY_UPDATES=true

## 三、根据响应文件静默安装Oracle11g

```
[oracle@localhost database]$ cd /home/database/
[oracle@localhost database]$ ./runInstaller -silent -responseFile /home/oracle/response/db_install.rsp  -ignorePrereq
#开始Oracle在后台静默安装。安装过程中，如果提示[WARNING]不必理会，此时安装程序仍在后台进行，如果出现[FATAL]，则安装程序已经停止了。
```
可以切换终端执行 tail -f /data/oracle/inventory/logs/installActions2015-06-08_04-00-25PM.log 命令查看后台安装程序日志

当出现以successfully Setup Software提示时，代表安装成功

2.安装成功后,按照要求执行脚本


```
[root@localhost ~]# sh /data/oracle/inventory/db_1/orainstRoot.sh
[root@localhost ~]#  sh /data/oracle/product/11.2.0/root.sh
```
## 四、静默方式配置监听
  重新使用oracle用户登录,命令安装


```
[oracle@localhost ~]$ netca /silent /responseFile /home/oracle/response/netca.rsp
```
成功运行后，在/data/oracle/product/11.2.0/db_1/network/admin/中生成listener.ora和sqlnet.ora

==修改listener.ora文件==


```
# listener.ora Network Configuration File: /data/oracle/product/11.2.0/network/admin/listener.ora
# Generated by Oracle configuration tools.

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
      (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.162.155)(PORT = 1521))
    )
  )
SID_LIST_LISTENER=
  (SID_LIST=
      (SID_DESC=
                      #BEQUEATH CONFIG
         (GLOBAL_DBNAME=ds)
         (SID_NAME=ds)
         (ORACLE_HOME=/data/oracle/product/11.2.0)
                      #PRESPAWN CONFIG
        (PRESPAWN_MAX=20)
        (PRESPAWN_LIST=
          (PRESPAWN_DESC=(PROTOCOL=tcp)(POOL_SIZE=2)(TIMEOUT=1))
        )
       )
      )
ADR_BASE_LISTENER = /data/oracle

```



通过netstat命令可以查看1521端口正在监听。

Yum安装netstat软件，软件包是在net-tools中。


```
[root@localhost ~]# yum install net-tools
[root@localhost ~]# netstat -tnulp | grep 1521
```


```
tcp        0      0 192.168.162.155:1521    0.0.0.0:*               LISTEN      2083/tnslsnr 
```

## 五、以静默方式建立新库，同时也建立一个对应的实例。

以oracle用户登录,再次进去响应文件夹


```
[oracle@localhost ~]$ vim /home/oracle/response/dbca.rsp
```

设置以下参数：

GDBNAME= "ds"

SID =" ds"

SYSPASSWORD= "system@2017"

SYSTEMPASSWORD= "system@2017"

SYSMANPASSWORD= "system@2017"

DBSNMPPASSWORD= "system@2017"

DATAFILEDESTINATION=/data/oracle/oradata

RECOVERYAREADESTINATION=/data/oracle/fast_recovery_area

CHARACTERSET= "ZHS16GBK"

TOTALMEMORY= "819"



进行静默配置：


```
[oracle@localhost ~]$  dbca -silent -responseFile /home/oracle/response/dbca.rsp
```
停止监听

```
lsnrctl stop
```
启动监听

```
lsnrctl start
```
查看监听状态

```
lsnrctl states
```
登录查看实例状态：

```
[oracle@localhost ~]$ sqlplus / as sysdba
```


```
[oracle@loaclhost response]$ sqlplus / as sysdba

SQL*Plus: Release 11.2.0.1.0 Production on Sun Sep 24 17:00:29 2017

Copyright (c) 1982, 2009, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> quit     
Disconnected from Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
[oracle@loaclhost response]$ sqlplus / as sysdba

SQL*Plus: Release 11.2.0.1.0 Production on Sun Sep 24 17:10:07 2017

Copyright (c) 1982, 2009, Oracle.  All rights reserved.


Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options

SQL> 

```

## 六:创建表空间,用户

1.创建表空间


```
CREATE TABLESPACE ds_tablespace DATAFILE '/data/oracle/oradata/ds/ds_tablespace.dbf' SIZE 200M AUTOEXTEND ON EXTENT MANAGEMENT LOCAL SEGMENT SPACE MANAGEMENT AUTO;
```

2.创建用户名和密码


```
CREATE USER inspur IDENTIFIED BY inspur DEFAULT TABLESPACE ds_tablespace;
```

3.用户授权


```
SQL> grant connect,resource to inspur;
SQL>grant unlimited tablespace to inspur;
SQL>grant create database link to inspur;
SQL>grant select any sequence,create materialized view to inspur;
SQL>grant unlimited tablespace to inpsur;     
SQL>grant select any table to inspur;                                       
SQL>grant create table to  inspur;    
SQL>grant create view to  inspur;
```
## 七、Oracle开机自启动设置

 > 1. 修改/data/oracle/product/11.2.0/bin/dbstart


```
[oracle@localhost ~]$ vim /data/oracle/product/11.2.0/bin/dbstart

#将ORACLE_HOME_LISTNER=$1修改为ORACLE_HOME_LISTNER=$ORACLE_HOME(大约在12%行左右)
```

 > 2. 修改/data/oracle/product/11.2.0/bin/dbshut


```
[oracle@localhost ~]$ vim /data/oracle/product/11.2.0/bin/dbshut

#将ORACLE_HOME_LISTNER=$1修改为ORACLE_HOME_LISTNER=$ORACLE_HOME(大约12%左右)
```
> 3. 修改/etc/oratab文件


```
[oracle@localhost ~]$ vim /etc/oratab

#将ds:/data/oracle/product/11.2.0:N中最后的N改为Y，成为ds:/data/oracle/product/11.2.0:Y
```

> 4. 输入命令dbshut和dbstart测试

    4.1 测试dbshut,监听停止



    4.2测试dbstart:监听启动



> 5. 配置rc.local (root用户执行）


```
su -

vi /etc/rc.d/rc.local

su - oracle -lc "/data/oracle/product/11.2.0/bin/dbstart $ORACLE_HOME"
```


最后根据提示需要运行 chmod+x /etc/rc.d/rc.local

```
[root@localhost ~]#chmod 777 /etc/rc.d/rc.local
```

这里要注意的是dbstart一定要写全路径，否则有可能无法正确调用。


参考文章：


[Oracle 11g 基于CentOS7静默安装教程(无图形界面，远程安装)](https://my.oschina.net/u/3406827/blog/889225?nocache=1506170161845)

[ORACLE监听器 The listener supports no services 问题解决方法](http://blog.csdn.net/snowfoxmonitor/article/details/47705885)
