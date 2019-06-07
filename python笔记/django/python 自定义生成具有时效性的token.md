# 原理
>注意测试django版本：

```
>>> import django
>>> print django.VERSION
(1, 11, 5, u'final', 0)

```

## 生成token

### 第一步：随机生成sha1秘钥
利用python里的hashlib库生成 sha1秘钥，这是一个单向加密过程，给这个sha1秘钥起名为sha1_token。
### 第二步：生成时间戳秘钥
获取当前的时间戳（秒级单位），以及设置token的失效性的时间戳（秒级单位）。将两个时间戳中间用“：”拼接成新的字符串。然后利用python里的base64库将时间戳字符串生成base编码，这里命名为time_token。

### 第三步：拼接token
将两次生成的token拼接起来，就是我们需要的token

## 检验token时效性

### 第一步：截取字符串
这里我们需要截取带有时间戳的编码的字符串，因为生成token时sha1的秘钥长度是一定的，这时候我们就可以很容易截取到时间戳字符串。
### 第二步：解码、分割
将获取的时间戳字符串进行解码，然后利用‘：’进行分割，生成创建token时的时间戳，和时效性时间戳
### 检验
获取当前的时间戳减去 创建token的时间戳与时效性时间戳做比较，如果超过这个范围，说明失效。

## 关于base64编码中特殊符号以及==对url传输数据的影响处理方式
1. 利用利用urlsafe_b64encode(s).strip().lstrip().rstrip('=')来去除特殊符号，空格，以及=号

2. 根据字符串长度对4求余数来判断后面=号有多少，解码的时候自动加上

## 实现


```
import hashlib
import os
import time
import base64

def generate_token(aging):
    # 加密
    sha1_token = hashlib.sha1(os.urandom(24)).hexdigest()
    create_time = int(time.time())
    time_group = str(create_time)+":"+str(aging)
    # 当前时间+时间间隔 生成base64编码 并且去掉 '='
    time_token = base64.urlsafe_b64encode(time_group).strip().lstrip().rstrip('=')
    token = sha1_token+time_token
    return token


def checkout_token(token):
    result = {}
    decode_time = safe_b64decode(token[40:])
    # 分割时间字符串
    decode_split_time = decode_time.split(':')
    # 解密创建时间
    decode_create_time = decode_split_time[0]
    # 解密时效
    decode_aging_time = decode_split_time[1]
    # 获取当前时间
    now_time = int(time.time())
    # 时间差
    difference_time = now_time-int(decode_create_time)
    # 判断 是否失效 如果失效state值为0，生成新的token
    if difference_time > int(decode_aging_time):
        result['state'] = 0
        result['token'] = generate_token(decode_aging_time)
    else:
        result['state'] = 1
        result['token'] = token
    return result


# base64'='符号添加

def safe_b64decode(s):
    length = len(s) % 4
    for i in range(length):
        s = s + '='
    return base64.b64decode(s)
```
