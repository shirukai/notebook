# all、filter、get、values、values_list 区别

我们在models.py里定义一个Student类，如：

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

## 结果集

### all()

```
In [2]: Student.objects.all()
# 这是执行的SQL查询
Out[2]: (0.000) SELECT @@SQL_AUTO_IS_NULL; args=None
(0.001) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` LIMIT 21; args=()
# 结果：
<QuerySet [
<Student: test1 test1  20 2017-09-26 02:59:01.191525+00:00>, 
<Student: test2 test2  19 2017-09-26 03:03:38.216921+00:00>, 
<Student: test3 test3  21 2017-09-26 03:03:39.481338+00:00>
]>
```

### filter() 

```
In [4]: Student.objects.filter()

Out[4]: (0.002) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` LIMIT 21; args=()

<QuerySet [
<Student: test1 test1  20 2017-09-26 02:59:01.191525+00:00>, 
<Student: test2 test2  19 2017-09-26 03:03:38.216921+00:00>, 
<Student: test3 test3  21 2017-09-26 03:03:39.481338+00:00>
]>
```

### get()

> get只能查询一条数据

```
In [3]: Student.objects.get(stu_name='test1')

(0.003) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` WHERE `blog_student`.`stu_name` = 'test1'; args=('test1',)

Out[3]: <Student: test1 test1  20 2017-09-26 02:59:01.191525+00:00>
```

### values()

字典形式结果

```
In [4]: Student.objects.values()

Out[4]: (0.003) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` LIMIT 21; args=()

<QuerySet [
{'stu_name': u'test1', 'stu_sex': u'', 'stu_no': u'201457507208', 'stu_age': 20L, 'stu_birth': datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>), u'id': 4L},
{'stu_name': u'test2', 'stu_sex': u'', 'stu_no': u'201457507203', 'stu_age': 19L, 'stu_birth': datetime.datetime(2017, 9, 26, 3, 3, 38, 216921, tzinfo=<UTC>), u'id': 5L}, 
{'stu_name': u'test3', 'stu_sex': u'', 'stu_no': u'201457507203', 'stu_age': 21L, 'stu_birth': datetime.datetime(2017, 9, 26, 3, 3, 39, 481338, tzinfo=<UTC>), u'id': 6L}
]>
```

### values_list()

元祖形式结果

```
In [5]: Student.objects.values_list()

Out[5]: (0.003) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` LIMIT 21; args=()

<QuerySet [
(4L, u'test1', u'201457507208', u'', 20L, datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>)), 
(5L, u'test2', u'201457507203', u'', 19L, datetime.datetime(2017, 9, 26, 3, 3, 38, 216921, tzinfo=<UTC>)), 
(6L, u'test3', u'201457507203', u'', 21L, datetime.datetime(2017, 9, 26, 3, 3, 39, 481338, tzinfo=<UTC>))
]>
```

* 从返回的结果集来看，all()跟filter()返回的结果集是一样的，但是all()不支持直接条件查询（all(stu_name='test1'))而filter可以，filter(stu_name='test1'),它等价于all().filter(stu_name='test1'),所以all()能用的方法，差不多filter都可以用
* 遍历all结果集

```
In [4]: stu = Student.objects.all()

In [5]: for row in stu:
   ...:     print row
   ...:     
(0.003) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student`; args=()
test1 test1  20 2017-09-26 02:59:01.191525+00:00
test2 test2  19 2017-09-26 03:03:38.216921+00:00
test3 test3  21 2017-09-26 03:03:39.481338+00:00
```

从遍历的结果集来看 ，遍历后的结果跟get获取的结果集是一样的，所以遍历row之后的用法，跟get是一样的。

```
In [6]: stu = Student.objects.all()

In [7]: for row in stu:
   ...:     print row.stu_name
   ...:     
(0.004) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student`; args=()
test1
test2
test3
```

```
In [9]: stu = Student.objects.get(stu_name='test1')
(0.003) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` WHERE `blog_student`.`stu_name` = 'test1'; args=('test1',)

In [10]: stu.stu_name
Out[10]: u'test1'

```

* values结果集也是queryset，但是它里面是数组和对象。所以通过list()方法，我们很容易得到一个json对象



