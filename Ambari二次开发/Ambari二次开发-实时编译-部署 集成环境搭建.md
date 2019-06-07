# Ambari二次开发-实时编译-部署 集成环境搭建
总体思路：对ambari-web、ambari-admin进行单独编译，利用brunch watch功能，对文件源码进行实时监控编译。ambari-web/public 里存放编译完成的文件，（这里的文件目录与部署ambari后  /usr/lib/ambari-server/web 里的相同），对/usr/lib/ambari-server/web 建立软链接到public，就能实现 开发-编译-web可视化 的功能。
#### 开发人员只需走的流程：
    1. 本地访问samba共享目录里的源码进行二次开发
    2. 访问虚拟机地址:8080 查看效果
    3. 刷新页面

## 第一步：安装虚拟机
1. 安装虚拟机
- 进行傻瓜式安装。注意：安装过程中 虚拟机安装目录可以在非C盘，硬盘大小调到120G，确保有足够大的空间。
2. 编辑虚拟机设置
- 点击第四行CD/DVD（IDE）,点击右侧的使用ISO映像文件，选择CentOS-7-x86-DVD-1611.iso，点击确定。**开启此虚拟机**
3. 配置虚拟机
- 选择语言，简体中文。
- 点击网络和主机名：
> 1. 开启以太网连接
> 2. 点击配置，IPv4设置，方法：手动；Add:填写信息：点击编辑-->虚拟网络编辑器-->点击第二栏-->NAT设置-->子网IP，前三位保持一致，最后一位自己取，子网掩码和网关都有了。DNS搜索器和网关一致。
- 禁用KDUMP

4. 点击安装，并点击左上角设置一下用户密码。

## 第二步：复制相关文件
说明：这里需要复制ambari源码文件、ambari部署文件以及一些配置环境中用到的软件包
1.  利用xshell连接虚拟机
  文件——新建——输入主机地址——确定——用户名——密码——成功连接
2.  打开 新建文件传输
3.  访问/opt目录，将相关文件复制到虚拟机
  ambari源码文件：apache-ambari-2.4.1-src
  ambari部署文件：deployer-inspur
  maven软件包：apache-maven-3.0.5-bin.tar.gz
4.  解压文件

```
tar zxvf deployer-inspur.tar //解压部署文件
tar zxvf apache-ambari-2.4.1-src.tar //解压源码文件
```
> 注意：czvf 是压缩命令，zxvf是解压命令。

>知识点：linux对文件的解压缩操作

```
tar命令
　　解包：tar zxvf FileName.tar
　　打包：tar czvf FileName.tar DirName
　
gz命令
　　解压1：gunzip FileName.gz
　　解压2：gzip -d FileName.gz
　　压缩：gzip FileName
　　.tar.gz 和 .tgz
　　解压：tar zxvf FileName.tar.gz
　　压缩：tar zcvf FileName.tar.gz DirName
   压缩多个文件：tar zcvf FileName.tar.gz DirName1 DirName2 DirName3 ...

bz2命令
　　解压1：bzip2 -d FileName.bz2
　　解压2：bunzip2 FileName.bz2
　　压缩： bzip2 -z FileName
　　.tar.bz2
　　解压：tar jxvf FileName.tar.bz2
　　压缩：tar jcvf FileName.tar.bz2 DirName

bz命令
　　解压1：bzip2 -d FileName.bz
　　解压2：bunzip2 FileName.bz
　　压缩：未知
　　.tar.bz
　　解压：tar jxvf FileName.tar.bz

Z命令
　　解压：uncompress FileName.Z
　　压缩：compress FileName
　　.tar.Z
　　解压：tar Zxvf FileName.tar.Z
　　压缩：tar Zcvf FileName.tar.Z DirName
　　
zip命令
　　解压：unzip FileName.zip
　　压缩：zip FileName.zip DirName
```

## 第三步：利用samba建立共享连接
### 一、 yum 安装samba
1. 检查是否安装
```
#rpm -qa | grep samba
```
2. 未安装的话，执行安装命令

```
yum install samba
```
3. 重启smb服务

```
service smb restart
```
4. 在Linux上建立samba用户

```
useradd samba
```
5. 创建Smb用户，此用户必须是Linux上已经建立的，输入密码，完成即可
```
smbpasswd -a root
```
> 注意：smbpasswd  -a 是添加用户的意思 后面跟的是用户名，此用户名一定要跟linux登录用户名一样。smbpasswd -x 用户名 ：是删除用户的意思

###   二、关闭防火墙
a.  查看防火墙状态
```
systemctl status firewalld
```
b.  查看开机是否启动防火墙服务
```
 systemctl is-enabled firewalld
```
c.  关闭防火墙
```
systemctl stop firewalld
systemctl status firewalld
```

d. 警用防火墙（系统启动时不启动防火墙）

```
systemctl disable firewalld
systemctl is-enabled firewalld
```
e. 确保setlinux关闭

```
setenforce 0
```
###  三、修改/etc/samba/smb.conf，在最后加入想要共享的文件夹：
```
[samba home]
    path = /home/samba
    writeable = yes
    guest ok = yes
    read only = no

[MyShare]
        path=/opt/apache-ambari-2.4.1-src
ls
```
### 四、修改文件权限
chown -R root. /opt/apache-ambari-2.4.1-src  //设置共享目录归属为root
chmod -R 777  /opt/apache-ambari-2.4.1-src //属性为所有用户都可以读写删
### 五、本地访问共享文件
1.  在本地电脑文件浏览器中输入 \ \自己的IP地址 访问samba目录
2.  测试是否有增删改查的权限
3.  右击samba目录，选择映射网络驱动器
4.  在编辑器里打开网络驱动器里的项目进行编辑

## 第三步： 配置编译环境
在/opt下创建software文件夹用来存放安装包
切换到software执行下列命令

### 1. yum安装jdk

a. 查看jdk版本
```
yum search java|grep jdk
```
b. 选择版本进行安装

```
yum install java-1.7.0-openjdk
```
### 2. yum安装maven
a.  安装wget用来下载工具
```
yum install wget
```
b. 下载maven

```
wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
```
c. 安装maven

```
yum -y install apache-maven
```

### 3. 安装Python2.6
1.下载安装包

```
wget http://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg#md5=bfa92100bd772d5a213eedd356d64086
```
2.安装

```
 sh setuptools-0.6c11-py2.6.egg
```
> 这里好像就出现了问题，不过咱新建的虚拟机有自带的Python，在命令行里输入：Python,检查一下是否有，检查是有，然后怎么退出呢，用Ctrl+d强制退出。

> 补充：Ctrl+c,Ctrl+d,Ctrl+z在Linux中意义
- Ctrl+c和ctrl+z都是中断命令,但是他们的作用却不一样
- Ctrl+c是强制中断程序的执行。
- Ctrl+z的是将任务中断,但是此任务并没有结束,他仍然在进程中他只是维持挂起的状态。
- Ctrl+d 不是发送信号，而是表示一个特殊的二进制值，表示 EOF。
### 4.安装rpmbuild

```
yum install rpm-build
```
### 5.安装g++

```
yum install gcc-c++
```

### 6.安装nodejs
1. 下载安装包 [版本地址](https://nodejs.org/dist/)
2. ​

```
wget http://nodejs.org/dist/v0.10.33/node-v0.10.33-linux-x64.tar.gz
```
3.解压

```
tar –zxvf node-v0.10.33-linux-x64.tar.gz
```
>注意：此时经常会因为本国的特殊网络环境，有些时候npm下载时特别慢，所以建议访问以上网址，知道相应版本，下载到本地，然后传到虚拟机里。
4. 配置环境变量/etc/profile

```
export NODE_HOME="/opt/software/node-v0.10.33-linux-x64"
export PATH=$PATH:$NODE_HOME/bin
```
5. 使修改后的文件生效
```
source /etc/profile
```
6. 查看安装情况

```
node -v
npm -v
```
## 7.安装Brunch

```
npm i -g brunch@1
```

>由于npm下载依赖包特别慢，而且容易出问题。所以我把之前下载好的包，打包本地，如果需要的话，可以传到ambari-web目录下，然后解压。

>注意打包好的源码里已经下载好了npm依赖包
## 第四步：测试编译
### 一、ambari-web编译：
a. 切换到ambari-web目录下

```
cd /opt/apache-ambari-2.4.1-src/ambari-web
```
b. 删除public文件目录

```
rm -rf public
```
c. 执行编译

```
brunch build
```
d. 查看ambai-web/public目录，如果生成新的文件，则说明编译成功（编译效果会在后面提到）
### 二、ambari-admin编译：
ambari-admin 使用的是angularjs + bower + gulp。

bower与npm的使用方式基本一样，angularjs也与emberjs风格类似。

a. 切换到admin-web目录下

```
cd 到 /源码目录/ambari-admin/src/main/resources/ui/admin-web
```


b. 编辑 .bowerrc 

```
{
    "directory": "app/bower_components",
    "allow_root": true //允许以root用户执行bower命令。也可以在执行命令的时候通过参数设定 如：bower install --allow-root    不要复制这段注释
}
```
c. 安装npm依赖包，全局安装gulp、bower

```
检查一下是否有npm  npm -v 
如果没有 npm install
继续安装bower和gulp
npm install -g bower
npm install -g gulp
```
d. 安装bower的依赖包

```
bower install
```
e. 安装 gulp-webserver

```
npm install gulp-webserver --save-dev
```
f. 开始构建

```
gulp
```


## 第五步：部署ambari
1. 切换到/opt目录下
```
cd /opt
```
2. 解压 deployer-inspur.tar
  之前解压过，此步可以跳过
3. 切换到 deployer-inspur目录下
```
cd /opt/deployer-inspur
```
4. 执行部署安装

```
bash env.sh
```
5. 输入虚拟机ip地址/重复输入
6. 安装成功后，访问 虚拟机ip地址:8000/index.html
7. 增加manager填写信息
8. 等待部署完成
9. 服务安装部署
  访问虚拟机ip:8080 进行服务部署（详情参考大数据平台管理指南）
10. 测试服务
## 第六步：建立软链接

### 一、建立ambari-web软链接
1. 切换到/usr/lib/ambari-server目录下
```
cd /usr/lib/ambari-server
```
2. 备份web目录
```
 mv web web-orig 
```
3. 建立软链接 使ambari-server可以访问到我们修改编译后的代码
```
ln -s /opt/apache-ambari-2.4.1-src/ambari-web/public web 
```

4. 重启服务

```
ambari-server restart
```
5. 刷新查看效果
### 二、建立ambari-admin软链接
1. 切换目录

```
cd /var/lib/ambari-server/resources/views/work
```
> **注意**下面的version是版本号的意思，根据上面的指令就可以知道版本号是多少。

> 然后将ADMIN_VIEW{version}文件备份一下。

```
mv ADMIN_VIEW{version} /tmp
ln -s /sourcepath/ambari/ambari-admin/src/main/resources/ui/admin-web/dist ADMIN_VIEW{version}
ambari-server restart
```
> 这时候貌似页面内容不全，实际上是创建的软连接ADMIN_VIEW\{version}缺少东西，将之前备份的ADMIN_VIEW{version}文件内容替换进去，然后再执行ambari-server restart，重启完后，刷新页面IP:8080/index.html应该就成功了。

> 现在，我们更改源码的时候，再执行一下gulp，就可以看到效果了。修改完一次，手动执行一次gulp

## 第七步：安装开发者工具
1. 对于ambari-web二次开发，可以选用轻量级编辑器sublime 3，
  也可以使用功能强大的 webstrom。
  使用编辑器打开网络映射的磁盘里的ambari-web目录，即可对源码进行开发。
2. 浏览器插件 （因为ambari缓存很厉害，为了达到实时显示效果，需要及时清理缓存，利用插件，可以很方便的达到清理缓存-刷新页面的目的）
  在谷歌浏览器里搜索“clear Cache，clean cache, 清理缓存”插件，并安装

## 第八步：开启新征程
### 一、虚拟机操作：
1. 打开虚拟机
2. 切换到 ambari-web目录下
3. 启动实时编译
  全写是 brunch watch ，这就是对源码进行实时监视，只要发生改变，就对其进行实时编译。编译后的文件放在public里
```
brunch w
```
### 二、浏览器操作：
在浏览器输入 虚拟机ip:8080查看效果
### 三、客户端编辑
使用编辑器对源码进行修改。

### 接下来只需进行
修改源码-刷新页面 -查看效果

## 总结
（遇到问题再做总结，此时已经能够正常工作）