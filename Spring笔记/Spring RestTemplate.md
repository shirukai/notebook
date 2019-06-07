# Spring RestTemplate 

发送请求除了使用httpclient之外，我们也可以使用spring的 RestTemplate

## GET请求 

在RestTemplate里可以通过getForEntity和getForObject发送请求。

### getForEntity

getForEntity方法的返回值是一个`ResponseEntity<T>`，`ResponseEntity<T>`是Spring对HTTP请求响应的封装，包括了几个重要的元素，如响应码、contentType、contentLength、响应消息体等。如：我们请求www.baidu.com

获取restTemplate实例

```
    private static RestTemplate restTemplate = null;

    static {
        SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
        requestFactory.setConnectTimeout(2000);
        requestFactory.setReadTimeout(2000);
        restTemplate = new RestTemplate(requestFactory);
    }
```

get请求www.baidu.com

````
        String URL = "http://www.baidu.com";
        ResponseEntity<String> responseEntity = restTemplate.getForEntity(URL, String.class);
        //获取状态码
        System.out.println(responseEntity.getStatusCode());
        //获取状态代码值
        System.out.println(responseEntity.getStatusCodeValue());
        //获取header
        System.out.println(responseEntity.getHeaders());
        //获取body
        System.out.println(responseEntity.getBody());
````

![](https://shirukai.gitee.io/images/201804171633_933.png)

### getForObject 

getForObject 函数实际上是对getForEntity函数的进一步封装，如果只关注返回的消息体的内容，对其他信息都不关注，可以用getForObject

```
        String string = restTemplate.getForObject(URL, String.class);
        System.out.println(string);
```

![](https://shirukai.gitee.io/images/201804171658_340.png)



#### Get传参方式

占位符方式

```
String string = restTemplate.getForObject("http://www.baidu.com?name={1}", String.class,"张三");
```

Map方式

```
Map<String, String> map = new HashMap<>();
map.put("name", "张三");
String string = restTemplate.getForObject("http://www.baidu.com?name={name}", String.class, map);
```

## POST请求

### postForEntity

```
Map<String, String> map = new HashMap<>();
map.put("name", "张三");
ResponseEntity responseEntity = restTemplate.postForEntity("http://www.baidu.com", map, String.class);
```

### postForObject

```
Map<String, String> map = new HashMap<>();
map.put("name", "张三");
String result = restTemplate.postForObject("http://www.baidu.com", map, String.class);
System.out.println(result);
```

带有头信息与参数的post请求

```
        HttpHeaders hs = new HttpHeaders();
        hs.add("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");
        hs.add("X-Requested-With", "XMLHttpRequest");
        LinkedMultiValueMap<String, String> linkedMultiValueMap = new LinkedMultiValueMap<>();
        linkedMultiValueMap.add("name", "张三");
        HttpEntity<LinkedMultiValueMap<String, String>> httpEntity = new HttpEntity<>(linkedMultiValueMap, hs);
        String result = restTemplate.postForObject("http://www.baidu.com", httpEntity, String.class);
```

