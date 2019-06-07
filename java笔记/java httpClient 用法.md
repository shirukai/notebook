# java httpClient 用法 

> 当我们需要利用java在后台发送http请求，并对请求之后的数据处理时，我们可以用HttpClient来实现。下面是学习官网文档，关于HttpClient的用法。
>
> http://hc.apache.org/httpcomponents-client-ga/tutorial/html/fundamentals.html



maven引入依赖jar包

```
    <!--http请求依赖-->
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpclient</artifactId>
      <version>4.5.2</version>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore</artifactId>
      <version>4.4.6</version>
    </dependency>
```

## 一、基础 

### 1.1 请求执行 Request Execution

HttpClient最重要的功能是执行HTTP方法。执行HTTP方法涉及一个或多个HTTP请求/ HTTP响应交换，通常由HttpClient内部处理。用户需要提供一个请求对象来执行，并且HttpClient需要向目标服务器传送请求返回相应的响应对象，或者如果执行不成功则抛出异常。

很自然地，HttpClient API的主要入口点是定义上述合同的HttpClient接口。

简单的请求实例

```
         CloseableHttpClient httpClient = HttpClients.createDefault();
         HttpGet httpGet = new HttpGet("http://10.110.13.216:8500/v1/kv/hosts?recurse");
         try {
             CloseableHttpResponse httpResponse = httpClient.execute(httpGet);
         } catch (Exception e) {
             logger.error(e.getMessage(), e);
         }finally {
             httpClient.close();
         }
```

#### 1.1.1 HTTP 请求  HTTP request 

所有的HTTP请求都有一个请求行，它包含一个方法名，一个请求URI和一个HTTP协议版本。

HttpClient的支持了在HTTP / 1.1规范中定义的所有HTTP方法的框的：`GET`，`HEAD`， `POST`，`PUT`，`DELETE`， `TRACE`和`OPTIONS`。没有为每个方法设置类型，而是一个特定的类`HttpGet`， `HttpHead`，`HttpPost`， `HttpPut`，`HttpDelete`， `HttpTrace`，和`HttpOptions`。

Request-URI是一个统一资源标识符，用于标识应用请求的资源。HTTP请求URI由协议方案，主机名，可选端口，资源路径，可选查询和可选片段组成。

> 可以自己拼接一个请求字符串，里面包括协议、主机名、端口、资源路径、以及参数

```
HttpGet httpget = new HttpGet（
     “http://www.google.com/search?hl=zh-CN&q=httpclient&btnG=Google+Search&aq=f&oq=”）;
```

HttpClient也提供了一个URIBuilder的工具类，来简化请求URI的创建和修改

> 如上一个请求，我们也可以用下面的方式表示

```
         CloseableHttpClient httpClient = HttpClients.createDefault();
         URI uri = new URIBuilder()
                 .setScheme("http")
                 .setHost("www.google.com")
                 .setPath("/search")
                 .setParameter("q", "httpclient")
                 .setParameter("btnG", "Google Search")
                 .setParameter("aq", "f")
                 .setParameter("oq", "")
                 .build();
         try {
             HttpGet httpGet = new HttpGet(uri);
             System.out.println(httpGet.getURI());
            // CloseableHttpResponse httpResponse = httpClient.execute(httpGet);
         } catch (Exception e) {
             System.out.println(e.getMessage());
         }finally {
             httpClient.close();
         }
```

以上的两种方法都是这样的http请求 http://www.google.com/search?q=httpclient&btnG=Google+Search&aq=f&oq=

#### 1.1.2 HTTP request 

HTTP响应是服务器收到并解释请求消息后发送回客户端的消息。该消息的第一行由协议版本和数字状态代码及其相关的文本短语组成。

```
    @Test
    public void httpResponse() {
        HttpResponse response = new BasicHttpResponse(HttpVersion.HTTP_1_1, HttpStatus.SC_OK, "OK");
        System.out.println(response.getProtocolVersion());
        System.out.println(response.getStatusLine().getStatusCode());
        System.out.println(response.getStatusLine().getReasonPhrase());
        System.out.println(response.getStatusLine().toString());
    }
```

运行结果

```
HTTP/1.1
200
OK
HTTP/1.1 200 OK

Process finished with exit code 0
```



#### 1.1.3 使用消息头 working with message headers

HTTP消息可以包含许多描述消息属性的标题，如内容长度，内容类型等等。HttpClient提供了检索，添加，删除和枚举标题的方法。

```
public void messageHeaders(){
     HttpResponse response = new BasicHttpResponse(HttpVersion.HTTP_1_1,HttpStatus.SC_OK,"OK");
     response.addHeader("Set-Cookie","c1=a;path=/;domain=localhost");
     response.addHeader("Set-Cookie","c2=b; path=\"/\", c3=c; domain=\"localhost\"");
     Header h1 = response.getFirstHeader("Set-Cookie");
     System.out.println(h1);
     Header h2 = response.getLastHeader("Set-Cookie");
     System.out.println(h2);
     Header[] hs = response.getHeaders("Set-Cookie");
     System.out.println(hs.length);
}
```

输出：

```
Set-Cookie: c1=a;path=/;domain=localhost
Set-Cookie: c2=b; path="/", c3=c; domain="localhost"
2

Process finished with exit code 0
```



获取指定类型的所有头文件的最有效的方法是使用HeaderIterator接口

```
@Test
public void headerIterator(){
    HttpResponse response = new BasicHttpResponse(HttpVersion.HTTP_1_1,HttpStatus.SC_OK,"OK");
    response.addHeader("Set-Cookie","c1=a;path=/;domain=localhost");
    response.addHeader("Set-Cookie","c2=b; path=\"/\", c3=c; domain=\"localhost\"");
    HeaderIterator iterator = response.headerIterator("Set-Cookie");
    while (iterator.hasNext()){
        System.out.println(iterator.next());
    }
}
```

输出

```
Set-Cookie: c1=a;path=/;domain=localhost
Set-Cookie: c2=b; path="/", c3=c; domain="localhost"
```

它还提供了便捷的方法来将HTTP消息解析为单独的头元素

```
public void headerElementIterator(){
    HttpResponse response = new BasicHttpResponse(HttpVersion.HTTP_1_1,HttpStatus.SC_OK,"OK");
    response.addHeader("Set-Cookie","c1=a;path=/;domain=localhost");
    response.addHeader("Set-Cookie","c2=b; path=\"/\", c3=c; domain=\"localhost\"");
    HeaderElementIterator iterator = new BasicHeaderElementIterator(response.headerIterator("Set-Cookie"));
    while (iterator.hasNext()){
        HeaderElement element = iterator.nextElement();
        System.out.println(element.getName()+"=" +element.getValue());
        NameValuePair[] pairs = element.getParameters();
        for (int i= 0;i<pairs.length;i++){
            System.out.println(""+pairs[i]);
        }
    }
}
```

输出

```
c1=a
path=/
domain=localhost
c2=b
path=/
c3=c
domain=localhost

Process finished with exit code 0
```

#### 1.1.4 HTTP 实体 HTTP entity

HTTP消息可以携带与请求或响应相关联的内容实体。实体可以在一些请求和一些响应中找到，因为它们是可选的。使用实体的请求被称为实体封闭请求。HTTP规范定义了两个实体封闭请求方法：`POST`和 `PUT`。通常预期响应将包含内容实体。有例外的情况，如应对 `HEAD`方法`204 No Content`， `304 Not Modified`，`205 Reset Content` 响应。



HttpClient根据内容的来源区分了三种实体：

- **流式传输： ** 内容是从流接收的，或者是随时产生的。具体来说，这个类别包括从HTTP响应中收到的实体。流派实体通常不可重复。
- **自包含： ** 内容在内存中或通过独立于连接或其他实体的方式获得。独立的实体通常是可重复的。这种类型的实体将主要用于包含HTTP请求的实体。
- **包装： ** 内容是从另一个实体获得的。

当从HTTP响应中流出内容时，这种区别对连接管理很重要。对于由应用程序创建并仅使用HttpClient发送的请求实体，流式和自包含之间的区别并不重要。在这种情况下，建议将不可重复的实体视为流式，将可重复的实体视为独立式。



##### 1.1.4.1 可重复的实体 

一个实体可以是可重复的，这意味着它的内容可以被多次读取。这只适用于自包含的实体（如 `ByteArrayEntity`或 `StringEntity`）

##### 1.1.4.2 使用HTTP实体 

由于实体可以表示二进制和字符内容，因此它支持字符编码（以支持后者，即字符内容）。

在执行带有封闭内容的请求时或者请求成功时使用响应主体将结果发送回客户端时创建实体。

要从实体读取内容，可以通过`HttpEntity#getContent()`返回一个方法来检索输入流，也`java.io.InputStream`可以向该`HttpEntity#writeTo(OutputStream)`方法提供一个输出流，一旦所有内容被写入给定流，该方法将返回。

当实体已经与传入消息接收，该方法 `HttpEntity#getContentType()`和 `HttpEntity#getContentLength()`方法可用于读取所述公共元数据，例如`Content-Type`与 `Content-Length`报头（如果可用）。由于 `Content-Type`标题可以包含文本MIME类型的字符编码，如text / plain或text / html，所以该 `HttpEntity#getContentEncoding()`方法用于读取这些信息。如果标题不可用，则将返回-1的长度，对于内容类型则返回NULL。如果`Content-Type` 头部可用，`Header`则会返回一个对象。

为外发消息创建实体时，此元数据必须由实体的创建者提供

```
@Test
public void httpEntity()throws Exception{
    StringEntity myEntity = new StringEntity("important message", ContentType.create("text/plain","UTF-8"));
    System.out.println(myEntity.getContentType());
    System.out.println(myEntity.getContentLength());
    System.out.println(EntityUtils.toString(myEntity));
    System.out.println(EntityUtils.toByteArray(myEntity).length);
}
```

输出

```
Content-Type: text/plain; charset=UTF-8
17
important message
17

Process finished with exit code 0
```

##### 1.1.5 释放资源 

为了确保正确释放系统资源，必须关闭与实体相关的内容流或响应本身

```
public void closeResource()throws Exception{
    CloseableHttpClient httpClient = HttpClients.createDefault();
    HttpGet httpGet = new HttpGet("http://10.110.13.216:8500/v1/kv/hosts?recurse");
    CloseableHttpResponse response = httpClient.execute(httpGet);
    try {
      
        HttpEntity entity = response.getEntity();
        if (entity !=null){
            InputStream inputStream = entity.getContent();
            System.out.println(inputStream.read());
            try {
            //todo
            } catch (Exception e) {
                logger.error(e.getMessage(), e);
            }finally {
                inputStream.close();
            }
        }
    } catch (Exception e) {
        logger.error(e.getMessage(), e);
    }finally {
        response.close();
    }

}
```

#### 1.1.6 相应处理 

```
CloseableHttpClient httpClient = HttpClients.createDefault();
HttpGet httpGet = new HttpGet("http://10.110.13.216:8500/v1/kv/hosts?recurse");
CloseableHttpResponse response = httpClient.execute(httpGet);
HttpEntity entity = response.getEntity();
System.out.println(EntityUtils.toString(entity));
```