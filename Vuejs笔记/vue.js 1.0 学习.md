# vue.js 1.0 学习

### 环境搭建

```
//安装全局的vue-cli命令行工具
cnpm install -g vue-cli
//创建基于'webpack'模板的新项目
vue init webpack#1.0 my-project
//切换到项目里安装依赖
cnpm install
//启动服务
npm run dev
```

MVVM框架

### vue.js 简介
什么是vue.js
他是一个轻量级 mvvm框架
数据驱动+组件化的前端开发

vue.js的核心思想
数据驱动、组件化


组件设计原则
页面上每个独立的可视/可交互区域视为一个组件
每个组件对应一个工程目录，组件所需要的各种资源目录下就近维护
页面不过是组件的容器，组件可以嵌套自由组合形成完整的页面

### webpack打包

### v-bind指令
v-bind:class="[value]" 这里的value是data里的一个值
v-bind:class="{class名:条件}"当条件为true时class=‘class名’，为false时不显示绑定的class，简写 :class

### v-on指令
点击指令 v-on:click="方法名(参数)"
methods：{
	方法名：function（参数）{
		方法体
	}
}

### watch指令

```
  watch: {
    items: {
      handler: function (val,oldVal) {
        //方法
      },
      deep:true
    }
  }
```

### 组件引入
//引入组件
```
import header from './components/header.vue'
```
//注册组件

```
  components:{
    'v-header':header
  }
```

### 组件间的通讯
子组件header，注册属性
```
 props:['parent'],
```
父组件导入子组件

```
import header from './components/header.vue'
```
父组件中注册子组件

```
  components:{
    'v-header':header
  }
```
父组件向子组件传递信息

```
 <v-header :parent="title"></v-header>
```

