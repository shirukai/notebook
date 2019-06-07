# django增删改查

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
python manage.py shell
from blog.models import Student
```



## 添加数据

第一种方法：

```
Student.objects.create(stu_name = 'test', stu_no = '201457507203', stu_age = 20)
```

第二种方法：

```
s  = Student(stu_name = 'test', stu_no = '201457507203', stu_age = 20)
s.save()
```

第三种方法：

```
s = Student()
s.stu_name = 'test'
s.stu_no = '201457507203'
s.stu_age = '20'
s.save()
```

第四种方法：

```
Student.objects.get_or_create(stu_name = 'test', stu_no = '201457507203', stu_age = 20)
```

这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.

```
(<Student: test test  20 2017-09-26 02:40:19.959604+00:00>, True)
```

## 删除数据

### 删除一条数据 

```
Student.objects.get(stu_name = 'test').delete()
```

> 注意：此时只能数据库只能有一条 stu_name = ‘test’的数据，这样才能删除，如果存在多条，则会显示：

```
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/lib/python2.7/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/django/db/models/query.py", line 384, in get
    (self.model._meta.object_name, num)
MultipleObjectsReturned: get() returned more than one Student -- it returned 2!
```

这时候我们就要用到下列操作：

### 删除一组数据

```
Student.objects.filter(stu_name = 'test').delete();
```

```
(2L, {u'blog.Student': 2L})
```

## 修改数据

修改 stu_name = 'test' 的stu_no字段为‘201457507208’

```
>>> student = Student.objects.get(stu_name = 'test')
>>> student.stu_no = '201457507208'
>>> student.save()
```

批量修改，**适用于 .all()  .filter()  .exclude() 等后面 (危险操作，正式场合操作务必谨慎)**

```
Person.objects.filter(name__contains="abc").update(name='xxx') # 名称中包含 "abc"的人 都改成 xxx
Person.objects.all().delete() # 删除所有 Person 记录
```



## 查询记录

1. 获取所有对象Student.objects.all()

``` 
>>> Student.objects.all()
<QuerySet [<Student: shirukai shirukai  20 2017-09-26 02:30:33.850131+00:00>, <Student: test test  20 2017-09-26 02:59:01.191525+00:00>]>
```

2. 切片操作某个区间Student.objects.all()[]

   如获取2到5区间3条记录[2:5]

```
>>> Student.objects.all()
<QuerySet [
<Student: test1 test1  20 2017-09-26 02:59:01.191525+00:00>, 
<Student: test2 test2  20 2017-09-26 03:03:38.216921+00:00>, 
<Student: test3 test3  20 2017-09-26 03:03:39.481338+00:00>,
<Student: test4 test4  20 2017-09-26 03:03:40.457119+00:00>,
<Student: test5 test5  20 2017-09-26 03:03:41.025110+00:00>,
<Student: test6 test6  20 2017-09-26 03:03:41.592895+00:00>, 
<Student: test7 test7  20 2017-09-26 03:03:42.152777+00:00>]>
```

```
Student.objects.all()[2:5]
<QuerySet [
<Student: test3 test3  20 2017-09-26 03:03:39.481338+00:00>, 
<Student: test4 test4  20 2017-09-26 03:03:40.457119+00:00>, 
<Student: test5 test5  20 2017-09-26 03:03:41.025110+00:00>]>

```

3. Student.objects.get(stu_uname = 'test1')获取的是一条记录

4. Student.objects.filter(stu_uname = 'test1')获取的是多条名字为test1的记录

5. Student.objects.filter(stu_uname __iexact="abc")  # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件

6. Student.objects.filter(stu_uname __contains="abc")  # 名称中包含 "abc"的人

7. Student.objects.filter(stu_uname __icontains="abc")  #名称中包含 "abc"，且abc不区分大小写

8. Student.objects.filter(stu_uname __regex="^abc")  # 正则表达式查询

9. Student.objects.filter(stu_uname __iregex="^abc")  # 正则表达式不区分大小写

   filter是找出满足条件的，当然也有排除符合某条件的

10. Person.objects.exclude(stu_uname __contains="WZ")  # 排除包含 WZ 的Person对象

11. Person.objects.filter(stu_uname __contains="abc").exclude(age=23)  # 找出名称含有abc, 但是排除年龄是23岁的



> 注意事项：

(1). 如果只是检查 Student 中是否有对象，应该用 Student .objects.all().**exists()**

(2). QuerySet 支持切片 Student .objects.all()[:10] 取出10条，可以节省内存

(3). 用 len(es) 可以得到Student 的数量，但是推荐用 Student .objects.count()来查询数量，后者用的是SQL：SELECT COUNT(\*)

(4). list(es) 可以强行将 QuerySet 变成 列表

### 查询排序

按照名称排序

```
Student.objects.all().order_by('stu_name')
Student.objects.all().order_by('-stu_name') # 在 column name 前加一个负号，可以实现倒序
```

### 链式查询

查询名字包含test的且年龄为20的学生

```
Student.objects.filter(stu_name__contains='test').filter(stu_age='20')
```

结果：

```
<QuerySet [
<Student: test1 test1  20 2017-09-26 02:59:01.191525+00:00>, 
<Student: test5 test5  20 2017-09-26 03:03:41.025110+00:00>, 
<Student: test7 test7  20 2017-09-26 03:03:42.152777+00:00>]>
```

查询名字包含test的且年龄不为20的学生

```
Student.objects.filter(stu_name__contains='test').exclude(stu_age='20')
```

结果：

```
<QuerySet 
[<Student: test1 test1  20 2017-09-26 02:59:01.191525+00:00>, 
<Student: test5 test5  20 2017-09-26 03:03:41.025110+00:00>, 
<Student: test7 test7  20 2017-09-26 03:03:42.152777+00:00>]>
```

### QuerySet不支持负索引

```
Student.objects.all()[:10] 切片操作，前10条
Student.objects.all()[-10:] 会报错！！！
# 1. 使用 reverse() 解决
Student.objects.all().reverse()[:2] # 最后两条
Student.objects.all().reverse()[0] # 最后一条
 
# 2. 使用 order_by，在栏目名（column name）前加一个负号
Student.objects.order_by('-id')[:3] # id最大的3条
```

### QuerySet 重复的问题，使用 .distinct() 去重

```
stu = Student.objects.all()
stu = stu.distinct()
```

