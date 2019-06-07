# Linux常用命令及技巧 

删除某个目录下，所有子目录中包含指定字符的文件或者文件夹 

例如删除 包含“index"的文件或目录

```
find * | grep index* | xargs rm
```



查看yum已安装的软件模糊查询

```
yum list | grep 关键字*
```



建立软链接

```
ln -s 连接地址 目录名
```



shell远程登录另一台主机，并执行命令

```
#!/bin/bash
echo "================集群启动……====================="
echo "启动hadoop……"
start-all.sh
echo "启动zookeeper……"
cd /usr/lib/zookeeper-3.5.0-alpha/bin
./zkServer.sh start
sleep 2
ssh Slave1.Hadoop "/usr/lib/zookeeper-3.5.0-alpha/bin/zkServer.sh start"
sleep 2
ssh Slave2.Hadoop "/usr/lib/zookeeper-3.5.0-alpha/bin/zkServer.sh start"
sleep 2
echo '启动HBase……'
start-hbase.sh
```



递归创建目录

```
mkdir -p data/11/11
```



解压tar.gz文件到指定目录

```
tar -zxvf ****.tar.gz -C /***/****
```



远程发送某个文件夹、或者文件到另一台主句

```
scp -r 要发送的文件或者目录 用户名@主机ip:目的路径
```



查看端口启动状态

```
netstat -ntlp | grep 8080
```



### 开机启动脚本的两种方法 

第一种 chkconfig方法：

1. 编写脚本 start-myshell.sh

```
#/bin/sh
#chkconfig: 2345 80 90
#description: 开机自启动脚本程序描述

#创建一个文件夹
mkdir /root/shirukai
```

脚本第一行 “#!/bin/sh” 告诉系统使用的shell； 
脚本第二行 “#chkconfig: 2345 80 90” 表示在2/3/4/5运行级别启动，启动序号(S80)，关闭序号(K90)； 
脚本第三行 表示的是服务的描述信息

**注意：** 第二行和第三行必写，否则会出现如“**服务 autostart.sh 不支持 chkconfig**”这样的错误。

2. 将写好的脚本复制到/etc/rc.d/init.d/目录下

3. 然后授予可执行权限

   ```
   chmod -x start-myshell.sh
   ```

4. 添加脚本到开机启动项目中

```
chkconfig -add start-myshell.sh
chkconfig start-myshell.sh on
```

chkconfig -del start-myshell.sh

第二种 修改/etc/rc.d/rc.local文件：

在文件中加入一行

```
sh /root/start-myshell.sh
```

sh 后面跟要运行的shell脚本文件的路径



chmod 权限使用

http://www.runoob.com/linux/linux-comm-chmod.html





### 定时任务：

crontab -e

https://www.cnblogs.com/intval/p/5763929.html



### 后台运行任务

运行任务后ctrl+z 

jobs查看后台任务

bg 任务编号  后台执行

fg 任务编号 前台执行

任务名 &  显示进程号

kill 进程号 



### vi多行删除、多行复制、查找

#### 删除 

dd 删除一行

ndd 删除以当前行开始的n行

dw 删除以当前字符开始的一个字符

ndw 删除以当前字符开始的n个字符

d$、D 删除以当前字符开始的一行字符

d) 删除到下一句的开始

d} 删除到下一段的开始

d回车 删除2行

#### 复制 

：9，15 copy 16  或 ：9，15 co 16
由此可有：
：9，15 move 16  或 :9,15 m 16 将第9行到第15行的文本内容到第16行的后面  



查找 /要查找的内容 n向下查找 N向上查找





#### 查看进程 

ps -ef | grep 条件



#### Vi 光标到最后一行 

shift+g

#### Vi 光标到最后一个字符 

shift+4 即$



### 删除除了某个或者某些文件之外的其他文件

```
rm -rf !(filename)
rm -rf !(filename1|filename2|filename3)
```



### 解压zip

1.把文件解压到当前目录下

```
unzip xxxx.zip
```

2.如果把文件解压到指定的目录下，需要用到-d参数

```
unzip -d /temp xxxx.zip
```

3.解压的时候，不覆盖已经存在的文件，使用-n参数

```
unzip -n xxxx.zip
unzip -n -d/temp xxxx.zip
```

4.只看一下压缩包中有哪些文件，不进行解压

````
unzip -l xxxx.zip
````

5.查看显示的文件列表，以及压缩比率

```
unzip -v xxxx.zip
```

6.检查zip文件是否损坏

```
unzip -t xxxx.zip
```

7.将压缩文件xxxx.zip解压到指定目录下，如果已有相同文件，进行覆盖操作

```
unzip -o xxxx.zip -d /tmp/
```

### 打包zip

http://man.linuxde.net/zip

```
zip -q -r xxx.zip /xxx/xxxx/xxx
```
