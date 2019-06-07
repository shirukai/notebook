# shell编程积累

## 一、Shell脚本中8种字符串截取方法

给定变量 str=home/user/test.jar 

```
export str="home/user/test.jar"
echo $str
home/user/test.jar
```

### 1.#截取

删除指定字符的左侧字符，保留右侧字符

从左到右找到第一个匹配的字符，然后进行截取

```
echo ${str#*/}
user/test.jar
```

### 2.##截取

同样是删除指定字符的左侧字符，保留右侧字符

但是##是从左到右找到最后一个匹配的字符，然后进行截取

```
echo ${str##*/}
test.jar
```

### 3.%截取

与单个#相反，删除指定字符的右侧字符，保留左侧字符

从右到左找到第一个匹配的字符，然后进行截取

```
echo ${str%/*}
home/user
```

### 4.%%截取

与##相反，删除指定字符的左侧字符，保留右侧字符

从右到左找到最后一个匹配的字符，然后进行截取

```
echo ${str%%/*}
home
```

### 5.从左边第几个字符开始，及字符个数

从左起第四个字符开始，截取6个字符

```
echo ${str:4:6}
/user/
```

### 6.从左边第几个字符开始一直到结束

从左起第四个字符，一直到结束

```
echo ${str:4}
/user/test.jar
```

### 7.从右边第几个字符开始，及字符个数

从右边起第四个字符，向右截取截取6个字符

```
echo ${str:0-4:6}
.jar
```

### 8.从右边第几个字符开始一直到结束

从右边起第四个字符，一直到结束

```
echo ${str:0-4}
.jar
```

## 二、shell中字符串比较相等、不相等方法

http://www.jb51.net/article/56559.htm

```
if [ $artifacts_suffix == "zip" ];then
unzip -o ${artifacts_dir}$artifacts_name -d ${artifacts_dir}${artifacts_name%%.*}
execute_artifacts_path=$artifacts_unzip_dir/azkaban.py
fi
```

## 三、shell 判断上一条命令是否执行成功

```
if [ $? -ne 0 ];then
echo execute error!
exit 1
fi
```

