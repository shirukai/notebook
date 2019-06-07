# django查询结果转json的几种方法

## 第一种：利用serializers转换

```
def json_test(request):
    data = {}
    book = Book.objects.all()
    data['list'] = json.loads(serializers.serialize("json", book))
    return JsonResponse(data)
```

得到的结果：

```
{
  "list": [
    {
      "pk": 3,
      "model": "myapp.book",
      "fields": {
        "book_name": "test",
        "add_time": "2017-09-15T00:48:45.123Z"
      }
    },
    {
      "pk": 14,
      "model": "myapp.book",
      "fields": {
        "book_name": "可以吗",
        "add_time": "2017-09-16T03:47:02.662Z"
      }
    },
    {
      "pk": 18,
      "model": "myapp.book",
      "fields": {
        "book_name": "dfs dsf ",
        "add_time": "2017-09-16T06:10:53.834Z"
      }
    },
    {
      "pk": 44,
      "model": "myapp.book",
      "fields": {
        "book_name": "122323",
        "add_time": "2017-09-25T07:15:56.058Z"
      }
    }
  ]
}
```

* 支持objects.all()的所有操作，如切片查询all()[:10]、链式过滤查询objects.all().filter(book_name='test')等价于objects.filter(book_name='test')等

* 支持objects.fifter()的所有操作

* 支持objects.values()的所有操作(但如果使用values的话，可以使用第二种方法转化json)

  ​

## 第二种 利用values+list转换

```
def json_test(request):
    data = {}
    book = Book.objects.values()
    data['list'] = list(book)
    return JsonResponse(data)
```

得到结果

```
{
  "list": [
    {
      "id": 3,
      "book_name": "test",
      "add_time": "2017-09-15T00:48:45.123Z"
    },
    {
      "id": 14,
      "book_name": "可以吗",
      "add_time": "2017-09-16T03:47:02.662Z"
    },
    {
      "id": 18,
      "book_name": "dfs dsf ",
      "add_time": "2017-09-16T06:10:53.834Z"
    },
    {
      "id": 44,
      "book_name": "122323",
      "add_time": "2017-09-25T07:15:56.058Z"
    }
  ]
}
```

这样的结果更简洁，也更适合使用。

* 同样支持链式条件过滤查询，如objects.values().filter(book_name='test')

* 支持切片查询，如objects.values()[:10]

* 支持字段过滤查询，如我只想查询id和book_name 这两个字段，只需这样写

  ```
  book = Book.objects.values('id','book_name')
  ```

### 第三种 转换objects.get()获取的对象

利用一下方法：

```
dict([(kk,stu.__dict__[kk]) for kk in stu.__dict__.keys() if kk != "_state"])
```

例子

```
base_config = BaseConfig.objects.get(config_name=config_name)
response['data'] = object_to_json(base_config)


# objects.get()结果转换
def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])
```