# python 获取路径的常见方法



## sys.path 

测试执行路径为：D:\Repository\testapi\learnpath\LearnPath.py

执行以下命令：

```
print(sys.path)
```

结果:

```
[
    "D:\\Repository\\testapi\\learnpath",
    "D:\\Repository\\testapi",
    "C:\\WINDOWS\\SYSTEM32\\python27.zip",
    "C:\\Python27\\DLLs",
    "C:\\Python27\\lib",
    "C:\\Python27\\lib\\plat-win",
    "C:\\Python27\\lib\\lib-tk",
    "C:\\Python27",
    "C:\\Python27\\lib\\site-packages",
    "C:\\Python27\\lib\\site-packages\\win32",
    "C:\\Python27\\lib\\site-packages\\win32\\lib",
    "C:\\Python27\\lib\\site-packages\\Pythonwin",
    "C:\\Program Files\\JetBrains\\PyCharm 2017.3.2\\helpers\\pycharm_matplotlib_backend"
]
```

所以使用sys.path[0]就能得到当前执行文件的工作路径了。

如果讲这个py里定义的方法，在别的文件里引用，再执行，就是当前执行的文件的路径。

如：

在D:\Repository\testapi\learnpath\LearnPath.py这个文件下定义一个变量：

```
LEARN_PATH = sys.path[0]
```

在D:\Repository\testapi\test\Test.py这个文件下引入，并执行打印：

```
import learnpath.LearnPath as LearnPath

if __name__ == "__main__":
    print(LearnPath.LEARN_PATH)
```

得到的结果：

```
C:\Python27\python.exe D:/Repository/testapi/test/Test.py
D:\Repository\testapi\test

Process finished with exit code 0
```

## sys.argv 

执行：

```
if __name__ == '__main__':
    print(sys.argv)
```

结果：

```
C:\Python27\python.exe D:/Repository/testapi/learnpath/LearnPath.py
['D:/Repository/testapi/learnpath/LearnPath.py']

Process finished with exit code 0
```

获取当前执行文件的文件路径,包含文件名，返回的是一个数组，通过sys.argv[0]来获取。

## os.getcwd() 

结果跟sys.path[0]一样

```
D:\Repository\testapi\learnpath
```

##  os.path.abspath(`__file__`)

获取所在文件的绝对路径，包含路径名

```
ABS_PATH = os.path.abspath(__file__)
if __name__ == '__main__':
    print(ABS_PATH)
```

```
C:\Python27\python.exe D:/Repository/testapi/test/Test.py
D:\Repository\testapi\learnpath\LearnPath.py

Process finished with exit code 0
```

如果在别的地方引用，同样返回的是上面的结果。

如果要去除文件名，只获取文件目录 os.path.dirname(LearnPath.ABS_PATH)

```
print(os.path.dirname(LearnPath.ABS_PATH))
```

```
C:\Python27\python.exe D:/Repository/testapi/test/Test.py
D:\Repository\testapi\learnpath

Process finished with exit code 0
```

## os.path.realpath(`__file__`)

获取所在文件的真实路径

```
REAL_PATH = os.path.realpath(__file__)
if __name__ == '__main__':
    print(REAL_PATH)
```

```
C:\Python27\python.exe D:/Repository/testapi/test/Test.py
D:\Repository\testapi\learnpath\LearnPath.py

Process finished with exit code 0
```

