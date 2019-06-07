# Java接口对Hadoop集群的操作 

> 首先要有一个配置好的Hadoop集群
>
> 这里是我在SSM框架搭建的项目的测试类中实现的

## 一、windows下配置环境变量 

### 下载文件并解压到C盘或者其他目录。

链接：http://pan.baidu.com/s/1jHHPElg 密码：aufd

### 配置环境变量

#### 1.配置HADOOP_HOME 

![https://shirukai.gitee.io/images/1509948477662hadoop.png](https://shirukai.gitee.io/images/1509948477662hadoop.png)

#### 2.配置PATH

在PATH中添加

```
%HADOOP_HOME%\bin
```

#### 3.配置HADOOP_USER_NAME 

这是Hadoop集群的用户名

```
HADOOP_USER_NAME root
```

## 二、Maven处理依赖jar包 

```
    <!--hadoop依赖-->
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-client</artifactId>
      <version>2.7.4</version>
    </dependency>
    <dependency>
      <groupId>commons-io</groupId>
      <artifactId>commons-io</artifactId>
      <version>2.4</version>
    </dependency>
```

## 三、创建测试类 

```
package com.mavenssmlr.hadoop;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * java接口对Hadoop进行操作
 * 1.配置环境变量：HADOOP_HOME
 * HADOOP_USER_NAME
 * Created by shirukai on 2017/11/2.
 */


@RunWith(SpringJUnit4ClassRunner.class)
//告诉junit spring配置文件
@ContextConfiguration({"classpath:spring/spring-dao.xml"})
public class TestHadoop {
    private Logger logger = LoggerFactory.getLogger(this.getClass());


    /**
     * 连接Hadoop
     */
    public FileSystem connectHadoop() {
        String nameNodeUrl = "hdfs://10.110.13.243:9000";
        String nameNodeName = "fs.defaultFS";
        FileSystem fs = null;
        Configuration configuration = new Configuration();
        try {
            configuration.set(nameNodeName, nameNodeUrl);
            fs = FileSystem.get(configuration);
            logger.info("连接成功：Path={}", fs.getFileStatus(new Path("/")));
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        return fs;
    }

    /**
     * 创建目录
     *
     * @throws Exception 异常
     */
    @Test
    public void mkdirFolder() throws Exception {
        FileSystem fs = connectHadoop();
        String folderName = "/input";
        fs.mkdirs(new Path(folderName));
    }

    /**
     * 上传文件到Hadoop
     *
     * @throws Exception 异常
     */
    @Test
    public void uploadFile() throws Exception {
        FileSystem fs = connectHadoop();
        //定义本地上传的文件路径
        String localFilePath = "D://Hadoop//upload//";
        //定义上传文件
        String fileName = "user.xlsx";
        //定义要上传到的文件夹
        String uploadFolder = "/input/";

        InputStream in = new FileInputStream(localFilePath + fileName);
        OutputStream out = fs.create(new Path(uploadFolder + fileName));

        IOUtils.copyBytes(in, out, 4096, true);

    }

    /**
     * 从Hadoop获取文件
     *
     * @throws Exception 异常
     */
    @Test
    public void getFileFromHadoop() throws Exception {
        FileSystem fs = connectHadoop();
        //定义要下载路径
        String downloadPath = "/input/";
        //定义要下载的文件名
        String downloadFileName = "user.xlsx";
        //定义要保存的路径
        String savePath = "D://Hadoop//download//" + downloadFileName;

        InputStream in = fs.open(new Path(downloadPath + downloadFileName));
        OutputStream out = new FileOutputStream(savePath);
        IOUtils.copyBytes(in, out, 4096, true);
    }

    /**
     * 删除文件
     * delete(path,boolean)
     * boolean如果为true，将进行递归删除，子目录及文件都会删除
     * false 只删除当前
     *
     * @throws Exception
     */
    @Test
    public void deleteFile() throws Exception {
        FileSystem fs = connectHadoop();
        //要删除的文件路径
        String deleteFilePath = "/inputuser.xlsx";
        Boolean deleteResult = fs.delete(new Path(deleteFilePath), true);
        logger.info("删除文件：={}", deleteResult);
    }

    /**
     * 遍历指定目录下所有的文件
     * @throws Exception 异常
     */
    @Test
    public void getAllFile()throws Exception{
        FileSystem fs = connectHadoop();
        //定义要获取的目录
        String getPath = "/";
        FileStatus[] statuses = fs.listStatus(new Path(getPath));
        for (FileStatus file: statuses
             ) {
            logger.info("fileName={}",file.getPath().getName());
        }
    }

    @Test
    public void otherOption() throws Exception{
        FileSystem fs = connectHadoop();
    }

}

```

