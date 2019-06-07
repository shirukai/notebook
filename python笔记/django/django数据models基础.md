# django数据models基础

## 例子

定义一个Persion模型类，包括first_name、last_name字段

```
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
```

first_name 和last_name是模型的领域。每个字段被指定为一个类属性，每个属性映射到一个数据库列，上面的Persion模型将创建一个数据库表，如下所示：

```
 CREATE TABLE myapp_person (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

说明：

* 表的名称myapp_person,是自动从某些模型元数据生成的，但可以覆盖。
* id为django自动添加的字段，也可以自己定义。
* 这个例子的sql是使用了postgersql语法进行格式化的，django会根据settings里配置的数据库自动对sql进行格式化。

## 使用模型

一旦我们定义了数据模型，就要告诉django我们要使用这些模型。这个是通过修改settings里的配置来添加应用模块的名字，让django来执行应用里的models.py。

如我们在myapp下定义了一个models，我们就需要这样设置：

```
INSTALLED_APPS = [
    #...
    'myapp',
    #...
]
```

> 注意：当我们添加新的模型的时候，需要运行 

```
python manage.py migrate

```

## 字段

数据库中的字段就是有模型中类的竖井来指定的，要注意的是，不要使用字段名称与modelAPI的关键字，如clean，sava，delete等。

例如：

```
from django.db import models

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
```

### 字段类型

模型中的每个字段应该是field类的一个实例，Django使用字段类型来确定一些事情：

* 列类型，它告诉数据库储存什么类型的数据（如INTEGER，VARCHAR，TEXT）
* 在呈现表单字段时使用的默认HTML小部件（例如`<input type="text">``<select>`）
* 最小的验证要求，用户Django的管理员和自动生成的表单

更多字段类型：https://docs.djangoproject.com/en/dev/ref/models/fields/#model-field-types

### 字段选项

每个字段都需要一组特定于字段的参数（在 [模型字段引用中记录](https://docs.djangoproject.com/en/dev/ref/models/fields/#model-field-types)）。例如， [`CharField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.CharField)（及其子类）需要一个[`max_length`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.CharField.max_length)参数，该 参数指定`VARCHAR`用于存储数据的数据库字段的大小。

#### null

null=True，django将数据库空值储存为null，默认为Talse

#### blank

blank=True，该字段被允许为空白，默认false

> 注意，blank不同于null，null是纯数据库相关的，而blank是与验证相关的，如果一个字段有blank=True表单验证将允许输入一个空值。如果字段有blank=False，则该字段将被要求。

#### choices

```
from django.db import models

class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
```

```
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large'
```

SHIRT_SIZES第一个参数‘s'是传过来的值，第二个参数’small‘是保存到数据库里的值。

#### default 

字段的默认值，这可以是值，也可以调用对象

#### help_text

额外的帮助文本将于窗体小部件一起显示，即使您的子弹在表单上使用，他对文档也很有用。

#### primary_key

primary_key=True,该字段是模型的主键

如果我们没有在模型中指定任何字段属性为primary_key=True，django将自动添加IntegerField以保存主键。

> 主键是只读的，如果你要改变主键的值，将会生成一个新的对象。如：

```
>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
<QuerySet ['Apple', 'Pear']>
```

#### unique 

unique = True，在这个表中这个字段必须是唯一的。

### 自动主键字段

默认情况下，Django为每个模型提供以下字段：

```
id = models.AutoField(primary_key=True)
```

这是一个自增的主键

如果你想要设置一个自己的主键，就在对应的字段属性里添加 primary_key = True,django将不会创建默认的主键。

### 详细字段名

每个字段类型，除了ForeignKey,ManyToManyField和OneToOneField，都可采用可选的第一个位置参数——一个详细名称。如果没有给出详细的名称，django将使用字段的属性名称自动创建它，将下划线转换为空格。

在这个例子中，详细名为“person's first name”

```
first_name = models.CharField("person's first name", max_length=30)
```

在这个例子中，详细名称为“first name”

```
first_name = models.CharField(max_length=30)
```

[`ForeignKey`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey), [`ManyToManyField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField) 和[`OneToOneField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField) 要求第一个参数为模型类，所以详细名字由verbose_name关键字来确定

```
poll = models.ForeignKey(
    Poll,
    on_delete=models.CASCADE,
    verbose_name="the related poll",
)
sites = models.ManyToManyField(Site, verbose_name="list of sites")
place = models.OneToOneField(
    Place,
    on_delete=models.CASCADE,
    verbose_name="related place",
)
```

### 关系

显然，关系数据库的力量在于彼此关联表。Django提供了定义三种最常见类型的数据库关系的方式：多对一，多对多和一一对应。

#### 多对一关系

通过使用django.db.models.ForeignKey来定义多对一的关系，使用跟其他的Field类型一样。

ForeignKey需要一个位置参数：模型相关的类

例如，如果car模型具有Manufacturer，一个Manufacturer制造多个汽车，但每个Car只有个manufacturer,使用一下定义：

```
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
```

#### 多对多关系 

通过使用 ManyToManyField来定义多对多的关系

ManyToManyField需要一个位置参数：模型相关的类

例如：一个Pizza有个多个Topping对象，一个Topping也有多个Pizza：

```
from django.db import models

class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```

#### 一对一关系

要定义一对一的关系，请使用 [`OneToOneField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField)。您可以像任何其他`Field`类型一样使用它 ：将其作为模型的类属性。

当对象以某种方式“扩展”另一个对象时，这对对象的主键最有用。

[`OneToOneField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField) 需要一个位置参数：模型相关的类。

例如，如果您正在构建“地方”数据库，则可以在数据库中构建非常标准的地址，电话号码等。然后，如果你想建立的地方顶部的餐馆数据库，而不是重复自己，在复制这些领域`Restaurant`模型，你可以把`Restaurant`有[`OneToOneField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.OneToOneField)到`Place`（因为餐厅“是”的地方;事实上，处理这通常使用 [继承](https://docs.djangoproject.com/en/dev/topics/db/models/#model-inheritance)，涉及隐式的一对一关系）。

与之一样[`ForeignKey`](https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey)，可以定义[递归关系，](https://docs.djangoproject.com/en/dev/ref/models/fields/#recursive-relationships)并且可以[对尚未定义的模型](https://docs.djangoproject.com/en/dev/ref/models/fields/#lazy-relationships)进行[引用](https://docs.djangoproject.com/en/dev/ref/models/fields/#lazy-relationships)。

## models使用

models.py

```
class Student(models.Model):
    stu_name = models.CharField(max_length=30)
    stu_no = models.CharField(max_length=20)
    stu_sex = models.CharField(max_length=10)
    stu_age = models.IntegerField()
    stu_birth = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s %s %s %s' % (self.stu_name, self.stu_name, self.stu_sex, self.stu_age, self.stu_birth)
```

```
 python manage.py migrate
 python manage.py makemigrations
```

