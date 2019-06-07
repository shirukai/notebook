# linux中使用echo更改用户密码

1. 创建用户

```
useradd 用户名
```
2. 用echo设置用户密码


```
echo 密码|passwd --stdin 用户名

//这个选项用于 从标准输入 管道读入新的密码
```

3. 用passwd设置密码


```
passwd 用户名
```
