# Django登录权限控制实现

>django版本:

```
>>> import django
>>> print django.VERSION
(1, 8, 14, 'final', 0)

```
>python版本：

```
[root@new_name ~]# python -V
Python 2.7.5

```
## 一、配置 settings.py

设置中间件
```
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

)
```


## 二、创建用户（create_user)

### 修改 url.py

```
 url(r'^create_user', views.create_user),
```
### 修改 views.py

#### 1. 导包
```
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

```

#### 2. 创建用户方法
利用提供的create_user()方法来保存用户名、密码等信息

```
def create_user(request):
    response={}
    username = request.GET.get('user_name')
    password = request.GET.get('user_pwd')
    email = request.GET.get('email')
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
        response['state'] = '1'
        response['info'] = '创建成功'
    except Exception as e:
        response['state'] = '0'
        response['info'] = '创建失败' + str(e)
    return JsonResponse(response)
```

## 三、用户登录(user_login)
### 修改 url.py

```
    url(r'^user_login', views.user_login),
```
### 登录方法(vews.py)
```
def user_login(request):
    username = request.POST.get('user_name')
    password = request.POST.get('user_pwd')
    url_next = request.POST.get('next')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            request.session['userName'] = usernames
            if url_next == "None":
                return HttpResponseRedirect('/index')
            else:
                return HttpResponseRedirect(url_next)
    else:
        response = "用户名或密码错误"
        return render(request, 'login.html', {'msg': response, 'next': 'None'})
```
## 四、用户注销(user_logout)
### 修改 url.py
```
    url(r'^user_logout', views.user_logout),
```
### 注销方法

```
def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
```

参考文献：
[http://blog.csdn.net/zzg_550413470/article/details/52239867](http://blog.csdn.net/zzg_550413470/article/details/52239867)



