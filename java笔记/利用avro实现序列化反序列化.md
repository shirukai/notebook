# 利用avro实现序列化/反序列化

摘一段来自https://www.jianshu.com/p/a5c0cbfbf608简书上介绍avro的内容：

Avro是一个数据序列化系统，设计用于支持大批量数据交换的应用。

它的主要特点有：支持二进制序列化方式，可以便捷，快速地处理大量数据；动态语言友好，Avro提供的机制使动态语言可以方便地处理Avro数据。

当前市场上有很多类似的序列化系统，如Google的Protocol Buffers, Facebook的Thrift。这些系统反响良好，完全可以满足普通应用的需求。针对重复开发的疑惑，Doug Cutting撰文解释道：Hadoop现存的RPC系统遇到一些问题，如性能瓶颈(当前采用IPC系统，它使用Java自带的DataOutputStream和DataInputStream)；需要服务器端和客户端必须运行相同版本的Hadoop；只能使用Java开发等。但现存的这些序列化系统自身也有毛病，以Protocol Buffers为例，它需要用户先定义数据结构，然后根据这个数据结构生成代码，再组装数据。如果需要操作多个数据源的数据集，那么需要定义多套数据结构并重复执行多次上面的流程，这样就不能对任意数据集做统一处理。其次，对于Hadoop中Hive和Pig这样的脚本系统来说，使用代码生成是不合理的。并且Protocol Buffers在序列化时考虑到数据定义与数据可能不完全匹配，在数据中添加注解，这会让数据变得庞大并拖慢处理速度。其它序列化系统有如Protocol Buffers类似的问题。所以为了Hadoop的前途考虑，Doug Cutting主导开发一套全新的序列化系统，这就是Avro，于09年加入Hadoop项目族中。

## 1 在maven项目中使用avro实现序列化/反序列化

### 1.1 引入依赖并添加avro插件

```xml
<dependency>
    <groupId>org.apache.avro</groupId>
    <artifactId>avro</artifactId>
    <version>1.8.2</version>
</dependency>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.avro</groupId>
                <artifactId>avro-maven-plugin</artifactId>
                <version>1.8.2</version>
                <executions>
                    <execution>
                        <phase>generate-sources</phase>
                        <goals>
                            <goal>schema</goal>
                        </goals>
                        <configuration>
                            <sourceDirectory>${project.basedir}/src/main/avro/</sourceDirectory>
                            <outputDirectory>${project.basedir}/src/main/java/</outputDirectory>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
```

说明：

${project.basedir}/src/main/avro/ 是用来存放avsc文件的路径

${project.basedir}/src/main/java/  用来存放输出类的路径



### 1.2 创建avsc文件

在项目中的src/mian/avro/目录下创建user.avsc文件，内容如下：

```json
{"namespace": "com.springboot.demo.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "age",  "type": ["int", "null"]},
     {"name": "favorite", "type": ["string", "null"]}
 ]
}
```

### 1.3 根据avsc文件生成类

执行maven install

![](http://shirukai.gitee.io/images/00dc9e3f127105eef06e06d1371281d3.jpg)

执行完成后会在${project.basedir}/src/main/java/目录下生成一个User.java的类

### 1.4 序列化

```java
    @Test
    public void serialization() throws Exception {
        User user = new User("shirukai", 18, "computer");
        User user2 = User.newBuilder().setName("licuiping").setAge(18).setFavorite("eat").build();
        DatumWriter<User> userDatumWriter = new SpecificDatumWriter<User>(User.class);
        DataFileWriter<User> dataFileWriter = new DataFileWriter<User>(userDatumWriter);
        dataFileWriter.create(user.getSchema(), new File("src/main/avro/users.avro"));
        dataFileWriter.append(user);
        dataFileWriter.append(user2);
        dataFileWriter.close();
    }
```

### 1.5 反序列化

```java
@Test
public void deserialization() throws Exception {
    DatumReader<User> userDatumReader = new SpecificDatumReader<User>(User.class);
    DataFileReader<User> dataFileReader = new DataFileReader<User>(new File("src/main/avro/users.avro"), userDatumReader);
    User user = null;
    while (dataFileReader.hasNext()) {
        user = dataFileReader.next(user);
        System.out.println(user);
    }
}
```

