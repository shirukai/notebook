# javascript面向对象编程(二):构造函数的继承 

摘录学习自：阮一峰老师的博客：http://www.ruanyifeng.com/blog/2010/05/object-oriented_javascript_inheritance.html

现在有一个“动物“构造函数

```
function Animal() {
    this.species = "动物";
}
```

还有一个“猫”的构造函数

```
function Cat(name,color) {
    this.name = name;
    this.color = color;
}
```



## 一、构造函数绑定 

第一种方法也是最简单的方法，使用call或apply方法，将父对象的构造函数绑定在子对象上，即在子对象构造函数中加一行：（关于cell、以及apply的用法：http://uule.iteye.com/blog/1158829）

```
function Animal() {
    this.species = "动物";
}

function Cat(name,color) {
    //Animal.call(this,arguments);
    Animal.apply(this,arguments);
    this.name = name;
    this.color = color;
}
var cat1 = new Cat("大毛","黄色");
alert(cat1.species) //动物
```

## 二、prototype模式 

第二种方法更常见，使用prototype属性。

如果"猫"的prototype对象，指向一个Animal的实例，那么所有"猫"的实例，就能继承Animal了。

```
Cat.prototype = new Animal();
Cat.prototype.constructor = Cat;
var cat1 = new Cat("大毛","黄色");
    alert(cat1.species)
```

代码的第一行，我们将Cat的prototype对象指向一个Animal的实例。

```
Cat.prototype = new Animal();
```

它相当于完全删除了prototype 对象原先的值，然后赋予一个新值。但是，第二行又是什么意思呢？

```
Cat.prototype.constructor = Cat;
```

原来，任何一个prototype对象都有一个constructor属性，指向它的构造函数。如果没有"Cat.prototype = new Animal();"这一行，Cat.prototype.constructor是指向Cat的；加了这一行以后，Cat.prototype.constructor指向Animal。

```
　alert(Cat.prototype.constructor == Animal); //true
```

更重要的是，每一个实例也有一个constructor属性，默认调用prototype对象的constructor属性。

```
alert(cat1.constructor == Cat.prototype.constructor); // true
```

因此，在运行"Cat.prototype = new Animal();"这一行之后，cat1.constructor也指向Animal！

```
alert(cat1.constructor == Animal); // true
```

这显然会导致继承链的紊乱（cat1明明是用构造函数Cat生成的），因此我们必须手动纠正，将Cat.prototype对象的constructor值改为Cat。这就是第二行的意思。

这是很重要的一点，编程时务必要遵守。下文都遵循这一点，即如果替换了prototype对象，

```
o.prototype = {};
```

那么，下一步必然是为新的prototype对象加上constructor属性，并将这个属性指回原来的构造函数。

```
o.prototype.constructor = o;
```

## 三、 直接继承prototype 

第三种方法是对第二种方法的改进。由于Animal对象中，不变的属性都可以直接写入Animal.prototype。所以，我们也可以让Cat()跳过 Animal()，直接继承Animal.prototype。

现在，我们先将Animal对象改写：

```
function Animal() {
    //this.species = "大动物"; 优先级大于prototype
}
Animal.prototype.species = "动物";
```

然后，将Cat的prototype对象，然后指向Animal的prototype对象，这样就完成了继承。

```
Cat.prototype = Animal.prototype;
Cat.prototype.constructor = Cat;
var cat1 = new Cat("大毛","黄色");
alert(cat1.species)
```

与前一种方法相比，这样做的优点是效率比较高（不用执行和建立Animal的实例了），比较省内存。缺点是 Cat.prototype和Animal.prototype现在指向了同一个对象，那么任何对Cat.prototype的修改，都会反映到Animal.prototype。

所以，上面这一段代码其实是有问题的。请看第二行

```
　Cat.prototype.constructor = Cat;
```

这一句实际上把Animal.prototype对象的constructor属性也改掉了！

```
alert(Animal.prototype.constructor); // Cat
```

## 四、利用空对象作为中介 

由于"直接继承prototype"存在上述的缺点，所以就有第四种方法，利用一个空对象作为中介

```
var F =  function () {
};
F.prototype = Animal.prototype;
Cat.prototype = new F();
Cat.prototype.constructor = Cat;
var cat1 = new Cat("大毛","黄色");
alert(cat1.species);
```

F是空对象，所以几乎不占内存。这时，修改Cat的prototype对象，就不会影响到Animal的prototype对象。

```
alert(Animal.prototype.constructor); // Animal
```

### 封装继承方法 

```
function extend(Child,Parent) {
    var F = function () {};
    F.prototype = Parent.prototype;
    Child.prototype = new F();
    Child.prototype.constructor = Child;
    Child.uber = Parent.prototype;
}
```

使用的时候，方法如下：

```
extend(Cat,Animal);
var cat1 = new Cat("大毛","黄色");
alert(cat1.species)
```

另外，说明一点，函数体最后一行

```
Child.uber = Parent.prototype;
```

意思是为子对象设一个uber属性，这个属性直接指向父对象的prototype属性。（uber是一个德语词，意思是"向上"、"上一层"。）这等于在子对象上打开一条通道，可以直接调用父对象的方法。这一行放在这里，只是为了实现继承的完备性，纯属备用性质。

## 五、拷贝继承 

上面是采用prototype对象，实现继承。我们也可以换一种思路，纯粹采用"拷贝"方法实现继承。简单说，如果把父对象的所有属性和方法，拷贝进子对象，不也能够实现继承吗？这样我们就有了第五种方法。



首先，还是把Animal的所有不变属性，都放到它的prototype对象上。

```
　function Animal(){}
　　Animal.prototype.species = "动物";
```

然后，再写一个函数，实现属性拷贝的目的。

```
function extendCopy(Child,Parent) {
    var p = Parent.prototype;
    var c = Child.prototype;
    for (var i in p){
        c[i] = p [i];
    }
    c.uber = p;
}
```

这个函数的作用，就是将父对象的prototype对象中的属性，一一拷贝给Child对象的prototype对象。

使用的时候，这样写：

```
extendCopy(Cat,Animal);
var cat1 = new Cat("大毛","黄色");
alert(cat1.species)
```

