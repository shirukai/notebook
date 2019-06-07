# Django 模板组件化

Django中也有模板组件化的思想。在模板的应用中有包含、继承的概念。

## 包含：include

> 不难理解，包含就是指一个模板里包含另一模板里内容

举个栗子

比如我们要再A.html里应用B.html里的内容，也就是A里包含B，我们可以这样写：

```
<!DOCTYPE html>
<html>
<head>
    <title>title</title>
</head>
<body> 
{% include 'B.html' %}
</body>
</html>
```

用

```
{% include 'B.html' %}
```

来写即可。这时候A里引用的js或者css，B都可以使用。所以B模板里可以只写body里的代码，如：

```
<div>
    <h1>我是B模板</h1>
</div>
```

## 继承：extends

> 所谓继承就是子页面可以继承父页面的里内容，也可以重写父页面的某些内容

举个栗子

比如我们要C.html继承A.html，并且重写指定部分的代码：

#### A.html

```English
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}默认标题{% endblock %}</title>
</head>
<body>
{% include 'B.html' %}
{% block content %}
<div>这里是默认内容，所有继承自这个模板的，如果不覆盖就显示这里的默认内容。</div>
{% endblock %}

</body>
</html>
```

#### C.html

```
{% extends 'A.html' %}
{% block title %}欢迎光临首页{% endblock %}
{% block content %}
这里是C页面，欢迎光临
{% endblock %}
```

说明：

```
block 标签是告诉django我这个地方是可以重写的。比如A页面里有个{% block title %}默认标题{% endblock %}，我在C页面同样通过{% block title %}欢迎光临首页{% endblock %}这个标签就可以重写A页面相对应的部分了。同理{% block content %}{% endblock %}标签也是一样的道理。
```

无论是继承还是包含，子页面里都可以使用父页面里引入的js和css。

