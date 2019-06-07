# 更改Linux登录的shell

1. 查看linux一共有哪些shell

```
chsh -l
```
2. 查看当前用户执行的shell

```
echo $ SHELL //SHELL一定要大写
```
3. 修改当前用户的shell为bin/sh


```
chsh -s /bin/sh
```
