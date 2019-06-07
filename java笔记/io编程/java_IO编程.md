# java_IO编程
## 一、流的概念
### 什么是流？
流是一个抽象出来的概念，具体说是对[输入/输出]设备的抽象（内存、网络、磁盘），对系统读写API的封装，对外提供数据操作接口
### 基本概念
流：数据在文件和程序（内存）之间经历的路径
输入流：数据从文件到程序（内存）的路径
输出流：数据从程序（内存）到文件的路径

根据处理数据类型的不同可以分为：字节流（抽象基类为InputStream和OutputStream)和字符流（抽象基类为Reader和Writer）根据流向不同可以分为：输入流、输出流，其中主要结构可以用下图来表示：
![image](https://shirukai.gitee.io/images/1349867949_2253.png)

### 字符流和字节流的主要区别
1. 字节流读取数据的时候，读到一个字节就返回一个字节；字符流读到一个字节（中文对应的字节数是两个，在UTF-8码表中是3个字节）时，先去查指定的编码表，将查到的字符返回。
2. 字节流可以处理所有类型数据，如：图片、MP3、AVI视频文件，二字符流只能处理字符数据。只要是处理纯文本数据，就要有限考虑使用字符流，除此之外都用字节流。

### IO流主要分为节点流和处理流两大类
#### 一、节点流类型

该类型可以从或者向一个特定的地点或者节点读写数据，主要类型如下：

类型 | 字符流 |字节流
---|---|---
File(文件)	|FileReader FileWriter|FileInputStream FileOutputSream
Memory Array|	CharArrayReader CharArrayWriter|ByteArrayInputStream    ByteArrayOutputSream
Memory String|StringReader StringWriter|   -
Pipe(管道)	|PipedReader PipedWriter|PipedInputSream PipedOutputSream

#### 二、处理流类型
该类型是对一个已存在的流的连接和封装，通过所封装的流的功能调用实现数据读写、处理流的构造方法总是要爱一个其他流作对象作为参数，一个流对象经过其他流的多次包装，叫做流的链接。主要可以分为以下几种：
1. 缓冲流（BufferedInPutStream/BufferedOutPutStream和BufferedWriter/BufferedReader）他可以提高对流的操作效率。

写入缓冲区对象

```
BufferedWriter bw = new BufferedWriter(writer);
```
读取缓冲区对象

```
BufferedReader br = new BufferedReader(reader);
```
 该类型的流有一个特有的方法：readLine()；一次读一行，到行标记时，将行标记之前的字符数据作为字符串返回，当读到末尾时，返回null，其原理还是与缓冲区关联的流对象的read方法，只不过每一次读取到一个字符，先不进行具体操作，先进行临时储存，当读取到回车标记时，将临时容器中储存的数据一次性返回。

```
while ((line = br.readLine())!=null&& line!=""){
                if (!"".equals(line.trim())){
                    result.add(line.trim());//读取词名及其对应的数量
                }
            }
```
2. 转换流（InputStreamReader/OutputStreamWriter）
 
      该类型时字节流和字符流之间的桥梁，该流对象中可以对读取到的字节数据进行指定编码的编码转换。
      构造函数主要有：


```
InputStreamReader(InputStream);        //通过构造函数初始化，使用的是本系统默认的编码表GBK。  
 InputStreamWriter(InputStream,String charSet);   //通过该构造函数初始化，可以指定编码表。  
 OutputStreamWriter(OutputStream);      //通过该构造函数初始化，使用的是本系统默认的编码表GBK。  
 OutputStreamwriter(OutputStream,String charSet);   //通过该构造函数初始化，可以指定编码表。
```
实例：

```
InputStreamReader reader = new InputStreamReader(new FileInputStream(targetFile));
```
 3. 数据流（DataInputStream/DataOutputStream）
该数据流可以方便地对一些基本类型数据进行直接的存储和读取，不需要再进一步进行转换，通常只要操作基本数据类型的数据，就需要通过DataStream进行包装。

构造方法： 

```
DataInputStreamReader（InputStream）；  
 DataInputStreamWriter（OutputStream）；
```
方法举例：

```
int readInt()；//一次读取四个字节，并将其转成int值  
writeInt(int)；//一次写入四个字节，注意和write(int)不同，write(int)只将该整数的最低一个8位写入，剩余三个8为丢失  
hort readShort();  
writeShort(short);  
String readUTF();//按照utf-8修改版读取字符，注意，它只能读writeUTF()写入的字符数据。  
 writeUTF(String);//按照utf-8修改版将字符数据进行存储，只能通过readUTF读取。
```
>注意：在使用数据流读/存数据的时候，需要有一定的顺序，即某个类型的数据先写入就必须先读出，服从先进先出的原则。

4. 打印流（PrintStream/PrintWriter）
 
PrintStream是一个字节打印流，System.out对应的类型就是PrintStream，它的构造函数可以接受三种数据类型的值：


字符串路径。

File对象 

OutputStream


PrintStream是一个字符打印流，它的构造函数可以接受四种类型的值：1.字符串路径。2.File对象 3.OutputStream  4.Writer  对于1、2类型的数据，可以指定编码表，也就是字符集，对于3、4类型的数据，可以指定自动刷新，当该自动刷新为True时，只有3个方法可以用：println,printf,format。
 
5. 对象流（ObjectInputStream/ObjectOutputStream）

该类型的流可以把类作为一个整体进行存取，主要方法有：
Object readObject();该方法抛出异常：ClassNotFountException。
void writeObject(Object)：被写入的对象必须实现一个接口：Serializable，否则就会抛出：NotSerializableException