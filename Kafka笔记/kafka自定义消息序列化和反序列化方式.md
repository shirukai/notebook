# kafka自定义消息序列化和反序列化方式

> 版本说明：

kafka版本：[kafka_2.12-2.0.0.tgz](https://www.apache.org/dyn/closer.cgi?path=/kafka/2.0.0/kafka_2.12-2.0.0.tgz)

pom依赖：

```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>2.0.0</version>
</dependency>
```



## 1 关于kafka的序列化和反序列化

kafka在发送和接受消息的时候，都是以byte[]字节型数组发送或者接受的。但是我们平常使用的时候，不但可以使用byte[]，还可以使用int、short、long、float、double、String等数据类型，这是因为在我们使用这些数据类型的时候，kafka根据我们指定的序列化和反序列化方式转成byte[]类型之后再进行发送或者接受的。

通常我们在使用kakfa发送或者接受消息的时候都需要指定消息的key和value序列化方式，如设置value.serializer为org.apache.kafka.common.serialization.StringSerializer，设置value的序列化方式为字符串，即我们可以发送string类型的消息。目前kafka原生支持的序列化和反序列化方式如下两表所示：

1.1kafka序列化方式表

| 序列化方式                                                 | 对应java数据类型 | 说明                                                         |
| ---------------------------------------------------------- | ---------------- | ------------------------------------------------------------ |
| org.apache.kafka.common.serialization.ByteArraySerializer  | byte[]           | 原生类型                                                     |
| org.apache.kafka.common.serialization.ByteBufferSerializer | ByteBuffer       | [关于ByteBuffer](https://blog.csdn.net/workformywork/article/details/26699345?utm_source=tuicool&utm_medium=referral) |
| org.apache.kafka.common.serialization.IntegerSerializer    | Interger         |                                                              |
| org.apache.kafka.common.serialization.ShortSerializer      | Short            |                                                              |
| org.apache.kafka.common.serialization.LongSerializer       | Long             |                                                              |
| org.apache.kafka.common.serialization.DoubleSerializer     | Double           |                                                              |
| org.apache.kafka.common.serialization.StringSerializer     | String           |                                                              |

1.2kafka反序列化方式表

| 序列化方式                                                   | 对应java数据类型 | 说明                                                         |
| ------------------------------------------------------------ | ---------------- | ------------------------------------------------------------ |
| org.apache.kafka.common.serialization.ByteArrayDeserializer  | byte[]           | 原生类型                                                     |
| org.apache.kafka.common.serialization.ByteBufferDeserializer | ByteBuffer       | [关于ByteBuffer](https://blog.csdn.net/workformywork/article/details/26699345?utm_source=tuicool&utm_medium=referral) |
| org.apache.kafka.common.serialization.IntegerDeserializer    | Interger         |                                                              |
| org.apache.kafka.common.serialization.ShortDeserializer      | Short            |                                                              |
| org.apache.kafka.common.serialization.LongDeserializer       | Long             |                                                              |
| org.apache.kafka.common.serialization.DoubleDeserializer     | Double           |                                                              |
| org.apache.kafka.common.serialization.StringDeserializer     | String           |                                                              |

## 2 kafka原生序列化和反序列化方式的实现

上面我们了解一些关于kafka原生的一些序列化和反序列化方式。它们究竟是如何实现的呢？以string类型为例子，我们看一下，kafka如何实现序列化/反序列化的。

kafka序列化/反序列化方式的实现代码在org.apache.kafka.common.serialization包下。

### 2.1 String 序列化

我们查看org.apache.kafka.common.serialization.StringSerializer这个类。

```java
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.kafka.common.serialization;

import org.apache.kafka.common.errors.SerializationException;

import java.io.UnsupportedEncodingException;
import java.util.Map;

/**
 *  String encoding defaults to UTF8 and can be customized by setting the property key.serializer.encoding,
 *  value.serializer.encoding or serializer.encoding. The first two take precedence over the last.
 */
public class StringSerializer implements Serializer<String> {
    private String encoding = "UTF8";

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
        String propertyName = isKey ? "key.serializer.encoding" : "value.serializer.encoding";
        Object encodingValue = configs.get(propertyName);
        if (encodingValue == null)
            encodingValue = configs.get("serializer.encoding");
        if (encodingValue instanceof String)
            encoding = (String) encodingValue;
    }

    @Override
    public byte[] serialize(String topic, String data) {
        try {
            if (data == null)
                return null;
            else
                return data.getBytes(encoding);
        } catch (UnsupportedEncodingException e) {
            throw new SerializationException("Error when serializing string to byte[] due to unsupported encoding " + encoding);
        }
    }

    @Override
    public void close() {
        // nothing to do
    }
}
```

由上面的代码我们可以看出，String的序列化类是继承了Serializer接口，指定`<String>`泛型，然后实现的Serializer接口的configure()、serialize()、close()方法。代码重点的实现是在serialize()，可以看出这个方法将我们传入的String类型的数据，简单的通过data.getBytes()方法进行了序列化。

### 2.1 String 反序列化

我们查看org.apache.kafka.common.serialization.StringDeserializer这个类。

```java
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.kafka.common.serialization;

import org.apache.kafka.common.errors.SerializationException;

import java.io.UnsupportedEncodingException;
import java.util.Map;

/**
 *  String encoding defaults to UTF8 and can be customized by setting the property key.deserializer.encoding,
 *  value.deserializer.encoding or deserializer.encoding. The first two take precedence over the last.
 */
public class StringDeserializer implements Deserializer<String> {
    private String encoding = "UTF8";

    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {
        String propertyName = isKey ? "key.deserializer.encoding" : "value.deserializer.encoding";
        Object encodingValue = configs.get(propertyName);
        if (encodingValue == null)
            encodingValue = configs.get("deserializer.encoding");
        if (encodingValue instanceof String)
            encoding = (String) encodingValue;
    }

    @Override
    public String deserialize(String topic, byte[] data) {
        try {
            if (data == null)
                return null;
            else
                return new String(data, encoding);
        } catch (UnsupportedEncodingException e) {
            throw new SerializationException("Error when deserializing byte[] to string due to unsupported encoding " + encoding);
        }
    }

    @Override
    public void close() {
        // nothing to do
    }
}
```

同样，由上面的代码我们可以看出，String的反序列化类是继承了Deserializer接口，指定`<String>`泛型，然后实现的Deserializer接口的configure()、deserialize()、close()方法。代码重点的实现是在deserialize()，可以看出这个方法将我们传入的byte[]类型的数据，简单的通过return new String(data, encoding)方法进行了反序列化得到了String类型的数据。

## 3 kafka自定义序列化/反序列化方式

通过上面，我们对kafka原生序列化/反序列化方式的了解，我们可以看出，kafka实现序列化/反序列化可以简单的总结为两步，第一步继承序列化Serializer或者反序列化Deserializer接口。第二步实现接口方法，将指定类型序列化成byte[]或者将byte[]反序列化成指定数据类型。所以接下来，我们来实现自己的序列化/反序列化方式。

这里我们介绍两种序列化方式一种是fastjson另一种是protostuff

### 3.1 基于fastjson的序列化/反序列化的实现

例如我们有一个Person实体类，我们需要将User利用fastjson进行序列化/反序列化操作之后，在kafka上发送接收消息。

#### 3.1.1 Person.java

```java
package com.springboot.demo.kafka.entity;

/**
 * Created by shirukai on 2018/8/25
 */
public class Person {
    private int id;
    private String name;
    private int age;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
}

```

#### 3.1.2 序列化实现PersonJsonSerializer.java

```java
package com.springboot.demo.kafka.serialization;

import com.alibaba.fastjson.JSON;
import com.springboot.demo.kafka.entity.Person;
import org.apache.kafka.common.serialization.Serializer;

import java.util.Map;

/**
 * Created by shirukai on 2018/8/25
 */
public class PersonJsonSerializer implements Serializer<Person> {
    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {

    }

    @Override
    public byte[] serialize(String topic, Person data) {
        return JSON.toJSONBytes(data);
    }

    @Override
    public void close() {

    }
}
```

#### 3.1.3 反列化实现PersonJsonDeserializer.java

```java
package com.springboot.demo.kafka.serialization;

import com.alibaba.fastjson.JSON;
import com.springboot.demo.kafka.entity.Person;
import org.apache.kafka.common.serialization.Deserializer;

import java.util.Map;

/**
 * Created by shirukai on 2018/8/25
 */
public class PersonJsonDeserializer implements Deserializer<Person> {
    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {

    }

    @Override
    public Person deserialize(String topic, byte[] data) {
        return JSON.parseObject(data, Person.class);
    }

    @Override
    public void close() {

    }
}
```

#### 3.1.4 kafka测试

##### 3.1.4.1 发送消息

```java
    @Test
    public void producerJson() {
        Properties props = new Properties();
        //kakfa 服务
        props.put("bootstrap.servers", "localhost:9092");
        //leader 需要等待所有备份都成功写入日志
        props.put("acks", "all");
        //重试次数
        props.put("retries", 0);
        props.put("batch.size", 16384);
        props.put("linger.ms", 1);
        props.put("buffer.memory", 33554432);
        //key的序列化方式
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        //value的序列化方式
        props.put("value.serializer", "com.springboot.demo.kafka.serialization.PersonJsonSerializer");
        Producer<String, Person> producer = new KafkaProducer<>(props);
        Person person = new Person();
        for (int i = 0; i < 100; i++) {
            System.out.println(i);
            person.setId(i);
            person.setName("personJsonSerialization_" + i);
            person.setAge(18);
            producer.send(new ProducerRecord<>("personJsonSerialization", "client" + i, person));
        }
        producer.close();
    }
```

##### 3.1.4.2 接收消息

```java
@Test
public void consumerJson() {
    Properties props = new Properties();
    props.put("bootstrap.servers", "localhost:9092");
    //五位数
    props.put("group.id", "123456");
    props.put("enable.auto.commit", "false");
    props.put("auto.offset.reset", "earliest");
    props.put("auto.commit.interval.ms", "1000");

    props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
    props.put("value.deserializer", "com.springboot.demo.kafka.serialization.PersonJsonDeserializer");
    KafkaConsumer<String, Person> consumer = new KafkaConsumer<>(props);
    consumer.subscribe(Arrays.asList("personJsonSerialization"));

    ConsumerRecords<String, Person> records = consumer.poll(Duration.ofMillis(1000));
    System.out.println(records.count());
    for (ConsumerRecord<String, Person> record : records) {
        System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
    }
}
```

### 3.2 基于protostuff的序列化/反序列化的实现

#### 3.2.1 ProtostuffUtil.java 工具类

```java
package com.springboot.demo.utils;

import com.dyuproject.protostuff.LinkedBuffer;
import com.dyuproject.protostuff.ProtostuffIOUtil;
import com.dyuproject.protostuff.Schema;
import com.dyuproject.protostuff.runtime.RuntimeSchema;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Created by shirukai on 2018/8/14
 * protostuff 序列化/反序列化工具类
 */
public class ProtostuffUtil {
    private static Map<Class<?>, Schema<?>> cachedSchema = new ConcurrentHashMap<>();

    /**
     * 序列化
     *
     * @param message 序列化数据
     * @param tClass  .class
     * @param <T>     类型
     * @return byte[]
     */
    public static <T> byte[] serializer(T message, Class<T> tClass) {
        Schema<T> schema = getSchema(tClass);
        return ProtostuffIOUtil.toByteArray(message, schema, LinkedBuffer.allocate(LinkedBuffer.DEFAULT_BUFFER_SIZE));
    }

    /**
     * 反序列化
     *
     * @param bytes  bytes
     * @param tClass .class
     * @param <T>    类型
     * @return T
     */
    public static <T> T deserializer(byte[] bytes, Class<T> tClass) {
        Schema<T> schema = getSchema(tClass);
        T message = schema.newMessage();
        ProtostuffIOUtil.mergeFrom(bytes, message, schema);
        return message;
    }

    private static <T> Schema<T> getSchema(Class<T> tClass) {
        Schema<T> schema = (Schema<T>) cachedSchema.get(tClass);
        if (schema == null) {
            schema = RuntimeSchema.createFrom(tClass);
            cachedSchema.put(tClass, schema);
        }
        return schema;
    }
}
```

#### 3.2.2 序列化实现PersonProtostuffSerializer.java

```java
package com.springboot.demo.kafka.serialization;

import com.springboot.demo.kafka.entity.Person;
import com.springboot.demo.utils.ProtostuffUtil;
import org.apache.kafka.common.serialization.Serializer;

import java.util.Map;

/**
 * Created by shirukai on 2018/8/25
 */
public class PersonProtostuffSerializer implements Serializer<Person> {
    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {

    }

    @Override
    public byte[] serialize(String topic, Person data) {
        return ProtostuffUtil.serializer(data, Person.class);
    }

    @Override
    public void close() {

    }
}
```

#### 3.2.3 反序列化实现PersonProtostuffDeserializer.java

```java
package com.springboot.demo.kafka.serialization;

import com.springboot.demo.kafka.entity.Person;
import com.springboot.demo.utils.ProtostuffUtil;
import org.apache.kafka.common.serialization.Deserializer;

import java.util.Map;

/**
 * Created by shirukai on 2018/8/25
 */
public class PersonProtostuffDeserializer implements Deserializer<Person> {
    @Override
    public void configure(Map<String, ?> configs, boolean isKey) {

    }

    @Override
    public Person deserialize(String topic, byte[] data) {
        return ProtostuffUtil.deserializer(data, Person.class);
    }

    @Override
    public void close() {

    }
}
```

#### 3.2.4 kafka测试

##### 3.2.4.1 发送消息

```java
@Test
public void producerProtostuff(){
    Properties props = new Properties();
    //kakfa 服务
    props.put("bootstrap.servers", "localhost:9092");
    //leader 需要等待所有备份都成功写入日志
    props.put("acks", "all");
    //重试次数
    props.put("retries", 0);
    props.put("batch.size", 16384);
    props.put("linger.ms", 1);
    props.put("buffer.memory", 33554432);
    //key的序列化方式
    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
    //value的序列化方式
    props.put("value.serializer", "com.springboot.demo.kafka.serialization.PersonProtostuffSerializer");
    Producer<String, Person> producer = new KafkaProducer<>(props);
    Person person = new Person();
    for (int i = 0; i < 100; i++) {
        System.out.println(i);
        person.setId(i);
        person.setName("personJsonSerialization_" + i);
        person.setAge(18);
        producer.send(new ProducerRecord<>("personProtostuffSerialization", "client" + i, person));
    }
    producer.close();
}
```

##### 3.2.4.2 接收消息

```java
@Test
public void consumerProtostuff(){
    Properties props = new Properties();
    props.put("bootstrap.servers", "localhost:9092");
    //五位数
    props.put("group.id", "123456");
    props.put("enable.auto.commit", "false");
    props.put("auto.offset.reset", "earliest");
    props.put("auto.commit.interval.ms", "1000");

    props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
    props.put("value.deserializer", "com.springboot.demo.kafka.serialization.PersonProtostuffDeserializer");
    KafkaConsumer<String, Person> consumer = new KafkaConsumer<>(props);
    consumer.subscribe(Arrays.asList("personProtostuffSerialization"));

    ConsumerRecords<String, Person> records = consumer.poll(Duration.ofMillis(1000));
    System.out.println(records.count());
    for (ConsumerRecord<String, Person> record : records) {
        System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
    }
}
```

## 4 总结

序列化方式还有好多种，关于采用什么样的方式去序列化数据还需要根据业务场景自己去定义。这里记录一下关于使用Protostuff的时候遇到的问题，当序列化Object data这样的数据的时候，protostuff在创建RuntimeSchema的时候会报空指针异常。查看源码是因为Object.class.getSuperclass()为null，这时候会抛出空指针异常