# 《Spark内核设计的艺术架构与实战》读书笔记

## 1 新名字及概念

### 1.1 Socket

https://www.cnblogs.com/yiwangzhibujian/p/7107785.html

### 1.2 RPC框架

https://blog.csdn.net/kingcat666/article/details/78577079

https://www.jianshu.com/p/5b90a4e70783

### 1.3 NIO

https://www.jianshu.com/p/0d497fe5484a

https://blog.csdn.net/u011381576/article/details/79876754

### 1.4 Netty

https://www.jianshu.com/p/b9f3f6a16911

### 1.5 Tungsten

### 1.5 EPOLL

## 1 编程思想及语法

### 1.1 java、scala读取配置和环境变量

#### 1.1.1 java读取配置和环境变量

```scala
 //java读取系统配置，并转为scala map
    val properties = System.getProperties.stringPropertyNames().asScala
      .map(key => (key, System.getProperty(key)))
    //筛选 java.*的配置
    for ((key, value) <- properties if key.startsWith("java.")) {
      println(key, value)
    }
    //java获取环境变量，并转为scala map
    val envs = System.getenv().asScala.map(x => (x._1, x._2))
    envs.foreach(println)
```

### 1.1.2 scala 读取配置和环境变量

```java
    // scala获取环境变量
    sys.env.foreach(println)
    // scala获取系统配置
    sys.props.foreach(println)
```

### 1.2 模拟SparkConf实现配置克隆的功能

#### 1.2.1 创建CloneCase类

```scala
package com.hollysys.scala.usecase.clone

import java.util.concurrent.ConcurrentHashMap
import scala.collection.JavaConverters._

/**
  * Created by shirukai on 2018/9/19
  * 创建一个 CloneCase类
  */
class CloneCase(loadDefaults: Boolean) extends Cloneable {
  //默认参数为 loadDefaults = true
  def this() = this(true)

  private val settings = new ConcurrentHashMap[String, String]()

  //是否加载默认配置
  if (loadDefaults) {
    loadSystemProperties
  }

  /**
    * 设置
    *
    * @param key   key
    * @param value value
    * @return this
    */
  private def set(key: String, value: String): CloneCase = {
    settings.put(key, value)
    this
  }

  def setMaster(name: String): CloneCase = {
    settings.put("clone.case.master", name)
    this
  }

  def printAll(): Unit = {
    settings.asScala.foreach(println)
  }

  private def loadSystemProperties: CloneCase = {
    //读取系统配置，并转为scala map
    val properties = System.getProperties.stringPropertyNames().asScala
      .map(key => (key, System.getProperty(key)))
    for ((key, value) <- properties if key.startsWith("java.")) {
      set(key, value)
    }
    this
  }

  override def clone(): CloneCase = {
    val cloned = new CloneCase(false)
    settings.entrySet().asScala.foreach(e => cloned.set(e.getKey, e.getValue))
    cloned
  }
}
```

#### 1.2.1 测试CloneCase

```scala
package com.hollysys.scala.usecase.clone

/**
  * Created by shirukai on 2018/9/19
  */
object CloneCaseTest {
  def main(args: Array[String]): Unit = {
    val cloneCase = new CloneCase().setMaster(this.getClass.getSimpleName)
    cloneCase.printAll()
    println("__________")
    val newCloneCase = cloneCase.clone()
    newCloneCase.printAll()
  }
}
```

