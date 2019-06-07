# Vue添加第三方iconfont图标库

## 一、图标包制作

我们需要到iconfont选择图标，然后下载到本地。

iconfont官网：http://www.iconfont.cn/

下面以导入官方提供的【AIS产品图标库】为例

### 1.登录到iconfont

![](https://shirukai.gitee.io/images/201802051137_533.png)



### 2.选择图标库

在导航栏点击【图标库】然后选择【官方图标库】

![](https://shirukai.gitee.io/images/201802051141_687.png)

这时候我们会看到官方图标库，我们找到【AIS产品图标库】，点击进入

![](https://shirukai.gitee.io/images/201802051143_896.png)

### 3.添加图标到自己的库

#### 添加入库

进入【AIS产品图标库】后，我们可以选择自己喜欢的图标，然后添加到自己的库，具体操作，鼠标放到图标上，会出现选项，选择【添加入库】

![](https://shirukai.gitee.io/images/201802051146_958.png)

#### 全部添加到库

打开开发者工具，在控制台输入：

```
document.querySelectorAll('.icon-gouwuche1').forEach(function(item){item.click()})
```

#### 添加至项目

点击右上角【购物车】选择【添加至项目】，然后创建项目，输入项目名即可。

![](https://shirukai.gitee.io/images/201802051335_497.png)

### 4.下载图标到本地

#### 修改前缀

点击导航栏【图标管理】，然后选择我们刚刚创建的项目。在【更多操作】里选择【修改项目】

![](https://shirukai.gitee.io/images/201802051341_214.png)

然后我们就可以修改【FontClass/Symbol前缀】了，这里我们修改前缀为【ais】

![](https://shirukai.gitee.io/images/201802051343_308.png)

然后点击【下载至本地】即可。

## 二、vue里使用iconfont

### 1. 准备

#### 创建vue项目

在代码存放目录下，创建名为vue_iconfont的项目

```
vue init webpack vue_iconfont
```

#### 复制图标到项目

在vue_iconfont\src\assets目录下创建iconfont目录，然后将下载的图标解压，复制到此位置。

![](https://shirukai.gitee.io/images/201802051409_415.png)

#### 修改iconfont.css

想要图标正常显示，我们需要修改iconfont.css,在大约17行插入如下代码，ais之前修改的前缀名，注意第二个ais前面有一个空格。

```
[class^="ais"], [class*=" ais"] {
  font-family:"iconfont" !important;
  font-size:16px;
  font-style:normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

![](https://shirukai.gitee.io/images/201802051411_74.png)

### 2.引入css

在vue项目的main.js里引入css

```
import './assets/iconfont/iconfont.css'
```

### 3.使用

使用iconfont图标很简单，class=“ ”，在标签图标的class属性指定iconfont图标即可

```
<template>
  <div>
    <span>
      <i class="ais-bangzhu"></i>
      <i class="ais-baocun"></i>
      <i class="ais-app"></i>
      <i class="ais-caidan"></i>
      <i class="ais-chakan"></i>
      <i class="ais-daxiao"></i>
    </span>
  </div>
</template>
```

![](https://shirukai.gitee.io/images/201802051416_564.png)

