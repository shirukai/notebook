# Django 多语言国际化
>django版本:

```
>>> import django
>>> print django.VERSION
(1, 11, 5, u'final', 0)
>>> 

```

>python版本：

```
[root@new_name ~]# python -V
Python 2.7.5

```
一、 构建Django项目
1. 创建项目

```
django-admin startproject myproject
```
目录结构：

![image](https://shirukai.gitee.io/images/django+vue.png)

2. 进入项目根目录，创建一个app

```
python manage.py startapp language
```
项目目录：

![image](https://shirukai.gitee.io/images/django+vue2.png)

3. 在languagetest下的settings.py中，配置数据库

```
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'language',
        'USER': 'root',
        'PASSWORD': 'inspur',
        'HOST': 'localhost',
    }
}
```
4. 把创建的language 加入到 INSTALLED_APPS列表里

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'language'
]
```
5. 创建模板

在language目录下创建templates目录

然后新建index.html文件

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Django多语言测试</title>
</head>
<body>

</body>
</html>
```

6. 添加视图
 在language目录下的views.py文件中添加：

```
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')

```

7. 添加url


```
from django.conf.urls import url
from django.contrib import admin
from language import views as language_views
urlpatterns = [
    url(r'^$', language_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
```

8. 创建数据库表


```
# 1. 创建更改的文件
python manage.py makemigrations
# 2. 将生成的py文件应用到数据库
python manage.py migrate
```
9. 运行服务器


```
python manage.py runserver 0.0.0.0 8001
```

访问服务器

如果出现如下问题：

![image](https://shirukai.gitee.io/images/django.png)
则需要修改settings配置


```
ALLOWED_HOSTS = ['*']
```


## 二、配置settings
> ==因为settings中用到了中文，为了防止报错，在settings头部添加一行代码如下：==


```
# -*- coding: utf-8 -*-
```




1. 添加中间件

```
MIDDLEWARE_CLASSES = (
#……省略好多中间件……

    'django.middleware.locale.LocaleMiddleware',
    
#……省略好多中间件……
)
```
2. 修改语言设置

```
LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('zh-hans', '中文简体'),
)

```
3. 添加语言目录

```
# 翻译文件所在目录，需要手工创建
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

```
4. 添加i18n上下文渲染器

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```


## 三、创建翻译文件的目录
在manage.py所在目录的根目录创建目录locale

## 四、 修改HTML模板
在头部添加多语言标签

```
<!DOCTYPE html>
{% load i18n %}
```

标注需要翻译的字符串

```
<h1>{% trans "Django多语言国际化测试"  %}</h1>
```

## 四、生成需要翻译的.po文件
在与manage.py同级目录下执行命令生成.po文件

```
python manage.py makemessages -l en

python manage.py makemessages -l zh-hant
```
## 五、编辑生成的.po文件
en文件夹下的.po文件

```
#: language/templates/index.html:9
msgid "Django多语言国际化测试"
msgstr "Django multilingual internationalization test"
```
## 六、编译


```
python manage.py compilemessages
```

## 七、 实现页面动态切换

1. 修改url.py

```
from django.conf.urls import include, url
from django.contrib import admin
from language import views as language_views
urlpatterns = [
    url(r'^$', language_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n'))
]
```
2. 修改 index.html

```
<!DOCTYPE html>
{% load i18n %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Django多语言测试</title>
</head>
<body>
<form action="{% url 'set_language' %}" id="language_form" method="post">
    {% csrf_token %}
    <input name="next" type="hidden" value="{{ redirect_to }}"/>
    <div style="display: flex">
        <label for="language_select" style="line-height: 30px">语言设置：</label>
        <select name="language" id="language_select" onchange="form.submit()">
            <option value="">选择语言</option>
            <option value="zh-hans">简体中文</option>
            <option value="en">English</option>
        </select>
    </div>
</form>
<h1>{% trans "Django多语言国际化测试" %}</h1>
</body>
</html>
```

3. 重启服务

![image](https://shirukai.gitee.io/images/changelanguage.gif)

gitHub源码 ：

[https://github.com/shirukai/Django_international.git](https://github.com/shirukai/Django_international.git)
