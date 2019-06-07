# django获取字段的方法

## 通过._meta.fields获取 

以Student这个model为例

```
In [59]: Student._meta.fields
Out[59]: 
(<django.db.models.fields.AutoField: id>,
 <django.db.models.fields.CharField: stu_name>,
 <django.db.models.fields.CharField: stu_no>,
 <django.db.models.fields.CharField: stu_sex>,
 <django.db.models.fields.IntegerField: stu_age>,
 <django.db.models.fields.DateTimeField: stu_birth>)
```

获取字段名：

```
In [62]: stu = Student._meta.fields    
In [62]: [stu[i].name for i in range(len(stu))]
Out[62]: [u'id', 'stu_name', 'stu_no', 'stu_sex', 'stu_age', 'stu_birth']
```

## 通过`__dick__.keys()` 获取

```
In [21]: stu = Student.objects.get(stu_name='test1')
(0.004) SELECT VERSION(); args=None
(0.002) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` WHERE `blog_student`.`stu_name` = 'test1'; args=('test1',)
In [23]: stu.__dict__.keys()
Out[23]: ['stu_name', '_state', 'stu_sex', 'stu_no', 'stu_birth', 'stu_age', 'id']
```

## `__dick__`用法 

```
In [24]: stu =Student.objects.all()
In [25]: stu.__dict__
Out[25]: 
{'_db': None,
 '_fields': None,
 '_for_write': False,
 '_hints': {},
 '_iterable_class': django.db.models.query.ModelIterable,
 '_known_related_objects': {},
 '_prefetch_done': False,
 '_prefetch_related_lookups': (),
 '_result_cache': None,
 '_sticky_filter': False,
 'model': blog.models.Student,
 'query': <django.db.models.sql.query.Query at 0x2e3b490>}

```

```
In [26]: stu =Student.objects.get(stu_name='test1')
(0.003) SELECT `blog_student`.`id`, `blog_student`.`stu_name`, `blog_student`.`stu_no`, `blog_student`.`stu_sex`, `blog_student`.`stu_age`, `blog_student`.`stu_birth` FROM `blog_student` WHERE `blog_student`.`stu_name` = 'test1'; args=('test1',)

In [27]: stu.__dict__
Out[27]: 
{'_state': <django.db.models.base.ModelState at 0x2efd4d0>,
 'id': 4L,
 'stu_age': 20L,
 'stu_birth': datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>),
 'stu_name': u'test1',
 'stu_no': u'201457507208',
 'stu_sex': u''}
```

## for遍历

```
In [22]: stu = Student.objects.get(stu_name='test1')
In [22]: [(kk,stu.__dict__[kk]) for kk in stu.__dict__.keys() if kk != "_state"]
Out[22]: 
[('stu_name', u'test1'),
 ('stu_sex', u''),
 ('stu_no', u'201457507208'),
 ('stu_birth', datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>)),
 ('stu_age', 20L),
 ('id', 4L)]

In [23]: dict([(kk,stu.__dict__[kk]) for kk in stu.__dict__.keys() if kk != "_state"])
    ...: 
    ...: 
Out[23]: 
{'id': 4L,
 'stu_age': 20L,
 'stu_birth': datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>),
 'stu_name': u'test1',
 'stu_no': u'201457507208',
 'stu_sex': u''}

```

说明：首先利用objects.get()方法，查询一条出一条数据。然后利用`stu.__dict__.keys()`  获取所有的字段

```
In [23]: stu.__dict__.keys()
Out[23]: ['stu_name', '_state', 'stu_sex', 'stu_no', 'stu_birth', 'stu_age', 'id']
```

然后遍历这个数组`for kk in stu.__dict__.keys()`，就可以得到每个字段,kk就是每个字段的名字，利用`stu__dict__[kk]` 就可以得到字段的名字。`(kk,stu_dict_[kk])`  的值取决去后面for循环的遍历结果以及if条件的筛选结果。然后放到一个[]里就会生成以下形式的数据：

```
[('stu_name', u'test1'),
 ('stu_sex', u''),
 ('stu_no', u'201457507208'),
 ('stu_birth', datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>)),
 ('stu_age', 20L),
 ('id', 4L)]
```

最后利用dict()这个方法，就可以把数据序列化成标准的键值对象

```
{'id': 4L,
 'stu_age': 20L,
 'stu_birth': datetime.datetime(2017, 9, 26, 2, 59, 1, 191525, tzinfo=<UTC>),
 'stu_name': u'test1',
 'stu_no': u'201457507208',
 'stu_sex': u''}
```

