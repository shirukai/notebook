# Scala基础

## 变量

### 三种变量修饰符

val 定义immutable variable 常量

var 定义 mutable variable 变量

lazy val 惰性求值

![](https://shirukai.gitee.io/images/201804041504_183.png)

```
scala> lazy val f= 1*4
f: Int = <lazy>
scala> f
res22: Int = 4
```

## 数据类型

![](https://shirukai.gitee.io/images/201804180929_870.png)

```
scala> val name:String = "srk"
name: String = srk

scala> s"name is ${name}"
res0: String = name is srk
```

## 函数和代码块

### 代码块

![](https://shirukai.gitee.io/images/201804250932_544.png)

### 函数

![](https://shirukai.gitee.io/images/201804250933_621.png)

```
def hello(name: String): String = {
  s"hello,${name}"
}
hello("shirukai")

def add(x:Int,y:Int)=x+y
add(1,5)

```

## if表达式

if(条件) valA else valB

```
if(true) 1 else 2
if(false) 3 else 4

val a = 1
if (a == 1) a
if (a != 1) "not one"
if (a != 1) "not one" else a
```

![](https://shirukai.gitee.io/images/201804250955_440.png)

## for comprechension

实现循环

![](https://shirukai.gitee.io/images/201804251005_30.png)



## try表达式

try{}

catch{}

finally{}

例如：

```
//try表达式
try {
  Integer.parseInt("dog")
} catch {
  case _: Exception => 0
} finally {
  println("always be printed")
}
```

## match 表达式

类似于java中的switch

```
exp match{
 case p1 => val1
 case p2 => val2
 ……
 case _ = valn
}
```

例如

```
//match 表达式
val code = 4
val result_match =
  code match {
    case 1 => "one"
    case 2 => "two"
    case _ => "others"
  }
```

## 求值策略

![](https://shirukai.gitee.io/images/201804251023_203.png)

例子：

![](https://shirukai.gitee.io/images/201804251027_637.png)

## 高阶函数

用函数作为参数类型或返回值的函数，称为高阶函数

### 匿名函数

### 柯里化

柯里化函数把具有多阿哥参数的函数转换为一条函数连，每个节点上是单一参数。

![](https://shirukai.gitee.io/images/201804251104_869.png)

```
def curriedAdd(a: Int)(b: Int) = a + b
val addOne = curriedAdd(1)_
addOne(4)

```

### 递归与尾递归 

递归函数在函数式编程中是实现循环的一种技术

```
//计算n!
def factorial(n: Int): Int = {
  if (n <= 0) 1
  else n * factorial(n - 1)
}
factorial(8)
```

#### 尾递归

尾递归函数中所有递归形式的调用都出现在函数的末尾。当编译器检测到一个函数调用的是尾递归的时候，它就会覆盖当前的活动记录而不是在栈中去创建一个新的。

```
@annotation.tailrec
def factorial2(n: Int, m: Int): Int = {
  if (n <= 0) m
  else factorial2(n - 1, m * n)
}
factorial2(5,1)
```

### 例子

![](https://shirukai.gitee.io/images/201804251118_846.png)

```
def sum(f: Int => Int)(a: Int)(b: Int): Int = {
  @annotation.tailrec
  def loop(n: Int, acc: Int): Int = {
    if (n > b) {
      println(s"n=${n}, acc=${acc}")
      acc
    }
    else {
      println(s"n=${n}, acc=${acc}")
      loop(n + 1, acc + f(n))
    }
  }

  loop(a, 0)
}

sum(x => x)(1)(5)
sum(x => x * x)(1)(5)
sum(x => x * x * x)(1)(5)
val sumSquare = sum(x => x * x) _
sumSquare(1)(5)
```

## 集合

![](https://shirukai.gitee.io/images/201804251131_573.png)

### List[T]

![](https://shirukai.gitee.io/images/201804251142_216.png)



#### list过滤

```
val a = List(1, 2, 3, 4)
a.filter(x => x % 2 == 1)
```

例子：取出字符串中的数字，并转为list

```
"99 Red Balloons".toList.filter(x => Character.isDigit(x))
```

#### takeWhile

达到某个条件之前一直取数

```
"99 Red Balloons".toList.takeWhile(x => x != 'B')
```

#### map

映射list里的元素

```
val c = "x" :: "y" :: "z" :: Nil
c.map(x => x.toUpperCase)
res13: List[String] = List(X, Y, Z)
```

```
a.filter(_ % 2 == 1).map(_ + 10)
```

