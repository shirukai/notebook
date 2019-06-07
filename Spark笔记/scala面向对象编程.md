## scala面向对象编程

![](https://shirukai.gitee.io/images/6879a99e78b0bae1c2f934f7f10d4f30.jpg)

```
package com.hollysys.scala

/**
  *
  * @author shirukai
  * Created in 2018/6/20 上午10:33
  */

trait Animal{
  def eat()
}
trait AnbleRun{
  def run() = {
    println("很正常的跑")
  }
}

class Dog extends Animal with AnbleRun {
  Dog.jiao()
  override def eat(): Unit = {
    println("小狗吃")
  }
  Dog.catHome()
  override def run(): Unit = {
    println("小狗跑")
  }
}

//Dog的伴生对象
object Dog{
  private val dogDefaultName = "dudu"
  private def jiao() = {
    println("汪汪的叫")
  }
  def catHome(): Unit ={
    println("狗会看家")
  }
}

class Cat(name:String) extends Animal with AnbleRun{
  def this() =this("小可爱")
  override def eat(): Unit = {
    println("小猫吃")
  }

  override def run(): Unit = {
    println("小猫跑")
  }
}

object entry{
  def main(args: Array[String]): Unit = {
    //val修饰的不可变的
    val dog = new Dog()
    val cat = new Cat()
    //var 修饰的是可变的
    var cat1 = new Cat("sss")

  }
}
```



## scala函数式编程

```
import scala.collection.mutable.ArrayBuffer

val seqStr: Seq[String] = Seq.apply("test", "my")
val seq: Seq[Int] = Seq(4, 5, 3, 5)
seq.length
def addTestStr(x: Int): String = {
  x + "test"
}

def addOne(x: Int): Int = {
  x + 1
}

def oneToSeq(x: Int): Seq[Int] = {
  0.to(x)
}
seq.map(addTestStr)
seq.map(addOne)
seq.map((x: Int) => x + 1)
seq.map(x => x + 1)
seq.map(_ + 1)
0.to(3)
seq.flatMap(oneToSeq)
seq.filter(_ > 3)
seq.filterNot(_ > 3)
seq.reduce((x, y) => x + y)
seq.fold(0)((x, y) => x + y)
seq.foldLeft(ArrayBuffer.newBuilder[String])((arr, x) => {
  if (x > 3) {
    arr += (x + "test")
  } else {
    arr
  }
})
seq.foreach(x => println(x))

seq.sorted

seqStr.zip(seq)

val it = Iterator("is","it","silly","?")

while (it.hasNext){
  println(it.next())
}
```

## 闭包

### scala中的闭包（clouse）

闭包就是一个函数，这个函数可能会访问定义在函数外面的变量

```
//闭包是一个函数
val addTwoFun = (i: Int) => i + 2
addTwoFun(2)

//应用到函数外面定义的变量，定义这个函数的过程
//是将这个自由变量捕获而构成一个封闭的函数

var factor = 2
val addFactorFun = (i: Int) => i + factor
addFactorFun(2)

addFactorFun.getClass

/**
  * res2: Class[?0] = class com.hollysys.scala.A$A13$A$A13$$anonfun$addFactorFun$1
  */
addFactorFun.isInstanceOf[Serializable]
```

### spark对闭包序列化的处理

1. 去掉闭包汇总无用的引用，减少闭包序列化后的大小，有利于网络传输
2. 尽可能的保证闭包可以序列化，如果不能则抛异常

```
package com.hollysys.scala

import org.apache.spark.{SparkConf, SparkContext}

/**
  *
  * @author shirukai
  *         Created in 2018/6/20 下午4:10
  */
object ClouseTest {
  def main(args: Array[String]): Unit = {
    val sc = new SparkContext("local", "myApp")
    val listRDD = sc.parallelize[Int](Seq(1, 2, 3, 3), 2)
    // 因为函数 x=> x+1是可以序列化的，所以这里没有问题
    val mapRDD = listRDD.map(x => x + 1)
    mapRDD.collect()

    /**
      * 因为函数addTwoFun依赖到了类AdderWithField中的成员变量n
      * 进而这个函数addTwoFun会依赖类AdderWithField
      * 然而类AdderWithField是不能被序列化的，所以这个闭包是不能被序列化的
      */
    val mapRDDError = listRDD.map(new AdderWithField().addTwoFun)
    mapRDDError.collect()

    /**
      * 这里的函数addTwoFun是不会依赖Adder中的任何成员变量
      * 所以相对addTwoFun来说，变量new Adder（）在闭包是无效的
      * 所以会被spark清除掉这个无用的变量
      */
    val addMapRDD = listRDD.map(new Adder().addTwoFun)
    addMapRDD.collect()
  }

}

class AdderWithField {
  val n = 2

  def addTwoFun = (i: Int) => i + n
}

class Adder {
  def addTwoFun = (i: Int) => i + 2
}
```



## Option

### option可以视作一个容器，这个容器中要么有东西，要么没有东西

same表示容器中有且仅有一个东西

None 表示空容器

```
import scala.reflect.io.File

var x: Option[String] = None
//x.get
/**
  * java.util.NoSuchElementException: None.get
  * at scala.None$.get(OptionTest.sc:343)
  * at scala.None$.get(OptionTest.sc:341)
  * at #worksheet#.#worksheet#(OptionTest.sc:1)
  **/

x.getOrElse("default")

x = Option(null)
x = Option("some value")
/**
  *
  * x: Option[String] = None
  * x: Option[String] = Some(some value)
  */

//option 可以当做集合来看待

val fileNameOption: Option[String] = Some("testfile")
fileNameOption.map(fileName => {
  println(s"have some value ${fileName}")
})
```

### Option可以被当做集合看待

```
package com.hollysys.scala

import java.io.File


/**
  *
  * @author shirukai
  *         Created in 2018/6/20 下午5:01
  */
object OptionTest {
  def main(args: Array[String]): Unit = {
    //val fileNameOpt: Option[String] = Some("testfile")
   println(getDir(Some("/Users/shirukai/Desktop/test")))
  }

  def getDir(fileNameOpt: Option[String]): java.io.File = {
    fileNameOpt.map(fileName => new File(fileName))
      .filter(_.isDirectory)
      .getOrElse(new File(System.getProperty("java.io.tmpdir")))
  }
}
```

## RDD概念

