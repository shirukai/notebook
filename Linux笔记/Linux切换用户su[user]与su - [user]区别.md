# Linux切换用户su[user]与su - [user]区别

1. linux 系统中用户切换的命令为su，语法为：

su[-flmp][-c command][-s shell][--help][--version][-][USER[ARG]

参数说明：

-f ， -fast：不必启动文件（如sch.cshrc等），仅用于csh或tcsh两种Shell。

-l， -login：加了这个参数之后，就好像是重新登录一样，大部分环境变量（例如HOME、SHELL和USER等）都是一该使用者（USER）为主，并且工作目录也会改变，如果没有指定的USER，缺省情况是root

-m， -p -preserve  -environment：执行su时不改变环境 变数

-c command：变更账号为USER的使用者，并执行指令（command）后再变回原来的使用者

-help：显示说明文档

-version:显示版本信息

USER：想要切换的账号

ARG:传入新的SHELL参数

2. su[user]和su -[user]的区别
 
su [user]切换到其他用户，但是不切换环境变量，su - [user]则是完整的切换到新的用户环境