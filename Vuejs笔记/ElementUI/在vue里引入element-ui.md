# 在vue里引入element-ui

## 一、安装element-ui
在项目路径下安装element-ui，运行命令：

```
npm install element-ui -s
```
## 二、项目导入 element-ui

修改main.js文件

```
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'

Vue.use(ElementUI)
```
