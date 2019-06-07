# Maven构建springmvc+mybatis+logback+redis项目 

## 一、利用maven指令创建web项目

### 1.创建一个名字为mavenssmlr的项目,在命令行输入以下指令： 

```
mvn archetype:generate -DgroupId=org.mavenssmls -DartifactId=mavenssmlr -DarchetypeArtifactId=maven-archetype-webapp
```

创建成功后，用IDEA导入项目：File - Open

### 2.补全目录 

打开Module settings 在Modules里创建目录

在src/main目录下创建名字为java的Sources目录

在src/main目录下创建名字resource的Resource目录

在src下创建test目录

在src/test下创建创建名字为java的Tests目录

在src/test下创建创建名字为Test Resource目录

在src/java下创建包

数据持久化层DAO：com.mavenssmlr.dao 

数据实体类：com.mavenssmlr.entity

Service层：com.mavenssmlr.service

Controller层：com.mavenssmlr.web

### 3.处理依赖pom.xml 

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.mavenssmlr</groupId>
  <artifactId>mavenssmlr</artifactId>
  <packaging>war</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>mavenssmlr Maven Webapp</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <!--使用junit4-->
      <!--为什么使用junit4？因为junit3是采用编程的方式运行junit，而junit4是采用注解的方式运行junit -->
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.12</version>
      <scope>test</scope>
    </dependency>
    <!--补全项目依赖-->
    <!--1：日志 java日志：slf4j，log4j，logback，common-logging
    slf4j 是规范/接口
    日志实现：log4j，logback，common-logging
    使用：slf4j + logback
    -->
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
    <!--2：数据库相关的依赖-->
    <!--数据库连接驱动-->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>5.1.35</version>
      <scope>runtime</scope>
    </dependency>
    <!--数据库连接池-->
    <dependency>
      <groupId>c3p0</groupId>
      <artifactId>c3p0</artifactId>
      <version>0.9.1.2</version>
    </dependency>
    <!--3：DAO框架：mybatis依赖-->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis</artifactId>
      <version>3.3.0</version>
    </dependency>
    <!--mybatis自身实现的spring整合依赖-->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis-spring</artifactId>
      <version>1.2.3</version>
    </dependency>
    <!--servlet web相关依赖-->
    <!--jsp标签-->
    <dependency>
      <groupId>taglibs</groupId>
      <artifactId>standard</artifactId>
      <version>1.1.2</version>
    </dependency>
    <!--jsp servlet-->
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>jstl</artifactId>
      <version>1.2</version>
    </dependency>
    <!--jackson-->
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.7.5</version>
    </dependency>
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>javax.servlet-api</artifactId>
      <version>3.1.0</version>
    </dependency>
    <!--4：spring依赖-->
    <!--1)spring核心依赖-->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-beans</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <!--2）spring DAO层依赖-->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-jdbc</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-tx</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <!--3)spring web 相关依赖-->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-web</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <!--4) spring test 相关依赖-->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-test</artifactId>
      <version>4.3.6.RELEASE</version>
    </dependency>
    <!--redis客户端 jedis-->
    <dependency>
      <groupId>redis.clients</groupId>
      <artifactId>jedis</artifactId>
      <version>2.7.3</version>
    </dependency>
    <!--protostuff序列化依赖-->
    <dependency>
      <groupId>com.dyuproject.protostuff</groupId>
      <artifactId>protostuff-core</artifactId>
      <version>1.1.2</version>
    </dependency>
    <dependency>
      <groupId>com.dyuproject.protostuff</groupId>
      <artifactId>protostuff-runtime</artifactId>
      <version>1.1.2</version>
    </dependency>
    <dependency>
      <groupId>commons-collections</groupId>
      <artifactId>commons-collections</artifactId>
      <version>3.2.1</version>
    </dependency>
  </dependencies>
  <build>
    <finalName>mavenssmlr</finalName>
  </build>

</project>
```

### 4.相关配置

#### 配置DAO层：

在java/resources里创建

##### mapper包：用来存放数据mapper映射的xml文件 

##### spring包：用来存放spring相关的xml配置文件 

在java/resources/spring包下创建：

spring-dao.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                    http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
                    http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd">
    <!--配置整合mybatis过程-->
    <!--1：配置数据库相关参数properties的属性：${url}-->
    <context:property-placeholder location="classpath:jdbc.properties"/>
    <!--2：数据库连接池-->
    <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
        <!--配置连接池属性-->
        <property name="driverClass" value="${driver}"/>
        <property name="jdbcUrl" value="${url}"/>
        <property name="user" value="${jdbc.username}"/>
        <property name="password" value="${password}"/>

        <!--c3po连接池的私有属性-->
        <property name="maxPoolSize" value="30"/>
        <property name="minPoolSize" value="10"/>
        <!--关闭连接后不自动commit-->
        <property name="autoCommitOnClose" value="false"/>
        <!--获取连接超时时间-->
        <property name="checkoutTimeout" value="1000"/>
        <!--当获取连接失败重试次数-->
        <property name="acquireRetryAttempts" value="2"/>
    </bean>
    <!--约定大于配置-->
    <!--3：配置sqlSessionFactory对象-->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <!--注入数据库连接池-->
        <property name="dataSource" ref="dataSource"/>
        <!--配置mybatis全局配置文件：mybatis-config.xml-->
        <property name="configLocation" value="classpath:mybatis-config"/>
        <!--扫描entity包 使用别名-->
        <property name="typeAliasesPackage" value="com.mavenssmlr.entity/>
        <!--扫描sql配置文件：mapper需要的xml文件-->
        <property name="mapperLocations" value="classpath:mapper/*.xml"/>
    </bean>
    <!--4：配置扫描Dao接口包，动态实现Dao接口，并注入到spring容器中-->
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <!--注入sqlSessionFactory-->
        <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"/>
        <!--给出扫描dao接口包-->
        <property name="basePackage" value="com.mavenssmlr.dao"/>
    </bean>
</beans>
```

##### jdbc.properties文件：数据库连接池相关的配置 

```
driver=com.mysql.jdbc.Driver
url=jdbc:mysql://localhost:3306/mavensslr?characterEncoding=UTF-8
jdbc.username=root
password=inspur
```

##### mybatis-config.xml：mybatis先关的配置文件

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--配置全局属性-->
    <settings>
        <!--使用jdbc的getGeneratedKeys 获取数据库自增主键值-->
        <setting name="useGeneratedKeys" value="true"/>
        <!--使用列别名替换列名 默认true-->
        <setting name="useColumnLabel" value="true"/>
        <!--开启驼峰命名转换-->
        <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>
</configuration>
```

##### logback.xml:配置logback 

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <jmxConfigurator />

    <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
        <layout class="ch.qos.logback.classic.PatternLayout">
            <Pattern>%date [%thread] %-5level %logger{25} - %msg%n</Pattern>
        </layout>
    </appender>

    <root level="debug">
        <appender-ref ref="console" />
    </root>
</configuration>
```

#### 配置Service层

在java/spring下创建

spring-service.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context" xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                    http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
                    http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
                     http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd">
    <!--扫描service包下所有使用注解的类型-->
    <context:component-scan base-package="com.mavenssmlr.service"/>

    <!--配置事务管理器-->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <!--注入数据库连接池-->
        <property name="dataSource" ref="dataSource"/>
    </bean>
    <!--配置基于注解的声明式事务-->
    <tx:annotation-driven transaction-manager="transactionManager"/>
</beans>
```

#### 配置web层

创建spring-web.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                    http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
                    http://www.springframework.org/schema/context
                    http://www.springframework.org/schema/context/spring-context.xsd
                    http://www.springframework.org/schema/mvc
                    http://www.springframework.org/schema/mvc/spring-mvc.xsd">
    <!--配置springmvc-->
    <!--1:开启springMVC注解模式-->
    <!--简化配置：
        （1）自动注册DefaultAnnotationHandlerMapping，AnnotationMethodHandlerAdapter
        （2）提供一系列：数据绑定，数字和日期的format @NumberFormat @DataTimeFormat,
             xml,json默认读写支持
    -->
    <mvc:annotation-driven/>
    <!--servlet-mapping 映射路径："/"-->
    <!--2:静态资源默认servlet配置
        (1)：加入对静态资源的处理 js，gif，png
        (2)：允许使用'/'做整体映射
    -->
    <mvc:default-servlet-handler/>
    <!--3:配置jsp 显示ViewResolver-->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="viewClass" value="org.springframework.web.servlet.view.JstlView"/>
        <property name="prefix" value="/WEB-INF/jsp/"/>
        <property name="suffix" value=".jsp"/>
    </bean>
    <!--4:扫描web相关的bean-->
    <context:component-scan base-package="com.mavenssmlr.web"/>
    <!--静态资源包-->
    <mvc:resources mapping="/skins/**" location="WEB-INF/skins/"/>
</beans>
```

#### 配置web.xml文件

```
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1"
         metadata-complete="true">
  <!--修改servlet版本为3.1-->
  <!--配置DispatcherServlet-->
  <servlet>
    <servlet-name>mavenssmlr-dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <!--配置Springmvc需要加载的配置文件
        spring-dao.xml,spring-service.xml,spring-web.xml
        mybatis -> spring -> spring mvc
    -->
    <init-param>
      <param-name>contextConfigLocation</param-name>
      <param-value>classpath:spring/spring-*.xml</param-value>
    </init-param>
  </servlet>
  <servlet-mapping>
    <servlet-name>mavenssmlr-dispatcher</servlet-name>
    <!--匹配/下请求-->
    <url-pattern>/</url-pattern>
  </servlet-mapping>
  <!-- Spring字符编码过滤器配置，处理中文乱码，针对post请求 -->
  <filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
    <init-param>
      <param-name>forceEncoding</param-name>
      <param-value>true</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
</web-app>
```

## 二、DAO层编写测试 

### 在resources下创建sql包用来存放sql脚本 

创建scahme.sql文件并初始化数据

```
-- 创建数据库
CREATE DATABASE mavenssmlr CHARSET 'UTF8';

-- 使用数据库
USE mavenssmlr;

-- 创建数据库表

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `uname` varchar(100) NOT NULL COMMENT '用户名',
  `create-time` datetime DEFAULT NOW() COMMENT '创建时间',
  `modify-time` TIMESTAMP NOT NULL DEFAULT current_timestamp ON UPDATE current_timestamp COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uname` (`uname`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='用户表';

INSERT INTO mavenssmlr.user (uname)
    VALUES ('test');
```

### 在java/com/mavenssmlr/entity/包下创建User实体类 

```
public class User {
    private int id;
    private String uname;
    private Date createTime;
    private Date modifyTime;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUname() {
        return uname;
    }

    public void setUname(String uname) {
        this.uname = uname;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getModifyTime() {
        return modifyTime;
    }

    public void setModifyTime(Date modifyTime) {
        this.modifyTime = modifyTime;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", uname='" + uname + '\'' +
                ", createTime=" + createTime +
                ", modifyTime=" + modifyTime +
                '}';
    }
}
```

### 在java/com/mavenssmlr/dao/包下创建Dao层接口 UserDao 

```
package com.mavenssmlr.dao;

import com.mavenssmlr.entity.User;

import java.util.List;

/**
 *
 * Created by shirukai on 2017/10/17.
 */
public interface UserDao {
    /**
     * 新增用户信息
     * @param user 用户实体类
     * @return
     */
    int insertUser(User user);

    /**
     * 查询所有用户
     * @return
     */
    List<User> queryAll();

    /**
     * 根据id查询用户
     * @param id
     * @return
     */
    User queryById(int id);

    /**
     * 根据id删除用户
     * @param id
     * @return
     */
    int deleteById(int id);
}
```

### 在resources/mapper下创建映射文件 UserMapper.xml 

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.mavenssmlr.dao.UserDao">
    <resultMap id="resultUser" type="com.mavenssmlr.entity.User">
         <id property="id" column="id"/>
        <result property="uname" column="uname" />
        <result property="createTime" column="create_time" />
        <result property="modifyTime" column="modify_time" />
    </resultMap>
    <insert id="insertUser" parameterType="User" >
        INSERT INTO mavenssmlr.user (uname)VALUES (#{uname})
    </insert>
    <select id="queryAll" resultMap="resultUser">
        SELECT * FROM mavenssmlr.user
    </select>
    <select id="queryById" parameterType="int">
        SELECT * FROM mavenssmlr.user
        WHERE id = #{id}
    </select>
    <delete id="deleteByid" parameterType="int">
        DELETE FROM mavenssmlr.user
        WHERE id=#{id}
    </delete>
</mapper>
```

#### 对UserDao进行单元测试 

在UserDao接口 内 快捷键 ctrl+shift+t生成单元测试，编写单元测试类：

```
package com.mavenssmlr.dao;

import com.mavenssmlr.entity.User;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;
import java.util.logging.Logger;

import static org.junit.Assert.*;


/**
 * 配置spring和junit整合，junit启动时加载springIOC容器
 */
@RunWith(SpringJUnit4ClassRunner.class)
//告诉junit spring配置文件
@ContextConfiguration({"classpath:spring/spring-dao.xml"})
public class UserDaoTest {
    private org.slf4j.Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    private UserDao userDao;

    @Test
    public void insertUser() throws Exception {
        User user = new User();
        user.setUname("史汝凯");
        int inserCount = userDao.insertUser(user);
        logger.info("_____________insertCount={}", inserCount);

    }

    @Test
    public void queryAll() throws Exception {
        List<User> userList = userDao.queryAll();
        logger.info("____________userList={}", userList);
    }

    @Test
    public void queryById() throws Exception {
    }

    @Test
    public void deleteById() throws Exception {
    }

}
```

## 三、service层单元测试 

### 创建service接口 

在 com/mavenssmlr/service包下创建MavenssmlrService接口

```
package com.mavenssmlr.service;

import com.mavenssmlr.entity.User;

import java.util.List;

public interface MavenssmlrService {
    List<User> queryAll();
}
```

### 创建接口service接口实现类

在 com/mavenssmlr/service包下创建Impl包然后创建是实现类 MavenssmlrServiceImpl

```
package com.mavenssmlr.service.Impl;

import com.mavenssmlr.dao.UserDao;
import com.mavenssmlr.entity.User;
import com.mavenssmlr.service.MavenssmlrService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MavenssmlrServiceImpl implements MavenssmlrService {
    @Autowired
    private UserDao userDao;
    public List<User> queryAll() {
        return userDao.queryAll();
    }
}
```

### 创建Service单元测试

在service接口按住 ctrl+shift+t生成单元测试

```
package com.mavenssmlr.service;

import com.mavenssmlr.entity.User;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;

import static org.junit.Assert.*;

@RunWith(SpringJUnit4ClassRunner.class)
//告诉junit spring配置文件
@ContextConfiguration({
        "classpath:spring/spring-dao.xml",
        "classpath:spring/spring-service.xml"})
public class MavenssmlrServiceTest {
     private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    private MavenssmlrService mavenssmlrService;
    @Test
    public void queryAll() throws Exception {
       List<User> usersList =  mavenssmlrService.queryAll();
       logger.info("usersList={}",usersList);
    }

}
```

## 四、编写controller  

在web下面创建UserController类

```
package com.mavenssmlr.web;

import com.mavenssmlr.service.MavenssmlrService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;


@Controller
@RequestMapping("/user")
public class UserController {
    @Autowired
    private MavenssmlrService mavenssmlrService;
    @RequestMapping("/list")
    public String userList(Model model){
        model.addAttribute("list",mavenssmlrService.queryAll());
        return "list";
    }
}
```



## 五、编写jsp 

在WEB-INF下创建jsp目录

在jsp目录下创建common目录

1.创建head.jsp 公共头部分，用于存放公用的css、js文件

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%--引入css文件--%>
<link href="<%=request.getContextPath()%>/skins/css/bootstrap.css" rel="stylesheet">
<%--引入js文件--%>
<script src="<%=request.getContextPath()%>/skins/js/jquery.js"></script>
<script src="<%=request.getContextPath()%>/skins/js/bootstrap.js"></script>
```

2.创建meta.jsp 公共meta部分

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
```

3.tag.jsp 引入jsp常用标签

```
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
```

在jsp目录下创建list.jsp文件用于测试Spring mvc项目的完成性

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <%--引入meta标签--%>
    <%@include file="common/meta.jsp" %>
    <title>用户列表</title>
    <%--引入jsp标签--%>
    <%@include file="common/tag.jsp" %>
    <%--引入css、js--%>
    <%@include file="common/head.jsp" %>
</head>
<body>
<table class="table table-bordered">
    <thead>
    <tr>
        <th>Id</th>
        <th>用户名</th>
        <th>创建时间</th>
        <th>修改时间</th>
    </tr>
    </thead>
    <tbody>
    <c:forEach var="user" items="${list}">
        <tr>
            <td>${user.id}</td>
            <td>${user.uname}</td>
            <td>
                <fmt:formatDate value="${user.createTime}" pattern="yyyy年MM月dd日 HH时mm分ss秒"/>
            </td>
            <td>
                <fmt:formatDate value="${user.modifyTime}" pattern="yyyy年MM月dd日 HH时mm分ss秒"/>
            </td>
        </tr>
    </c:forEach>
    </tbody>
</table>
</body>
</html>
```

## 五、logback使用详解

待补充

## 六、Redis使用详解 

待补充