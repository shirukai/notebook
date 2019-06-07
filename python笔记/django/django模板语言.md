# django模板语言

### 一、``` {{}} ```获取render字典

如views.py

```
def index(request):
    return render(request, 'index.html', {'hello': 'hello blog'})
```

templates/index.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>index</title>
</head>
<body>
<h1>Hello blog</h1>
{{ hello }}
</body>
</html>
```

### 二、模板for循环 

views.py

```
def index(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'index.html', {'TutorialList': TutorialList})
```

templates/index.html

```
<h1>模板for循环</h1>
{% for aa in TutorialList %}
{{ aa }}
{% endfor %}
```

### 三、显示字典中的内容  

views.py

```
def index(request):
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    return render(request, 'index.html', {'info_dict': info_dict})
```

templates/index.html

```
<h1>显示字典内容</h1>
站点：{{ info_dict.site }}内容：{{ info_dict.content }}
```

模板还可以这样遍历字典：

```
{% for key, value in info_dict.items %}
    {{ key }}: {{ value }}
{% endfor %}
```

### 四、模板汇中显示当前网址，当前用户等

获取当前用户

{{ request.user }}

用户名{{ request.user.username }}

获取当前网址

{{ request.path }}

获取当前GET参数

{{ request.GET.urlencode }}