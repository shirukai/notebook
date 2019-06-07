## 一、引入全局框架、及用法

### 1.安装vue-resource

#### cnpm安装依赖

```
cnpm install vue-resource
```

#### 安装完成后在项目中全局引入

修改main.js文件

```
import VueResource from 'vue-resource'
Vue.use(VueResource);
```

#### vue-resource使用 

```
// 传统写法
this.$http.get('/someUrl', [options]).then(function(response){    
    // 响应成功回调
}, function(response){    
    // 响应错误回调
});

// Lambda写法
this.$http.get('/someUrl', [options]).then((response) => {    
    // 响应成功回调
}, (response) => {    
    // 响应错误回调
});
```

#### 例子： 

```
var data = {
  key1:value1,
  key2:value2,
}
this.$http.post('/api/product/insert',data,{emulateJSON:true}).then(
(response)=>{
  const res = JSON.pares(response.bodyText);
  console.log(res)
},
(respones)=>{
	//相应错误回调
}
)
```



### 2.安装muse-ui 

#### cnpm安装依赖 

```
cnpm install muse-ui --save
```

#### 全局引入 

```
import MuseUI from 'muse-ui'
import 'muse-ui/dist/muse-ui.css'
import 'muse-ui/dist/theme-default.css' // 使用 default 主题
Vue.use(MuseUI);
```

各组件的应用：http://www.muse-ui.org/#/install

## 二、定义全局变量、方法 

### 在assets下创建 global.js

```
export default {
  install(Vue, options) {
    //定义全局变量
    Vue.prototype.global_value = {
      value1: "this is value11",
      value2: "this is value2"
    };
    //定义全局方法
    /**
     * 保存信息到localStorage
     * @param key 键： 字符串
     * @param value 值：数组、对象、字符串
     */
    Vue.prototype.setItemsToLocalStorage =
      function (key, value) {
      //判断参数是否为对象\数组
        if (typeof(value) === "object"){
          value = JSON.stringify(value)
        }
        window.localStorage.setItem(key, value);
      };

    /**
     * 从localStorage中查询信息
     * @param key
     */
    Vue.prototype.getItemsFromLocalStorage =
      function (key) {
      const value = JSON.parse( window.localStorage.getItem(key))
        return value
      }
  }
}
```

### 在main.js中引入全局变量

```
import Global from './assets/global.js'
Vue.use(Global)
```

### 使用全局变量 

```
      this.global_value.value1 = "gloab_value is changed"
      console.log(this.global_value)
```

### 使用全局方法 

```
//向localStorage中存入信息
this.setItemsToLocalStorage("gloab",this.global_value)
//从localStorage中读取信息
console.log(this.getItemsFromLocalStorage("gloab"))
```

## 三、vue指令 

### 常用的指令 

#### v-text =“msg”          {{msg}} 

#### v-if 跟 v-show的区别：

v-if 当不满足条件的时候，不会显示到dom里

v-show 当不满足条件的时候，虽然不显示，但是仍然在dom中渲染

#### v-for 

```
<div v-for="item in items">
  {{ item.text }}
</div>
```

#### v-on  简写@ 监听事件

##### 修饰符 

- `.stop` - 调用 `event.stopPropagation()`。
- `.prevent` - 调用 `event.preventDefault()`。
- `.capture` - 添加事件侦听器时使用 capture 模式。
- `.self` - 只当事件是从侦听器绑定的元素本身触发时才触发回调。
- `.{keyCode | keyAlias}` - 只当事件是从特定键触发时才触发回调。
- `.native` - 监听组件根元素的原生事件。
- `.once` - 只触发一次回调。
- `.left` - (2.2.0) 只当点击鼠标左键时触发。
- `.right` - (2.2.0) 只当点击鼠标右键时触发。
- `.middle` - (2.2.0) 只当点击鼠标中键时触发。
- `.passive` - (2.3.0) 以 `{ passive: true }` 模式添加侦听器

如：鼠标点击事件

@click

```
<!-- 方法处理器 -->
<button v-on:click="doThis"></button>
<!-- 对象语法 (2.4.0+) -->
<button v-on="{ mousedown: doThis, mouseup: doThat }"></button>
<!-- 内联语句 -->
<button v-on:click="doThat('hello', $event)"></button>
<!-- 缩写 -->
<button @click="doThis"></button>
<!-- 停止冒泡 -->
<button @click.stop="doThis"></button>
<!-- 阻止默认行为 -->
<button @click.prevent="doThis"></button>
<!-- 阻止默认行为，没有表达式 -->
<form @submit.prevent></form>
<!--  串联修饰符 -->
<button @click.stop.prevent="doThis"></button>
<!-- 键修饰符，键别名 -->
<input @keyup.enter="onEnter">
<!-- 键修饰符，键代码 -->
<input @keyup.13="onEnter">
<!-- 点击回调只会触发一次 -->
<button v-on:click.once="doThis"></button>
```

获得焦点事件: @focus 

失去焦点事件: @blur

## 四、路由传递参数 

官网：https://router.vuejs.org/zh-cn/installation.html

### 安装路由 

```
cnpm install vue-router
```

### 引入全局路由 

```
import VueRouter from 'vue-router'
Vue.use(VueRouter)
```

### 动态路由 

```
//动态路由
{
  path:'/index/:username/:id',
  name:'Index',
  component:Index
}
```

访问链接

```
index/shirukai/308899573
```

接受参数

```
  <div>
    <h1>{{$route.params.username}}</h1>
    <h1>{{$route.params.id}}</h1>
  </div>
```

js跳转

```
this.$router.push({path:'/index'})
```

带参数跳转

```
//如果要传一个对象
var shopString = JSON.stringify(shopInfos)
this.$router.push({path: '/addproduct', query: {shopInfos: shopString}})
```

接受参数

```
const shopinfos = JSON.parse( this.$route.query.shopInfos)
console.log(shopinfos)
```

### 滚动条 

https://github.com/BosNaufal/vue2-scrollbar