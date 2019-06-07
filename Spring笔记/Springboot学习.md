# Springboot学习 

## 1利用IDEA创建springboot web 项目 

### 1.1 新建项目 

选择spring Initializr,然后点下一步。

![](https://shirukai.gitee.io/images/201711191434_36.png)

### 1.2填写项目信息 

![](https://shirukai.gitee.io/images/201711191438_694.png)

### 1.3选择项目类型 

![](https://shirukai.gitee.io/images/201711191439_112.png)

### 1.4项目名和项目路径

![](https://shirukai.gitee.io/images/201711191440_711.png)

### 1.5补充包目录

在com.springboot.demo下创建

controller包

entity包

jpa包

service包

### 1.6 依赖处理 

在pom.xml里导入数据库依赖

```
<!--数据库相关依赖-->
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
   <groupId>mysql</groupId>
   <artifactId>mysql-connector-java</artifactId>
</dependency>
```

### 1.7项目配置 

在resource下新建一个application.yml文件，并删除原有的application.properties文件

application.yml配置文件如下

```
spring:
 #配置数据库
 datasource:
   driver-class-name: com.mysql.jdbc.Driver
   url: jdbc:mysql://localhost:3306/springboot?useSSL=false
   username: root
   password: inspur
 #配置jpa
 jpa: 
  show-sql: true
  database: mysql
  hibernate:
    ddl-auto: update
```



## 2项目开发 

### 2.1编写entity层 

User

```
package com.springboot.demo.entity;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

/**User entity
 * Created by shirukai on 2017/11/19.
 */
@Entity
public class User {
    @Id
    @GeneratedValue
    private Integer id;
    private String userName;
    private String password;
    //创建一个无参的构造方法（必须）
    public User(){}

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}

```

### 2.2编写jpa 

UserRepository

```
package com.springboot.demo.jpa;

import com.springboot.demo.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * 
 * Created by shirukai on 2017/11/19.
 */
public interface UserRepository extends JpaRepository<User,Integer> {
}

```

### 2.3编写service 

```
package com.springboot.demo.service;

import com.springboot.demo.entity.User;

import java.util.List;

/**
 *
 * Created by shirukai on 2017/11/19.
 */
public interface UserService {
    /**
     * 新增用户
     * @param user user
     * @return user
     */
    User insertUser(User user);

    /**
     * 根据id删除用户
     * @param id
     */
    void deleteUser(int id);

    /**
     * 获取所有用户
     * @return
     */
    List<User> getAll();

    /**
     * 更新
     * @param user
     * @return
     */
    User updateUser(User user);

    /**
     * 根据id获取用户信息
     * @param id
     * @return
     */
    User getById(Integer id);
}

```

### 2.4编写service实现类 

```
package com.springboot.demo.service.Impl;

import com.springboot.demo.entity.User;
import com.springboot.demo.jpa.UserRepository;
import com.springboot.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 *
 * Created by shirukai on 2017/11/19.
 */
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public User insertUser(User user) {
        return userRepository.save(user);
    }

    @Override
    public void deleteUser(int id) {
        userRepository.delete(id);
    }

    @Override
    public List<User> getAll() {
        return userRepository.findAll();
    }

    @Override
    public User updateUser(User user) {
        return userRepository.save(user);
    }

    @Override
    public User getById(Integer id) {
        return userRepository.getOne(id);
    }
}

```

### 2.5 编写controller 

```
package com.springboot.demo.controller;

import com.springboot.demo.entity.User;
import com.springboot.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Created by shirukai on 2017/11/19.
 */
@RestController
public class UserController {
    @Autowired
    private UserService userService;

    @RequestMapping(value = "/insertuser", method = RequestMethod.POST)
    public User insertUser(
            User user
    ) {
        return userService.insertUser(user);
    }

    @RequestMapping(value = "/getAll", method = RequestMethod.GET)
    List<User> getAll() {
        return userService.getAll();
    }

    @RequestMapping(value = "/delete/{id}", method = RequestMethod.DELETE)
    void deleteById(
            @PathVariable("id") Integer id
    ) {
        userService.deleteUser(id);
    }

    @RequestMapping(value = "/update/{id}", method = RequestMethod.PUT)
    public User updateById(
            @PathVariable("id") Integer id,
            @RequestParam("password") String password
    ) {
        User user = userService.getById(id);
        user.setPassword(password);
        return userService.updateUser(user);
    }
}

```

## 3 运行 测试

### 3.1运行DemoApplication的main方法 

![](https://shirukai.gitee.io/images/201711191940_734.png)



### 3.2利用Postman进行测试

#### 3.2.1 新增用户

![](https://shirukai.gitee.io/images/201711191942_909.png)

#### 3.2.2根据id删除用户 

![](https://shirukai.gitee.io/images/201711191943_933.png)



#### 3.2.3更新用户 

![](https://shirukai.gitee.io/images/201711191944_315.png)



#### 3.2.4获取用户列表 

![](https://shirukai.gitee.io/images/201711191945_753.png)



## 4补充：Controller

### 4.1 @Controller和@RestController的区别 

在之前使用Springmvc的时候，当我们使用@Controller注解的controller层需要返回json数据时，需要在方法的前面加上@ResponseBody。

但是等我们使用RestController注解Controller层时，无需添加@ResponseBody直接就返回json类型的数据。

### 4.2 @RequestMapping

@RequestMapping是注解在Controller层方法前的。

通俗的讲，在Spring中使用@RequestMapping注解时，当访问指定url时，会调用的相应的方法。

### 4.3 @RequestMapping六种使用方法 

#### 4.3.1 基本的无参方法

```
@RequestMapping("/login)public String testFunction(){……} 
```

说明：访问http://localhost/xxxx/login的时候，就会调用testFunction方法

#### 4.3.2 参数绑定

```
@RequestMapping("/login")public String testFunction(@RequestParam ("userId") String userId){System.out.println("用户id为："+ userId);}}
```

说明：/login?userId=12 就可以触发调用testFunction方法

#### 4.3.3 Rest风格的参数 

```
@RequestMapping("/login/{userId}")public String testFunction(@PathVariable String userId){System.out.println("用户id为："+userId);}
```

说明：

形如 /login/23 ,其中用PathVariable接受rest风格的参数

#### 4.3.4 Rest风格参数绑定2 

```
@RequestMapping ("/login/{userId}")public String testFunction(@ParhVariable("userId")String someUserId){System.out.println("用户id为："+someUserId)}
```

说明：形如/login/23,会把23传入给userId,然后传值绑定给自定义的 someUserId，

在实际方法中调用someUserId值为23.

#### 4.3.4 Url中同时绑定多个id

```
    @RequestMapping("/login/{userId}/password/{passwordId}")
    public String testFunction(@PathVariable String userId, @PathVariable String passwordId) {
        System.out.println("用户名Id：" + userId);
        System.out.println("密码Id：" + passwordId);
    }
```

说明：形如/login/23/password/46 ,调用testFunction方法，赋值给userId=23，passwordId=46

#### 4.3.5 支持正则表达式 

```
    @RequestMapping("/{textualPart:[a-z-]+}.{numericPart:[\d]+}")
    public String testFunction(@PathVariable String textualPart, @pathVariable String numericPart) {
        System.out.println("Textual part:" + textualPart + ",numeric part:" + numericPart);
    }
```

说明：形如/sometext.123则输出Textual part: sometext, numeric part: 123. 

### 4.4 @GetMapping、@PostMapping

@GetMapping("/get") 相当于 @RequestMapping(value="/get",method.RequestMethod.GET)

@PostMapping ("/post")相当于@RequestMapping(value="/post",method.RequestMethod.POST)

### 4.5 处理参数

#### 4.5.1 @PathVariable 

获取url里的参数，例如：

@RequestMapping("/login/{userId}/password/{passwordId}")

#### 4.5.2 @RequetParam 

获取请求中的参数



## 5 补充：Spring-Data-Jpa



![](https://shirukai.gitee.io/images/201711181543_110.png)

## 6 补充：Springboot 通用配置、开发、生产环境配置 

有时候，我们需要两套配置，比如开发的时候是一个配置，生产的时候是一个配置。这样我们就需要对Springboot的配置进行改造了。

首先复制原来的配置文件同样粘贴到相同目录下并且重名为application-dev.yml 

然后在复制原来的配置文件，重名为application-pro.yml

最后清空application.yml里的配置，并添加如下内容：

```
spring:
  profiles:
   active: dev
```

active后为dev说明用的是application-dev.yml配置文件，如果改为pro则使用的是application-pro.yml文件