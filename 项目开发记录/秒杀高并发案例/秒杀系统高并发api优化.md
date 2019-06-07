# 秒杀系统高并发api优化

## 为什么要单独获取系统时间？

用户大量刷新页面，用户访问的静态资源、css、js都部署在CDN上，用户访问时，是不会访问到我们的服务器上的，所以，这个时候的时间是不可控的也不是同步的。所以我们需要一个统一的api来，来获取系统服务器上的一致性的时间。

### CDN的理解： 

CDN（内容分发网络）加速用户获取数据的系统

部署在离用户最近的网络节点上

命中CDN不需要访问后端服务器

互联网公司自己搭建或者租用

## 秒杀地址接口分析

无法使用CDN缓存，适合服务器端缓存：redis等，一致性维护成文低

### 秒杀地址接口优化

请求地址 访问 redis 如果没有在访问mysql，

redis和mysql一致性维护，当redis超时，可以做超时穿透到mysql更新数据。当mysql更新数据之后，可以主动更新我们的redis

## 秒杀操作的优化分析 

无法使用CDN缓存

后端缓存困难：库存问题

一行数据竞争：热点商品



## 其他方案分析

![Screenshot_2017-10-17-10-30-55-186_cn.com.open.mo](C:/Users/shirukai/Desktop/img/Screenshot_2017-10-17-10-30-55-186_cn.com.open.mo.png)

### 成本分析

运维成本和稳定型：NoSQL，MQ等

开发成本：数据一致性，回滚方案等

幂等性难以保证：重复秒杀问题

不适合新手的架构



## 为什么不用mysql解决 

mysql真的低效吗?一秒钟（4万）



## 瓶颈分析 

延迟



## redis缓存优化

使用redis优化地址暴露接口

###  windows下安装redis-3.2

下载redis-3.2.zip 

https://github.com/MicrosoftArchive/redis/releases

解压文件

然后运行：.\redis-server.exe

#### 与java结合

配置pom.xml

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
```

在dao包下创建cache包然后新建RedisDao.java文件

```
package org.seckill.dao.cache;

import com.dyuproject.protostuff.LinkedBuffer;
import com.dyuproject.protostuff.ProtostuffIOUtil;
import com.dyuproject.protostuff.runtime.RuntimeSchema;
import org.seckill.entity.Seckill;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

/**
 * Created by shirukai on 2017/10/17.
 */
public class RedisDao {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());
    private JedisPool jedisPool;

    public RedisDao(String ip, int port) {
        jedisPool = new JedisPool(ip, port);
    }

    private RuntimeSchema<Seckill> schema = RuntimeSchema.createFrom(Seckill.class);

    public Seckill getSeckill(long sekillId) {
        //redis操作逻辑
        try {
            Jedis jedis = jedisPool.getResource();
            try {
                String key = "seckill" + sekillId;
                //并没有实现内部序列化操作
                //get -> byte[] -->反序列化 -> Object(seckill)
                //采用自定义序列化
                //protostuff:pojo.(标准的具有get、set方法的对象)
                byte[] bytes = jedis.get(key.getBytes());
                //缓存获取到
                if (bytes != null) {
                    //空对象
                    Seckill seckill = schema.newMessage();
                    ProtostuffIOUtil.mergeFrom(bytes, seckill, schema);
                    //seckill 被反序列化
                    return seckill;
                }
            } finally {
                jedis.close();
            }

        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        return null;
    }

    public String putSeckill(Seckill seckill) {
        //set Object（seckill）->序列化-> byte[]
        try {
            Jedis jedis = jedisPool.getResource();
            try {
                String key = "seckill" + seckill.getSeckillId();
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

配置spirng-dao.xml

```
<!--RedisDao-->
<bean id="redisDao" class="org.seckill.dao.cache.RedisDao">
    <constructor-arg index="0" value="localhost"/>
    <constructor-arg index="1" value="6379"/>
</bean>
```

修改service层

```
//缓存优化:超时的基础上维护一致性
//从缓存中查找数据
Seckill seckill = redisDao.getSeckill(seckillId);
if (seckill == null){
    //如果缓存中没有查找数据库
    seckill = seckillDao.queryById(seckillId);
    if (seckill == null){
        return new Exposer(false,seckillId);
    }else {
        //将查找数据写入缓存
        redisDao.putSeckill(seckill);
    }
}
```

### 并发优化

调整减库存和插入购买明细的顺序，减低rowlock的持有时间



### 深度优化 

事务sql在mysql端执行(存储过程)



```
-- 秒杀执行的存储过程
DELIMITER $$ -- console ;转换为
-- 定义存储过程
-- 参数： in 输入参数；out 输出参数
-- row_count() 返回上一条修改类型sql（delete，insert，update）的影响行数
-- row_count : 0 未修改函数 >0：修改的行数 <0 sql错误或者未执行
CREATE PROCEDURE `seckill`.`excute_seckill`
  (IN v_seckill_id BIGINT, IN v_phone BIGINT,
   IN v_kill_time  TIMESTAMP, OUT r_result INT)
  BEGIN
    DECLARE insert_count INT DEFAULT 0;
    START TRANSACTION;
    INSERT IGNORE INTO seckill.success_killed (seckill_id, user_phone, create_time)
    VALUES (v_seckill_id, v_phone, v_kill_time);
    SELECT row_count()
    INTO insert_count;
    IF (insert_count < 0)
    THEN
      ROLLBACK;
      SET r_result = -1;
    ELSE IF (insert_count < 0)
    THEN
      ROLLBACK;
      SET r_result = -2;
    ELSE
      UPDATE seckill.seckill
      SET number = number - 1
      WHERE seckill_id = v_seckill_id
            AND end_time > v_kill_time
            AND start_time < v_kill_time
            AND number > 0;
      SELECT row_count()
      INTO insert_count;
      IF (insert_count = 0)
      THEN
        ROLLBACK;
        SET r_result = 0;
      ELSEIF (insert_count < 0)
        THEN
          ROLLBACK;
          SET r_result = -2;
      ELSE
        COMMIT;
        SET r_result = 1;
      END IF;
    END IF;
    END IF;
  END;
$$

SET @r_result = -3;
-- 执行存储过程
CALL excute_seckill(1003,15552211520,now(),@r_result);

-- 获取结果
SELECT @r_result;
```

