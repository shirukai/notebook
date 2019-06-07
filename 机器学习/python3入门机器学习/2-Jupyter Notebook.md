## 快捷键

a 单元格之前创建新的单元格

b单元格之后创建新的单元格

dd 删除当前单元格

ctrl+enter 运行单元格

## Jupyter Notebook高级-魔法命令

### %run

运行.py的文件

比如我要执行当前notebook所在的目录下的myscript目录里有一个hello.py文件

```
%run myscript/hello.py
```

![](https://shirukai.gitee.io/images/201805081655_697.png)

### 引入包

在notebook里引入一个包，直接用import即可

![](https://shirukai.gitee.io/images/201805081700_289.png)

### %timeit

显示项目运行的时间

![](https://shirukai.gitee.io/images/201805081727_725.png)



### %lsmagic

查询所有魔法命令

### %run ？

查看run命令的用法

## numpy.array 基础

### 创建numpy.array

```
nparr2 = np.array([1,1.0,2])
```

