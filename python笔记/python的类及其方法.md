# python的类及其方法 

## 一、python中的类 

在python中，面向对象编程主要有两个主题，就是类和类实例

类与实例：

类与实例相互关联着：类是对象的定义，而实例是"真正的实物"，它存放了类中所定义的对象
的具体信息

类的优点：

>1、类对象是多态的：也就是多种形态，这意味着我们可以对不同的类对象使用同样的操作方法，而不需要额外写代码。

> 2、类的封装：封装之后，可以直接调用类的对象，来操作内部的一些类方法，不需要让使用者看到代码工作的细节。

> 3、类的继承：类可以从其它类或者元类中继承它们的方法，直接使用。

## 二、类的定义 

### 1. 定义类（class）的语法 

```
class LearnClass:
    def __init__(self):
        self.content = "how to use python class"

    def learn_content(self):
        print self.content
```

### 2. 初始化对象

创建类时，需要定义一个特定的方法，名为`__init__()`,只要创建这个类的实例，就会运行这个方法。如：我们在初始化方法里设置一个变量 content =“how to use python class”

```
    def __init__(self):
        self.content = "how to use python class"
```

调用`__init__()`  里的参数,用self.content即可

```
	def learn_content(self):
        print self.content
```

### 3.其他专用方法 

> 像`__init__()` 这样python类里专用的方法，还有`__del__、__repr__、__str__、__cmp__、__getitem__、__setitem__、__delitem__`  等



#### `__del__（）` ：

与`__init__()` 方法相反，该方法是类的实例被销毁的时候会触发。例如：

```
class LearnClass:
    def __init__(self):
        print ('hello!')

    def __del__(self):
        print('goodbye!')


if __name__ == "__main__":
    learn = LearnClass()
    del learn # 销毁实例
```

![](https://shirukai.gitee.io/images/201802021508_560.png)

#### `__repr__()`:

当使用repr(obj)的时候，会调用该类的`__repr__` 函数，该函数返回对象字符串表达式

如果没有定义这个函数，会返回如下信息：

```
<__main__.LearnClass instance at 0x0000000003DE4BC8>
```

如果定义这个函数，如：

```
class LearnClass:
    def __init__(self):
        print ('hello!')

    def __del__(self):
        print('goodbye!')

    def __repr__(self):
        return "the class is learn"


if __name__ == "__main__":
    learn = LearnClass()
    print(repr(learn))

```

![](https://shirukai.gitee.io/images/201802021520_316.png)

可以用于重构对象

```
class LearnClass:
    def __init__(self):
        print ('hello!')

    def __del__(self):
        print('goodbye!')

    def __repr__(self):
        return "LearnClass()"

    def test(self):
        print('________test___')


if __name__ == "__main__":
    learn = LearnClass()
    new_learn = eval(repr(learn))
    new_learn.test()
```

#### `__str__()`:

Python能用print语句输出内建数据类型。有时，程序员希望定义一个类，要求它的对象也能用print语句输出。Python类可定义特殊方法`__str__`，为类的对象提供一个不正式的字符串表示。

```
class LearnClass:
    def __init__(self, params):
        self.username = params['username']
        self.password = params['password']
        self.phone = params['phone']

    def __str__(self):
        return "name:%s password:%s phone:%s" % (self.username, self.password, self.phone)


if __name__ == "__main__":
    params = {
        'username': 'shirukai',
        'password': '123456a?',
        'phone': '15552211520'
    }
    learn = LearnClass(params)
    print(learn)
```

![](https://shirukai.gitee.io/images/201802021532_875.png)

#### `__cmp__()`:

比较运算符

```
class LearnClass:
    def __init__(self):
        pass

    def __cmp__(self, other):
        print(other) # 10
        return -1 # False


if __name__ == "__main__":
    learn = LearnClass()
    print(learn > 10)
```

#### `__getitem__()`:

使用方法跟获取字典值一样，通过   对象['key'] 的方式获取

```
class LearnClass:
    def __init__(self):
        pass

    def __getitem__(self, item):
        return item


if __name__ == "__main__":
    learn = LearnClass()
    print learn['getitem']
    print learn['1']
```

```
C:\Python27\python.exe D:/Repository/testapi/learnclass/LearnClass.py
getitem
1

Process finished with exit code 0
```

#### `__getitem__()`:

使用方法跟设置字典key、value一样

```
class LearnClass:
    def __init__(self):
        self.my_dict = {

        }
        pass

    def __getitem__(self, item):
        return self.my_dict[item]

    def __setitem__(self, key, value):
        self.my_dict[key] = value


if __name__ == "__main__":
    learn = LearnClass()
    learn['a'] = 1
    learn['b'] = 2
    print(learn['a'])
    print(learn['b'])

```

运行结果：

```
C:\Python27\python.exe D:/Repository/testapi/learnclass/LearnClass.py
1
2

Process finished with exit code 0
```



#### `__delitem__()`:

当使用del 对象[key] 时，会触发这个函数，如：

```
class LearnClass:
    def __init__(self):
        self.my_dict = {

        }
        pass

    def __getitem__(self, item):
        return self.my_dict[item]

    def __setitem__(self, key, value):
        self.my_dict[key] = value

    def __delitem__(self, key):
        self.my_dict.pop(key)


if __name__ == "__main__":
    learn = LearnClass()
    learn['a'] = 1
    learn['b'] = 2
    print(learn['a'])
    print(learn['b'])
    del learn['a']
    print(learn['a'])
```

运行结果：

```
C:\Python27\python.exe D:/Repository/testapi/learnclass/LearnClass.py
1
Traceback (most recent call last):
2
  File "D:/Repository/testapi/learnclass/LearnClass.py", line 25, in <module>
    print(learn['a'])
  File "D:/Repository/testapi/learnclass/LearnClass.py", line 9, in __getitem__
    return self.my_dict[item]
KeyError: 'a'

Process finished with exit code 1
```

由于删除了 a，所以print(learn['a'])的时候就会报错了。

### 4.类的私有属性 

　　`__private_attrs` 两个下划线开头，声明该属性为私有，不能在类地外部被使用或直接访问。在类内部的方法中使用时 self.__private_attrs
类的方法
　　在类地内部，使用def关键字可以为类定义一个方法，与一般函数定义不同，类方法必须包含参数self,且为第一个参数
私有的类方法
　　`__private_method` 两个下划线开头，声明该方法为私有方法，不能在类地外部调用。在类的内部调用slef.__private_methods



### 5.classmethod类方法 

python用@classmethod修饰符来表示一个类方法，类方法的参数是cls。类方法既可以用类直接调用，也可以类实例化后调用。常见参数为self的是实例方法， 只能在类被实例化后调用。

类方法中的变量，cls是将整个类当做参数传入。当有子类继承时，调用该类方法时，闯入的类变量cls是子类，而非父类。

##### 定义类方法： 

```
    @classmethod
    def class_method(cls):
        print(cls)
```

##### 调用类方法

```
if __name__ == "__main__":
    learn = LearnClass()
    LearnClass.class_method()
    learn.class_method()
```

##### 输出结果: 

```
C:\Python27\python.exe D:/Repository/testapi/learnclass/LearnClass.py
__main__.LearnClass
__main__.LearnClass

Process finished with exit code 0

```

### 6.staticmethod静态方法

静态方法可以用@staticmethod来修饰，静态方法没有特定的参数self或者cls，静态方法跟类方法一样，有两种调用方式，一种是直接调用，另一种是实例化调用。

```
    @staticmethod
    def static_method():
        print('this is static method')
```

### 7.@property 装饰

使用@property最简单的方法之一是将它作为一个方法的装饰器来使用，可以将一个类里的方法转变成一个类里的属性。

定义：

```
    @property
    def score(self):
        return 100
```

使用：

```
if __name__ == "__main__":
    learn = LearnClass()
    print(learn.score)
```

使用@property的setter、getter方法

```
    @property
    def score(self):
        return self.score

    @score.setter
    def score(self, value):
        self.score = value

```

```
    learn = LearnClass()
    print(learn.score)
    learn.score = 90
    print(learn.score)

```

