# Redis的安装以及与java结合使用 

## Redis简介：

Redis本质上是一个Key-Value类型的内存数据库，很像memcached，整个数据库统统加载在内存当中进行操作，定期通过异步操作把数据库数据flush到硬盘上进行保存。因为是纯内存操作，Redis的性能非常出色，Redis最大的魅力是支持保存List链表和Set集合的数据结构，而且还支持对List进行各种操作，例如从List两端push和pop数据，取 List区间，排序等等，对Set支持各种集合的并集交集操作，此外单个value的最大限制是1GB，不像memcached只能保存1MB的数据，Redis可以用来实现很多有用的功能，比方说用他的List来做FIFO双向链表，实现一个轻量级的高性能消息队列服务，用他的Set可以做高性能的tag系统等等。另外Redis也可以对存入的Key-Value设置expire时间，因此也可以被当作一个功能加强版的memcached来用。 

## Redis在windos下安装：

### 1.下载 （官网不支持windos下载，所以这里提供百度云）

百度云分享地址：链接：http://pan.baidu.com/s/1dFq4ETb 密码：8y5g

下载后解压到指定目录，我解压到了：C:\Program Files\Redis-x64-3.2.100

### 2.配置环境变量 

将C:\Program Files\Redis-x64-3.2.100添加到环境变量里即可。

### 3.配置文件

配置参考：http://www.runoob.com/redis/redis-conf.html

配置参考博客：http://cardyn.iteye.com/blog/794194

### 4.运行 

在cmd命令行运行 redis-server.exe即可运行服务



## Redis在linux下安装： 

### 1.下载(官网直接下载即可) 

官网地址：https://redis.io/download

下载后利用shell文件管理工具将下载后的文件复制到linux里

### 2.解压：

```
tar -xzvf redis-4.0.2.tar.gz 
```

### 3.编译安装 

进入解压后的目录

```
cd redis-4.0.2
```

编译安装

```
make
```

make完后 redis-4.0.2目录下会出现编译后的redis服务程序redis-server,还有用于测试的客户端程序redis-cli,两个程序位于安装目录 src 目录下。

配置环境变量

```
vi  /etc/profile
```

添加如下内容：

```
export PATH=$PATH:/root/redis-4.0.2/src
```

修改配置文件 redis.conf

修改绑定ip以及将protected-mode yes设置为no才可以远程访问，启动的时候带着配置文件一起启动即可。

如：

./redis-server ../ redis.conf

### 4.运行 

输入redis-server.exe即可运行

## mave项目中配置相关依赖 

在pom.xml文件中添加相关依赖

```
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
```

## Redis与Springmvc项目整合



### 利用spring-data-redisr进行整合 

#### 配置依赖：

```
<dependency>
  <groupId>org.springframework.data</groupId>
  <artifactId>spring-data-commons</artifactId>
  <version>1.8.4.RELEASE</version>
</dependency>
<!--spring-data-redisr-->
<dependency>
  <groupId>org.springframework.data</groupId>
  <artifactId>spring-data-redis</artifactId>
  <version>1.8.4.RELEASE</version>
</dependency>
<dependency>
<!--redis客户端 jedis-->
  <groupId>redis.clients</groupId>
  <artifactId>jedis</artifactId>
  <version>2.9.0</version>
</dependency>
```

在resources/spring下新建spring-redis.xml

```
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context" xmlns:p="http://www.springframework.org/schema/p"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                    http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
                    http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd">
    <!--redis配置-->
    <context:property-placeholder location="classpath:redis.properties" ignore-unresolvable="true"/>
    <!-- 1:pool的配置 -->
    <bean id="poolConfig" class="redis.clients.jedis.JedisPoolConfig">
        <property name="maxIdle" value=" ${redis.maxIdle}"/>
        <property name="maxTotal" value="${redis.maxTotal}"/>
        <property name="maxWaitMillis" value="${redis.maxWaitMillis}"/>
        <property name="testOnBorrow" value="${redis.testOnBorrow}"/>
    </bean>
    <!--2:创建连接工厂-->
    <bean id="jedisConnectionFactory" class="org.springframework.data.redis.connection.jedis.JedisConnectionFactory"
          p:host-name="${redis.host}"
          p:port="${redis.port}"
          p:password="${redis.pass}"
          p:pool-config-ref="poolConfig"/>
    <!--3:连接实例-->
    <bean id="redisTemplate" class="org.springframework.data.redis.core.RedisTemplate"
          p:connection-factory-ref="jedisConnectionFactory">
        <!-- 序列化方式 建议key/hashKey采用StringRedisSerializer。 -->
        <property name="keySerializer">
            <bean class="org.springframework.data.redis.serializer.StringRedisSerializer"/>
        </property>
        <property name="hashKeySerializer">
            <bean class="org.springframework.data.redis.serializer.StringRedisSerializer"/>
        </property>
        <property name="valueSerializer">
            <bean class="org.springframework.data.redis.serializer.JdkSerializationRedisSerializer"/>
        </property>
        <property name="hashValueSerializer">
            <bean class="org.springframework.data.redis.serializer.JdkSerializationRedisSerializer"/>
        </property>
    </bean>
    <!-- 对string操作的封装 -->
    <bean id="stringRedisTemplate" class="org.springframework.data.redis.core.StringRedisTemplate"
          p:connection-factory-ref="jedisConnectionFactory"/>
    <bean id="redisDao" class="com.mavenssmlr.dao.redis.RedisDao"/>
</beans>
```

在resources下新建redis.properties配置文件

```
redis.host=127.0.0.1
redis.port=6379
redis.pass=

redis.maxIdle=300
redis.maxTotal=600
redis.maxWaitMillis=1000
redis.testOnBorrow=true
```

注意：    <context:property-placeholder location="classpath:redis.properties" ignore-unresolvable="true"/>当配置文件中有多个这样的配置时，应该在每一个后面都加上 ignore-unresolvable="true"否则会报错。

在dao层新新建redis包，然后新建RedisDao类

```
package com.mavenssmlr.dao.redis;

import com.mavenssmlr.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

public class RedisDao{
    @Autowired
    private RedisTemplate<String,User> redisTemplate;
    public void save(User user){
        ValueOperations<String,User> valueOperations = redisTemplate.opsForValue();
        valueOperations.set(String.valueOf(user.getId()),user);
    }
    public User get(String id){
        ValueOperations<String,User> valueOperations = redisTemplate.opsForValue();
        return valueOperations.get(id);
    }
}
```

测试：

```
package com.mavenssmlr.dao;

import com.mavenssmlr.dao.redis.RedisDao;
import com.mavenssmlr.entity.User;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
//告诉junit spring配置文件
@ContextConfiguration({"classpath:spring/spring-dao.xml","classpath:spring/spring-redis.xml"})
public class RedisDaoTest {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    @Autowired
    private UserDao userDao;
    @Autowired
    private RedisDao redisDao;
    @Test
    public void save() throws Exception {
        User user = userDao.queryById(2);
        redisDao.save(user);
    }
    @Test
    public void get() throws Exception {
        User user = redisDao.get("2");
        logger.info("_______________________________user={}",user);
    }

}
```

RedisTemplate主要支持String，List，Hash，Set，ZSet这几种方式的参数，其对应的方法分别是opsForValue()、opsForList()、opsForHash()、opsForSet()、opsForZSet()。

### opsForValue()方法的使用：

```
    ValueOperations<String,String> valueOperations = redisTemplate.opsForValue();
    //1.set(key,value)
    //新增一个字符串类型的值
    valueOperations.set("string","这是一个字符串");
    //2.get(key)
    //根据key获取值
    String string = valueOperations.get("string");
    logger.info("string_____________________________={}",string);
    //3.append(key,value)
    //在原有的值基础上新增字符串到末尾
    valueOperations.append("string","哈哈我是新增的字符串");
    logger.info("__________________stringAppend={}",valueOperations.get("string"));
    //4.get(key,long start,long end)
    //截取key键对应值得字符串，从开始下标位置开始到结束下标的位置(包含结束下标)的字符串。
    String cutString = valueOperations.get("string",0,10);
    logger.info("__________________cutString={}",cutString);
    //5.getAndSet(key,value)
    //获取原来的值然后重新复制
    String oldValueAndNewSet = valueOperations.getAndSet("string","哼，你被我重新赋值啦！");
    logger.info("__________________oldValueAndNewSet={}",oldValueAndNewSet);
    logger.info("__________________newValue={}",valueOperations.get("string"));
    //6.size(key)
    //获取长度
    logger.info("__________________length={}",valueOperations.size("string"));
    //7.setIfAbsent(key,value)
    //如果键不存在则新增，存在则不改变已经有的值
    //返回false说明已经存在
    logger.info("___________________setIfAbsentResult={}",valueOperations.setIfAbsent("string","1111"));
    //8.set(K key, V value, long timeout, TimeUnit unit)
    //设置变量过期时间
    valueOperations.set("stringTime","timeOut",5, TimeUnit.SECONDS);
    logger.info("_________________getTimeValue__获取没有过期的值={}",valueOperations.get("stringTime"));
    Thread.sleep(5*1000);
    logger.info("_________________getTimeOutValue__获取过期后的值={}",valueOperations.get("stringTime"));
    //9.multiSet(Map<? extends K,? extends V> map)
    //设置map集合到redis
    Map<String,String> valueMap = new HashMap<String, String>();
    valueMap.put("mapKey1","mapValue1");
    valueMap.put("mapKey2","mapKey2");
    valueMap.put("mapKey3","mapKey3");
    valueOperations.multiSet(valueMap);
    //10.multiGet(Collection<K> keys)
    List<String> list = new ArrayList<String>();
    for (String key: valueMap.keySet()
         ) {
        list.add(key);
    }
    List<String> valueList = valueOperations.multiGet(list);
    logger.info("_____________valueList={}",valueList);
}
```

关于 redisTemplate集合的使用 参考：

简介：http://www.bijishequ.com/detail/442744?p=

opsForValue()：http://www.bijishequ.com/detail/443107?p=

opsForList(): http://www.bijishequ.com/detail/443086?p=

opsForHash(): http://www.bijishequ.com/detail/443483?p=

opsForSet(): http://www.bijishequ.com/detail/443818?p=

opsForZSet(): http://www.bijishequ.com/detail/444106?p=



### 利用jedis原生客户端进行整合 

依赖：

```
<dependency>
  <groupId>redis.clients</groupId>
  <artifactId>jedis</artifactId>
  <version>2.9.0</version>
</dependency>
```

在spring-redis.xml文件中配置：

```
    <!--原生RedisDao-->
    <bean id="redisDao1" class="com.mavenssmlr.dao.cache.RedisDao">
        <constructor-arg index="0" value="localhost"/>
        <constructor-arg index="1" value="6379"/>
    </bean>
```

在 com.mavenssmlr.entirty.cache下创建RedisDao类

```
package com.mavenssmlr.dao.cache;

import com.dyuproject.protostuff.LinkedBuffer;
import com.dyuproject.protostuff.ProtostuffIOUtil;
import com.dyuproject.protostuff.runtime.RuntimeSchema;
import com.mavenssmlr.entity.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;


public class RedisDao {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());
    private JedisPool jedisPool;

    public RedisDao(String ip, int port) {
        jedisPool = new JedisPool(ip, port);
    }

    private RuntimeSchema<User> schema = RuntimeSchema.createFrom(User.class);
    public User getUser(long userId) {
        //redis操作逻辑
        try {
            Jedis jedis = jedisPool.getResource();
            try {
                String key = "user" + userId;
                //并没有实现内部序列化操作
                //get -> byte[] -->反序列化 -> Object(User)
                //采用自定义序列化
                //protostuff:pojo.(标准的具有get、set方法的对象)
                byte[] bytes = jedis.get(key.getBytes());
                //缓存获取到
                if (bytes != null) {
                    //空对象
                    User user = schema.newMessage();
                    ProtostuffIOUtil.mergeFrom(bytes, user, schema);
                    //user 被反序列化
                    return user;
                }
            } finally {
                jedis.close();
            }

        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        return null;
    }

    public String setUser(User seckill) {
        //set Object（seckill）->序列化-> byte[]
        try {
            Jedis jedis = jedisPool.getResource();
            try {
                String key = "user" + seckill.getId();
                byte[] bytes = ProtostuffIOUtil.toByteArray(seckill, schema,
                        LinkedBuffer.allocate(LinkedBuffer.DEFAULT_BUFFER_SIZE));
                //超时缓存
                int timeout = 60 * 60; //一小时
                String result = jedis.setex(key.getBytes(),timeout,bytes);
                return result;
            } finally {
                jedis.close();
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        return null;
    }

}

```

测试：

```
package org.seckill.dao.cache;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.seckill.dao.SeckillDao;
import org.seckill.entity.Seckill;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static org.junit.Assert.*;

@RunWith(SpringJUnit4ClassRunner.class)
//告诉junit spring配置文件
@ContextConfiguration({"classpath:spring/spring-dao.xml"})
public class RedisDaoTest {
    private  long id = 1001;
    @Autowired
    private RedisDao redisDao;
    @Autowired
    private SeckillDao seckillDao;
    @Test
    public void testRedisDao()throws Exception{
        //get and put
        Seckill seckill = redisDao.getSeckill(id);
        if (seckill == null){
            seckill = seckillDao.queryById(id);
            if (seckill != null){
               String result = redisDao.putSeckill(seckill);
               System.out.println(result);
               seckill = redisDao.getSeckill(id);
               System.out.println(seckill);
            }
        }
        System.out.println(seckill);
    }
}
```

java对redis的基本操作

参考文献：http://www.cnblogs.com/edisonfeng/p/3571870.html