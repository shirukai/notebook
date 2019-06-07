# Linux常用解压缩操作

## gzip 对文件进行解压缩 

压缩

~~~
gzip -v helloword.txt
~~~

查看压缩内容

~~~
zcat helloword.txt.gz
~~~

解压缩文件

```
gzip -d helloword.txt.gz
```

使用最佳压缩比，并保留原文件

~~~
gzip -9 -c helloword.txt > helloword.txt.gz
~~~

## bzip2 对文件进行解压缩 

压缩

```
bzip2 -z hellowrd.txt
```

查看压缩文件

```
bzcat helloword.txt.bz2
```

解压文件

```
bzip2 -d helloword.txt.bz2
```

使用最佳压缩比，并保留源文件

```
bzip2 -9 -c helloword.txt > helloword.txt.bz2
```

## 利用tar对文件夹进行打包解压缩

```
gzip：

bzip2：

tar:             打包压缩

 -c              归档文件

 -x              解压文件

 -z              gzip压缩文件

 -j              bzip2压缩文件
 
 -v              显示压缩或解压缩过程 v(view)

 -f              使用档名
```

例：

tar -cvf /home/abc.tar /home/abc              只打包，不压缩

tar -zcvf /home/abc.tar.gz /home/abc        打包，并用gzip压缩

tar -jcvf /home/abc.tar.bz2 /home/abc      打包，并用bzip2压缩

当然，如果想解压缩，就直接替换上面的命令  tar -cvf  / tar -zcvf  / tar -jcvf 中的“c” 换成“x” 就可以了。