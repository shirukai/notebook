# Hive大数据仓库进阶 

## 1 Hive的数据导入 

### 1.1 使用load语句 

#### 语法 

LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE]

INTO TABLE tablename [PARTITION (partcoll=val1,partcol2=val2...)]

说明：

[LOCAL] 是否从linux本地去取文件。加上local是从linux读取文件，不加local是从hdfs中读取文件

[OVERWRITE] 是否要覆盖表中原来的数据 

#### 示例： 

将student01.txt数据导入t3表

```
hive> load data local inpath '/root/hadoop_practice/student01.txt' into table t3;
```

将/root/hadoop_practice下所有的数据文件导入到t3表中，并且覆盖原来的数据

```
hive> load data local inpath '/root/hadoop_practice/' overwrite into table t3;
```

将HDFS中，/student/student01.txt 导入到t3表

```
hive> load data inpath '/student/student01.txt' overwrite into table t3;
```

### 1.2 使用sqoop导入数据 

#### 1.2.1 安装配置sqoop 

官网下载sqoop

```
wget https://mirrors.tuna.tsinghua.edu.cn/apache/sqoop/1.4.6/sqoop-1.4.6.bin__hadoop-0.23.tar.gz
```

解压 

```
tar -zxvf sqoop-1.4.6.bin__hadoop-0.23.tar.gz
```

配置变量（配置Hadoop的环境变量）

```
export HADOOP_COMMON_HOME=/usr/hadoop/hadoop-2.7.4/
export HADOOP_MAPRED_HOME=/usr/hadoop/hadoop-2.7.4/
```

复制jdbc驱动到sqoop-1.4.6.bin__hadoop-0.23/lib下

```
 cp /usr/share/java/mysql-connector-java.jar /root/sqoop-1.4.6.bin__hadoop-0.23/lib
```

#### 1.2.2 利用sqoop将mysql中的表导入的hdfs中 

将mysql数据库中的user表导入到hdfs中的/sqoop/user下

```
./sqoop import --connect jdbc:mysql://192.168.162.177:3306/mysql  --username root --password root --table user -m 1 --target-dir '/sqoop/user'
```

注意：jdbc:mysql://192.168.162.177:3306/mysql 中不要使用localhost，使用ip地址

导出完成后生成的hdfs文件

![](https://shirukai.gitee.io/images/201711231157_851.png)

内容：

![](https://shirukai.gitee.io/images/201711231157_852.png)

#### 1.2.2 利用sqoop将mysql中的表导入的Hive中  ,并制定表名

问题：为什么当hive中表名为user的时候，无法对user表进行操作？

```
./sqoop import --hive-import  --connect jdbc:mysql://192.168.162.177:3306/mysql  --username root --password root --table user -m 1 --columns 'User,Password' --hive-table user1
```

#### 1.2.3 利用sqoop将mysql中的表导入到Hive中，并使用where条件 

```
 ./sqoop import --hive-import  --connect jdbc:mysql://192.168.162.177:3306/mysql  --username root --password root --table user -m 1 --columns 'Host,User,Password' --hive-table user2 --where "Host='localhost'";
```

注意：条件语句的引号

#### 1.2.4 利用sqoop将mysql中的表导入到Hive中，并使用查询语句 

问题：（未解决） 条件查询不到，总是报错

```
./sqoop import --hive-import  --connect jdbc:mysql://192.168.162.177:3306/mysql  --username root --password root  -m 1 --query 'SELECT * FROM user WHERE Host="localhost" AND $CONDITIONS ' --target-dir '/sqoop/user3' --hive-table user3;
```

#### 1.2.5 利用sqoop将hive中的数据导入mysql 

问题：数据类型不匹配 string

```
./sqoop export  --connect jdbc:mysql://192.168.162.177:3306/mysql  --username root --password root -m 1 --table t3 --export-dir /user/hive/warehouse/t3;
```



## 2 Hive的数据查询

### 2.1 基础查询 

![](https://shirukai.gitee.io/images/201711231538_28.png)

### 2.2 简单查询的Fetch Task 功能。

#### 配置方式：

* set hive.fetch.task.conversion=more;
* hive --hiveconf hive.fetch.task.conversion=more
* 修改hive-site.xml文件

### 2.3 在查询中使用过滤

![](https://shirukai.gitee.io/images/201711231549_31.png)



![](https://shirukai.gitee.io/images/201711231554_396.png)



### 2.4 在查询中使用排序 ORDER BY

![](https://shirukai.gitee.io/images/201711231557_412.png)



## 3 Hive 中的函数 

内置函数 自定义函数

![](https://shirukai.gitee.io/images/201711231559_300.png)

### 3.1 数学函数 

* #### round 四舍五入 

round(reg1,reg2)

reg1 表示要处理的数据

reg2 表示保留小数点后的位数

```
hive> select round(45.926,2),round(45.926,1),round(45.926,0),round(45.926,-1),round(45.926,-2);
OK
45.93	45.9	46	50	0
Time taken: 1.646 seconds, Fetched: 1 row(s)
```

* #### ceil 向上取整

```
hive> select ceil(45.9);
OK
46
Time taken: 0.275 seconds, Fetched: 1 row(s)

```



* #### floor 向下取整 

```
hive> select floor(45.9);
OK
45
Time taken: 0.732 seconds, Fetched: 1 row(s)
```

### 3.2 字符函数 

* #### lower 把字符串转成小写

```
hive> select lower('Hello World');
OK
hello world
Time taken: 0.626 seconds, Fetched: 1 row(s)
```



* #### upper 把字符串转成大写

```
hive> select upper('Hello World');
OK
HELLO WORLD
Time taken: 0.67 seconds, Fetched: 1 row(s)

```



* #### length 字符串的长度(字符数)

```
hive> select length('Hello World');
OK
11
Time taken: 0.251 seconds, Fetched: 1 row(s)
```



* #### concat 拼加一个字符串

```
hive> select concat ('Hello','World');
OK
HelloWorld
Time taken: 0.703 seconds, Fetched: 1 row(s)

```



* #### substr 求子串

> 补充： 与java中的substring、js中的substring、substr区别
>
> java和js中都有substring方法用来截取字符串
>
> 用法：字符串.substring(起始位置从零开始、结束位置)
>
> js中有substr方法
>
> 用法： 字符串.substr(起始位置从零开始、截取长度)

substr(a,b) 从a中，第b位开始取，取右边所有的字符串

substr(a,b,c) 从a中，第b位开始取，取右边c个字符串

```
hive> select substr('Hello world',3);
OK
llo world
Time taken: 0.676 seconds, Fetched: 1 row(s)
```



* #### trim 去掉字符串前后的空格

```
hive> select trim('   Hello World'   );
OK
Hello World
Time taken: 0.337 seconds, Fetched: 1 row(s)

```



* #### lpad 左填充

```
hive> select lpad('abc',10,'*');
OK
*******abc
Time taken: 0.625 seconds, Fetched: 1 row(s)

```



* #### rpad 右填充

```
hive> select rpad('abc',10,'*');
OK
abc*******
Time taken: 0.663 seconds, Fetched: 1 row(s)

```

### 3.2 收集函数

* #### size 

```
hive> select size(map(1,'Tom',2,'Mary'));
OK
2
Time taken: 0.853 seconds, Fetched: 1 row(s)
```

### 3.3 转换函数 

* #### cast 

```
hive> select cast(1 as bigint);
OK
1
Time taken: 0.373 seconds, Fetched: 1 row(s)
hive> select cast(1 as float);
OK
1.0
Time taken: 0.669 seconds, Fetched: 1 row(s)
```

### 3.4 日期函数 

* #### to_date 返回日期部分

```
hive> select to_date('2017-11-23 16:48:21');
OK
2017-11-23
Time taken: 0.711 seconds, Fetched: 1 row(s)
```



* #### year 返回年

```
hive> select year('2017-11-23 16:48:21');
OK
2017
Time taken: 0.647 seconds, Fetched: 1 row(s)
```



* #### month 返回月

```
hive> select month('2017-11-23 16:48:21');
OK
11
Time taken: 0.413 seconds, Fetched: 1 row(s)
```



* #### day 返回日

```
hive> select day('2017-11-23 16:48:21');
OK
23
Time taken: 0.174 seconds, Fetched: 1 row(s)
```



* #### weekofyear 返回当年中第几个周

```
hive> select weekofyear('2017-11-23 16:48:21');
OK
47
Time taken: 0.688 seconds, Fetched: 1 row(s)

```



* #### datediff 返回两个日期相差的天数

```
hive> select datediff('2017-11-23 16:48:21','2014-11-23 17:00:52');
OK
1096
Time taken: 0.306 seconds, Fetched: 1 row(s)
```



* #### date_add 加上多少天

```
hive> select date_add('2017-11-23 16:48:21',2);
OK
2017-11-25
Time taken: 0.216 seconds, Fetched: 1 row(s)
```



* #### date_sub 减去多少天

```
hive> select date_sub('2017-11-23 16:48:21',2);
OK
2017-11-21
Time taken: 0.614 seconds, Fetched: 1 row(s)

```

### 3.5 条件函数 

* #### coalesce ：从左到右返回第一个不为null的值



* #### case ... when ...: 条件表达式

### 3.6 聚合函数 

* #### count 统计

* #### sum 求和

* #### min 最小值

* #### max 最大值

* #### avg 平均值

### 3.7 表生成函数 

* #### explode

```
hive> select explode(map(1,'Tom',2,'Mary',3,'Mell'));
OK
1	Tom
2	Mary
3	Mell
Time taken: 0.36 seconds, Fetched: 3 row(s)

```

## 5 Hive 表连接 

* #### 等值连接 

* #### 不等值连接

* #### 外链接（左外连接、右外连接）

* #### 内连接

## 6 Hive 子查询 

![](https://shirukai.gitee.io/images/201711231715_587.png)

## 7 Hive的Java客户端和自定义函数

### 7.1 启动Hive远程服务 

```
hiveserver2
```

### 7.2 JDBC 客户端 

![](https://shirukai.gitee.io/images/201711231718_673.png)

### 7.3 代码实现 

#### 7.3.1 IDEA使用Maven创建一个项目 

![](https://shirukai.gitee.io/images/201711240909_244.gif)

#### 7.3.2 pom引入依赖 

```
<dependencies>
    <!--日志依赖-->
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>1.7.12</version>
    </dependency>
    <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-core</artifactId>
        <version>1.1.1</version>
    </dependency>
    <!--实现slf4j接口并整合-->
    <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-classic</artifactId>
        <version>1.1.1</version>
    </dependency>
    <!--hive jdbc 依赖-->
    <dependency>
        <groupId>org.apache.hive</groupId>
        <artifactId>hive-jdbc</artifactId>
        <version>2.3.2</version>
    </dependency>
</dependencies>
```

引入依赖之后Reimport maven project

#### 7.3.3 配置logback日志 

在resource下创建logback.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <jmxConfigurator/>
    <!--
    将日志打印到控制台
    -->
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <layout class="ch.qos.logback.classic.PatternLayout">
            <Pattern>%date [%thread] %-5level %logger{25} - %msg%n</Pattern>
        </layout>
    </appender>

    <!--
    level:设置日志级别，大小写无关：TRACE, DEBUG, INFO, WARN, ERROR, ALL 和 OFF，不能设置为INHERITED或者同义词NULL。默认是DEBUG
    ref:日志信息交给已经配置好的名为"console"的appender处理，appender将信息打印到控制台
    -->
    <root level="INFO">
        <appender-ref ref="console"/>
    </root>
</configuration>
```



#### 7.3.4 创建jdbc连接工具类 

在java下创建 org.hive.demo.untils包，然后在包下创建JDBCUtils类

```
package org.hive.demo.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

/**
 * Hive JDBC 连接工具类
 * Created by shirukai on 2017/11/23.
 */
public class JDBCUtils {
    private static Logger logger = LoggerFactory.getLogger("JDBCUtils");
    private static String url = "jdbc:hive2://192.168.162.177:10000/default";
    public static String user = "root";
    public static String pass = "root";

    //获取连接
    public static Connection getConnection(){
        try {
            return DriverManager.getConnection(url,user,pass);
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
       return null;
    }

    //释放资源
    public static void release(Connection conn, Statement st, ResultSet rs){
        if (rs != null){
            try {
                rs.close();
            } catch (Exception e) {
                logger.error(e.getMessage(), e);
            }finally {
                rs = null;
            }

        }
        if (st != null){
            try {
            st.close();
            } catch (Exception e) {
                logger.error(e.getMessage(), e);
            }finally {
                st = null;
            }
        }
        if (conn != null){
            try {
                conn.close();
            } catch (Exception e) {
                logger.error(e.getMessage(), e);
            }finally {
                conn = null;
            }
        }
    }
}

```

#### 7.3.4 创建hive测试类 

创建org.hive.demo.hive包，然后创建HiveJDBCDemo类

```
package org.hive.demo.hive;

import org.hive.demo.utils.JDBCUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

/**
 *
 * Created by shirukai on 2017/11/23.
 */
public class HiveJDBCDemo {
    private static Logger logger = LoggerFactory.getLogger("HiveJDBCDemo");
    public static void main(String[] args){
        Connection conn = null;
        Statement st = null;
        ResultSet rs = null;
        String sql = "select * from t3";
        try {
            //获取连接
            conn = JDBCUtils.getConnection();
            //创建运行环境
            st = conn.createStatement();
            //运行HQL
            rs = st.executeQuery(sql);
            while (rs.next()){
                logger.info("rs={}",rs.getString(1));
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }finally {
            JDBCUtils.release(conn,st,rs);
        }
    }
}
```



#### 7.3.5 运行main方法

#### 7.3.6 出现如下错误的解决方法 

报错：root is not allowed to impersonate root

![](https://shirukai.gitee.io/images/201711240906_230.png)



修改 hadoop的配置文件 core-site.xml ，加入以下内容,修改完成后重启hadoop服务

```
<property>
    <name>hadoop.proxyuser.root.hosts</name>
    <value>*</value>
</property>
<property>
    <name>hadoop.proxyuser.root.groups</name>
    <value>*</value>
</property>

```



参考资料：https://www.waitig.com/user-root-is-not-allowed-to-impersonate-anonymous.html

#### 7.3.7 注意版本问题 

加载HiveServer2 JDBC驱动程序。从[1.2.0版开始，](https://issues.apache.org/jira/browse/HIVE-7998)不再需要使用Class.forName（）来显式加载JDBC驱动程序。

如：

```
Class.forName("org.apache.hive.jdbc.HiveDriver");
```

通过`Connection`使用JDBC驱动程序创建对象来连接到数据库。

```
Connection cnct = DriverManager.getConnection("jdbc:hive2://<host>:<port>", "<user>", "<password>");
```



## 8 Hive Thrift客户端 

（……）

## 9 hive 自定义函数 

* Hive的自定义函数(UDF):User Defined Function 
* 可以直接应用于select语句，对查询结果做格式化处理后，再输出内容。



### Hive自定义函数的实现细节 

* 自定义UDF需要继承org.apache.hadoop.hive.ql.UDF
* 需要实现evaluate函数，evaluate函数支持重载

### Hive自定义函数的部署运行 

* 把程序打包放到目标机器上去
* 进入hive客户端，添加jar包

```
add jar /root/training/udfjar/udf_test.jar
```

* 创建临时函数

```
CREATE TEMPORARY FUNCTION <函数名>
AS'Java类名'
```

### 自定义函数案例 

拼加两个字符串 

创建 ConcatString类

```
package org.hive.demo.hive;

import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public class ConcatString extends UDF {
    public Text evaluate(Text a,Text b){
        return new Text(a.toString()+"***"+b.toString());
    }
}
```

利用 Eclipse将ConcatString类导出成jar包

![](https://shirukai.gitee.io/images/201711241149_149.gif)



导出jar后上传到linux

![](https://shirukai.gitee.io/images/201711241150_704.png)

进入hive客户端，添加jar包

```
hive> add jar /root/concatstring.jar;
Added [/root/concatstring.jar] to class path
Added resources: [/root/concatstring.jar]
```



创建临时函数

```
hive> create temporary function myconcat as 'org.hive.demo.hive.ConcatString';
OK
Time taken: 0.183 seconds
```

测试

```
hive> select myconcat('Hello','Word');
OK
Hello***Word
Time taken: 3.523 seconds, Fetched: 1 row(s)
```

## 10 总结 

### 为什么要使用hive呢？

hive是一个数据仓库，用来支持我们的OLAP的应用，hive的数据仓库是建立咋Hadoop集群之上的，它的数据是存放在HDFS系统中，在hive中执行的操作会转换成MapReduce作业进行提交运行。我们的Hive也支持类似SQL的语言，即HQL。Hive采用元数据对表进行管理，元数据有三种存放模式：嵌入模式、本地模式、远程模式。hive提供了非常强大的编程接口：JDBC、客户端、自定义函数。这就是我们学习的Hive。

![](https://shirukai.gitee.io/images/201711241158_587.png)

学习自：慕课网《走进大数据之Hive入门、进阶》