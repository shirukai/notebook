# 在vue里引入jquery

## 一、npm安装jquery

在项目文件目录下运行如下命令，安装jquery

```
npm install jquery
```
## 二、配置webpack
修改build/webpack.base.conf.js文件

在开头加入一行代码

```
 var webpack=require("webpack")
```

然后在这个文件中的module.exports添加如下代码：

```
  plugins: [
new webpack.optimize.CommonsChunkPlugin('common.js'),
new webpack.ProvidePlugin({
    jQuery: "jquery",
    $: "jquery"
})
]
```
## 三、引入全局jquery
在 main.js文件中添加如下代码：

```
   import $ from 'jquery'
```

## 四、重新运行 npm run dev