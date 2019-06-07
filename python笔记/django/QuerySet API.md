# django QuerySet API 进阶

从数据库中查询出来的结果一般是一个集合，这个集合叫做queryset

## 查看Django QuerySet执行的SQL

在python Manage.py shell 里执行下列操作

```
print str(Author.objects.all().query)
```

结果：

```
SELECT `blog_author`.`id`, `blog_author`.`name`, `blog_author`.`qq`, `blog_author`.`addr`, `blog_author`.`email` FROM `blog_author`
```

## values_list 获取元素形式结果

获取作者的name和qq

```
authors = Author.objects.values_list('name','qq')
authors
```

结果：

```
<QuerySet [(u'WeizhongTu', u'039333829'), (u'twz915', u'372770695'), (u'dachui', u'705162036'), (u'zhe', u'814146503'), (u'zhen', u'570022208')]>
```

如果只需要一个字段，可以指定flat=True

```
<QuerySet [u'WeizhongTu', u'twz915', u'dachui', u'zhe', u'zhen']>
```

## values 获取字典形式的结果

比如我们要获取作者的 name 和 qq

```
Author.objects.values('name', 'qq')
<QuerySet [{'qq': u'336643078', 'name': u'WeizhongTu'}, {'qq': u'915792575', 'name': u'twz915'}, {'qq': u'353506297', 'name': u'wangdachui'}, {'qq': u'004466315', 'name': u'xiaoming'}]>
```

### list

```
list(Author.objects.values('name', 'qq'))
[{'name': u'WeizhongTu', 'qq': u'336643078'},
 {'name': u'twz915', 'qq': u'915792575'},
 {'name': u'wangdachui', 'qq': u'353506297'},
 {'name': u'xiaoming', 'qq': u'004466315'}]
```



查询twz915这个人的文章标题

```
Article.objects.filter(author__name='twz915').values('title')
```

结果：

```
<QuerySet [{'title': u'Django \u6559\u7a0b_3'}, {'title': u'Django \u6559\u7a0b_5'}, {'title': u'Django \u6559\u7a0b_7'}]>
```

> 注意：

1. values_list 和 values 返回的并不是真正的 列表 或 字典，也是 queryset，他们也是 lazy evaluation 的（惰性评估，通俗地说，就是用的时候才真正的去数据库查）
2. 如果查询后没有使用，在数据库更新后再使用，你发现得到在是新内容！！！如果想要旧内容保持着，数据库更新后不要变，可以 list 一下
3. 如果只是遍历这些结果，没有必要 list 它们转成列表（浪费内存，数据量大的时候要更谨慎！！！）

## extra 实现 别名，条件，排序等

extra 中可实现别名，条件，排序等，后面两个用 filter, exclude 一般都能实现，排序用 order_by 也能实现。我们主要看一下别名这个

比如 Author 中有 name， Tag 中有 name 我们想执行

SELECT name AS tag_name FROM blog_tag;

这样的语句，就可以用 select 来实现，如下：

```
tags = Tag.objects.all().extra(select={'tag_name':'name'})
tags[0].name
tags[0].tag_name
```

结果是一样的

```
u'Django'
```

## annotate 聚合计数、求和、平均数 

### 计数 

我们来计算一下每个作者的文章数

```
Article.objects.all().values('author_id').annotate(count=Count('author')).values('author_id', 'count')
```

结果：

```
<QuerySet [{'count': 3, 'author_id': 2L}, {'count': 37, 'author_id': 4L}, {'count': 20, 'author_id': 5L}]>
```

工作原理：

```
>>> Article.objects.all().values('author_id').annotate(count=Count('author')).values('author_id', 'count').query.__str__()
u'SELECT `blog_article`.`author_id`, COUNT(`blog_article`.`author_id`) AS `count` FROM `blog_article` GROUP BY `blog_article`.`author_id` ORDER BY NULL'
```

### 求和 平均值

求一个作者的所有文章的得分(score)平均值

```
from django.db.models import Avg
Article.objects.values('author_id').annotate(avg_score=Avg('score')).values('author_id', 'avg_score')
<QuerySet [{'author_id': 1, 'avg_score': 86.05}, {'author_id': 2, 'avg_score': 83.75}, {'author_id': 5, 'avg_score': 85.65}]>
```

求一个作者所有文章的总分

```
from django.db.models import Sum
 Article.objects.values('author__name').annotate(sum_score=Sum('score')).values('author__name', 'sum_score')
<QuerySet [{'author__name': u'WeizhongTu', 'sum_score': 1721}, {'author__name': u'twz915', 'sum_score': 1675}, {'author__name': u'zhen', 'sum_score': 1713}]>
```

## select_related优化一对一，多对一查询 

修改settings配置在尾部添加如下信息：

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}
```

这样当 DEBUG 为 True 的时候，我们可以看出 django 执行了什么 SQL 语句

 

```
  articles = Article.objects.all()[:10]
  a1 = articles[0]  # 取第一篇
  (0.000) SELECT "blog_article"."id", "blog_article"."title", "blog_article"."author_id", "blog_article"."content", "blog_article"."score" FROM "blog_article" LIMIT 1; args=()
 a1.title

 u'Django \u6559\u7a0b_1'

 a1.author_id

 5

 a1.author.name   # 再次查询了数据库，注意！！！

(0.000) SELECT "blog_author"."id", "blog_author"."name", "blog_author"."qq", "blog_author"."addr", "blog_author"."email" FROM "blog_author" WHERE "blog_author"."id" = 5; args=(5,)

u'zhen'

```



这样的话我们遍历查询结果的时候就会查询很多次数据库，能不能只查询一次，把作者的信息也查出来呢？

当然可以，这时就用到 select_related，我们的数据库设计的是一篇文章只能有一个作者，一个作者可以有多篇文章。

现在要查询文章的时候连同作者一起查询出来，“文章”和“作者”的关系就是**多对一**，换句说说，就是一篇文章只可能有一个作者。

```
 articles = Article.objects.all().select_related('author')[:10]

 a1 = articles[0]  # 取第一篇

(0.000) SELECT "blog_article"."id", "blog_article"."title", "blog_article"."author_id", "blog_article"."content", "blog_article"."score", "blog_author"."id", "blog_author"."name", "blog_author"."qq", "blog_author"."addr", "blog_author"."email" FROM "blog_article" INNER JOIN "blog_author" ON ("blog_article"."author_id" = "blog_author"."id") LIMIT 1; args=()

 a1.title

 u'Django \u6559\u7a0b_1'

 a1.author.name   # 嘻嘻，没有再次查询数据库！！

 u'zhen'

```

## prefetch_related 优化一对多，多对多查询

和 select_related 功能类似，但是实现不同。

select_related 是使用 SQL JOIN 一次性取出相关的内容。

prefetch_related 用于 一对多，多对多 的情况，这时 select_related 用不了，因为当前一条有好几条与之相关的内容。

prefetch_related是通过再执行一条额外的SQL语句**，**然后用 Python 把两次SQL查询的内容关联（joining)到一起

我们来看个例子，查询文章的同时，查询文章对应的标签。“文章”与“标签”是多对多的关系。

````
>>> articles = Article.objects.all().prefetch_related('tags')[:10]
>>> articles
(0.001) SELECT `blog_article`.`id`, `blog_article`.`title`, `blog_article`.`author_id`, `blog_article`.`content`, `blog_article`.`score` FROM `blog_article` LIMIT 10; args=()
(0.002) SELECT (`blog_article_tags`.`article_id`) AS `_prefetch_related_val_article_id`, `blog_tag`.`id`, `blog_tag`.`name` FROM `blog_tag` INNER JOIN `blog_article_tags` ON (`blog_tag`.`id` = `blog_article_tags`.`tag_id`) WHERE `blog_article_tags`.`article_id` IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10); args=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
<QuerySet [<Article: Django 教程_1>, <Article: Django 教程_2>, <Article: Django 教程_3>, <Article: Django 教程_4>, <Article: Django 教程_5>, <Article: Django 教程_6>, <Article: Django 教程_7>, <Article: Django 教程_8>, <Article: Django 教程_9>, <Article: Django 教程_10>]>
````

遍历查询结果

不用prefetch_related时

```
>>> articles = Article.objects.all()[:3]
>>> for a in articles:
...  print a.title,a.tags.all()
... 
(0.001) SELECT `blog_article`.`id`, `blog_article`.`title`, `blog_article`.`author_id`, `blog_article`.`content`, `blog_article`.`score` FROM `blog_article` LIMIT 3; args=()
(0.001) SELECT `blog_tag`.`id`, `blog_tag`.`name` FROM `blog_tag` INNER JOIN `blog_article_tags` ON (`blog_tag`.`id` = `blog_article_tags`.`tag_id`) WHERE `blog_article_tags`.`article_id` = 1 LIMIT 21; args=(1,)
Django 教程_1 <QuerySet [<Tag: Django>]>
(0.001) SELECT `blog_tag`.`id`, `blog_tag`.`name` FROM `blog_tag` INNER JOIN `blog_article_tags` ON (`blog_tag`.`id` = `blog_article_tags`.`tag_id`) WHERE `blog_article_tags`.`article_id` = 2 LIMIT 21; args=(2,)
Django 教程_2 <QuerySet [<Tag: Django>]>
(0.001) SELECT `blog_tag`.`id`, `blog_tag`.`name` FROM `blog_tag` INNER JOIN `blog_article_tags` ON (`blog_tag`.`id` = `blog_article_tags`.`tag_id`) WHERE `blog_article_tags`.`article_id` = 3 LIMIT 21; args=(3,)
Django 教程_3 <QuerySet [<Tag: Django>]>
>>> 
```

使用prefetch_related时

```
>>> articles = Article.objects.all().prefetch_related('tags')[:3]
>>> for a in articles:
...  print a.title, a.tags.all()
... 
(0.030) SELECT `blog_article`.`id`, `blog_article`.`title`, `blog_article`.`author_id`, `blog_article`.`content`, `blog_article`.`score` FROM `blog_article` LIMIT 3; args=()
(0.001) SELECT (`blog_article_tags`.`article_id`) AS `_prefetch_related_val_article_id`, `blog_tag`.`id`, `blog_tag`.`name` FROM `blog_tag` INNER JOIN `blog_article_tags` ON (`blog_tag`.`id` = `blog_article_tags`.`tag_id`) WHERE `blog_article_tags`.`article_id` IN (1, 2, 3); args=(1, 2, 3)
Django 教程_1 <QuerySet [<Tag: Django>]>
Django 教程_2 <QuerySet [<Tag: Django>]>
Django 教程_3 <QuerySet [<Tag: Django>]>
>>> 

```

## defer 排除不需要的字段

在复杂的情况下，表中可能有些字段内容非常多，取出来转化成 Python 对象会占用大量的资源。

这时候可以用 defer 来排除这些字段，比如我们在文章列表页，只需要文章的标题和作者，没有必要把文章的内容也获取出来（因为会转换成python对象，浪费内存）

```
Article.objects.all().defer('content')
```

## only 仅选择需要的字段

和 defer 相反，only 用于取出需要的字段，假如我们只需要查出 作者的名称

```
 Author.objects.all().only('name')
```

