# NIFI学习记录

> 一个易于使用，功能强大且可靠的系统来处理和分发数据。

## 一、特征 

Apache NiFi支持强大且可扩展的数据路由，转换和系统中介逻辑的有向图。Apache NiFi的一些高级功能和目标包括：

- 基于Web的用户界面
  - 设计，控制，反馈和监控之间的无缝体验
- 高度可配置
  - 容忍损失与保证交付
  - 低延迟vs高吞吐量
  - 动态优先化
  - 流量可以在运行时修改
  - 背压
- 数据来源
  - 跟踪数据流从头到尾
- 为扩展而设计
  - 建立你自己的处理器等等
  - 实现快速开发和有效测试
- 安全
  - SSL，SSH，HTTPS，加密内容等...
  - 多租户授权和内部授权/策略管理

## 二、安装

官网下载: http://nifi.apache.org/download.html

版本：1.6.0

```
wget http://mirrors.hust.edu.cn/apache/nifi/1.6.0/nifi-1.6.0-bin.tar.gz
```

解压：

```
tar -zxvf nifi-1.6.0-bin.tar.gz
```

简单配置：

```
vi nifi-1.6.0/conf/nifi.properties
```

```
    133 nifi.web.war.directory=./lib
    134 nifi.web.http.host=192.168.66.193 #本机ip
    135 nifi.web.http.port=9191 #端口号
    136 nifi.web.http.network.interface.default=
    137 nifi.web.https.host=
    138 nifi.web.https.port=
    139 nifi.web.https.network.interface.default=
    140 nifi.web.jetty.working.directory=./work/jetty
    141 nifi.web.jetty.threads=200
    142 nifi.web.max.header.size=16 KB
    143 nifi.web.proxy.context.path=
    144 nifi.web.proxy.host=
```

nifi启动：

前台运行：bin/nifi.sh run

后台运行：bin/nifi.sh start

重新启动：bin/nifi,sh restart

![](https://shirukai.gitee.io/images/201804090947_695.png)

### 三、NiFi实例

#### 1.读取某个文件夹下的所有文件，并移动到到另一个文件夹下。

如：

将/root/shirukai/nifi_test/1目录下所有的文件，读取，然后存到/root/shirukai/nifi_test/2下

##### a.添加一个GetFile处理器，用于读取文件

![](https://shirukai.gitee.io/images/201804090954_965.png)

拖动处理器到画布，这时候会出现弹窗，需要我们选择合适的处理器，这时候我们在搜索框搜索 【GetFile】

![](https://shirukai.gitee.io/images/201804090956_168.png)

然后点击【ADD】将处理器添加到画布，如下图：

![](https://shirukai.gitee.io/images/201804090957_103.png)

配置GetFile处理器：选中处理器之后，右击鼠标，会弹出选项框，我们选择【Configure】进行处理器配置

![](https://shirukai.gitee.io/images/201804090958_350.png)

在弹出的配置框中我们选择【PROPERTIES】tab页来进行相关配置,在这里我们仅仅设置【Input Directory】输入的文件目录为：/root/shirukai/nifi_test/1即可，其他的过滤文件的正则等配置暂时用默认的。

![](https://shirukai.gitee.io/images/201804090959_128.png)

然后点击【APPLY】应用即可。

#### b 创建PutFile处理器 

创建PutFile的过程跟上面一样，先将处理器拖到画布中，然后搜索【PutFile】处理添加到画布。

![](https://shirukai.gitee.io/images/201804091011_762.gif)

配置PutFile处理器，在【PROPERTIES】的【Directory】的value值填为我们要将文件保存到的路径，然后点击【APPLY】

![](https://shirukai.gitee.io/images/201804091013_454.png)

#### c 建立连接，将GetFile与PutFile两个处理器连接 

![](https://shirukai.gitee.io/images/201804091018_255.gif)

建立连接完成后，我们会发现GetFile处理器前面出现一个停止的状态

![](https://shirukai.gitee.io/images/201804091019_330.png)

而PutFile处理前面为警告状态，将鼠标放到警告图标上，会出现警告信息，提示失败和成功关系无效，因为没有连接任何组件并且不会自动终止

![](https://shirukai.gitee.io/images/201804091020_530.png)

这时候我们在PutFile的配置里选择【SETTINGS】将自动终止关系的【failure】和【success】设置为勾选状态。

![](https://shirukai.gitee.io/images/201804091026_252.png)

#### d启动实例

在画布空白处右击会出现选项框，选择【start】运行实例

![](https://shirukai.gitee.io/images/201804091029_780.png)

运行状态如下图所示：

![](https://shirukai.gitee.io/images/201804091036_365.png)

这一个过程是一个实时的，只要/root/shirukai/nifi_test/1下有文件nifi就会移动到/root/shirukai/nifi_test/2目录下。

![](https://shirukai.gitee.io/images/201804091042_478.gif)

### 2.执行python脚本编写的wordCount实例

#### a 创建GenerateFlowFile处理器

将处理器图标拖到画布，并选择【GenerateFlowFile】处理器，用于生成流数据。

![](https://shirukai.gitee.io/images/201804091442_493.png)

修改GenerateFlowFile处理器，添加自定义文本，用来做单词计数的源文件。

在处理器配置里【PROPERTIES】里的【Custom Text】的value栏，将以下文本填入其中：

```
Apache NiFi supports powerful and scalable directed graphs of data routing, transformation, and system mediation logic. Some of the high-level capabilities and objectives of Apache NiFi include:
```

![](https://shirukai.gitee.io/images/201804091444_421.png)

#### b创建ExecuteScript处理器，用于执行脚本

如何编写脚本？可参考博客：https://blog.csdn.net/quguang65265/article/details/77916855

![](https://shirukai.gitee.io/images/201804091447_604.png)

配置ExecuteScript处理器，在【PROPERTIES】里的【Script Engine】选择执行的脚本语言，并将事先写好的脚本加到【Script Body】中。python脚本代码如下：

```
import re
import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
 
class WordCount(StreamCallback):
  def __init__(self):
        pass
  def process(self, inputStream, outputStream):
    words = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    words_array = re.split(r'(?:,|;|\s)\s*', words)
    word_count = {}
    for word in words_array:
        if word in word_count:
            tmp_count = word_count[word]
            word_count[word] = tmp_count + 1
        else:
            word_count[word] = 1
    word_str = ''
    for key, val in word_count.items():
        word_str += key + ":" + str(val) + "\n"
    outputStream.write(bytearray(word_str.encode('utf-8')))
 
flowFile = session.get()
if (flowFile != None):
  flowFile = session.write(flowFile, WordCount())
  flowFile = session.putAttribute(flowFile, "filename", "wordCount")
session.transfer(flowFile, REL_SUCCESS)
session.commit()
```

![](https://shirukai.gitee.io/images/201804091448_88.png)

#### c 添加PutFile处理器，用来将处理后的结果一文件的形式保存到指定目录下的文件里 

![](https://shirukai.gitee.io/images/201804091453_714.png)

配置Putfile处理器，添加要输出的文件目录

![](https://shirukai.gitee.io/images/201804091456_924.png)

d建立关联

![](https://shirukai.gitee.io/images/201804091501_466.gif)

执行：

![](https://shirukai.gitee.io/images/201804091503_49.gif)

结果：

![](https://shirukai.gitee.io/images/201804091506_679.png)

当然也可以从文件中读取数据，然后进行单词统计。只需添加一个FetchFile处理器，选择要获取数据的文件即可。



```

```

