# vue+cordova构建安卓应用 

# 一、环境准备

java、安卓sdk(安装Android Studio)、Node.js、cordova。

### 安装 cordova

```
npm install -g cordova
```

## 二、cordova创建App 

在自己的源码目录下运行命令行，创建cordova项目。创建名字为shoppingmall的项目

```\\
cordova create shoppingmall com.inspur.shoppingmall shoppingmall
```

执行完成后，切换到项目里

```
cd shoppingmall
```

给App添加目标平台，这里我们添加android平台，并确保他们保存到了config.xml

```
cordova plaform add android --save
```

查看当前平台设置情况

```
cordova plalform ls
```

检测是否满足构建平台的需求

```
cordova requirements
```

在这里会提示我们的android target版本不对，通过查看我们的sdk我们是 android-25 默认生成的是26所以我们可以通过修改配置文件来门族平台需求。

D:\Repository\Android\shoppingmall\platforms\android

修改此目录下的project.properties配置文件

```
target=android-25
```

D:\Repository\Android\shoppingmall\platforms\android\CordovaLib

同时修改此目录下的project.properties配置文件，都改成25

构建安卓平台

```
cordova build android
```

## 三、测试 

在虚拟机上运行

```
cordova emulate android
```

在真机上运行

```
 cordova run android
```

## 四、vue创建项目 

创建项目

```
vue init webpack shoppingmall
cd shoppingmall
npm install
```

添加 vue-resource 用于前后端交互

```
npm install vue-resource
```

添加 muse-ui 样式文件

```
npm install --save muse-ui
```

修改配置文件，使vue在dis生成的文件能直接打开

路径:config/index.js

```
assetsPublicPath: './',
```

启动vue服务器预览

```
npm run dev
```



## 五、整合vue与cordova 

在vue项目下运行命令：

```
npm run build
```

编译完成后会在项目dist目录下生成index页面和static静态文件

复制所有文件到 之前用cordova生成的项目目录下的www文件夹下。

然后运行

```
cordova build
cordova run android
```

## 六、cordova修改启动页和图标 

安装splashcreen插件

```
cordova plugin add cordova-plugin-splashscreen
```

基本配置,修改config.xml文件

    <icon density="ldpi" src="res/icon/android/icon-36-ldpi.png" />
    <icon density="mdpi" src="res/icon/android/icon-48-mdpi.png" />
    <icon density="hdpi" src="res/icon/android/icon-72-hdpi.png" />
    <icon density="xhdpi" src="res/icon/android/icon-96-xhdpi.png" />
    <icon density="xxhdpi" src="res/icon/android/icon-96-xhdpi.png" />
    <splash density="land-hdpi" src="res/screen/android/screen-xhdpi-portrait.png" />
    <splash density="land-ldpi" src="res/screen/android/screen-xhdpi-portrait.png" />
    <splash density="land-mdpi" src="res/screen/android/screen-xhdpi-portrait.png" />
    <splash density="land-xhdpi" src="res/screen/android/screen-xhdpi-portrait.png" />
    <splash density="port-hdpi" src="res/screen/android/screen-xhdpi-portrait.png" />
    <splash density="port-ldpi" src="res/screen/android/screen-xhdpi-portrait.png" />
    <splash density="port-mdpi" src="res/screen/android/screen-xhdpi-portrait.png" />
其他的配置查看这个：http://www.cnblogs.com/a418120186/p/5856371.html