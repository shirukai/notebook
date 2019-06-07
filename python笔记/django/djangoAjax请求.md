# Django Ajax POST请求

> Django 中自带了防止CSRF攻击的功能，所以在表单或者Ajax发送POST的请求的时候，如果没有带有`csrf_token` ，请求会被拒绝

## 设置django表单提交

GET请求不需要csrf认证，POST请求需要认证才能得到正确的结果。一般在POST表单中加入

```
{% csrf_token%}
```

```
<form method="POST" action="/post-url/">
    {% csrf_token %}
    <input name='zqxt' value="">
    <button type='submit'>提交</button>
</form>
```

## 设置Ajax POST 提交

### 模板中`<script>`标签写法

```
<script type="text/javascript">
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});
</script>
```

在模板里的`<script>`标签中直接加上如上的代码，然后ajax post请求就跟之前一样使用即可

### 引入js写法，引入csrf.js

js代码如下

```
/*====================django ajax ======*/
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
/*===============================django ajax end===*/
```

#### 也可以 

在views.py里面添加from django.views.decorators.csrf import csrf_exempt
在你ajax要用到的方法前面加一个`@csrf_exempt`

#### 项目案例：

##### 模板HTML

```
<h1>Django ajax POST 方法测试</h1>
<input id="ajaxTest" value=""><button id="send">ajax测试POST</button><br>
测试结果：<h4 style="color: red" id="result"></h4>
csrf_token:{{ csrf_token }}
```

##### 模板js

需要引入jquery

```
<script type="text/javascript">
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' }
});
$('#send').click(function () {
    $.ajax({
    type:'POST',
    url:'/testAjax',
    data: {'test':$('#ajaxTest').val()},
    success: function (data) {
        if(data.state = 1){
             $('#result').text("POST请求成功！返回值为："+data.info);
        }
        console.log(data)
    }
})
});
</script>
```

##### url.py

```
from language import views as language_views
url(r'^testAjax', language_views.test_ajax)
```

##### views.py

```
from django.http import JsonResponse
def test_ajax(request):
    result = {}
    if request.POST:
        result['state'] = 1
        result['info'] = request.POST.get('test')
    return JsonResponse(result)
```

### 或者注释掉settings里的一个中间件：

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # 这个中间件注释掉
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```



##### 效果：

![https://shirukai.gitee.io/images/djangoAjaxPost.gif](https://shirukai.gitee.io/images/djangoAjaxPost.gif)

