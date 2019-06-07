# linux环境下编译安装prometheus 并实现汉化 

## go语言环境 

```
yum insatll go
```

## git源码 

```
export GOPATH=`pwd`
cd $GOPATH/src/github.com/prometheus
git clone https://github.com/prometheus/prometheus.git
cd prometheus
```

## 编译前端静态文件 

```
make assets
```

## 整体编译 

```
make build
```

## 运行 

复制prometheus.yml到目录下，然后运行

```
./prometheus
```

## 汉化 

promethus的前端页面在/root/src/github.com/prometheus/prometheus/web/ui/templates这个路径下，我们修改相应的文件即可。