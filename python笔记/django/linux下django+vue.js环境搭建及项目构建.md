# Django+Vue 环境搭建及项目整合构建

## 一、环境搭建 

>python: 2.7.5
>
>django: 1.11.7
>
>node: 8.5.0
>
>mysql: 5.7

### 1. 安装python
centos下默认已经安装了python

### 2. 安装 node.js
下载安装包 [版本地址](https://nodejs.org/dist/)

```
wget https://nodejs.org/dist/v8.5.0/node-v8.5.0-linux-x64.tar.gz
```
解压

```
tar zxvf node-v8.5.0-linux-x64.tar.gz
```
配置环境变量/etc/profile

```
export NODE_HOME="/root/node-v8.5.0-linux-x64"
export PATH=$PATH:$NODE_HOME/bin
```
使修改后的文件生效

```
source /etc/profile
```
查看安装情况

```
node -v
npm -v
```

### 3. 安装mysql

安装mysql源

```
wget http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
rpm -ivh mysql57-community-release-el7-9.noarch.rpm
```

安装

```
yum install mysql-community-server
```

启动mysql

```
service mysqld start
```

查看初始密码

```
grep 'temporary password' /var/log/mysqld.log
```

使用初始密码登录

```
mysql -u root -p //回车，然后输入上一步查到的初始密码
```

更改初始密码

```
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456Aa?';
```

创建名为config_tool的数据库

```
mysql> create database config_tool;
Query OK, 1 row affected (0.00 sec)

```



### 4. 安装pip


```
yum install python-pip
```
如果yum源中没有这个安装包，需要安装epel扩展源，然后再尝试安装

```
yum -y install epel-release
```

### 5. 安装Django 

```
pip install Django==1.11.7
# 查看django版本
python -m django --version
```
![](https://shirukai.gitee.io/images/201801171551_800.png)



### 6. 安装vue-cli 

安装cnpm

安装npm淘宝源cnpm：在cmd下运行 

	​```
	npm install -g cnpm --registry=https://registry.npm.taobao.org
	​```
安装vue-cli

```
//安装全局的vue-cli命令行工具
cnpm install -g vue-cli
```

#### 7.安装samba服务 

由于是环境是在linux虚拟机上，我们需要在windows下开发，这时候就需要用到samba服务来共享数据。

检查是否安装

```
#rpm -qa | grep samba
```

未安装的话，执行安装命令

```
yum install samba
```

重启smb服务

```
service smb restart
```

在Linux上建立samba用户

```
useradd samba
```

创建Smb用户，此用户必须是Linux上已经建立的，输入密码，完成即可

```
smbpasswd -a root
```

> 注意：smbpasswd  -a 是添加用户的意思 后面跟的是用户名，此用户名一定要跟linux登录用户名一样。smbpasswd -x 用户名 ：是删除用户的意思

添加共享目录到samba,修改/etc/samba/smb.conf

```
[indta_dev]
        path = /root/indata_dev
        browsable=yes
        writable=yes
        guest ok=yes
        read only=no
```

重启samba服务

在windos下打开计算机，在导航栏输入 `\\192.168.162.111`

![](https://shirukai.gitee.io/images/201801171910_90.png)

输入用户名和密码，然后右击indata_dev目录，选择映射到网络磁盘驱动器，然后点击【完成】

![](https://shirukai.gitee.io/images/201801180817_987.png)



#### 8.关闭防火墙 

```
systemctl stop firewalld
systemctl disable firewalld
systemctl is-enabled firewalld
改/etc/selinux/config文件中设置SELINUX=disabled
```



## 二、构建项目

### 构建Django项目 

#### 1. 创建项目 

在指定目录下创建一个名字为indata_dev的项目

```
django-admin startproject indata_dev
```
#### 2. 创建APP

切换到上一步创建的项目indata_dev目录下

```
cd indata_dev
```

然后创建利用下面的命令创建一个名为 indata_tool_api 的app

```
python manage.py startapp indata_tool_api
```
目录结构：

![](https://shirukai.gitee.io/images/201801171547_405.png)

#### 3.配置数据库 

django默认配置的数据库是 sqlite3，这个数据库无需安装配置，直接就可以用，但是不支持并发操作，性能上不如mysql。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```

所以我们选用mysql数据库，配置在 indata_dev/settiongs.py里，如下图所示：

name 为数据库的名字,user 为mysql的用户名，password为msql用户密码 host，host是主机地址

```
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'config_tool',
        'USER': 'root',
        'PASSWORD': '123456Aa?',
        'HOST': 'localhost',
    }
}
```
#### 4. 添加app到列表 

把创建的 indata_tool_api 加入到 settings.py中的 INSTALLED_APPS列表里

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'indata_tool_api'
]
```

#### 5. 创建测试model

在indata_tool_api目录下的models.py里我们写一个测试model 如下：

 ```
# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class TestModel(models.Model):
    model_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)
 ```

#### 6.创建测试方法 

在indta_tool_api 目录下的views.py里创建两个测试方法如下：

```
# -*- coding: utf-8 -*-
from django.http import JsonResponse
from indata_tool_api.models import TestModel


def add_model(request):
    model_name = request.GET.get('model_name')
    response = {}
    try:
        test_model = TestModel(model_name=model_name)
        test_model.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def show_models(request):
    response = {}
    try:
        test_model = TestModel.objects.values()
        response['list'] = list(test_model)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception, e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
```

#### 7.配置URL 

在app目录下创建一个urls.py的文件

```
from django.conf.urls import url, include
from indata_tool_api import views

urlpatterns = [
url(r'add_model$', views.add_model, ),
url(r'show_models$', views.show_models, ),
]
```

把app下的urls.py添加到项目下的urls里。在indata_dev/indta_dev/urls.py里

```
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import indata_tool_api.urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(indata_tool_api.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
```

#### 8.初始化数据库表

在项目根目录下运行如下命令，用以生成创建或更改数据库表结构的文件：

```
python manage.py makemigrations
```

将更改应用到数据库

```
python manage.py migrate
```

注意在执行第一条命令的时候会报错：

![](https://shirukai.gitee.io/images/201801171636_114.png)

看错误信息，是因为我们没有安装 mysqlclient导致的。所以我们可以通过pip安装

```
pip install mysqlclient
```

![](https://shirukai.gitee.io/images/201801171638_670.png)

但是在安装mysqlclient的时候报错了，原因是没有安装 mysql-devel导致的。

所以利用yum安装mysql-devel

```
yum install mysql-devel
```

![](https://shirukai.gitee.io/images/201801171649_295.png)

仍然报错。。错误信息提示没有安装gcc，执行如下命令安装gcc以及依赖环境

```
yum install gcc libffi-devel python-devel openssl-devel
```

![](https://shirukai.gitee.io/images/201801171656_435.png)



执行完上面命令之后，我们就可以看到数据库中被创建了我们需要的表。

![](https://shirukai.gitee.io/images/201801171701_586.png)

#### 9. 运行django项目

```
python manage.py runserver 0.0.0.0:8000 

```

```
[root@localhost indata_dev]# python manage.py runserver 0.0.0.0:8000
Performing system checks...

System check identified no issues (0 silenced).
January 17, 2018 - 09:02:38
Django version 1.11.7, using settings 'indata_dev.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

```

![](https://shirukai.gitee.io/images/201801171708_768.png)

报错，因为django不允许其他host访问，所以我们可以通过修改settings.py里的配置，来允许所有hosts访问

```
ALLOWED_HOSTS = ['*']
```

![](https://shirukai.gitee.io/images/201801171710_107.png)

#### 10.测试api 

写入数据

![](https://shirukai.gitee.io/images/201801171826_772.png)

读取数据

![](https://shirukai.gitee.io/images/201801171839_481.png)

### 构建VUE项目 

#### 1.创建项目 

在indta_dev项目根目录下运行如下命令，创建VUE项目

```
vue-init webpack indata_tool_web
```

![](https://shirukai.gitee.io/images/201801171849_253.png)

创建过程需要填写项目名、描述、作者、以及一些选项。

#### 2.启动服务 

创建完成后，我们进入该vue项目indta_tool_web下进入config目录修改index.js，修改host为0.0.0.0

```
 host: '0.0.0.0', 
```

然后保存退出。

在VUE项目根目录下，运行如下命令，启动vue server测试vue项目是否创建成功

```
npm run dev
```

![](https://shirukai.gitee.io/images/201801171855_204.png)

访问：192.168.162.111:8080

![](https://shirukai.gitee.io/images/201801171854_162.png)

#### 3.安装组件 

vue-router 路由功能（已安装）

vue-resource 用于发送http请求

element-ui 饿了吗ui组件库

nprogress 进度条（可选）

##### 安装vue-resource 

在vue项目根目录运行如下命令：

```
npm install vue-resource
```

![](https://shirukai.gitee.io/images/201801180848_626.png)

在indata_tool_web\src\main.js里引入vue-resource

```
import VueResource from 'vue-resource'
Vue.use(VueResource)
```

##### 安装element-ui 

在vue项目根目录运行如下命令：

```
npm install element-ui
```

![](https://shirukai.gitee.io/images/201801180852_553.png)

在indata_tool_web\src\main.js里引入element-ui

```
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)
```

##### 安装 nprogress  

```
npm install nprogress
```

![](https://shirukai.gitee.io/images/201801180857_547.png)

在indata_tool_web\src\main.js里引入nprogress

```
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css'// Progress 进度条样式
```



## 三、项目整合 

前面我们已经把django、vue的环境搭建起来，以及能够使他们各自能独立运行起来，下面我们将对两个项目进行整合开发。

### 1. 项目导入pycharm 

![](https://shirukai.gitee.io/images/201801180835_101.gif)

### 2. 调用api

在vue 项目里测试调用django的api.

修改indata_tool_web\src\components\HelloWorld.vue，添加如下代码：

```
<template>
  <div>
    <el-input v-model="model_name"></el-input>
    <el-button type="primary" @click="addModel">提交</el-button>
  </div>
</template>
```

```
export default {
  name: 'HelloWorld',
  data() {
    return {
      model_name: ''
    }
  },
  methods: {
    addModel() {
      this.$http.get('http://192.168.162.111:8000/api/add_model?model_name=' + this.add_model).then(
        (response) => {
          const res = JSON.parse(response.bodyText);
          //console.log(res);
        },
        (response) => {
        }
      );
    }
  }
}
```

![](https://shirukai.gitee.io/images/201801180917_733.png)

出现这种错误，是django不允许跨域的问题，所以我们需要设置django允许跨域访问。这时候我们须要在Django层注入header，用Django的第三方包`django-cors-headers`来解决跨域问题：

```
  pip install django-cors-headers
```

![](https://shirukai.gitee.io/images/201801180919_585.png)

修改settings.py

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
```

![](https://shirukai.gitee.io/images/201801180920_257.png)

### 3.打包vue 

在前端工程目录下，输入`npm run build`，如果项目没有错误的话，就能够看到所有的组件、css、图片等都被webpack自动打包到dist目录下了：

![](https://shirukai.gitee.io/images/201801180925_919.png)

### 4.Django、vue整合

>  将django的TemplateView指向我们刚才生成的前端dist文件 

找到project目录的urls.py，使用通用视图创建最简单的模板控制器，访问 『/』时直接返回 index.html:

```
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import indata_tool_api.urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(indata_tool_api.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
```

上一步使用了Django的模板系统，所以需要配置一下模板使Django知道从哪里找到index.html。在project目录的settings.py下：

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['indata_tool_web/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

我们还需要配置一下静态文件的搜索路径。同样是project目录的settings.py下：

```
# Add for vuejs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "indata_tool_web/dist/static"),
]
```

配置完成，我们在project目录下输入命令`python manage.py runserver 0.0.0.0:8000`，就能够看到我们的前端页面在浏览器上展现：

![](https://shirukai.gitee.io/images/201801180932_190.png)

至此，一个django+vue的环境以及整合项目就搭建完成了。

参考文章：[https://www.qcloud.com/community/article/774449：	](https://www.qcloud.com/community/article/774449)