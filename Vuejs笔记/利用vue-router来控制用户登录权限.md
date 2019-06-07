# 原理
用vue-router来控制用户登录权限的原理，实际上就是应用了vue-router提供的router.beforeEach来注册一个全局钩子。[具体用法](https://router.vuejs.org/zh-cn/advanced/navigation-guards.html)

根据判断是否具有登录权限来设置路由跳转，如果没有全选统一跳转到登录页面。

## 第一步：新建一个名字为permission的js文件，代码如下
```
import router from './router'
import NProgress from 'nprogress' // Progress 进度条
import 'nprogress/nprogress.css'// Progress 进度条样式

router.beforeEach((to, from, next) => {
  NProgress.start(); // 开启Progress
  if (sessionStorage.getItem('accessToken')) {
    next()
  } else {
    if (to.path ==="/login"|| to.path ==='/register'){
      next()
    }else {
      next('/login')
    }
    NProgress.done()
  }
});
router.afterEach(() => {
  NProgress.done() // 结束Progress
});


```
## 在mian.js中导入permission.js,代码如下：


```
import './permission' // 权限
```
