# django返回对象Response

https://www.cnblogs.com/huwei934/p/6978641.html

## 一、不调用模板 

不使用模板，直接返回数据,如：

```
def test_response(request):
    return HttpResponse('this is response test!')
```

![](https://shirukai.gitee.io/images/201802041429_170.png)

## 二、调用模板 

```
from django.template import loader

def test_response(request):
    t1 = loader.get_template('index.html')
    context = {'h1': 'hello'}
    return HttpResponse(t1.render(context))
```



## 三、HttpResponse属性

- content：表示返回的内容，字符串类型
- charset：表示response采用的编码字符集，字符串类型
- status_code：响应的HTTP响应状态码
- content-type：指定输出的MIME类型

## 四、HttpResponse方法 

- init ：使用页内容实例化HttpResponse对象
- write(content)：以文件的方式写
- flush()：以文件的方式输出缓存区
- set_cookie(key, value='', max_age=None, expires=None)：设置Cookie
  - key、value都是字符串类型
  - max_age是一个整数，表示在指定秒数后过期
  - expires是一个datetime或timedelta对象，会话将在这个指定的日期/时间过期，注意datetime和timedelta值只有在使用PickleSerializer时才可序列化
  - max_age与expires二选一
  - 如果不指定过期时间，则两个星期后过期

## 五、简写函数

### render(request,template_name,content=None,content_type=None,status=None,using=None)

- render(request, template_name[, context])
- 结合一个给定的模板和一个给定的上下文字典，并返回一个渲染后的HttpResponse对象
- request：该request用于生成response
- template_name：要使用的模板的完整名称
- context：添加到模板上下文的一个字典，视图将在渲染模板之前调用它

```
from django.shortcuts import render
def test_response(request):
    return render(request, 'index.html', {'11': '1111'})
```

## 六、常见用法 

### 1.返回json数据

#### HttpResponse

```
    data = {
        'test1': 1,
        'test2': 2,
        'test3': 3
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
```

![](https://shirukai.gitee.io/images/201802041602_653.png)

#### 子类JsonResponse

```
def test_response(request):
    data = {
        'test1': 1,
        'test2': 2,
        'test3': 3
    }
    return JsonResponse(data)
```

![](https://shirukai.gitee.io/images/201802041603_487.png)

### 2.写入cookie

#### 不带模板写入：

##### JsonResponse

```
def test_response(request):
    data = {
        'test1': 1,
        'test2': 2,
        'test3': 3
    }
    response = JsonResponse(data)
    response.set_cookie('test_cookie', "test")
    return response
```

##### HttpResponse

```
def test_response(request):
    data = {
        'test1': 1,
        'test2': 2,
        'test3': 3
    }
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response.set_cookie('test_cookie', "test")
    return response
```



#### 带模板写入： 

##### render_to_response 

```
from django.shortcuts import render, render_to_response

def test_response(request):
    response = render_to_response('index.html', {'test': 'hello'})
    response.set_cookie('test_cookie', 'set cookie')
    return response
```

