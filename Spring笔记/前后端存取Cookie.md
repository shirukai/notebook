# 前后端存取cookie

## 一、前端存取cookie 

### 1.前端jsp存入cookie 

```
<%@ page import="java.util.Map" %>
<%@ page contentType="text/html;charset=UTF-8" language="java"  %>
<html>
<head>
    <title>jsp获取cookie</title>
</head>
<body>
<%
    //创建一个cookie包括（key，value）
    Cookie cookie = new Cookie("jspSetCookie","这是我通过jsp存入的cookie");
    //设置cookie的生命周期，如果为负值的话，关闭浏览器就失效
    cookie.setMaxAge(60*60*24*365);
    // 设置Cookie路径,不设置的话为当前路径(对于Servlet来说为request.getContextPath() + web.xml里配置的该Servlet的url-pattern路径部分)
    //cookie.setPath("/");

    response.addCookie(cookie);
%>
</body>
</html>
```

### 2.前端jsp获取cookie

```
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page import="java.util.Map" %>
<%@ page import="java.util.HashMap" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>前端jsp获取cookie</title>
</head>
<body>
<%
    //将cookie封装到map里
    Map<String, Cookie> cookieMap = new HashMap<String, Cookie>();
    Cookie[] cookies = request.getCookies();
    if (null != cookies) {
        for (Cookie cookie : cookies) {
            cookieMap.put(cookie.getName(), cookie);
        }
    }
%>
<%--显示所有cookie--%>
<table border="1">
    <thead>
    <tr>
        <th>key</th>
        <th>value</th>
    </tr>
    </thead>
    <tbody>
    <%
        for (String key : cookieMap.keySet()
                ) { %>
    <tr>
        <td><%=key%>
        </td>
        <td><%=cookieMap.get(key).getValue()%>
        </td>
    </tr>

    <%
        }
    %>
    </tbody>
</table>
<%--根据key获取cookie--%>
<h2>获取key为jspSetCookie的值：</h2>
<%= cookieMap.get("jspSetCookie").getValue()%>
</body>
</html>
```

### 3.前端js存入cookie 

引入jquery-cookie.js和jquery.js文件

https://cdn.bootcss.com/jquery/3.2.1/core.js

https://cdn.bootcss.com/jquery-cookie/1.4.1/jquery.cookie.js

```
//js存入cookie expires:有效期 path:按个路径有效
//是否自动进行编码和解码，true为关闭
$.cookie.raw = true;
//将数据转为json
$.cookie.json= true;
$.cookie("jsSetCookie","这是我通过js存入的cookie",{expires:7,path:'/'});
    var jsonData = {
        'name':{
            'data1':11,
            'data2':22
        }
    };
    $.cookie("jsonData",jsonData);
```



### 4.前端读取cookie 

```
$.cookie('jsSetCookie')
```



### jquery-cookie.js使用说明：

- 创建一个整站cookie

```
$.cookie('name', 'value');1
```

- 创建一个整站cookie ，cookie 的有效期为 7 天

```
$.cookie('name', 'value', { expires: 7 });1
```

- 创建一个仅对 `path` 路径页面有效的 cookie ，cookie 的有效期为 7 天

```
$.cookie('name', 'value', { expires: 7, path: '/' });1
```

- 读取 cookie

```
$.cookie('name'); // 如果cookie存在 则获取到cookie值 => 'value'
$.cookie('nothing'); // 如果cookie不存在 则返回 => undefined12
```

- 获取所有可见的 cookie

```
$.cookie(); // 数据格式 => { name: 'value' }1
```

- 删除 cookie

```
$.removeCookie('name'); // => true
$.removeCookie('nothing'); // => false12
```

- 删除带属性的cookie

```
$.cookie('name', 'value', { path: '/' });
// 错误
$.removeCookie('name'); // => false
// 正确
$.removeCookie('name', { path: '/' }); // => true
```

#### 属性 

##### domain 

创建cookie所在网页所拥有的域名

```
$.cookie('name', 'value', { domain: 'weber.pub' });1
```

##### secure 

默认是false，如果为true，cookie的传输协议需为https；

```
$.cookie('name', 'value', { secure: true });
$.cookie('name'); // => 'value'
$.removeCookie('name', { secure: true }); 123
```

##### raw 

默认为false，读取和写入时候自动进行编码和解码（使用encodeURIComponent编码，使用decodeURIComponent解码），关闭这个功能，请设置为true。

```
$.cookie.raw = true;1
```

##### json 

```
$.cookie.json = true;
```

### 注意： row属性 

默认jquery-cookie是开启自动编码和解码的。如果要开启的话，后台获取的是经过encodeURIComponent编码的value。

#### java来解码encodeURIComponent编码的value： 

```
try{
    String value =  URLDecoder.decode(cookieMap.get("jsonData").getValue(),"UTF-8");
    System.out.println("____________value___________="+value);
    map.put("testCookie", testCooke);
}catch (UnsupportedEncodingException e){
    e.printStackTrace();
}
```

#### java来encodeURI编码 

```
try{
    String encodeValue = URLEncoder.encode("这是我利用controller存入的，经过encode编码后的cookie","UTF-8");
    response.addCookie(new Cookie("encodeCookie",encodeValue));
}catch (UnsupportedEncodingException e){
    e.printStackTrace();
}
```

如果$.cookie.raw = true;前端不进行自动编码与解码。数据会原样输出，默认是false,自动进行编解码。

如果$.cookie.json属性设置为true，编解码的cookie将查询不到，注意这个问题，具体原因不知道。

## 二、后端存取cookie(controller) 

### 1.后端存入cookie 及编码

```
//controller 存入cookie
@RequestMapping(value = "/setCookie")
@ResponseBody
public Map<String, String> setCookie(
        HttpServletResponse response
) {
    // 存入
    Cookie cookie = new Cookie("controllerSetCookie","这是我通过后台添加的cookie");
    //设置cookie的生命周期，如果为负值的话，关闭浏览器就失效
    cookie.setMaxAge(60*60*24*365);
    // 设置Cookie路径,不设置的话为当前路径(对于Servlet来说为request.getContextPath() + web.xml里配置的该Servlet的url-pattern路径部分)
    //cookie.setPath("/");
    response.addCookie(cookie);
    try{
        String encodeValue = URLEncoder.encode("这是我利用controller存入的，经过encode编码后的cookie","UTF-8");
        response.addCookie(new Cookie("encodeCookie",encodeValue));
    }catch (UnsupportedEncodingException e){
        e.printStackTrace();
    }

    Map<String, String> map = new HashMap<String, String>();
    map.put("info", "存入成功");
    return map;
}
```

### 2.后端读取cookie 及解码

（1）通过注解的方式直接获取value

  @CookieValue(value = "testCookie", required = false) String testCooke（适用于少量cookie的情况下）

（2）通过request.getCookies()获取所有cookie，然后遍历分装到map里，然后读取（适用于多个cookie的情况）

```
// controller 读取cookie
@RequestMapping(value = "/getCookie")
@ResponseBody
public Map<String, Cookie> getCookie(
        @CookieValue(value = "testCookie", required = false) String testCooke,
        HttpServletRequest request
) {
    //将cookie封装到map里
    Map<String,Cookie> cookieMap = new HashMap<String, Cookie>();
    Cookie[] cookies =request.getCookies();
    if (null != cookies){
        for(Cookie cookie:cookies){
            cookieMap.put(cookie.getName(),cookie);
        }
    }
    Map<String, String> map = new HashMap<String, String>();
    try{
        String value =  URLDecoder.decode(cookieMap.get("jsonData").getValue(),"UTF-8");
        System.out.println("____________value___________="+value);
        map.put("testCookie", testCooke);
    }catch (UnsupportedEncodingException e){
        e.printStackTrace();
    }

    return cookieMap;
}
```

其他操作http://blog.csdn.net/u011848397/article/details/52201339