# CentOS安装jenkins

## Jenkins安装过程

下载yum源

```
wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
```

安装 yum 源

```
rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key
```

yum 安装jenkins

```
yum -y install jenkins
```

## 配置Java的实际安装路径

查看 JAVA_HOME

```
echo $JAVA_HOME 
```

添加实际的jdk安装路径  /usr/local/jdk/bin/java到jenkins的配置文件里

```
vi /etc/rc.d/init.d/jenkins
```

添加位置

```
candidates="
/etc/alternatives/java
/usr/lib/jvm/java-1.8.0/bin/java
/usr/lib/jvm/jre-1.8.0/bin/java
/usr/lib/jvm/java-1.7.0/bin/java
/usr/lib/jvm/jre-1.7.0/bin/java
/usr/bin/java
/usr/local/jdk/bin/java #这行是添加的
"
```

reload

```
systemctl daemon-reload
```

启动 jenkins

```
service jenkins start
```

## 浏览器地址栏输入

http://ip:8080/

```
cat /var/lib/jenkins/secrets/initialAdminPassword
```

复制key粘贴至web页面