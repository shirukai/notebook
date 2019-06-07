## ansible.cfg配置

```
1）inventory 
该参数表示资源清单inventory文件的位置，资源清单就是一些Ansible需要连接管理的主机列表 
inventory = /root/ansible/hosts

2）library 
Ansible的操作动作，无论是本地或远程，都使用一小段代码来执行，这小段代码称为模块，这个library参数就是指向存放Ansible模块的目录 
library = /usr/share/ansible

3）forks 
设置默认情况下Ansible最多能有多少个进程同时工作，默认设置最多5个进程并行处理。具体需要设置多少个，可以根据控制主机的性能和被管理节点的数量来确定。 
forks = 5

4）sudo_user 
这是设置默认执行命令的用户，也可以在playbook中重新设置这个参数 
sudo_user = root
//注意:新版本已经作了修改，如ansible2.4.1下已经为：
default_sudo_user = root 

5）remote_port 
这是指定连接被关节点的管理端口，默认是22，除非设置了特殊的SSH端口，不然这个参数一般是不需要修改的 
remote_port = 22

6）host_key_checking 
这是设置是否检查SSH主机的密钥。可以设置为True或False 
host_key_checking = False

7）timeout 
这是设置SSH连接的超时间隔，单位是秒。 
timeout = 20

8）log_path 
Ansible系统默认是不记录日志的，如果想把Ansible系统的输出记录到人i治稳健中，需要设置log_path来指定一个存储Ansible日志的文件 
log_path = /var/log/ansible.log

另外需要注意，执行Ansible的用户需要有写入日志的权限，模块将会调用被管节点的syslog来记录，口令是不会出现的日志中的

9）private_key_file

在使用ssh公钥私钥登录系统时候，使用的密钥路径。

private_key_file=/path/to/file.pem
```

官网：http://docs.ansible.com/ansible/latest/intro_configuration.html#private-key-file



## ansible hosts 配置文件

密码的配置方式：

```
[group_name]
192.168.162.180 ansible_ssh_user=root ansible_ssh_pass=root
```

秘钥的配置方式：

```
[group_name]
192.168.162.180 ansible_ssh_user=root ansible_ssh_private_file=idrsapath
```

别名的配置方式

```
test1 ansible_ssh_host=192.168.162.180 ansible_ssh_port=22 ansible_ssh_user=root ansible_ssh_pass=root
```



## ad-hoc相关参数

```
-v, --verbose：输出更详细的执行过程信息，-vvv可得到所有执行过程信息。

-i PATH, --inventory=PATH：指定inventory信息，默认/etc/ansible/hosts。

-f NUM, --forks=NUM：并发线程数，默认5个线程。

--private-key=PRIVATE_KEY_FILE：指定密钥文件。

-m NAME, --module-name=NAME：指定执行使用的模块。

-M DIRECTORY, --module-path=DIRECTORY：指定模块存放路径，默认/usr/share/ansible，也可以通过ANSIBLE_LIBRARY设定默认路径。

-a 'ARGUMENTS', --args='ARGUMENTS'：模块参数。

-k, --ask-pass SSH：认证密码。

-K, --ask-sudo-pass sudo：用户的密码（—sudo时使用）。

-o, --one-line：标准输出至一行。

-s, --sudo：相当于Linux系统下的sudo命令。

-t DIRECTORY, --tree=DIRECTORY：输出信息至DIRECTORY目录下，结果文件以远程主机名命名。

-T SECONDS, --timeout=SECONDS：指定连接远程主机的最大超时，单位是：秒。

-B NUM, --background=NUM：后台执行命令，超NUM秒后kill正在执行的任务。

-P NUM, --poll=NUM：定期返回后台任务进度。

-u USERNAME, --user=USERNAME：指定远程主机以USERNAME运行命令。

-U SUDO_USERNAME, --sudo-user=SUDO_USERNAM：E使用sudo，相当于Linux下的sudo命令。

-c CONNECTION, --connection=CONNECTION：指定连接方式，可用选项paramiko (SSH), ssh, local。Local方式常用于crontab 和 kickstarts。

-l SUBSET, --limit=SUBSET：指定运行主机。

-l ~REGEX, --limit=~REGEX：指定运行主机（正则）。

--list-hosts：列出符合条件的主机列表，不执行任何其他命令

```

## ad-hoc模式常用模块

![](http://shirukai.gitee.io/images/1f6ec4995c8631b857c83c06f44baf2a.jpg)

![](http://shirukai.gitee.io/images/1cc4a3c2bea11b9be1881288e1d560be.jpg)



## play book

![](http://shirukai.gitee.io/images/dcde9fedc2ad2a920f27d7db4caf0888.jpg)

![](http://shirukai.gitee.io/images/50772333ea001ceebe7ee40a41c8a604.jpg)



mysql

```
   - name: Install Requirement Packages
     yum: name={{ item }} state=present update_cache=yes
     with_items:
     - mysql-devel
     - MySQL-python
   - name: change password
     mysql_user:
       login_user=root login_password={{ tmppassword.stdout }} user=root password=root  priv=*.*:ALL,GRANT state=present
   - debug: var=tmppassword

```

