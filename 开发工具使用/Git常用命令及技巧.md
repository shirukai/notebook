# Git常用命令及技巧

## 1 git stash

应用场景：当修改当前分支文件（非新建），且要切换到其它分支时，系统会提示如下信息，这时需要缓存当前分支更改的内容，然后才可以切换分支。

![](http://shirukai.gitee.io/images/856d10967c0c3697b3ac33a6120bf145.jpg)

### 1.1 git stash save

缓存当前更改的内容

```shell
git stash save -a "change1"
```

```
Saved working directory and index state On master: change1
```

### 1.2 git stash list

查看所有的缓存

```shell
git stash list
```

```
shirukaideMacBook-Pro:git-test shirukai$ git stash list
stash@{0}: On master: change1
```

### 1.3 git stash pop

还原缓存

```shell
git stash pop 0
```

![](http://shirukai.gitee.io/images/1fa403e9a5b4f96c491887e6a3d85959.jpg)

### 1.4 git stash drop

删除某个缓存

```shell
git stash drop 0
```

```
shirukaideMacBook-Pro:git-test shirukai$ git stash drop 0
Dropped refs/stash@{0} (d4006767bed1a93250dc3420b4619eeb3f1ad088)
```

### 1.5 git stash clear

删除所有缓存

```shell
git stash clear
```

## 2 添加新的远程仓库

```shell
git init
git remote add origin 远程仓库地址xxxxx.git
git add .
git commit
git push -u origin master
```



## 3 拉取远程仓库的的分支（本地不存在的分支）

```shell
git checkout -b 本地分支名 origin/远程分支名
```



## 4 删除分支

### 4.1 删除一个不是当前打开的分支

```shell
git branch -d 分支名称
```

### 4.2 删除一个正在使用的分支

```shell
git branch -D 分支名称
```



https://www.cnblogs.com/utank/p/7880441.html