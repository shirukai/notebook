# Springmvc拦截器 

> 什么是拦截器？

拦截器是指通过统一拦截从浏览器发往服务器的请求来完成功能的增强

使用场景：解决请求的共性问题(如：乱码问题、权限验证问题等)

## 拦截器的实现

### 编写拦截器类 

在 interceptor包想创建TestInterceptor类继承HandlerInterceptor 也可以继承WebRequestInterceptor(preHandle方法里没有返回值，无法终止请求)

```
package com.mavenssmlr.interceptor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * Created by shirukai on 2017/10/31.
 */
public class TestInterceptor implements HandlerInterceptor {
     private Logger logger = LoggerFactory.getLogger(this.getClass());
     //请求之前被调用：返回值表示是否将当前请求拦截下来，如果返回false，请求被终止
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        logger.info("_____________preHandle方法执行了哦_______________________________________");
        //解决乱码问题
        request.setCharacterEncoding("utf-8");
        //对用户是否登录做判断 终止请求、返回登录页面 request.getRequestDispatcher().forward(req,res)
        return true;
    }
    //请求被处理之后进行调用
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        logger.info("_____________postHandle方法执行了哦_______________________________________");
        //可以通过ModelAndView参数来改变显示的视图，或修改发往视图的方法
    }
    //请求结束之后才进行调用
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        logger.info("_____________afterCompletion方法执行了哦_______________________________________");
    }
}
```

### 注册拦截器  

```
<!--注册拦截器-->
<mvc:interceptors>
    <mvc:interceptor>
    	//要拦截的地址、可以正则
        <mvc:mapping path="/plugins/upload"/>
        //拦截器名
        <bean class="com.mavenssmlr.interceptor.TestInterceptor"/>
    </mvc:interceptor>
</mvc:interceptors>
```

## 拦截器的使用场景

### 利用拦截器解决乱码问题 

#### 编写EncodeingInterceptor类 

```
/**
 * 利用拦截器解决中文乱码问题
 * Created by shirukai on 2017/10/31.
 */
public class EncodingInterceptor implements HandlerInterceptor {
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //解决中文乱码问题
        request.setCharacterEncoding("utf-8");
        return true;
    }

    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}
```

#### 注册拦截器 

```
<!--解决中文乱码的拦截器-->
<mvc:interceptors>
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <bean class="com.mavenssmlr.interceptor.EncodingInterceptor"/>
    </mvc:interceptor>
</mvc:interceptors>
```

### 利用拦截器解决登录权限问题 

思路：用户登录成功后生产accessToken，并保存的cookie里，拦截器拦截指定请求后，获取cookie中的accessToken进行判断，通过后继续执行请求，否则拦截重定向到登录页面。

关于Springmvc重定向、和内部转发的问题：

http://www.cnblogs.com/phpzxh/archive/2010/02/01/1661137.html

request.getRequestDispatcher()是请求转发，前后页面共享一个request ; 
response.sendRedirect()是重新定向，前后页面不是一个request。

#### 编写LoginInterceptor类

```
/**
 * 登录拦截
 * Created by shirukai on 2017/10/31.
 */
public class LoginInterceptor implements HandlerInterceptor {
    private Logger logger = LoggerFactory.getLogger(this.getClass());
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //将cookie封装到map里
        Map<String, Cookie> cookieMap = new HashMap<String, Cookie>();
        Cookie[] cookies = request.getCookies();
        if (null != cookies) {
            for (Cookie cookie : cookies) {
                cookieMap.put(cookie.getName(), cookie);
            }
        }
        Cookie accessToken = cookieMap.get("accessToken");
        if (accessToken == null) {
          	request.getRequestDispatcher("/user/login").forward(request,response);
            return false;
        }
        return true;
    }

    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
} 
```

### 注册拦截器 

关于登录的请求都在/user/这个路径下面，所以这个路径下的所有请求我们不做拦截。

```
<!--登录拦截器-->
<mvc:interceptor>
	//拦截路径
    <mvc:mapping path="/**"/>
    //不拦截的路径
    <mvc:exclude-mapping path="/user/*"/>
    <mvc:exclude-mapping path="/skins/*"/>
    <bean class="com.mavenssmlr.interceptor.LoginInterceptor"/>
</mvc:interceptor>
```



## 多个拦截器执行顺序 

假如有 拦截器1、拦截器2、拦截器3

那么执行顺序是  

拦截器1的preHandle --> 拦截器2的preHandle --> 拦截器3的preHandle -->拦截器3的postHandle --> 拦截器2的postHandle -->拦截器1的postHandle -->拦截器3的afterCompletion -->拦截器2的afterCompletion -->拦截器1的afterCompletion

## 拦截器和过滤器的区别

过滤器Filter依赖于Servlet容器，基于回调函数。过滤范围大

拦截器Interceptor 依赖于框架容器，机器反射机制，只过滤请求