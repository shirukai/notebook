# Springmvc过滤器 

过滤源--过滤规则--过滤结果



### 过滤器是否能改变用户请求的web资源呢?也就是能否改变用户请求的路径? 

可以

### 过滤器能否直接返回数据，能不能直接处理用户请求？ 

不能

## 多个过滤器详解

假如有两个过滤器，TestFilter、SecondFilter，他们的执行顺序如下：

start______doFilter_________TestFilter
start_________________doFilter____________SecondFilter

end_________________doFilter________________SecondFilter
 end______doFilter_________TestFilter



## Springmvc配置过滤器 

### 编写TestFilter类 

```
/**
 * 过滤器测试
 * Created by shirukai on 2017/10/31.
 */
public class TestFilter implements Filter {
     private Logger logger = LoggerFactory.getLogger(this.getClass());
    public void init(FilterConfig filterConfig) throws ServletException {
        logger.info("__________________init________________TestFilter");
    }

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        logger.info("start__________doFilter_________TestFilter");
        chain.doFilter(request,response);//放行
        logger.info("end__________doFilter_________TestFilter");
    }

    public void destroy() {
        logger.info("__________________destroy________________TestFilter");
    }
}
```

### 注册过滤器 

在web.xml注册过滤器

```
<!--测试过滤器-->
<!--  <filter>
    <filter-name>TestFilter</filter-name>
    <filter-class>com.mavenssmlr.filter.TestFilter</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>TestFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>-->
```

## 过滤器在实际项目中的应用场景 

### 1. 对用户请求进行统一认证 

#### 编写LoginFilter类 

```
/**
 * 登录权限过滤器
 * Created by shirukai on 2017/10/31.
 */
public class LoginFilter implements Filter {
     private Logger logger = LoggerFactory.getLogger(this.getClass());
    private FilterConfig config;

    public void init(FilterConfig filterConfig) throws ServletException {
        config = filterConfig;
    }

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpServletRequest =(HttpServletRequest)request;
        HttpServletResponse httpServletResponse = (HttpServletResponse) response;
        //将cookie封装到map里
        Map<String, Cookie> cookieMap = new HashMap<String, Cookie>();
        Cookie[] cookies = httpServletRequest.getCookies();
        if (null != cookies) {
            for (Cookie cookie : cookies) {
                cookieMap.put(cookie.getName(), cookie);
            }
        }
        Cookie accessToken = cookieMap.get("accessToken");
        //获取配置文件：不需要过滤的url
        String[] noFilterUrls = config.getInitParameter("noFilterUrls").split(";");
        for (int i = 0;i < noFilterUrls.length; i++){
            if (httpServletRequest.getRequestURI().contains(noFilterUrls[i])){
                chain.doFilter(request,response);
            }
        }
        if (accessToken == null){
            httpServletRequest.getRequestDispatcher("/user/login").forward(request,response);;
        }
        logger.info(httpServletRequest.getRequestURI());
        String url = ((HttpServletRequest) request).getRequestURI();
        chain.doFilter(request,response);

    }

    public void destroy() {

    }
}
```

#### 注册过滤器 

```
<!--登录过滤器-->
<filter>
    <filter-name>LoginFilter</filter-name>
    <filter-class>com.mavenssmlr.filter.LoginFilter</filter-class>
    <init-param>
        <!--不需要过滤的url、静态资源-->
        <param-name>noFilterUrls</param-name>
        <param-value>/user/;/skins/</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>LoginFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

### 2. 编码转换

直接在web.xml配置即可

```
<!-- Spring字符编码过滤器配置，处理中文乱码，针对post请求 -->
<filter>
  <filter-name>characterEncodingFilter</filter-name>
  <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
  <init-param>
    <param-name>encoding</param-name>
    <param-value>UTF-8</param-value>
  </init-param>
  <init-param>
    <param-name>forceEncoding</param-name>
    <param-value>true</param-value>
  </init-param>
</filter>
<filter-mapping>
  <filter-name>characterEncodingFilter</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>

```

### 3.利用过滤器允许ajax跨域请求 

#### 编写过滤器类 

```
/**
 * 允许跨域请求过滤
 * Created by shirukai on 2017/11/1.
 */
public class CORSFilter implements Filter {

    public void init(FilterConfig filterConfig) throws ServletException {

    }

    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletResponse response = (HttpServletResponse) servletResponse;
        String origin = (String) servletRequest.getRemoteHost() + ":" + servletRequest.getRemotePort();
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "x-requested-with,Authorization");
        response.setHeader("Access-Control-Allow-Credentials", "true");
        filterChain.doFilter(servletRequest, servletResponse);
        
    }

    public void destroy() {

    }
}
```

#### 注册过滤器 

```
<!--允许跨域请求过滤-->
<filter>
    <filter-name>CORSFilter</filter-name>
    <filter-class>com.mavenssmlr.filter.CORSFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>CORSFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>

```

参考地址：http://www.imooc.com/article/7719



1. ### 对用户发送的数据进行过滤替换

2. ### 转换图片格式

3. ### 对响应的内容进行压缩

​