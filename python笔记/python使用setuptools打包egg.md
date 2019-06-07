# Python使用setuptools打包egg

作为Python标准的打包及分发工具，setuptools可以说相当得简单易用。相面记录一下Python如何利用setuptools进行分发打包。

## 安装Setuptools

方式一：通过python安装

```
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py
```

方式二：yum 安装

```
yum install python-setuptools
```

## 打包一个简单的egg文件

创建一个setup-demo目录

```
mkdir setup-demo
```

进入setup-demo目录并创建一个firstapp的目录

```
cd setup-demo
mkdir firstapp
```

进入firstapp创建一个.py文件

```
vi say_hello_word.py
```

内容为：

```
say():
  print('hello word !')
```

在setup-demo目录下创建一个setup.py的文件

```
vi setup.py
```

内容为：

```
from setuptools import setup
setup(
  name="firsapp",
  version="1.0",
  packages=['firstapp']
)
```

name为打包app的名字

version为版本号

packages为要打包的包名，可以通过数组的形式指定，也可以通过from setuptools import find_packages 这个方法，读取setup.py所在目录的所有包

```
packages=find_packages()
```

最后整个目录结构如下所示：

```
[root@localhost setup-demo]# find ./
./
./firstapp
./firstapp/say_hello_word.py
./setup.py
```

打包成egg文件

```
python setup.py bdist_egg
```

打包后的目录结构如下图所示：

```
[root@localhost setup-demo]# find ./
./
./firstapp
./firstapp/say_hello_word.py
./setup.py
./firsapp.egg-info
./firsapp.egg-info/PKG-INFO
./firsapp.egg-info/top_level.txt
./firsapp.egg-info/dependency_links.txt
./firsapp.egg-info/SOURCES.txt
./build
./build/lib
./build/lib/firstapp
./build/lib/firstapp/say_hello_word.py
./build/bdist.linux-x86_64
./dist
./dist/firsapp-1.0-py2.7.egg
```

生成的egg文件会保存在dist目录下面。

## 安装egg

安装egg文件，其实就是通过命令将打包的应用安装到python环境的“site-packages”目录下，这样其他程序就可以向导入标准库一样导入该应用的代码了。

安装

```
python setup.py install
```

![](https://shirukai.gitee.io/images/201804161434_161.png)

或者

```
easy_install firsapp-1.0-py2.7.egg
```



测试

```
[root@localhost dist]# python
Python 2.7.5 (default, Nov  6 2016, 00:28:07) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from firstapp.say_hello_word import say
>>> say()
hello word !

```



## 引入非Python文件

上例子中只将包下的python文件打包，如果要打包一些非.py的文件，需要在setup.py的同级添加一个MANIFEST.in的配置文件，来告诉setuptools我们打包的东西包括哪些内容。

例如：我们在创建一个名为secondapp包，里面有一个word文件夹，用来存放一个words.txt的文件，我们来读取这个文件里的内容，然后输出。

目录结构如下所示：

```
[root@localhost secondapp]# find ./
./
./secondapp
./secondapp/word
./secondapp/word/words.txt
./secondapp/__init__.py
./secondapp/handle_word.py
./setup.py
./MANIFEST.in
```

words.txt

```
Here are some words to deal with
```

handle_word.py

```
import os
def print_words():
        f_p = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'word/words.txt')
        print(f_p)
        with open(f_p) as f :
            print(f.read())

```

MANIFEST.in 

清单文件，用来列出想要引入的目录路径

```
recursive-include secondapp/word *
```

“recursive-include”表明包含子目录。别急，还有一件事要做，就是在”setup.py”中将” include_package_data”参数设为True：

```
from setuptools import setup
setup(
  name="secondapp",
  version="1.0",
  packages=['secondapp'],
  include_package_data=True 
)
```

如果不想包含某些目录，可以添加以下配置

```
setup(
    ...
    include_package_data=True,    # 启用清单文件MANIFEST.in
    exclude_package_date={'':['.gitignore']}
)
```

打包

```
python setup.py install
```

测试

```
[root@localhost site-packages]# python
Python 2.7.5 (default, Nov  6 2016, 00:28:07) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from secondapp.handle_word import print_words as pw
>>> pw()
/usr/lib/python2.7/site-packages/secondapp-1.0-py2.7.egg/secondapp/word/words.txt
Here are some words to deal with

```



参考博客：http://python.jobbole.com/87240/