# Python 使用subprocess开启新进程之旅

> 版本说明：Python2.7

感觉好久没有写博客了，最近接连两项工作，忙的不亦乐乎，难得空档期，做一下笔记总结。同样是工作中遇到的问题，简单描述一下：有这样一段脚本，它执行时间比较长，而且不断地有标准输出，需要Flask提供REST服务去异步执行这段脚本，并且实时捕获标准输出，通过WebSocket推送给前台。关键点：异步调用，实时获取标准输出，并且可能涉及到实时交互。当时解决这个问题，一开始使用的是Python的输出重定向sys.stdout，然后重写write方法，将输出写到Queue里，然后起一个线程轮询Queue,但是发现输出不全，而且对于输出的控制不理想。重要的是无法进行交互。后来发现使用Python的subprocess能够很好的解决问题。

# 1 关于subprocess

官网：https://docs.python.org/2/library/subprocess.html

subprocess模块允许我们生成一个新进程，连接到新进程的输出、输出、错误管道，并获取它们的返回码。该模块旨在替换几个比较旧的模块和功能

```python
os.system
os.spawn*
os.popen*
popen2.*
commands.*
```

那么我们到底可以使用subprocess来做什么呢？执行一个程序，执行一个shell命令，调用一个脚本等。

# 2 使用subprocess

## 2.1 call()

call()方法能便捷的调用一个程序，并得到执行的返回码。该方法是同步执行，需要等待命令执行完成，并且stdout不能指向PIPE，默认继承父进程的输出。

```python
subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
```

args可以是字符串，也可以是列表，如果是字符串的话，会被当做shell命令，必须指定shell=True。args为列表的话，列表第一个元素会认为是程序路径，后面元素为参数。如我要执行"ls ."这个命令，可以使用call("ls .",shell=True)，它相当于call(['/bin/sh','-c','ls .'])。我们也可以直接使用call(['ls','.'])该方法返回值是一个返回码，表示该进行执行的状态，如果返回0表示正常，返回其它状态码表示异常。

如：我们使用call方法，执行命令ls .查看当前路径所有的文件

```python
"""
使用call()方法执行一个命令
返回值为0说明执行成功，此命令不能将输出定向到PIPE
非异步
"""
return_code = subprocess.call('ls .', shell=True)
print return_code
```

## 2.2 check_call()

check_call()方法与call类似，不同点在于，该方法会检查返回状态，如果返回码不等于0将抛出[`CalledProcessError`](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError)异常。

```python
subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
```

该方法的参数与call()相同，返回值也是返回码。

```python
"""
使用check_all()方法执行一个命令
返回码不为0，将会抛出CalledProcessError异常
非异步
"""
subprocess.check_call(['ls', '.'], shell=False)
subprocess.check_call('exit 1', shell=True)
```

![](https://raw.githubusercontent.com/shirukai/images/master/42c92e611a9b574ad6800d091f352bee.jpg)

## 2.3 check_output()

上述的两个方法，返回值都是一个状态码，表示该进程的结果状态，而输出信息都是定向到父进程的标准输出里了，有时候我们需要拿到执行某条命令的结果，我们可以使用check_output()方法。它可以返回执行的结果，如果执行失败同样会抛出[`CalledProcessError`](https://docs.python.org/2/library/subprocess.html#subprocess.CalledProcessError)异常，此方法也是同步的。

```python
subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False)
```

该方法前面几个参数与上述几个方法相同，universal_newlines方法表示是否换行，默认为False，如果为True会在返回的输出后面添加"\n"进行换行。

```python
"""
使用check_output()方法执行一个命令
返回码不为0，将会抛出CalledProcessError异常
运行正常，将会把标准输出结果返回,
要想将标准错误返回，可以使用stderr=subprocess.STDOUT
非异步
"""
output = subprocess.check_output(['echo', 'hello world'], universal_newlines=True)
print output
```

## 2.4 Popen 构造器

subprocess可以使用Popen构造，功能更强大，使用更灵活，可以做到异步调用，实时交互等。

```python
subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)
```

### 2.4.1 参数说明

Popen构造器所需要的参数列表如下所示：

| 参数名称                    | 说明                                                         |
| --------------------------- | ------------------------------------------------------------ |
| args                        | 字符串或者是列表，表示被调用程序的路径和参数                 |
| bufsize                     | 0 表示无缓存<br />1 表示行缓冲 <br />其它正值 表示缓冲区大小<br />负值 采用系统默认缓冲(全缓冲) |
| executable                  | 可执行程序，如果为None取args列表的第一个值                   |
| stdin<br/>stdout<br/>stderr | None 没有任何重定向，继承父进程<br />PIPE 创建管道<br/>文件对象<br/>文件描述符(整数)<br/>stderr 还可以设置为STDOUT |
| preexec_fn                  | 钩子函数，在fork和exec之前执行(unix)                         |
| close_fds                   | unix下执行新进程之前是否关闭0/1/2之外的文件<br/>windows下不继承是继承父进程的文件描述符 |
| shell                       | unix下相当于在args前面添加了"/bin/sh" "-c"<br/>window下相当于添加"cmd.exe /c" |
| cwd                         | 设置工作目录                                                 |
| env                         | 设置环境变量                                                 |
| universal_newlines          | 添加换行符"\n"                                               |
| startupinfo                 | window下传递给CreateProcess的结构体                          |
| creationflags               | window下，传递CREATE_NEW_CONSOLE创建自己的控制台窗口         |

### 2.4.2 方法说明

使用Popen构造器产生的对象具有以下方法。

| 方法名称                | 说明                                                         |
| ----------------------- | ------------------------------------------------------------ |
| poll()                  | 检查子进程是否已经结束，设置并返回returncode属性，非结束返回None |
| wait()                  | 阻塞主进程等待子线程完成，返回returncode，注意：如果子进程输出了大量数据到stdout或者stderr的管道，并达到了系统pipe的缓存大小的话，子进程会等待父进程读取管道，而父进程此时正wait着的话，将会产生传说中的死锁，后果是非常严重滴。建议使用communicate() 来避免这种情况的发生。 |
| communicate(input=None) | 和子进程交互，发送数据到stdin，并从stdout和stderr读数据，直到收到EOF，阻塞，一直等待子进程结束。input输出要为字符串。该方法返回一个元组(stdoutdata,stderrdata)。注意：要给子进程的stdin发送数据，则Popen的时候，stdin要为PIPE；同理，要可以接收数据的话，stdout或者stderr也要为PIPE。 |
| send_signal(signal)     | 在子进程发送signal信号，注意：window下目前只支持发送SIGTERM，等效于小面的terminate() |
| terminate()             | 停止子进程。Posix下是发送SIGTERM信号。windows下是调用TerminateProcess()这个API。 |
| kill()                  | 杀死子进程。Posix下是发送SIGKILL信号。windows下和terminate() 无异。 |
| stdin                   | 如果stdin 参数是PIPE，此属性就是一个文件对象，否则为None 。  |
| stdout                  | 如果stdout参数是PIPE，此属性就是一个文件对象，否则为None。   |
| stderr                  | 如果stderr参数是PIP，此属性就是一个文件对象，否则为None。    |
| pid                     | 子进程的进程号。注意，如果shell 参数为True，这属性指的是子shell的进程号。 |
| returncode              | 子程序的返回值，由poll()或者wait()设置，间接地也由communicate()设置。<br/>如果为None，表示子进程还没终止。<br/>如果为负数-N的话，表示子进程被N号信号终止。（仅限unix） |

# 3 应用Demo

## 3.1 调用脚本并获取实时输出

假如我有如下名为callme.py的脚本，我想使用subprocess实时调用，该怎么写？

```python
# encoding: utf-8
"""
@author : shirukai
@date : 2019-05-16 10:03
用来测试subprocess脚本调用
"""
import time

if __name__ == '__main__':
    for i in range(10):
        print "I was called {0} times.".format(str(i + 1))
        time.sleep(5)

```

可以这样写：

```python
    process = subprocess.Popen(['python', 'callme.py'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    while process.poll() is None:
        print process.stdout.readline()
```

https://stackoverflow.com/questions/874815/how-do-i-get-real-time-information-back-from-a-subprocess-popen-in-python-2-5

