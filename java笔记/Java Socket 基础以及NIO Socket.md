# Java Sokcet 基础以及NIO Socket

## 1 什么是Socket？

网络上的两个程序通过一个双向的通信连接实现数据的交换，这个连接的一端称为一个socket。

关于Socket的介绍：https://blog.csdn.net/httpdrestart/article/details/80670388

## 2 简单的Socket通讯

下面记录一下，基于java实现Socket通讯，主要包括Socket服务端和Socket客户端两部分。

### 2.1 基于TCP的Socket服务端

服务端的实现主要有一下几步：

第一步：创建socket服务，并绑定监听端口

第二步：调用accept()方法开始监听，等待客户端的链接

第三步：获取输入流，读取客户端信息

第四步：获取输出流，响应客户端信息

第五步：关闭资源

这里写一个简单的例子，实现服务端读取并客户端发送的消息，然后将客户端发送过来的信息再发回客户端。实现代码如下：

```java
package com.springboot.demo.socket.tcp;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Created by shirukai on 2018/9/19
 * 基于Tcp的socket服务端
 */
public class TcpSocketServer {
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    public TcpSocketServer() {
    }

    public TcpSocketServer(int port) {
        try {
            // 1. 创建一个服务器端Socket，指定监听端口
            ServerSocket serverSocket = new ServerSocket(port);
            // 2. 调用accept()方法开始监听，等待客户端的连接
            Socket client = serverSocket.accept();
            // 处理Socket
            handleSocket(client);
        } catch (IOException e) {
            log.error("Create ServerSocket failed:{}", e.getMessage());
            throw new RuntimeException("Create ServerSocket failed:" + e.getMessage());
        }
    }

    public void handleSocket(Socket client) {
        BufferedReader bufferedReader = null;
        BufferedWriter bufferedWriter = null;
        try {
            // 3. 获取输入流，读取客户端信息
            bufferedReader = new BufferedReader(new InputStreamReader(client.getInputStream()));
            // 4. 获取输出流，响应客户端信息
            bufferedWriter = new BufferedWriter(new OutputStreamWriter(client.getOutputStream()));
            String messages;
            while ((messages = bufferedReader.readLine()) != null) {
                log.info("Receive message sent by the client:{}", messages);
                bufferedWriter.write("Hi Client,Your message is " + messages + "\n");
                bufferedWriter.flush();
            }

        } catch (IOException e) {
            log.error("The Server accept error:{}", e.getMessage());
        } finally {
            // 5. 关闭资源
            try {
                if (bufferedWriter != null) {
                    bufferedWriter.close();
                }
                if (bufferedReader != null) {
                    bufferedReader.close();
                }
                if (client != null) {
                    client.close();
                }
            } catch (IOException e) {
                log.error("Close source error:{}", e.getMessage());
            }

        }
    }


    public static void main(String[] args) {
        TcpSocketServer socketServer = new TcpSocketServer(9090);
    }
}
```

### 2.2 基于TCP的Socket客户端

基于TCP的Socket客户端实现主要有四步：

第一步：创建客户端Socket，指定远程服务器的地址和端口

```java
Socket clientSocket = new Socket(remoteIp,remotePort)
```

第二步：获取输出流，用来向服务器发送信息

```java
clientSocket.getOutputStream()
```

第三步：获取输入流，用来获取服务器的响应

```java
clientSocket.getInputStream()
```

第四步：释放资源

```java
socket.close()
```

具体实现代码如下所示：

```java
package com.springboot.demo.socket.tcp;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.Socket;
import java.nio.charset.Charset;
import java.util.Scanner;

/**
 * Created by shirukai on 2018/9/19
 * 基于Tcp 的socket 客户端
 */
public class TcpSocketClient {
    private String remoteIp;
    private int remotePort;
    private Socket socket;
    private final Logger log = LoggerFactory.getLogger(this.getClass());
    private BufferedReader bufferedReader;
    private BufferedWriter bufferedWriter;

    public TcpSocketClient(String remoteIp, int port) {
        this.remoteIp = remoteIp;
        this.remotePort = port;
        connectRemote();
    }


    private void connectRemote() {
        try {
            // 1. 创建客户端Socket，指定远程服务器地址和端口
            this.socket = new Socket(remoteIp, remotePort);
            // 2. 获取输出流，向服务器发送信息
            this.bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            // 3. 获取输入流，获取服务器信息
            this.bufferedReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        } catch (IOException e) {
            log.error("Connect remote service error:{}", e.getMessage());
            throw new RuntimeException("Connect remote service error");
        }
    }

    public void sendByConsole() {
        Scanner scanner = new Scanner(System.in);
        log.info("Please enter the message: ");
        while (scanner.hasNextLine()) {
            // 读取键盘的输入
            String message = scanner.nextLine();
            sendMessage(message);
        }
        scanner.close();
    }

    public String sendMessage(String message) {
        String result = "";
        try {
            bufferedWriter.write(message + "\n");
            bufferedWriter.flush();
            result = bufferedReader.readLine();
            log.info("From Server:{}", result);
            log.info("Please enter the message: ");
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    // 4. 关闭资源
    public void release() {
        try {
            bufferedWriter.close();
            bufferedReader.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public static void main(String[] args) {

        TcpSocketClient client = new TcpSocketClient("127.0.0.1", 9090);
        client.sendByConsole();
        // 释放资源
        client.release();
    }
}
```

效果演示：

![](http://shirukai.gitee.io/images/b5a4d8ef620275748f867776653490ef.gif)

### 2.3 多线程的TCP Socket服务端

上面实现的TCP Socket的服务端，只能处理一个客户端的请求。现在我们要使用多线程，来实现服务端处理多个客户端请求。

```java
package com.springboot.demo.socket.tcp;

import com.google.common.util.concurrent.ThreadFactoryBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.*;

/**
 * Created by shirukai on 2018/9/19
 * 多线程的socket服务端
 */
public class ThreadSocketServer {
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    public ThreadSocketServer(int port) {
        try {
            // 1. 创建一个服务器端Socket，指定监听端口
            ServerSocket serverSocket = new ServerSocket(port);
            //创建线程池
            ThreadFactory namedThreadFactory = new ThreadFactoryBuilder().setNameFormat("thread-call-runner-%d").build();
            int size = 10;
            ExecutorService executorService = new ThreadPoolExecutor(size, size, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue<Runnable>(), namedThreadFactory);

            while (true) {
                //循环监听
                // 2. 调用accept()方法开始监听，等待客户端的连接
                Socket socket = serverSocket.accept();
                executorService.execute(() -> new TcpSocketServer().handleSocket(socket));
            }
        } catch (IOException e) {
            log.error("Create ServerSocket failed:{}", e.getMessage());
            throw new RuntimeException("Create ServerSocket failed:" + e.getMessage());
        }
    }

    public static void main(String[] args) {
        ThreadSocketServer socketServer = new ThreadSocketServer(9090);
    }
}
```

### 2.4 基于UDP的Sokcet服务端

基于UDP的Sokcet服务端实现步骤主要有：

第一步：创建服务器端DatagramSocket,指定端口

第二步：创建数据包，用于接收客户端发送的数据

第三步：接收客户端发来的信息

第四步：创建数据包，用于响应客户端

第五步：响应客户端

第六步：关闭资源

具体代码如下所示：

```scala
package com.springboot.demo.socket.udp;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 * Created by shirukai on 2018/9/19
 * 基于UDF的Socket服务端
 */
public class UDPSocketServer {
    public static void main(String[] args) throws Exception {
        // 1.创建服务器端DatagramSocket,指定端口
        DatagramSocket server = new DatagramSocket(9090);
        // 2.创建数据包，用于接收客户端发送的数据
        byte[] requestMessage = new byte[1024];
        DatagramPacket requestPacket = new DatagramPacket(requestMessage, requestMessage.length);
        // 3.接收客户端发来的信息
        server.receive(requestPacket);//此方法在接收到数据报之前一直会阻塞
        String info = new String(requestMessage, 0, requestPacket.getLength());
        System.out.println("客户端发来信息：" + info);
        // 4. 创建数据包，用于响应客户端
        InetAddress address = requestPacket.getAddress();
        int port = requestPacket.getPort();
        byte[] responseMessage = "欢迎你".getBytes();
        DatagramPacket responsePacket = new DatagramPacket(responseMessage, responseMessage.length, address, port);
        // 5. 响应客户端
        server.send(responsePacket);
        //关闭资源
        server.close();
    }
}
```



### 2.5 基于UDP的Sokcet客户端

基于UDF的Socket客户端的实现主要包括：

第一步：定义服务器的地址、端口号、数据

第二步：创建数据报，包含发送的数据信息

第三步：创建数据报，用于接收服务器响应的数据

第四步：接收服务器响应的数据

第五步：读取数据

第六步：关闭资源

具体实现代码如下所示：

```java
package com.springboot.demo.socket.udp;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 * Created by shirukai on 2018/9/19
 * 基于UDP的Socket客户端
 */
public class UDPSocketClient {
    public static void main(String[] args) throws Exception {
        // 1.定义服务器的地址、端口号、数据
        InetAddress address = InetAddress.getByName("localhost");
        int port = 9090;
        DatagramSocket client = new DatagramSocket();
        byte[] sendMessage = "向服务端发送信息".getBytes();
        // 2.创建数据报，包含发送的数据信息
        DatagramPacket sendPacket = new DatagramPacket(sendMessage, sendMessage.length, address, port);
        client.send(sendPacket);
        // 3.创建数据报，用于接收服务器响应的数据
        byte[] receiveMessage = new byte[1024];
        DatagramPacket receivePacket = new DatagramPacket(receiveMessage, receiveMessage.length);
        // 4.接收服务器响应的数据
        client.receive(receivePacket);
        // 5.读取数据
        String reply = new String(receiveMessage, 0, receivePacket.getLength());
        System.out.println(reply);
        // 6.关闭资源
        client.close();
    }
}

```

## 3 NIO Socket

上面一节，学习了java基本的Sokcet网络编程，接下来将学习一个新名词，NIO。java.nio全称java non-blocking IO（实际上是 new io），是指jdk1.4 及以上版本里提供的新api（New IO），为所有的原始类型（boolean类型除外）提供缓存支持的数据容器，使用它可以提供非阻塞式的高伸缩性网络。

关于更多的NIO的资料：

https://www.jianshu.com/p/3cec590a122f

这一节主要记录一下NIO Socket的学习，为什么要用NIO Socket？我们可以通过下面两张图来对比传统的BIO Socket。图片来自https://www.jianshu.com/p/b9f3f6a16911（Netty入门教程——认识Netty）

![](http://shirukai.gitee.io/images/cf028523cd1d9f3c0407428354b2beef.png)

<center>传统BIO Socket</center>

![](http://shirukai.gitee.io/images/1600992f4267319b4ef6b0ceb42a6dfc.png)

<center>NIO Sokcet</center>

从上面两张图可以看出，BIO想要通过多线程来实现多连接，因为单个Socket的会发生阻塞。而NIO的单线程的处理能力比BIO强的多，NIO处理socket的不会发送阻塞的现象。这是因为NIO把所有的Socket都交给Selector来处理，只需要不断的遍历Selector里的Socket的然后处理该Socket即可。

下面将分别以具体代码实现NIO Socket的服务端和客户端。

### 3.1 NIO Socket 服务端

NIO Socket服务端的实现主要有以下几步：

第一步： 创建一个信道并设置信道为非阻塞

```java
ServerSocketChannel channel = ServerSocketChannel.open();
// 设置信道为non-blocking（非阻塞） 默认为blocking
channel.configureBlocking(false);
```

第二步：从信道中获取SeverSocket并绑定监听端口

```java
ServerSocket socket = channel.socket();
// 获取本机的address
InetSocketAddress address = new InetSocketAddress(9001);
// 将端口绑定到ServerSocket上
socket.bind(address);
```

第三步： 创建一个Socket选择器

```java
Selector selector = Selector.open();
```

第四步： 将选择器注册到信道中

```java
// SelectKey四种状态：OP_CONNECT 连接就绪、OP_ACCEPT 接收就绪、OP_READ 读就绪、OP_WRITE 写就绪
channel.register(selector, SelectionKey.OP_ACCEPT);
```

第五步：搜索信道

```java
selector.select();
```

第六步： 获取准备好的信道所关联的key几步的iterator实例

```java
Iterator<SelectionKey> keyIterator = selector.selectedKeys().iterator();
```

第七步：遍历selectedKey，根据key的状态处理Socket

具体代码如下所示：

```java
package com.springboot.demo.netty;

import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

/**
 * Created by shirukai on 2018/9/27
 * 非阻塞 I/O socket
 */
public class NioSocketServer {
    public static void main(String[] args) {
        try {
            // 1. 创建一个信道并设置信道为非阻塞
            ServerSocketChannel channel = ServerSocketChannel.open();
            // 设置信道为non-blocking（非阻塞） 默认为blocking
            channel.configureBlocking(false);
            // 2. 从信道中获取ServerSocket并绑定监听端口
            ServerSocket socket = channel.socket();
            // 获取本机的address
            InetSocketAddress address = new InetSocketAddress(9001);
            // 将端口绑定到ServerSocket上
            socket.bind(address);
            // 3. 创建一个Socket选择器
            Selector selector = Selector.open();
            // 4. 将选择器注册到各个信道上
            // SelectKey四种状态：OP_CONNECT 连接就绪、OP_ACCEPT 接收就绪、OP_READ 读就绪、OP_WRITE 写就绪
            channel.register(selector, SelectionKey.OP_ACCEPT);
            while (true) {
                // 5. 搜索信道
                selector.select();
                // 6. 获取准备好的信道所关联的key集合的iterator实例
                Iterator<SelectionKey> keyIterator = selector.selectedKeys().iterator();
                // 7.遍历selectedKey,根据状态处理Socket
                while (keyIterator.hasNext()) {
                    // 获取key值
                    SelectionKey key = keyIterator.next();
                    keyIterator.remove();
                    try {
                        if (key.isAcceptable()) {
                            SocketChannel client = ((ServerSocketChannel) key.channel()).accept();
                            client.configureBlocking(false);
                            client.register(key.selector(), SelectionKey.OP_READ);
                            System.out.println("Accepted connection from: " + client);
                        }
                        if (key.isReadable()) {
                            SocketChannel client = (SocketChannel) key.channel();
                            ByteBuffer buffer = ByteBuffer.allocate(1024);
                            int readLength = client.read(buffer);
                            //如果有记录
                            if (readLength > 0) {
                                key.interestOps(SelectionKey.OP_READ);
                                String record = new String(buffer.array(), 0, readLength);
                                System.out.println(record);
                                client.write(ByteBuffer.wrap(("服务器已经接受消息：" + record).getBytes()));
                            }
                        }
                        if (key.isWritable()) {

                        }
                    } catch (Exception e) {
                        key.cancel();
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

```



### 3.2 NIO Socket 客户端

NIO Socket客户端的实现主要有以下几步：

第一步：创建一个信道，并绑定远程服务器的IP和端口

```java
SocketChannel channel = SocketChannel.open();
// 设置服务器的address
InetSocketAddress remote = new InetSocketAddress("127.0.0.1", 9001);
```

第二步： 连接远程服务器

```java
channel.connect(remote);
channel.configureBlocking(false);
```

第三步： 创建一个Socket选择器

```java
Selector selector = Selector.open();
```

第四步： 将选择器注册到信道中

```java
channel.register(selector, SelectionKey.OP_READ);
```

第五步： 启动一个县城用来接收服务器消息

第六步：从键盘获取输入发送给服务器

具体实现代买如下所示：

```java
package com.springboot.demo.netty;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.nio.charset.Charset;
import java.util.Scanner;

/**
 * Created by shirukai on 2018/9/27
 * Nio Socket Client
 */
public class NioSocketClient {
    public static void main(String[] args) {
        try {
            // 1. 创建一个信道,并绑定远程服务器的ip和端口
            SocketChannel channel = SocketChannel.open();
            // 设置服务器的address
            InetSocketAddress remote = new InetSocketAddress("127.0.0.1", 9001);
            // 2. 连接远程服务器
            channel.connect(remote);
            channel.configureBlocking(false);
            // 3. 创建一个Socket选择器
            Selector selector = Selector.open();
            // 4. 将选择器注册到信道中
            channel.register(selector, SelectionKey.OP_READ);
            // 5. 启动一个线程用来接收服务器消息
            new Thread(() -> {
                while (true) {
                    //读取数据
                    ByteBuffer buffer = ByteBuffer.allocate(1024);
                    int length = 0;
                    try {
                        length = channel.read(buffer);
                        if (length > 0) {
                            System.out.println(new String(buffer.array(), 0, length));
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }).start();
            // 6. 从键盘获取输入发送给服务器
            Scanner scanner = new Scanner(System.in);
            System.out.println("输入数据:\n");
            while (scanner.hasNextLine()) {
                System.out.println("输入数据:\n");
                // 读取键盘的输入
                String line = scanner.nextLine();
                // 将键盘的内容输出到SocketChannel中
                channel.write(Charset.forName("UTF-8").encode(line));
            }
            scanner.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

```

演示效果：

![](http://shirukai.gitee.io/images/4fe57a6e04fecc5f6d0c22a88416ff79.gif)