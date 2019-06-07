# 利用AOP对Azkaban进行登录控制

azkaban使用的是session进行登录控制，session过期时间为1天。所以对于azkaban接口服务的调用，首先要进行登录获取session。解决方案有三种：

1.在执行请求前，先进行登录。

优点：实现简单

缺点：每次都要发送登录请求，azkaban服务器负担较大

2.通过某个请求来判断是否登录，如果登录，继续执行，没有登录，先执行登录，再执行下面的请求操作。

优点：无需每次都进行登录

缺点：每次同样要发送两次请求

3.利用AOP来对请求方法进行切面注入，通过判断请求结果来进行登录控制，如果请求结果里有未登录信息，则进行登录，如果登录了直接返回结果。

优点：无需对已有方法进行修改、无需每次都登录

缺点：对返回结果具有约束性

下面主要记录一下利用AOP思想对azkaban进行的登录控制。

## 控制流程

![](https://shirukai.gitee.io/images/201805041148_236.png)

## 代码实现

项目中是使用注解的方式实现的AOP

AOP实现参考文章：

https://blog.csdn.net/qgfjeahn/article/details/60144241

https://www.cnblogs.com/programmer1/p/7994031.html

```
**
 * 基于AOP的azkaban登录控制
 * Created by shirukai on 2018/5/2.
 */
@Component
@Aspect
public class AzkabanLogin {
    private static Logger log = LoggerFactory.getLogger(AzkabanHandle.class);
    @Autowired
    AzkabanAdapter azkabanAdapter;

    @Around("execution(* com.emcc.hiacloud.analytics.azkaban.AzkabanAdapter.*(..))")
    public Object loginHandle(ProceedingJoinPoint proceedingJoinPoint) {
        Object result = null;
        try {
            //执行代理方法
            result = proceedingJoinPoint.proceed();
            log.info("azkaban login handle:checking...");
            boolean isLogin = false;
            if (!"login".equals(proceedingJoinPoint.getSignature().getName())) {
                try {
                    String errorStr = JSON.parseObject(result.toString()).getString("error");
                    if (errorStr == null) {
                        throw new Exception("");
                    }
                    isLogin = "session".equals(errorStr);
                } catch (Exception e) {
                    isLogin = result.toString().contains("login");
                    log.warn(e.getMessage());
                } finally {
                    if (isLogin) {
                        log.info("azkaban login handle:re-login");
                        azkabanAdapter.login();
                        result = proceedingJoinPoint.proceed();
                    }
                }
            }
        } catch (Throwable e) {
            e.printStackTrace();
        }
        return result;
    }

}
```