# Settings详解

### 项目根目录：

```
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### 项目安全码：

```
SECRET_KEY = ')b)3406p#v$u4ft(v@9ex*=0*w1l*=0v0ixdrey)mmcd2uf#(x'
```

### DEBUG调试：

```
DEBUG = True
```

> 不要在实际生产中打开debug

### 允许访问的主机：

```
ALLOWED_HOSTS = ['*']
```

> *是代表允许所有主机访问

### 已安装的应用：

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp'
]
```

> 如果我们自己创建了应用需要把应用名添加到这个地方

### 中间件（工具集）：

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
```

### url根文件：

```
ROOT_URLCONF = 'myproject.urls'
```

### 模板配置： 

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['appfront/dist'],
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

### 数据库配置： 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'root',
        'PASSWORD': 'inspur',
        'HOST': 'localhost',
    }
}
```

> https://docs.djangoproject.com/en/1.11/ref/settings/#databases 这个网址里有不同的数据的配置方式

### 密码认证：

```
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### 国际化： 

```
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

### 静态文件地址： 

```
STATIC_URL = '/static/'
```