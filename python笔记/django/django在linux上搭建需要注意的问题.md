# Django在远程linux下搭建需要注意的几个问题：

启动runserver时需要在命令行后添加 地址和端口号，如下：

```
python manage.py runserver 0.0.0.0:8000
```

修改settings文件，允许访问的主机参数：

```
ALLOWED_HOSTS = ['*']
```

