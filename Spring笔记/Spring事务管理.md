# Spring 事务管理机制 

## 事务的概念和特性 

事务：一起成功、一起失败

> 什么是事务呢？ 

##### 事务指的是逻辑上的一组操作，这组操作要么全部成功，要么全部失败 

> 事务的特性：

##### 原子性、一致性、隔离性、持久性 

原子性：原子性是值事务是一个不可分割的工作单位，事务中的操作要么都发生，要么都不发生

一致性：一致性指事务前后数据的完整性必须保持一致

隔离性：隔离性是指多个用户并发访问数据库时，一个用户的事务不能被其他用户的事务所干扰，多个并发事务之间数据要相互隔离。

持久性：一个事务一旦被提交，它对数据库中数据的改变就是永久性的，即使数据库发生故障也不应该对其有任何影响。



#### 如果不考虑隔离性，会引发安全问题如下： 

脏读、不可重复读、幻读

脏读：一个事务读取了另一个事务改写但还未提交的数据，如果这些数据被回滚，则读到的数据是无效的。

不可重复读：在同一事务中，多次读取同一数据返回的结果有所不同。

幻读：一个事务读取了几行记录后，另一个事务插入一些记录，幻读就发生了，再后来的查询中，第一个数据就会发现有些原来没有的记录

## Spring接口介绍 

### Spring事务管理高层首相主要包括三个接口 

PlatformTransactionManager

平台事务管理器

TransactionDefinition

事务定义信息（隔离、传播、超时、只读）

TransactionStatus

事务具体运行状态

#### 平台事务管理器 

![https://shirukai.gitee.io/images/15094422425335962e81e000113e312800720.jpg](https://shirukai.gitee.io/images/15094422425335962e81e000113e312800720.jpg)

#### 事务的四种隔离级别

![https://shirukai.gitee.io/images/150944206092159f71a160001178612800720.jpg](https://shirukai.gitee.io/images/150944206092159f71a160001178612800720.jpg)

```
MySql默认的事务隔离级别为REPEATABLE_READ
Oracle默认的事务隔离级别为READ_COMMITTED
```

#### spring 事务的七种传播行为 

##### 什么是事务的传播行为？

![https://shirukai.gitee.io/images/150949928102259c31b1b000123d712800720.jpg](https://shirukai.gitee.io/images/150949928102259c31b1b000123d712800720.jpg)



##### 事务有哪些传播行为？

![https://shirukai.gitee.io/images/150944240857759eee1ff0001bb2c12800720.jpg](https://shirukai.gitee.io/images/150944240857759eee1ff0001bb2c12800720.jpg)



重点记第一个PROPAGATION_REQUIRED、第四个PROPAGATION_REQUIRES_NEW、和最后一个PROPAGATION_NESTED

### Spring事务管理 

Spring支持两种方式

##### 1.编程式的事务 

在实际应用中很少使用

通过TransactionTemplate手动管理事务

##### 2.使用xml配置声明式事务

开发中推荐使用（代码侵入性最小）

Spring的声明式事务是通过AOP实现的

## Spring事务管理的实现 

描述：在ssm环境下，以简单的转账案例，分别使用编程式事务管理、以及声明式事务管理来实现Spring事务管理。

#### 创建数据库表

```
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `money` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
INSERT INTO `account` VALUES ('1', 'aaa', '1000');
INSERT INTO `account` VALUES ('2', 'bbb', '1000');
INSERT INTO `account` VALUES ('3', 'ccc', '1000');
```

#### 编写AccountDaO层 

```
package com.mavenssmlr.dao;

import org.apache.ibatis.annotations.Param;

/**
 * 转账案例的Dao层的接口
 * Created by shirukai on 2017/11/1.
 */
public interface AccountDao {
    /**
     *
     * @param out   转出账号
     * @param money 转出金额
     */
    public void outMoney(@Param("out") String out,@Param("money") Double money);

    /**
     *
     * @param in    转入账号
     * @param money 转入金额
     */
    public void inMoney(@Param("in") String in,@Param("money") Double money);
}
```

#### 编写 AccountDaoMappper

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.mavenssmlr.dao.AccountDao">
    <update id="outMoney">
        UPDATE mavenssmlr.account SET money = money - #{money} WHERE name = #{out}
    </update>
    <update id="inMoney">
        UPDATE mavenssmlr.account SET money = money+ #{money} WHERE name = #{in}
    </update>
</mapper>
```

#### 编写Service接口 

```
/**
 * 转账案例的业务接口
 * @param out   转出的账号
 * @param in    转入的账号
 * @param money 转账金额
 */
Map<String,String> transfer(String out ,String in ,Double money);
```

#### 编写Service接口实现类 

```
public Map<String, String> transfer(String out, String in, Double money) {
    accountDao.outMoney(out, money);
    accountDao.inMoney(in, money);
    return null;
}
```

#### 编写service测试类 

```
@Test
public void accountTest()throws Exception{
    mavenssmlrService.transfer("aaa","bbb",200d);
}
```

以上基本的转账案例就写完了，但是没有加入事务管理。



### 一、基于编程式的事务管理 

Spring-service.xml 

##### 配置事务管理器

```
<!--配置事务管理器-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <!--注入数据库连接池-->
    <property name="dataSource" ref="dataSource"/>
</bean>

```

##### 配置事务管理模板

```
<!--配置事务管理的模板：Spring为了简化事务管理的代码而提供的类-->
<bean id="transactionTemplate" class="org.springframework.transaction.support.TransactionTemplate">
    <property name="transactionManager" ref="transactionManager"/>
</bean>
```

service实现类

##### 注入编程事务模板 

```
//注入编程式事务模板
@Autowired
private TransactionTemplate transactionTemplate;
```

##### 编程式事务方法 

```
public Map<String, String> transfer(final String out,final String in,final Double money) {
    transactionTemplate.execute(new TransactionCallbackWithoutResult() {
        @Override
        protected void doInTransactionWithoutResult(TransactionStatus status) {
            accountDao.outMoney(out, money);
            //制造异常
            int i = 1 / 0;
            accountDao.inMoney(in, money);
        }
    });
    return null;
}
```

##### 测试类 无需改动

```
@Test
public void accountTest()throws Exception{
    mavenssmlrService.transfer("aaa","bbb",200d);
}
```

### 二、基于声明式的事务管理



#### 1.基于TransactionProxy的声明式事务管理 

Spring-service.xml 

##### 配置事务管理器

```
<!--配置事务管理器-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <!--注入数据库连接池-->
    <property name="dataSource" ref="dataSource"/>
</bean>
```

##### 配置业务代理 

```
<!--配置业务代理：-->
<bean id="accountServiceProxy" class="org.springframework.transaction.interceptor.TransactionProxyFactoryBean">
    <!--配置目标对象-->
    <property name="target" ref="mavenssmlrServiceImpl"/>
    <!--注入事务管理器-->
    <property name="transactionManager" ref="transactionManager"/>
    <!--注入事务属性-->
    <property name="transactionAttributes">
        <props>
            <!--prop的格式
                    * PROPAGATION ：事务的传播行为
                    * ISOLATION   ：事务的隔离级别
                    * readOnly    ：只读
                    * -Exception  ：发生哪些异常回滚事务
                    * +Exception  ：发生哪些以上不回滚事务
            -->
            <prop key="transfer">PROPAGATION_REQUIRED</prop>
        </props>
    </property>
```

service实现类

```
public Map<String, String> transfer(String out, String in, Double money) {
    accountDao.outMoney(out, money);
    //制造异常
    int i = 1 / 0;
    accountDao.inMoney(in, money);
    return null;
}
```

##### 测试类 需要引入Service的增强类

```
@Resource(name = "accountServiceProxy")
private MavenssmlrService mavenssmlrService;

@Test
public void accountTest()throws Exception{
    mavenssmlrService.transfer("aaa","bbb",200d);
}
```



### 2.基于AspectJ的xml配置声明式事务（没有实现）



```

<!--配置事务管理器-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <!--注入数据库连接池-->
    <property name="dataSource" ref="dataSource"/>
</bean>


<!--2)配置事务的通知（事务的增强）-->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
    <tx:attributes>
        <!--
            propagation    :事务传播行为
            isolation  :事务的隔离级别
            read-only  :只读
            rollback-for:发生哪些异常回滚
            no-rollback-for    :发生哪些异常不回滚
            timeout       :过期信息
         -->
        <tx:method name="transfer" propagation="REQUIRED"/>
    </tx:attributes>
</tx:advice>

<!-- 配置切面 -->
<aop:config>
    <!-- 配置切入点 -->
    <aop:pointcut expression="execution(* com.mavenssmlr.service.MavenssmlrService+.*(..))" id="pointcut1"/>
    <!-- 配置切面 -->
    <aop:advisor advice-ref="txAdvice" pointcut-ref="pointcut1"/>
</aop:config>
```

### 3.基于注解的声明式事务 

Spring-service.xml 

```

<!--配置事务管理器-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <!--注入数据库连接池-->
    <property name="dataSource" ref="dataSource"/>
</bean>

<!--2配置基于注解的声明式事务-->
<tx:annotation-driven transaction-manager="transactionManager"/>
```

#### 在方法上添加@Transactional 

```
/**
 * 
 * @param out   转出的账号
 * @param in    转入的账号
 * @param money 转账金额
 * @return
 * 
 * Transactional注解中的属性
 * propagation：事务的传播行为
 * isolation：隔离基本
 * readOnly：只读信息
 * rollbackFor：发生哪些异常回滚
 * noRollbackFor：发生哪些异常不回滚
 */
@Transactional(propagation = Propagation.REQUIRED,isolation = Isolation.DEFAULT,readOnly = false)
public Map<String, String> transfer(String out, String in, Double money) {
    accountDao.outMoney(out, money);
    //制造异常
    int i = 1 / 0;
    accountDao.inMoney(in, money);
    return null;
}
```

## 总结：

Spring将事务管理分成了两类

* 编程式事务管理

  手动编写代码进行事务管理（很少使用）

* 声明式事务管理

  基于TransactionProxyFactoryBean（很少使用）

  基于AspectJ的XMl方式

  基于注解方式（经常使用）

  ​