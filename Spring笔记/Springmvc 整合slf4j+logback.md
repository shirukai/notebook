# Springmvc 整合slf4j+logback

日志组件：slf4j，log4j，logback，common-logging

slf4j是日志规范，没有任何实现

日志实现：log4j，logback，common-logging

## 为什么采用 slf4j+logback组合呢? 

### 一、slf4j的介绍：

SLF4J，即简单日志门面（Simple Logging Facade for Java），不是具体的日志解决方案，它只服务于各种各样的日志系统。按照官方的说法，SLF4J是一个用于日志系统的简单[Facade](https://baike.baidu.com/item/Facade)，允许最终用户在部署其应用时使用其所希望的日志System

### 二、logback介绍：

 Logback是由log4j创始人设计的又一个开源日志组件。logback当前分成三个模块：logback-core,logback- classic和logback-access。logback-core是其它两个模块的基础模块。logback-classic是log4j的一个 改良版本。此外logback-classic完整实现[SLF4J API](http://www.oschina.net/p/slf4j)使你可以很方便地更换成其它日志系统如log4j或JDK14 Logging。logback-access访问模块与Servlet容器集成提供通过Http来访问日志的功能。 Logback是要与SLF4J结合起来用两个组件的官方网站如下：

​    logback的官方网站： [http://logback.qos.ch](http://logback.qos.ch/download.html)

​    SLF4J的官方网站：[http://www.slf4j.org](http://www.slf4j.org/download.html)

### 三、logback取代log4j的理由：

​    Logback和log4j是非常相似的，如果你对log4j很熟悉，那对logback很快就会得心应手。下面列了logback相对于log4j的一些优点：

**1、更快的实现**  

Logback的内核重写了，在一些关键执行路径上性能提升10倍以上。而且logback不仅性能提升了，初始化内存加载也更小了。

**2、Logback-classic非常自然实现了SLF4j**    

Logback-classic实现了 SLF4j。在使用SLF4j中，你都感觉不到logback-classic。而且因为logback-classic非常自然地实现了SLF4J，  所 以切换到log4j或者其他，非常容易，只需要提供成另一个jar包就OK，根本不需要去动那些通过SLF4JAPI实现的代码。

**3、非常充分的文档**  

官方网站有两百多页的文档。

**4、自动重新加载配置文件 **

 当配置文件修改了，Logback-classic能自动重新加载配置文件。扫描过程快且安全，它并不需要另外创建一个扫描线程。这个技术充分保证了应用程序能跑得很欢在JEE环境里面。

**5、Lilith**   

Lilith是log事件的观察者，和log4j的chainsaw类似。而lilith还能处理大数量的log数据 。

**6、谨慎的模式和非常友好的恢复 **

在谨慎模式下，多个FileAppender实例跑在多个JVM下，能 够安全地写道同一个日志文件。RollingFileAppender会有些限制。Logback的FileAppender和它的子类包括 RollingFileAppender能够非常友好地从I/O异常中恢复。

**7、配置文件可以处理不同的情况  **

开发人员经常需要判断不同的Logback配置文件在不同的环境下（开发，测试，生产）。而这些配置文件仅仅只有一些很小的不同，可以通过,和来实现，这样一个配置文件就可以适应多个环境。

**8、Filters（过滤器） **

有些时候，需要诊断一个问题，需要打出日志。在log4j，只有降低日志级别，不过这样会打出大量的日志，会影响应用性能。在Logback，你可以继续 保持那个日志级别而除掉某种特殊情况，如alice这个用户登录，她的日志将打在DEBUG级别而其他用户可以继续打在WARN级别。要实现这个功能只需 加4行XML配置。可以参考MDCFIlter 。

**9、SiftingAppender（一个非常多功能的Appender）**  

它可以用来分割日志文件根据任何一个给定的运行参数。如，SiftingAppender能够区别日志事件跟进用户的Session，然后每个用户会有一个日志文件。

**10、自动压缩已经打出来的log** 

 RollingFileAppender在产生新文件的时候，会自动压缩已经打出来的日志文件。压缩是个异步过程，所以甚至对于大的日志文件，在压缩过程中应用不会受任何影响。

**11、堆栈树带有包版本 ** 

Logback在打出堆栈树日志时，会带上包的数据。

**12、自动去除旧的日志文件** 

 通过设置TimeBasedRollingPolicy或者SizeAndTimeBasedFNATP的maxHistory属性，你可以控制已经产生日志文件的最大数量。如果设置maxHistory 12，那那些log文件超过12个月的都会被自动移除。

## 配置slf4j+logback 

### maven配置相关jar包依赖

```
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
```

### 配置文件 

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!--定义日志文件存储地址，勿在logback的配置中使用相对路径-->
    <property name="LOG_HOME" value="D:/var/log/"/>
    <jmxConfigurator/>
    <!--
    将日志打印到控制台
    -->
    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <layout class="ch.qos.logback.classic.PatternLayout">
            <Pattern>%date [%thread] %-5level %logger{25} - %msg%n</Pattern>
        </layout>
    </appender>

    <!--将日志打印到文件
    file:文件保存的路径，可以是相对路径也可以是绝对路径，如果目录不存在会自动创建，没有默认值
    append:如果是true，日志被追加到文件结尾，如果是false，清空现存文件，默认是true
    encoder:对记录进行格式化
    prudent: 如果是true，日志会被安全的写入文件，即使其他的FileAppender也在向此文件做接入操作，效率低，默认是false
    -->
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <file>mavenssmlr.log</file>
        <append>true</append>
        <encoder>
            <pattern>%date [%thread] %-5level %logger{25} - %msg%n</pattern>
        </encoder>
    </appender>


    <!--每天生成一个日志文件，保存30天的日志文件-->

    <appender name="30DAY" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>log/logFile.%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>

        <encoder>
            <pattern>%-4relative [%thread] %-5level %logger{35} - %msg%n</pattern>
        </encoder>
    </appender>

    <!--
    level:设置日志级别，大小写无关：TRACE, DEBUG, INFO, WARN, ERROR, ALL 和 OFF，不能设置为INHERITED或者同义词NULL。默认是DEBUG
    ref:日志信息交给已经配置好的名为"console"的appender处理，appender将信息打印到控制台
    -->
    <root level="DEBUG">
        <appender-ref ref="30DAY"/>
    </root>
</configuration>
```

### 使用 

```
private org.slf4j.Logger logger = LoggerFactory.getLogger(this.getClass());
logger.info("_____________msg={}", msg);
```