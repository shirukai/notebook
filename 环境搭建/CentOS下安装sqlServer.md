# CentOS下安装SqlServer数据库

1.下载 Microsoft SQL Server Red Hat 存储库配置文件：

```
curl -o /etc/yum.repos.d/mssql-server.repo https://packages.microsoft.com/config/rhel/7/mssql-server-2017.repo
```

2.通过yum安装

```
yum install -y mssql-server
```

![](https://shirukai.gitee.io/images/201803301056_47.png)

3.运行包安装完成后mssql conf 安装并按照提示操作以设置 SA 密码，并选择你的版本，安装完成后会自动启动数据库服务。

```
/opt/mssql/bin/mssql-conf setup
```

> 注意，这一步需要选择所要安装的数据库版本和管理员sa账户密码，请按照实际需求选择版本，并记住所设置的密码。

![](https://shirukai.gitee.io/images/201803301057_398.png)

选择合适的版本，这里选择的是开发环境。

![](https://shirukai.gitee.io/images/201803301059_188.png)

同意条款，并选择语言，输入管理密码

4.查看是否启动成功

```
systemctl status mssql-server
```

![](https://shirukai.gitee.io/images/201803301100_955.png)

安装完成！

开放1433端口关闭防火墙即可远程连接。