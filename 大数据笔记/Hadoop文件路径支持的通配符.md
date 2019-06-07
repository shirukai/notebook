# Hadoop文件路径支持的通配符

> 摘自《Hadoop权威指南》

## 1 Hadoop中的通配符

在单个操作中处理一批文件，这是一个常见要求，举例来说，处理日志的MapReduce作业可能需要分析一个月内包含在大量目录中的日志文件。在一个表达式中使用通配符来匹配多个文件是比较方便的，无需列举每个文件和目录来指定输入，该操作称为“通配符”（globbing）。Spark读取文件时，也可以使用通配符去匹配文件，直接在文件路径里使用通配符表达式即可。Hadoop 为执行统配提供了两个FileSystem方法：

```
public FileStatus[] globStatus(Path pathPattern) throws IOException {
    return (new Globber(this, pathPattern, DEFAULT_FILTER)).glob();
}

public FileStatus[] globStatus(Path pathPattern, PathFilter filter) throws IOException {
    return (new Globber(this, pathPattern, filter)).glob();
}
```

globStatus() 方法返回与路径想匹配的所有文件的FileStatus对象数组，并按照路径排序。PathFilter命令作为可选项可进一步对匹配进行限制。

Hadoop支持的通配符与Unix bash 相同，如下表所示：

<center>表 通配符及其含义</center>

| 通配符 | 名称       | 匹配                                                         |
| ------ | ---------- | ------------------------------------------------------------ |
| *      | 星号       | 匹配0或多个字符串                                            |
| ?      | 问号       | 匹配单一字符                                                 |
| [ab]   | 字符类     | 匹配{a,b}集合中的一个字符                                    |
| [^ab]  | 非字符类   | 匹配非{a,b}集合中的一个字符                                  |
| [a-b]  | 字符范围   | 匹配一个在{a,b}范围内的字符（包含a,b），a在字典顺序上要小于或等于b |
| [^a-b] | 非字符范围 | 匹配一个不在{a,b}范围内的字符（包含a,b），a在字典顺序上要小于或等于b |
| {a,b}  | 或选择     | 匹配包含a或b中的一的表达式                                   |
| \c     | 转义字符   | 匹配元字符c                                                  |

## 2 Demo

### 2.1 列出目录下的所有文件或者文件夹元数据信息

```java
// 列出指定目录下的所信息
log.info("Get metadata for all files and directories.");
FileStatus[] statuses = fs.listStatus(new Path("/MergedParquetData/000000/"));
for (FileStatus status : statuses) {
    log.info("path={}",status.getPath());
}
```

![](http://shirukai.gitee.io/images/2899c8e42962f1f552fb9809207c0d65.jpg)

### 2.2 列出目录下通配符匹配的文件或者文件夹元数据信息

```java
// 使用通配符匹配
log.info("Get metadata for files and directories by globbing.");
FileStatus[] globStatuses = fs.globStatus(new Path("/MergedParquetData/000000/2018092*"));
for (FileStatus status : globStatuses) {
    log.info("path={}",status.getPath());
}
```

![](http://shirukai.gitee.io/images/90210bae5a90f36a6064a96c06e745e3.jpg)

### 2.3 列出目录下通配符匹配并且使用PathFilter过滤的文件或者文件夹元数据信息

#### 创建RegexExculdePath类继承PathFilter类

创建RegexExculdePath类，使用正则表达式过滤路径，代码如下：

```java
package learn.demo.hadoop.hdfs.usecase;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.PathFilter;

/**
 * Created by shirukai on 2018/10/13
 */
public class RegexExcludePathFilter implements PathFilter {
    private final String regex;

    public RegexExcludePathFilter(String regex) {
        this.regex = regex;
    }

    public boolean accept(Path path) {
        return !path.toString().matches(regex);
    }
}

```

#### 使用正则表达式过滤通配符匹配过的路径

```java
// 使用正则表达式过滤通配符匹配过的路径
log.info("Get metadata for files and directories by globbing and filter by regex.");
FileStatus[] filterStatuses = fs.globStatus(new Path("/MergedParquetData/000000/2018092*"),
                                            // 通过正则表达式做过滤
                                            new RegexExcludePathFilter("^.*/2018092*[5|6]"));
for (FileStatus status : filterStatuses) {
    log.info("path={}",status.getPath());
}
```

![](http://shirukai.gitee.io/images/7d4be3874ae930f98f5198a5b231a513.jpg)

完整代码：

```java
package learn.demo.hadoop.hdfs.usecase;

import learn.demo.hadoop.hdfs.util.HdfsUtils;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by shirukai on 2018/10/13
 */
public class ListFileTest {
    private static final Logger log = LoggerFactory.getLogger(ListFileTest.class);
    public static void main(String[] args) throws Exception {
        String uri = "hdfs://cdh-master:8020";
        // 获取FileSystem
        FileSystem fs = HdfsUtils.getFileSystem(uri);
        // 列出指定目录下的所信息
        log.info("Get metadata for all files and directories.");
        FileStatus[] statuses = fs.listStatus(new Path("/MergedParquetData/000000/"));
        for (FileStatus status : statuses) {
            log.info("path={}",status.getPath());
        }
        // 使用通配符匹配
        log.info("Get metadata for files and directories by globbing.");
        FileStatus[] globStatuses = fs.globStatus(new Path("/MergedParquetData/000000/2018092*"));
        for (FileStatus status : globStatuses) {
            log.info("path={}",status.getPath());
        }
        // 使用正则表达式过滤通配符匹配过的路径
        log.info("Get metadata for files and directories by globbing and filter by regex.");
        FileStatus[] filterStatuses = fs.globStatus(new Path("/MergedParquetData/000000/2018092*"),
                // 通过正则表达式做过滤
                new RegexExcludePathFilter("^.*/2018092*[5|6]"));
        for (FileStatus status : filterStatuses) {
            log.info("path={}",status.getPath());
        }

    }
}

```

