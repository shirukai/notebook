# 基于Netty的http server实现

> 版本说明：
>
> netty：4.1.17.Final
>
> 项目地址：https://github.com/shirukai/netty-http-server-demo.git

最近在看Spark源码的RPC框架实现的代码的时候，接触到Netty。在Spark1.6之后，Spark中RPC通信的框架由Netty逐渐代替了Akka。

为什么Netty可以取代Akka？首先毋庸置疑的是Akka可以做到的，Netty也可以做到，但是Netty可以做到，Akka却无法做到，原因是啥？在软件栈中，Akka相比Netty要Higher一点，它专门针对RPC做了很多事情，而Netty相比更加基础一点，可以为不同的应用层通信协议（RPC，FTP，HTTP等）提供支持，在早期的Akka版本，底层的NIO通信就是用的Netty；其次一个优雅的工程师是不会允许一个系统中容纳两套通信框架，恶心！最后，虽然Netty没有Akka协程级的性能优势，但是Netty内部高效的Reactor线程模型，无锁化的串行设计，高效的序列化，零拷贝，内存池等特性也保证了Netty不会存在性能问题。（摘自：http://www.aboutyun.com/thread-21115-1-1.html。关于为什么Spark要使用Netty替代Akka的详细内容，可以参考这篇文章）

## 1 什么是Netty？

>Netty 是一个利用 Java 的高级网络的能力，隐藏其背后的复杂性而提供一个易于使用的 API 的客户端/服务器框架。
> Netty 是一个广泛使用的 Java 网络编程框架（Netty 在 2011 年获得了Duke's Choice Award，见<https://www.java.net/dukeschoice/2011>）。它活跃和成长于用户社区，像大型公司 Facebook 和 Instagram 以及流行 开源项目如 Infinispan, HornetQ, Vert.x, Apache Cassandra 和 Elasticsearch 等，都利用其强大的对于网络抽象的核心代码。

Essential Netty in Action 《Netty 实战(精髓)》:https://waylau.gitbooks.io/essential-netty-in-action/content/

关于Netty介绍：https://www.jianshu.com/p/b9f3f6a16911

## 2 Netty的简单使用

### 2.1 准备

在开始之前，我们需要创建一个maven项目。这里就不做演示了。项目的目录结构如下图所示：

![](http://shirukai.gitee.io/images/63c3ddf6d58191988f38dd86281d3f73.jpg)

关于Netty的简单使用的Demo在项目中netty.demo的包下。

相关jar包依赖：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>netty.http.server</groupId>
    <artifactId>server</artifactId>
    <version>1.0</version>
    <dependencies>
        <!--netty-->
        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-all</artifactId>
            <version>4.1.17.Final</version>
        </dependency>
        <!--log-->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
            <version>1.5.8</version>
        </dependency>
        <!--json-->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.1.37</version>
        </dependency>
    </dependencies>

</project>
```



### 2.2 创建Netty 服务端

#### 2.2.1 创建Server启动类

该类主要用于对Netty Server进行一些配置，如端口号、EventLoopGroup、ServerBootstrap以及chanal中的pipline等，以及netty服务的启动。代码如下所示：

```java
package netty.demo;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.charset.Charset;

/**
 * Created by shirukai on 2018/9/30
 * 基于Netty实现的Socket Server
 */
public class NettySocketServer {
    public final Logger log = LoggerFactory.getLogger(this.getClass());
    private int port;

    public NettySocketServer(int port) {
        this.port = port;
    }

    public void start() {

        EventLoopGroup bossGroup = new NioEventLoopGroup();
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        ServerBootstrap bootstrap = new ServerBootstrap();
        try {
            bootstrap
                    .option(ChannelOption.SO_BACKLOG, 1024)
                    // BACKLOG用于构造服务端套接字ServerSocket对象，标识当服务器请求处理线程全满时，
                    // 用于临时存放已完成三次握手的请求的队列的最大长度。如果未设置或所设置的值小于1，Java将使用默认值50。
                    .group(bossGroup, workerGroup) //绑定线程池
                    .channel(NioServerSocketChannel.class)// 指定使用的channel
                    .localAddress(port)
                    .childHandler(new ChannelInitializer<SocketChannel>() {
                        // 绑定客户端时触发的操作
                        @Override
                        protected void initChannel(SocketChannel socketChannel) throws Exception {
                            log.info("Client connected service：{}", socketChannel);
                            ChannelPipeline pipeline = socketChannel.pipeline();
                            pipeline.addLast(new StringDecoder(Charset.forName("UTF-8")));
                            pipeline.addLast(new NettySocketServerHandler());//服务器处理客户端请求
                            pipeline.addLast(new StringEncoder(Charset.forName("UTF-8")));
                        }
                    });
            ChannelFuture channelFuture = bootstrap.bind().sync(); //服务器异步创建绑定
            log.info("Server is listening：{}", channelFuture.channel());
            channelFuture.channel().closeFuture().sync();//关闭服务器
        } catch (Exception e) {
            log.error(e.getMessage());
        } finally {
            try {
                // 释放线程池资源
                workerGroup.shutdownGracefully().sync();
                bossGroup.shutdownGracefully().sync();
            } catch (InterruptedException e) {
                log.error(e.getMessage());
            }
        }

    }

    public static void main(String[] args) {
        NettySocketServer server = new NettySocketServer(9099);
        server.start();
    }
}
```

Bootstrap的option参数：https://blog.csdn.net/zhousenshan/article/details/72859923

#### 2.2.2 Netty 服务端处理类

如上代码，我们在pipeline中指定了服务端处理客户端请求的实例

```java
 pipeline.addLast(new NettySocketServerHandler());
```

下面我们就要实现NettySocketServerHandler这个类，代码如下所示：

```java
package netty.demo;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by shirukai on 2018/9/30
 * netty socket server 处理器
 */
public class NettySocketServerHandler extends ChannelInboundHandlerAdapter {
    public final Logger log = LoggerFactory.getLogger(this.getClass());

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        log.info("The channel {} is ACTIVE.");
    }

    @Override
    public void channelInactive(ChannelHandlerContext ctx) throws Exception {
        log.info("The channel {} is INACTIVE.");
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        log.info("message:{}", msg);
        ctx.channel().writeAndFlush("返回信息给客户端：" + msg);
    }

    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        super.channelReadComplete(ctx);
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        super.exceptionCaught(ctx, cause);
    }
}
```

### 2.3 创建Netty 客户端

客户端的创建于服务端类似，也需要一个客户端配置类和处理类。

#### 2.3.1 创建 Client 配置类

```java
package netty.demo;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;

import java.nio.charset.Charset;

/**
 * Created by shirukai on 2018/9/30
 * netty socket client
 */
public class NettySocketClient {
    private String host;
    private int port;

    public NettySocketClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void start() {
        EventLoopGroup group = new NioEventLoopGroup();
        Bootstrap bootstrap = new Bootstrap();
        try {
            bootstrap
                    .group(group)//注册线程池
                    .channel(NioSocketChannel.class)// 使用NioSocketChannel来作为连接用的Channel类
                    .remoteAddress(host, port)//绑定远程服务的IP和端口
                    .handler(new ChannelInitializer<SocketChannel>() {//连接初始化
                        @Override
                        protected void initChannel(SocketChannel socketChannel) throws Exception {
                            ChannelPipeline pipeline = socketChannel.pipeline();
                            // 输入流编码为StringEncoder
                            pipeline.addLast(new StringDecoder(Charset.forName("UTF-8")));
                            pipeline.addLast(new NettySocketClientHandler());
                            // 输出流编码为StringDecoder
                            pipeline.addLast(new StringEncoder(Charset.forName("UTF-8")));
                        }
                    });
            ChannelFuture channelFuture = bootstrap.connect().sync();
            channelFuture.channel().closeFuture().sync();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                group.shutdownGracefully().sync();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }

    public static void main(String[] args) {
        NettySocketClient client = new NettySocketClient("127.0.0.1", 9099);
        client.start();
    }
}
```

#### 2.3.2 Netty 客户端处理类

```java
package netty.demo;

import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Created by shirukai on 2018/9/30
 */
public class NettySocketClientHandler extends SimpleChannelInboundHandler<String> {
    public final Logger log = LoggerFactory.getLogger(this.getClass());

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        ctx.channel().writeAndFlush("向客户端发送消息");
    }

    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, String s) throws Exception {
        log.info(s);
    }
}
```

### 2.4 Demo 演示

首先启动服务端，然后启动客户端，效果如下图所示：

![](http://shirukai.gitee.io/images/3beb7d5ba5dd4a2cd56f3eb113cf6857.gif)



## 3 基于Netty的http server实现

上面已经记录了Netty的简单实用，接下来记录一下在学习实用Netty实现http server实现。从0到1的搭建一个http服务。通过实现Netty http服务，学到了以下几个知识点：

* java 中注解的使用（模仿spring对请求路由和参数进行控制）

* 通过反射机制执行路由指定的方法

* 处理http请求
* java链式调用

设计思路：

首先实现一个基于Netty的http server，使用HttpRequestDecoder和HttpResponseEncoder进行输入流输出流编解码。

然后使用自定义的HttpServerhandler类进行请求处理。模仿springmvc的controller层，使用注解的方式，设置方法路由。扫描指定类下的注解，将注解信息以及类信息缓存到Map里。

最后根据请求的url从Map中获取相关信息，路由到指定的方法，利用反射机制，实例化该方法，传入参数并执行。

对于请求参数，支持传统的url传参，使用？id=1或者/{id}两种url参数的形式获取，支持处理post请求中的json请求。其他请求，如formdata等传参形式没有支持，处理逻辑相似，对于请求的不同类型处理可以参考：https://www.cnblogs.com/cyfonly/p/5616493.html。

### 3.1 Http Server的实现

实现代码如下：

```java
package netty.http.server;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.http.HttpObjectAggregator;
import io.netty.handler.codec.http.HttpRequestDecoder;
import io.netty.handler.codec.http.HttpResponseEncoder;
import netty.http.server.entity.Router;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

/**
 * Created by shirukai on 2018/9/30
 * 基于netty 实现httpSever
 */
public class HttpServer {
    private HttpServerConfig config;
    private int port;
    private Map<String, Router> routers;

    public final Logger log = LoggerFactory.getLogger(this.getClass());

    public HttpServerConfig builder() {
        this.config = new HttpServerConfig(this);
        return config;
    }

    public void start() {
        ServerBootstrap bootstrap = new ServerBootstrap();
        NioEventLoopGroup group = new NioEventLoopGroup();
        try {
            bootstrap
                    .group(group)
                    .channel(NioServerSocketChannel.class)
                    .childHandler(new ChannelInitializer<SocketChannel>() {
                        @Override
                        protected void initChannel(SocketChannel socketChannel) {
                            socketChannel.pipeline()
                                    .addLast("decoder", new HttpRequestDecoder())
                                    .addLast("encoder", new HttpResponseEncoder())
                                    .addLast("aggregator", new HttpObjectAggregator(512 * 1024))
                                    .addLast("handler", new HttpServerHandler(routers));
                        }
                    })
                    .option(ChannelOption.SO_BACKLOG, 128)
                    .childOption(ChannelOption.SO_KEEPALIVE, Boolean.TRUE);
            bootstrap.bind(port).sync();
        } catch (Exception e) {
            e.printStackTrace();
        }
        log.info("Start app server at port:{}", port);
    }

    public void setPort(int port) {
        this.port = port;
    }

    public void setRouters(Map<String, Router> routers) {
        this.routers = routers;
    }
}
```

由上面代码可以看出，在HttpServer这个类中，我们设置了三个私有的属性：config、port、routers，分别为服务器配置、端口和路由信息。提供一个builder方法，返回HttpServerConfig实例，用来构建HttpServer。

### 3.2 HttpServerConfig的实现

该类主要是对服务的配置信息进行缓存。如端口号、controller等，实现代码如下：

```java
package netty.http.server;

import java.util.concurrent.ConcurrentHashMap;

/**
 * Created by shirukai on 2018/9/30
 * 用来配置HttpServer
 */
public class HttpServerConfig {
    // 初始化Map用来缓存配置信息
    private ConcurrentHashMap<String, Object> conf = new ConcurrentHashMap<>();
    private static final String SERVER_CONTROLLERS = "netty.http.server.controllers";
    private static final String SERVER_PORT = "netty.http.server.port";
    private HttpServer httpServer;

    public HttpServerConfig(HttpServer httpServer) {
        this.httpServer = httpServer;
    }

    public HttpServerConfig set(String name, Object value) {
        conf.put(name, value);
        return this;
    }

    /**
     * 设置端口号
     *
     * @param port 端口
     * @return conf
     */
    public HttpServerConfig setPort(int port) {
        conf.put(SERVER_PORT, port);
        return this;
    }

    /**
     * 设置多个Controller的class 以便进行注解扫描
     *
     * @param className class names
     * @return conf
     */
    public HttpServerConfig setControllers(Class<?>... className) {
        Class<?>[] oldClasses = getClasses();
        Class<?>[] newClasses = insertClasses(oldClasses, className);
        conf.put(SERVER_CONTROLLERS, newClasses);
        return this;
    }

    /**
     * 设置单个controller的class
     *
     * @param className class name
     * @return conf
     */
    public HttpServerConfig setController(Class<?> className) {
        //获取已有的class
        Class<?>[] oldClasses = getClasses();
        //新增class
        Class<?>[] newClasses = insertClass(oldClasses, className);
        conf.put(SERVER_CONTROLLERS, newClasses);
        return this;
    }

    /**
     * 获取String类型的值
     *
     * @param key key
     * @return value
     */
    public String getString(String key) {
        return conf.get(key).toString();
    }

    /**
     * 获取 int类型的值
     *
     * @param key key
     * @return value
     */
    public int getInt(String key) {
        return (int) conf.get(key);
    }

    /**
     * 获取所有的class
     *
     * @return classes
     */
    public Class<?>[] getClasses() {
        return (Class<?>[]) conf.get(SERVER_CONTROLLERS);
    }

    /**
     * 插入一个class
     *
     * @param oldClasses 旧的classes
     * @param addClass   要添加的class
     * @return 新的 classes
     */
    private Class<?>[] insertClass(Class<?>[] oldClasses, Class<?> addClass) {
        Class<?>[] newClasses;
        //判断原始的Class 数组是否为null
        if (oldClasses != null) {
            //获取数组长度
            int length = oldClasses.length;
            //创建一个新数组
            newClasses = new Class<?>[length + 1];
            //copy数组
            System.arraycopy(oldClasses, 0, newClasses, 0, length);
            newClasses[length + 1] = addClass;
        } else {
            newClasses = new Class<?>[]{addClass};
        }
        return newClasses;
    }

    /**
     * 插入多个class
     *
     * @param oldClasses 旧的classes
     * @param addClasses 要添加的classes
     * @return 新的classes
     */
    private Class<?>[] insertClasses(Class<?>[] oldClasses, Class<?>[] addClasses) {
        Class<?>[] newClasses;
        if (oldClasses != null) {
            int oldLength = oldClasses.length;
            int addLength = addClasses.length;
            newClasses = new Class<?>[oldLength + addLength];
            System.arraycopy(oldClasses, 0, newClasses, 0, oldLength);
            System.arraycopy(addClasses, 0, newClasses, oldLength, addLength);
        } else {
            newClasses = addClasses;
        }
        return newClasses;
    }

    public HttpServer create() {
        httpServer.setPort(this.getInt(SERVER_PORT));
        //获取controller类
        Class<?>[] classes = this.getClasses();
        //扫描注解
        httpServer.setRouters(AnnotationScan.getRouters(classes));
        return this.httpServer;
    }

    public ConcurrentHashMap<String, Object> getConf() {
        return this.conf;
    }

}
```

通过上面两个类，我们基本可以完成一个HttpServer的初始化操作：

```java
import netty.http.server.HttpServer;
import netty.http.worker.controller.TestController;

/**
 * Created by shirukai on 2018/9/30
 * netty sever 启动类
 */
public class App {
    public static void main(String[] args) {
        HttpServer server = new HttpServer();
        server.builder()
                .setPort(9090)
                .setController(TestController.class)
                .create().start();
    }
}
```

当然到目前为止，我们的服务是没有办法启动的，因为我们还没有HttpServerHandler类用来处理http请求和AnnotationScan类用来扫描指定Controller类下的注解信息。所以接下来，我们先实现AnnotationScan类，演示注解在该Demo中的使用。

### 3.3  路由控制

这里，我们模仿spring mvc 使用注解的方式，对Controller层进行路由控制。

#### 3.3.1 注解类设置

在netty.http.server.annotation包下创建相关注解类。

##### 3.3.1.1 @RouterMapping

@RouterMapping，功能类似于spring中的RequestMapping主要是对Controller层方法的路由。该注解作用于方法，根据用于发送的url，执行映射的方法。

```java
package netty.http.server.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Created by shirukai on 2018/9/30
 * 路由
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RouterMapping {
    String api() default "";

    String method() default "GET,POST,PUT,DELETE";
}
```

##### 3.3.1.2 @RequestParam

@RequestParam，功能类似于spring中的@RequestParam，作用于方法中的参数列表，服务会根据该注解自动去匹配请求参数。主要是从url中获取？id=1这样形式的参数。代码如下：

```java
package netty.http.server.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Created by shirukai on 2018/9/30
 */
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequestParam {
    String value() default "";
}
```

##### 3.3.1.3 @PathParam

@PathParam同样是作用于参数列表，用以获取/{id} 这样形式的参数，代码如下：

````java
package netty.http.server.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Created by shirukai on 2018/9/30
 */
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface PathParam {
    String value() default "";
}
````

##### 3.3.1.4 @JsonParam

 @JsonParam也是作用于参数列表，用于获取json参数格式的请求，代码如下：

```java
package netty.http.server.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Created by shirukai on 2018/9/30
 */
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface JsonParam {
    String value() default "";
}
```

#### 3.3.2 注解扫描

有了注解类之后，我们需要知道，我们的哪些方法使用了注解，哪些参数使用了注解。所以我们需要进行注解的扫描，并将扫描的注解信息缓存到Map里。AnnotationScan类的代码如下所示：

```java
package netty.http.server;

import netty.http.server.annotation.JsonParam;
import netty.http.server.annotation.PathParam;
import netty.http.server.annotation.RequestParam;
import netty.http.server.annotation.RouterMapping;
import netty.http.server.entity.Param;
import netty.http.server.entity.Router;

import java.lang.reflect.Method;
import java.lang.reflect.Parameter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by shirukai on 2018/9/30
 * 注解扫描
 */
public class AnnotationScan {
    public static Map<String, Router> getRouters(Class<?>... classes) {
        Map<String, Router> routers = new HashMap<>(16);
        // 遍历传入的class
        for (Class<?> tClass : classes) {
            // 遍历类中的方法
            for (Method method : tClass.getDeclaredMethods()) {
                // 扫描方法的注解
                RouterMapping routerMapping = method.getAnnotation(RouterMapping.class);
                // 如果注解不为空，扫描该方法内的参数注解
                if (routerMapping != null) {
                    Router router = new Router();
                    // 获取参数
                    List<Param> params = new ArrayList<>(16);
                    // 遍历方法中的参数
                    for (Parameter parameter : method.getParameters()) {
                        // 扫描参数注解
                        PathParam pathParam = parameter.getAnnotation(PathParam.class);
                        RequestParam requestParam = parameter.getAnnotation(RequestParam.class);
                        JsonParam jsonParam = parameter.getAnnotation(JsonParam.class);
                        Param param = new Param();
                        // 将注解写入到信息写入到Param中
                        if (pathParam != null) {
                            param.setType("path");
                            param.setValue(pathParam.value());
                        }
                        if (requestParam != null) {
                            param.setType("request");
                            param.setValue(requestParam.value());
                        }
                        if (jsonParam != null) {
                            param.setType("json");
                            param.setValue(jsonParam.value());
                        }
                        // 将Param信息写入到List里
                        params.add(param);
                    }
                    router.setParams(params);
                    router.settClass(tClass);
                    router.setMethodType(routerMapping.method());
                    router.setMethod(method);
                    router.setUrl(routerMapping.api());
                    // 保存Router信息
                    routers.put(router.getUrl(), router);
                }
            }
        }
        return routers;
    }
}

```

#### 3.3.3 请求处理

完成上面的工作之后，接下来是该demo的核心功能，就是对http请求进行处理。根据请求的url，获取参数，通过反射执行相应方法。

```java
package netty.http.server;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.*;
import io.netty.util.AsciiString;
import netty.http.server.entity.Param;
import netty.http.server.entity.Router;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Method;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Created by shirukai on 2018/9/30
 * Http服务处理器
 */
public class HttpServerHandler extends SimpleChannelInboundHandler<FullHttpRequest> {
    private Map<String, Router> routers;
    private AsciiString contentType = HttpHeaderValues.APPLICATION_JSON;
    public final Logger log = LoggerFactory.getLogger(this.getClass());

    public HttpServerHandler(Map<String, Router> routers) {
        this.routers = routers;
    }

    @Override
    protected void channelRead0(ChannelHandlerContext channelHandlerContext, FullHttpRequest request) {
        log.info("Handler request:{}", request);
        Object result = null;
        HttpResponseStatus status = null;
        try {
            // 初始化请求参数
            List<Object> params = new ArrayList<>(16);
            // 解析URL中的参数
            QueryStringDecoder decoder = new QueryStringDecoder(request.uri(), Charset.forName("UTF-8"));
            // 获取请求路径
            String url = decoder.path();
            // 获取请求方法
            String method = request.method().toString();
            // 获取URL中的参数
            Map<String, List<String>> urlParams = decoder.parameters();
            // 从扫描的注解中获取Router信息
            Router router = getRoute(url);
            //判断router里是否包含url
            if (router == null) {
                throw new RuntimeException("URL does not exist!");
            }
            //判断请求方法是否匹配
            if (!router.getMethodType().contains(method)) {
                throw new RuntimeException("Method does not match!");
            }
            //获取controller里请求参数信息
            List<Param> paramInfo = router.getParams();
            if (paramInfo != null) {
                //处理URL参数
                Map<String, String> pathParams = PathUrlHandler.getParams(url, router.getUrl());
                JSONObject initJson = null;
                //处理POST请求
                if (method.equals("POST")) {
                    String contentType = request.headers().get("Content-Type");
                    //处理application/json请求
                    if (contentType.contains("application/json")) {
                        initJson = JSON.parseObject(request.content().toString(Charset.forName("UTF-8")));
                    }
                }
                JSONObject finalJson = initJson;
                paramInfo.forEach(param -> {
                    String type = param.getType();
                    String value = param.getValue();
                    // 如果参数在url里形如/test/{id}时 添加参数
                    if (type.equals("path")) {
                        params.add(pathParams.get(value));
                    }
                    // 如果参数在url里形如/test?id=124时 添加参数
                    if (type.equals("request")) {
                        params.add(urlParams.get(value).get(0));
                    }
                    // 如果参数在body里以json形如传入时 添加参数
                    if (type.equals("json")) {
                        params.add(finalJson);
                    }
                });
                // 执行router映射的方法，并获取返回结果
                result = executeMethod(router, params.toArray());
                // 设置response状态为 OK
                status = HttpResponseStatus.OK;
            } else {
                // 如果没有参数，直接执行映射的方法
                result = executeMethod(router);
            }
        } catch (Exception e) {
            // 如果捕获到异常，将异常信息放到返回结果里
            result = e.getMessage();
        } finally {
            // 如果状态为null,将返回结果设置为500
            if (status == null) {
                status = HttpResponseStatus.INTERNAL_SERVER_ERROR;
            }
        }
        // 包装response
        DefaultFullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1,
                status,
                Unpooled.wrappedBuffer(JSON.toJSONBytes(result)));

        // 设置response 的header
        HttpHeaders heads = response.headers();
        heads.add(HttpHeaderNames.CONTENT_TYPE, contentType + "; charset=UTF-8");
        heads.add(HttpHeaderNames.CONTENT_LENGTH, response.content().readableBytes());
        heads.add(HttpHeaderNames.CONNECTION, HttpHeaderValues.KEEP_ALIVE);
        // 将返回结果返回
        channelHandlerContext.write(response);


    }

    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        super.channelReadComplete(ctx);
        ctx.flush();
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        if (null != cause) cause.printStackTrace();
        if (null != ctx) ctx.close();
    }

    /**
     * 获取Router信息
     *
     * @param url url
     * @return Router
     */
    private Router getRoute(String url) {
        AtomicReference<Router> router = new AtomicReference<>();
        routers.keySet().forEach(routerKey -> {
            if (PathUrlHandler.verify(url, routerKey)) {
                router.set(routers.get(routerKey));
            }
        });
        return router.get();
    }

    /**
     * 执行路由映射的方法
     *
     * @param router Router
     * @param params params
     * @return Object
     * @throws Exception 执行异常
     */
    private Object executeMethod(Router router, Object... params) throws Exception {
        Class<?> cls = router.gettClass();
        Object obj = cls.newInstance();
        Method method = router.getMethod();
        return method.invoke(obj, params);
    }

}
```

对于url中类似于/{id}这样参数的处理，单独写到了PathUrlHandler类里，代码如下：

```java
package netty.http.server;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by shirukai on 2018/10/8
 * 处理URL中的参数
 */
public class PathUrlHandler {
    private static final String pattern = "(\\{[^}]*})";


    /**
     * 校验请求url和路由中的url是否匹配
     * 如：/test/111 匹配 /test/{id}
     *
     * @param requestUrl 请求的url
     * @param routerUrl  路由中设置的url
     * @return boolean
     */
    public static boolean verify(String requestUrl, String routerUrl) {
        Matcher keyMatcher = Pattern.compile(pattern).matcher(routerUrl);
        String replacePattern = keyMatcher.replaceAll("(.*)");
        Matcher valueMatcher = Pattern.compile(replacePattern).matcher(requestUrl);
        return valueMatcher.matches();
    }

    /**
     * 获取参数
     * 请求URL：/test/111
     * 路由URL：/test/{id}
     * 参数为{"id":"111"}
     *
     * @param requestUrl 请求的url
     * @param routerUrl  路由中设置的url
     * @return map
     */
    public static Map<String, String> getParams(String requestUrl, String routerUrl) {
        Map<String, String> params = new HashMap<>(16);
        Matcher keyMatcher = Pattern.compile(pattern).matcher(routerUrl);
        List<String> keys = new ArrayList<>(16);
        List<String> values = new ArrayList<>(16);
        while (keyMatcher.find()) {
            keys.add(keyMatcher.group(1).replace("{", "").replace("}", ""));
        }
        String replacePattern = keyMatcher.replaceAll("(.*)");
        Matcher valueMatcher = Pattern.compile(replacePattern).matcher(requestUrl);
        if (valueMatcher.find()) {
            int count = valueMatcher.groupCount();
            for (int i = 1; i <= count; i++) {
                values.add(valueMatcher.group(i));
            }
        }
        int valueSize = values.size();
        for (int i = 0; i < keys.size(); i++) {
            String value = i < valueSize ? values.get(i) : "";
            params.put(keys.get(i), value);
        }
        return params;
    }

}
```

### 3.4 Demo演示

完成以上工作之后，我们的Http服务相关的操作都已经完成了，下面我们将写一个简单的例子，来测试我们的服务。

在netty.http.worker.controller包下创建一个TestController类，该类里面使用了我们之前设置好的@RouterMapping、 @RequestParam、@PathParam、@JsonParam注解。并且分别展示了GET请求和POST请求。

代码如下：

```java
package netty.http.worker.controller;

import com.alibaba.fastjson.JSONObject;
import netty.http.server.annotation.JsonParam;
import netty.http.server.annotation.PathParam;
import netty.http.server.annotation.RequestParam;
import netty.http.server.annotation.RouterMapping;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by shirukai on 2018/9/30
 * controller
 */
public class TestController {
    /**
     * 测试GET请求
     *
     * @param name name
     * @param id   id
     * @return map
     */
    @RouterMapping(api = "/api/v1/test/get/{id}", method = "GET")
    public Map<String, Object> testGet(
            @RequestParam("name") String name,
            @PathParam("id") String id
    ) {
        Map<String, Object> map = new HashMap<>(16);
        map.put("name", name);
        map.put("id", id);
        return map;
    }

    /**
     * 测试POST请求
     *
     * @param json json
     * @return json
     */
    @RouterMapping(api = "/api/v1/test/post", method = "POST")
    public JSONObject testPost(
            @JsonParam("json") JSONObject json
    ) {
        return json;
    }
}

```



在App类里我们启动Http Server，设置我们刚才创建的Controller类到Http Server

```java
import netty.http.server.HttpServer;
import netty.http.worker.controller.TestController;

/**
 * Created by shirukai on 2018/9/30
 * netty sever 启动类
 */
public class App {
    public static void main(String[] args) {
        HttpServer server = new HttpServer();
        server.builder()
                .setPort(9090)
                .setController(TestController.class)
                .create().start();
    }
}

```

![](http://shirukai.gitee.io/images/c764779fc1406084401997db1f603eb8.jpg)

使用PostMan向服务器发送GET请求：

![](http://shirukai.gitee.io/images/468cbedc3994f9f6160363f3725837e5.jpg)

服务器日志：

![](http://shirukai.gitee.io/images/66c62cbfbf3d494adebf8055ad627f40.jpg)

使用PostMan向服务器发送POST请求

![](http://shirukai.gitee.io/images/a60eb2a54564cc8a5a4ff63f5204e20d.jpg)

服务器日志：

![](http://shirukai.gitee.io/images/d2f5350e034c9defaa8ecd2cbb5e9595.jpg)