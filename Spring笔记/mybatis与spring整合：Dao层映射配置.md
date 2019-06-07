# mybatis与spring整合：Dao层映射配置 

要想mybatis查询数据库后，数据自动映射到指定的entity里的pojo类里，这里有三种方法，一种是通过XML文件里resultMap来建立对应关系、第二种是entity的类属性与表字段名字保持一致、第三种:其实原理是跟第二种一样，只不过是开启的mybatis的驼峰命名自动转换，即数据库字段 user_id的会对应到类属性里的userId，更符合java的命名规范。

## 第一种：通过resultMap来建立对应关系 

### UserDaoMapper.xml为例 

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.mavenssmlr.dao.UserDao">
    <resultMap id="resultUser" type="com.mavenssmlr.entity.User">
         <id property="id" column="id"/>
        <result property="uname" column="uname" />
        <result property="createTime" column="create_time" />
        <result property="modifyTime" column="modify_time" />
    </resultMap>
    <select id="queryAll" resultMap="resultUser">
        SELECT * FROM mavenssmlr.user
    </select>
</mapper>
```

说明：

type是指定实体类的路径

* <id property="id" column="id"> property 指的是类属性 column指的是字段名
* resultMap=“id名” 

### entity/User.java

```
package com.mavenssmlr.entity;

import java.io.Serializable;
import java.util.Date;

public class User implements Serializable{
    private int id;
    private String uname;
    private Date createTime;
    private Date modifyTime;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUname() {
        return uname;
    }

    public void setUname(String uname) {
        this.uname = uname;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getModifyTime() {
        return modifyTime;
    }

    public void setModifyTime(Date modifyTime) {
        this.modifyTime = modifyTime;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", uname='" + uname + '\'' +
                ", createTime=" + createTime +
                ", modifyTime=" + modifyTime +
                '}';
    }
}
```

测试：

```
@Test
public void queryAll() throws Exception {
    List<User> userList = userDao.queryAll();
    logger.info("____________userList={}", userList);
}
```

也可以利用注解：即resultMap里不写东西，在实体类里加上@Table @Id @Coulum等注解，进行关系映射

## 第二种：与数据库字段名保持一直或者开启驼峰命名转换 

配置方法：

mbatis-config.xml

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--配置全局属性-->
    <settings>
        <!--使用jdbc的getGeneratedKeys 获取数据库自增主键值-->
        <setting name="useGeneratedKeys" value="true"/>
        <!--使用列别名替换列名 默认true-->
        <setting name="useColumnLabel" value="true"/>
        <!--开启驼峰命名转换-->
       <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>
</configuration>
```