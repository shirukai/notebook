# Springboot项目整合MongoDB

本文主要记录在Springboot项目中整合MongoDB，并演示增删改查，以及分页查询。

## 1 整合MongoDB

### 1.1 引入依赖

在sparingboot项目中引入MongoDB依赖

```
<!--mongodb-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
```

### 1.2 MongoDB配置

引入依赖之后，需要在springboot配置中，加入MongoDB的配置信息。

这里我使用的springboot项目的配置文件是yml格式的，配置内容如下：

```
spring:
 data:
  mongodb:
    uri: mongodb://192.168.162.128:27017/local?maxPoolSize=256
```

如果为properties格式，添加内容如下：

```
spring.data.mongodb.uri=mongodb://192.168.162.128:27017/local?maxPoolSize=256
```

uri格式解释

```
mongodb://用户名:密码@连接地址:端口/数据库名
```

## 2 MongoDB的CRUD操作

### 2.1 entity层

java实体类用来映射MongoDB中的Collection

如：我们创建一个User的实体类，里面包含id、userName、password字段。

```
package com.springboot.demo.mongo.entity;

import org.springframework.data.mongodb.core.mapping.Field;

import java.io.Serializable;

/**
 * Created by shirukai on 2018/8/8
 */
public class User implements Serializable {
    private static final long serialVersionUID = -3258839839160856613L;
    @Field("id")
    private Long id;
    @Field("user_name")
    private String userName;
    @Field("password")
    private String password;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
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

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", userName='" + userName + '\'' +
                ", password='" + password + '\'' +
                '}';
    }
}
```

### 2.2 dao层

DAO层主要提供对MongoBD的基础操作 如增删改查等。

#### 2.2.1 添加操作

对MongoDB的添加，主要是调到mongoTemplate的save()方法,首相通过Spring注入mongoTemplate。

```
    //注入mongoTemplate
    @Autowired
    private MongoTemplate mongoTemplate;
    
     /**
     * 保存user
     *
     * @param user user
     */
    public void saveUser(User user) {
        mongoTemplate.save(user);
    }
```

#### 2.2.2 删除操作

调用mongoTemplate中的remove()方法实现删除操作

```
/**
 * 删除user
 *
 * @param id id
 */
public void deleteUserById(Long id) {
    Query query = new Query(Criteria.where("id").is(id));
    mongoTemplate.remove(query, User.class);
}
```

#### 2.2.3 修改操作

调用mongoTemplate中的update()方法实现修改操作

```
/**
 * 更新user
 *
 * @param user user
 */
public void updateUser(User user) {
    Query query = new Query(Criteria.where("id").is(user.getId()));
    Update update = new Update().set("userName", user.getUserName()).set("password", user.getPassword());
    mongoTemplate.updateFirst(query, update, User.class);
}
```

#### 2.2.4 查找操作

调用mongoTemplate中的findOne()方法实现查找操作

```
    /**
     * 根据用户名查询user
     *
     * @param userName userName
     * @return user
     */
    public User findUserByUserName(String userName) {
        Query query = new Query(Criteria.where("userName").is(userName));
        return mongoTemplate.findOne(query, User.class);
    }

```

#### 2.2.5 分页查找

##### 2.2.5.1 创建PageModel类

```
package com.springboot.demo.mongo.page;

import org.springframework.data.domain.Sort;

import java.io.Serializable;

/**
 * Created by shirukai on 2018/8/8
 */
public class PageModel implements Serializable {
    private static final long serialVersionUID = -3258839839160856613L;
    private Integer pagenumber = 1;
    private Integer pagesize = 10;
    private Sort sort;

    public Integer getPagenumber() {
        return pagenumber;
    }

    public void setPagenumber(Integer pagenumber) {
        this.pagenumber = pagenumber;
    }

    public Integer getPagesize() {
        return pagesize;
    }

    public void setPagesize(Integer pagesize) {
        this.pagesize = pagesize;
    }

    public Sort getSort() {
        return sort;
    }

    public void setSort(Sort sort) {
        this.sort = sort;
    }
}
```

##### 2.2.5.2 创建SpringPageable类

```
package com.springboot.demo.mongo.page;

import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

import java.io.Serializable;

/**
 * Created by shirukai on 2018/8/8
 */
public class SpringPageable implements Pageable, Serializable {
    private static final long serialVersionUID = -3258839839160856613L;

    private PageModel page;

    public PageModel getPage() {
        return page;
    }

    public void setPage(PageModel page) {
        this.page = page;
    }


    @Override
    public int getPageNumber() {
        return page.getPagenumber();
    }

    @Override
    public int getPageSize() {
        return page.getPagesize();
    }

    @Override
    public long getOffset() {
        return (page.getPagenumber() - 1) * page.getPagesize();
    }

    @Override
    public Sort getSort() {
        return page.getSort();
    }

    @Override
    public Pageable next() {
        return null;
    }

    @Override
    public Pageable previousOrFirst() {
        return null;
    }

    @Override
    public Pageable first() {
        return null;
    }

    @Override
    public boolean hasPrevious() {
        return false;
    }
}

```

##### 2.2.5.2 在DAO层实现分页方法

```
    /**
     * 分页查询
     * @param pageNum 页数
     * @param pageSize 每页数量
     * @param sortField 排序字段
     * @return pages
     */
    public Page<User> findUserPagination(Integer pageNum, Integer pageSize, String sortField) {
        SpringPageable pageable = new SpringPageable();
        PageModel pm = new PageModel();
        Query query = new Query();
        Sort sort = new Sort(Sort.Direction.DESC, sortField);
        pm.setPagenumber(pageNum);
        pm.setPagesize(pageSize);
        pm.setSort(sort);
        pageable.setPage(pm);
        Long count = mongoTemplate.count(query, User.class);
        List<User> list = mongoTemplate.find(query.with(pageable), User.class);
        return new PageImpl<>(list, pageable, count);
    }
```

#### 2.2.6 DAO层完成代码

```
package com.springboot.demo.mongo.dao;

import com.springboot.demo.mongo.entity.User;
import com.springboot.demo.mongo.page.PageModel;
import com.springboot.demo.mongo.page.SpringPageable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Component;
import java.util.List;

/**
 * Created by shirukai on 2018/8/8
 */
@Component
public class UserDao {
    @Autowired
    private MongoTemplate mongoTemplate;

    /**
     * 保存user
     *
     * @param user user
     */
    public void saveUser(User user) {
        mongoTemplate.save(user);
    }

    /**
     * 根据用户名查询user
     *
     * @param userName userName
     * @return user
     */
    public User findUserByUserName(String userName) {
        Query query = new Query(Criteria.where("userName").is(userName));
        return mongoTemplate.findOne(query, User.class);
    }

    /**
     * 更新user
     *
     * @param user user
     */
    public void updateUser(User user) {
        Query query = new Query(Criteria.where("id").is(user.getId()));
        Update update = new Update().set("userName", user.getUserName()).set("password", user.getPassword());
        mongoTemplate.updateFirst(query, update, User.class);
    }

    /**
     * 删除user
     *
     * @param id id
     */
    public void deleteUserById(Long id) {
        Query query = new Query(Criteria.where("id").is(id));
        mongoTemplate.remove(query, User.class);
    }

    /**
     * 分页查询
     * @param pageNum 页数
     * @param pageSize 每页数量
     * @param sortField 排序字段
     * @return pages
     */
    public Page<User> findUserPagination(Integer pageNum, Integer pageSize, String sortField) {
        SpringPageable pageable = new SpringPageable();
        PageModel pm = new PageModel();
        Query query = new Query();
        Sort sort = new Sort(Sort.Direction.DESC, sortField);
        pm.setPagenumber(pageNum);
        pm.setPagesize(pageSize);
        pm.setSort(sort);
        pageable.setPage(pm);
        Long count = mongoTemplate.count(query, User.class);
        List<User> list = mongoTemplate.find(query.with(pageable), User.class);
        return new PageImpl<>(list, pageable, count);
    }
}
```

### 2.2 测试类

```
package com.springboot.demo.mongo.dao;

import com.springboot.demo.mongo.entity.User;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.test.context.junit4.SpringRunner;


/**
 * Created by shirukai on 2018/8/8
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class UserDaoTest {

    @Autowired
    UserDao userDao;

    @Test
    public void saveUser() {
        User user = new User();
        for (int i = 0; i < 100; i++) {
            user.setId((long) (100 + i));
            user.setUserName("hollysys_" + i);
            user.setPassword("123456a?");
            userDao.saveUser(user);
            System.out.println("insert:" + i);
        }
    }

    @Test
    public void findUserByUserName() {
        User user = userDao.findUserByUserName("shirukai");
        System.out.println(user);
    }

    @Test
    public void updateUser() {
        User user = new User();
        user.setId(1L);
        user.setUserName("hollysys");
        user.setPassword("123456a?");
        userDao.updateUser(user);

    }

    @Test
    public void deleteUser() {
        userDao.deleteUserById(1L);
    }

    @Test
    public void findUserPagination() {
        Page<User> userPages = userDao.findUserPagination(1, 5, "id");
        userPages.forEach(u -> {
            System.out.println(u);
        });
    }
}
```