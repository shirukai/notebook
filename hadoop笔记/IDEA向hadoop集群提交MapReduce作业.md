# IDEA向Hadoop集群提交作业环境搭建 

windows环境：IntelliJ IDEA 2017.2.3、JRE: 1.8.0_152-release-915-b11 、hadoop-2.7.4.tar.gz、hadoop-common-2.2.0-bin-master.rar

## 一、windows下配置hadoop环境 

### 1.解压hadoop-2.7.4.tar.gz到c盘(或者任意目录)

解压hadoop-2.7.4.tar.gz到C盘，路径为：C:\hadoop-2.7.4

解压 hadoop-common-2.2.0-bin-master.rar 并复制bin目录下所有的文件到 C:\hadoop-2.7.4\bin目录下

hadoop-common-2.2.0-bin-master.rar的下载链接：http://pan.baidu.com/s/1jHHPElg 密码：aufd

### 2.配置hadoop的环境变量 

![https://shirukai.gitee.io/images/1510112190836ZTGONK2UJN_2~_~GXQFXBOB.png](https://shirukai.gitee.io/images/1510112190836ZTGONK2UJN_2~_~GXQFXBOB.png)

```
变量名：HADOOP_HOME          路径：C:\hadoop-2.7.4
变量名：HADOOP_BIN_PATH      路径：%HADOOP_HOME%\bin
变量名：HADOOP_PREFIX        路径：C:\hadoop-2.7.4
变量名：HADOOP_USER_NAME     路径：root  
变量名：Path                 添加 %HADOOP_HOME%\bin
								 %HADOOP_HOME%\sbin
```

注意 HADOOP_USER_NAME 是集群中HADOOP用户的名字

### 3.配置内网映射 

修改C:\Windows\System32\drivers\etc\hosts文件，添加集群里/etc/hosts相同的主机映射

```
192.168.162.177 Master.Hadoop
192.168.162.155 Slave1.Hadoop
192.168.162.166 Slave2.Hadoop
```

## 二、搭建项目 

### 1.IDEA创建Maven项目 

![https://shirukai.gitee.io/images/1510112985864createmavenproject.gif](https://shirukai.gitee.io/images/1510112985864createmavenproject.gif)

### 2.在pom.xml中加入依赖 

加入依赖后需要点击右侧工具栏的maven然后点击刷新。

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>testHadoop</groupId>
    <artifactId>testHadoop</artifactId>
    <version>1.0-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-client</artifactId>
            <version>2.7.4</version>
        </dependency>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-common</artifactId>
            <version>2.7.4</version>
        </dependency>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-hdfs</artifactId>
            <version>2.7.4</version>
        </dependency>
    </dependencies>

</project>
```

### 3.配置项目

将hadoop集群中的配置文件：core-site.xml、mapred-site.xml、yarn-site.xml、log4j.properties复制到resource目录下。

#### core-site.xml

```
<configuration>
 <property>
    <name>fs.default.name</name>
    <value>hdfs://Master.Hadoop:9000</value>
    <description>HDFS的URI，文件系统://namenode标识:端口号</description>
</property>

<property>
    <name>hadoop.tmp.dir</name>
    <value>/usr/hadoop/tmp</value>
    <description>namenode上本地的hadoop临时文件夹</description>
</property>
<property>
   <name>io.file.buffer.size</name>
   <value>131073</value>
</property>
</configuration>
```

#### mapred-site.xml 

```
<configuration>
<property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
          <property>
                  <name>mapreduce.jobhistory.address</name>
                  <value>Master.Hadoop:10020</value>
          </property>
          <property>
                <name>mapreduce.jobhistory.webapp.address</name>
                <value>Master.Hadoop:19888</value>
       </property>
</property>
</configuration>
```

#### yarn-site.xml

```
<configuration>

<!-- Site specific YARN configuration properties -->
<property>
  <name>yarn.resourcemanager.address</name>
  <value>Master.Hadoop:18040</value>
</property>
<property>
  <name>yarn.resourcemanager.scheduler.address</name>
  <value>Master.Hadoop:18030</value>
</property>
<property>
  <name>yarn.resourcemanager.webapp.address</name>
  <value>Master.Hadoop:18088</value>
</property>
<property>
  <name>yarn.resourcemanager.resource-tracker.address</name>
  <value>Master.Hadoop:18025</value>
</property>
<property>
  <name>yarn.resourcemanager.admin.address</name>
  <value>Master.Hadoop:18141</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services</name>
  <value>mapreduce_shuffle</value>
</property>
<property>
  <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
  <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
```

#### log4j.properties

```
log4j.rootLogger=INFO, stdout
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=%d{ABSOLUTE} | %-5.5p | %-16.16t | %-32.32c{1} | %-32.32C %4L | %m%n
```

### 4.补全目录 

在java下创建org.hadoop.mrs包用来存放Mapper、Reducer、MR类

在java下创建org.hadoop.run包用来存放Main方法

![https://shirukai.gitee.io/images/1510119968249directory2017118134506.png](https://shirukai.gitee.io/images/1510119968249directory2017118134506.png)



### 5.创建静态方法 

在run目录下创建一个RunHadoop类，然后创建一个静态方法

```
package org.hadoop.run;


public class RunHadoop {
    public static void main(String[] args){
        //TODO 这里写运行mapperReduce的方法

    }
} 
```

### 6.导出jar 

配置jar位置，并复制路径。如下图所示

![https://shirukai.gitee.io/images/1510120931849exportjar.gif](https://shirukai.gitee.io/images/1510120931849exportjar.gif)

最终的生成的jar路径为：D:\Repository\testHadoop\out\artifacts\testHadoop_jar\testHadoop.jar

### 7.连接配置 

##### 连接类 (用于配置与hadoop的连接)

在org.hadoop包下创建conf包用来编写连接类

然后在org.hadoop.conf包下创建Conf.java类

```
package org.hadoop.conf;

import org.apache.hadoop.conf.Configuration;

/**
 * 获得hadoop连接配置
 * Created by shirukai on 2017/11/8.
 */
public class Conf {
    public static Configuration get (){
        //hdfs的链接地址
        String hdfsUrl = "hdfs://Master.Hadoop:9000";
        //hdfs的名字
        String hdfsName = "fs.defaultFS";
        //jar包文位置(上一个步骤获得的jar路径)
        String jarPath = " D:\\Repository\\testHadoop\\out\\artifacts\\testHadoop_jar\\testHadoop.jar";

        Configuration conf = new Configuration();
        conf.set(hdfsName,hdfsUrl);
        conf.set("mapreduce.app-submission.cross-platform", "true");
        conf.set("mapreduce.job.jar",jarPath);
        return conf;
    }
}

```

#### 文件类(对HDFS文件进行操作)

在org.hadoop包下创建files包用来编写文件类

然后在org.hadoop.files包下创建Files.java类

```
package org.hadoop.files;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.log4j.Logger;
import org.hadoop.conf.Conf;

import java.io.*;

/**
 * 对HDFS文件操作
 * Created by shirukai on 2017/11/8.
 */
public class Files {
    private static Logger logger = Logger.getLogger("this.class");
    public static  FileSystem getFiles() {
        //获得连接配置
        Configuration conf = Conf.get();
        FileSystem fs = null;
        try {
            fs = FileSystem.get(conf);
        } catch (IOException e) {
            logger.error("配置连接失败"+e.getMessage());
        }
        return fs;
    }

    /**
     * 创建文件夹
     */
    public static void mkdirFolder(String folderPath) {
        try {
            FileSystem fs = getFiles();
            fs.mkdirs(new Path(folderPath));
            logger.info("创建文件夹成功："+folderPath);
        } catch (Exception e) {
            logger.error("创建失败"+e.getMessage());
        }

    }


    /**
     * 上传文件到hdfs
     *
     * @param localFolderPath 本地目录
     * @param fileName        文件名
     * @param hdfsFolderPath  上传到hdfs的目录
     */
    public static void uploadFile(String localFolderPath, String fileName, String hdfsFolderPath) {
        FileSystem fs = getFiles();
        try {
            InputStream in = new FileInputStream(localFolderPath + fileName);
            OutputStream out = fs.create(new Path(hdfsFolderPath + fileName));
            IOUtils.copyBytes(in, out, 4096, true);
            logger.info("上传文件成功："+fileName);
        } catch (Exception e) {
            logger.error("上传文件失败"+e.getMessage());
        }
    }


    /**
     * 从hdfs获取文件
     *
     * @param downloadPath     hdfs的路径
     * @param downloadFileName hdfs文件名
     * @param savePath         保存的本地路径
     */
    public static void getFileFromHadoop(String downloadPath, String downloadFileName, String savePath) {
        FileSystem fs = getFiles();
        try {
            InputStream in = fs.open(new Path(downloadPath + downloadFileName));
            OutputStream out = new FileOutputStream(savePath + downloadFileName);
            IOUtils.copyBytes(in, out, 4096, true);
        }  catch (Exception e) {
            logger.error("获取文件失败"+e.getMessage());
        }
    }

    /**
     * 删除文件
     * delete(path,boolean)
     * boolean如果为true，将进行递归删除，子目录及文件都会删除
     * false 只删除当前

     */
    public static void deleteFile(String deleteFilePath) {
        FileSystem fs = getFiles();
        //要删除的文件路径
        try {
            Boolean deleteResult = fs.delete(new Path(deleteFilePath), true);

        } catch (Exception e) {
            logger.error("删除文件失败"+e.getMessage());
        }
    }

    /**
     * 日志打印文件内容
     * @param filePath 文件路径
     */
    public static void readOutFile(String filePath) {
        try {
            InputStream inputStream = getFiles().open(new Path(filePath));
            BufferedReader bf = new BufferedReader(new InputStreamReader(inputStream, "GB2312"));//防止中文乱码
            String line = null;
            while ((line = bf.readLine()) != null) {
                logger.info(line);
            }

        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }
}

```

#### 8.测试

在RunHadoop的main方法里添加方法：

```
public class RunHadoop {
    public static void main(String[] args){
        //创建目录 
        String folderName = "/test";
        Files.mkdirFolder(folderName);
    }
}
```

运行main方法，然后http://192.168.162.177:50070/explorer.html#/查看是否创建目录



至此一个远程执行Hadoop作业的程序已经完成，下面将一个具体的MapReduce例子来运行这个项目

## 三、测试运行wordCount

接下来我们做一个MapReduce基础案例wordCount。利用MapReduce来统计words.txt文件里，每个单词出现的个数。

### 1.准备

在org.hadoop.mrs下创建一个wordcount的目录

在D:\Hadoop\upload创建一个名字为words.txt文本文档，保存格式为utf-8内容如下

```
this is a tests
this is a tests
this is a tests
this is a tests
this is a tests
this is a tests
this is a tests
this is a tests
this is a tests
```

### 2.编写mapper类

在org.hadoop.mrs.wordcount目录下出创建WordCountMapper类

```
package org.hadoop.mrs.wordcount;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * LongWritable 行号 类型
 * Text 输入的value 类型
 * Text 输出的key 类型
 * IntWritable 输出的vale类型
 * Created by shirukai on 2017/11/8.
 */
public class WordCountMapper extends Mapper<LongWritable,Text,Text,IntWritable> {
    /**
     *
     * @param key 行号
     * @param value 第一行的内容 如  this is a tests
     * @param context 输出
     * @throws IOException 异常
     * @throws InterruptedException 异常
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        //以空格分割获取字符串数组
        String[] words = line.split(" ");
        for (String word : words) {
            context.write(new Text(word),new IntWritable(1));
        }
    }
}
```

### 3.编写Reducer类 

在org.hadoop.mrs.wordcount目录下创建WordCountReucer类

```
package org.hadoop.mrs.wordcount;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Text 输入的key的类型
 * IntWritable 输入的value的类型
 * Text 输出的key类型
 * IntWritable 输出的value类型
 * Created by shirukai on 2017/11/8.
 */
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

    /**
     *
     * @param key 输入map的key
     * @param values 输入map的value
     * @param context 输出
     * @throws IOException 异常
     * @throws InterruptedException 异常
     */
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int count = 0;
        for (IntWritable value : values) {
            count += value.get();
        }
        context.write(key, new IntWritable((count)));
    }
}

```

### 4.编写 WordCountMR类

在org.hadoop.mrs.wordcount目录下出创建WordCountMR类

```
package org.hadoop.mrs.wordcount;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.hadoop.conf.Conf;
import org.hadoop.files.Files;


/**
 *
 * Created by shirukai on 2017/11/8.
 */
public class WordCountMR {
    //输入文件路径
    private static String inPath = "/word_input/words.txt";
    //输出文件目录
    private static String outPath = "/word_output/words_result.txt";
    public  int MR() throws Exception{
            //获取连接配置
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"wordCount");

            //设置job的主类
            job.setJarByClass(WordCountMR.class);
            //设置job的mapper类和reducer类
            job.setMapperClass(WordCountMapper.class);
            job.setReducerClass(WordCountReducer.class);

            //设置Mapper的输出类型
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(IntWritable.class);
            //设置Reduce的输出类型
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(IntWritable.class);
            //设置输入和输出路径
            FileSystem fs = Files.getFiles();
            Path inputPath = new Path(inPath);
            FileInputFormat.addInputPath(job,inputPath);
            Path outputPath = new Path(outPath);
            fs.delete(outputPath,true);

            FileOutputFormat.setOutputPath(job,outputPath);
            return job.waitForCompletion(true)?1:-1;

    }
}

```

### 5.编写WordCountRun方法 

org.hadoop.wordcount下创建WordCountRun类

```
package org.hadoop.mrs.wordcount;

import org.apache.log4j.Logger;
import org.hadoop.files.Files;

/**
 * 执行WordCount
 * Created by shirukai on 2017/11/8.
 */
public class WordCountRun {
    private static Logger logger = Logger.getLogger("this.class");

    public static void Run() {
        //创建word_input目录
        String folderName = "/word_input";
        Files.mkdirFolder(folderName);
        //创建word_input目录
        folderName = "/word_output";
        Files.mkdirFolder(folderName);
        //上传文件
        String localPath = "D:\\Hadoop\\upload\\";
        String fileName = "words.txt";
        String hdfsPath = "/word_input/";
        Files.uploadFile(localPath, fileName, hdfsPath);
        //执行wordcount

        try {
            new WordCountMR().MR();
            //成功后下载文件到本地
            String downPath = "/word_output/";
            String downName = "part-r-00000";
            String savePath = "D:\\Hadoop\\download\\";
            Files.getFileFromHadoop(downPath, downName, savePath);
        } catch (Exception e) {
            logger.error(e.getMessage());
        }

    }
}

```



### 5.编写主方法

org.hadoop.run先编写RunHadoop的主方法

```
package org.hadoop.run;

import org.hadoop.files.Files;
import org.hadoop.mrs.wordcount.WordCountMR;

/**
 *
 * Created by shirukai on 2017/11/8.
 */
public class RunHadoop {
    public static void main(String[] args) {
           WordCountRun.Run();
    }
}

```

### 6.运行主方法

运行结果：

```
a	9
is	9
tests	9
this	9
```

