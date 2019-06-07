# Springboot项目启动自动执行方法

平时项目里可能会遇到，在启动项目的时候，需要进行初始化操作，如执行一段SQL脚本，或者提前对一些类进行实例化。这时候可以使用ApplicationRunner接口进行操作。下面将从初始化执行SQL脚本为例，记录在项目中应用ApplicationRunner的方法。

## 1 利用ApplicationRunner初始化SQL脚本

在项目resources目录下存放我们将要初始化的sql脚本，内容如下：

create_table_sql.sql

```
-- 创建模型表
CREATE TABLE IF NOT EXISTS `model`(
  `modelKey` VARCHAR(64) PRIMARY KEY COMMENT 'modelKey',
  `name` VARCHAR(20) NOT NULL UNIQUE COMMENT '模型名',
  `description`VARCHAR(64) COMMENT '描述',
  `user` VARCHAR(20) COMMENT '用户',
  `createTime` DATETIME DEFAULT NOW() COMMENT '创建日期',
  `modifyTime` TIMESTAMP NOT NULL DEFAULT current_timestamp ON UPDATE current_timestamp COMMENT '修改时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='模型表';
```

在init包下创建一个类InitProject.java，该类需要继承ApplicationRunner接口并实现里面的run方法，并将该类通过@Component 注入到spring里，如下所示：

```
@Component
public class InitProject implements ApplicationRunner {
    private static final Logger LOG = LoggerFactory.getLogger(InitProject.class);

    @Override
    public void run(ApplicationArguments args) throws Exception {
        LOG.info("==========init project===========");
    }
}
```

这时候，当我们启动项目的时候，就会执行run内日志打印的方法，效果如下图所示：

![](https://shirukai.gitee.io/images/d9276af6541e72164962b852e1ca4a68.jpg)

项目初始化执行sql的原理，其实就是在上面的run方法里执行初始化sql的方法。在初始sql之前，我们需要获取到当前项目的数据库连接池DataSource，我们可以通过@Autowired注解来拿到DataSource，测试方法如下：

```
@Component
public class InitProject implements ApplicationRunner {
    private static final Logger LOG = LoggerFactory.getLogger(InitProject.class);
    
    @Autowired
    DataSource dataSource;
    
    @Override
    public void run(ApplicationArguments args) throws Exception {
        LOG.info("==========init project===========");
        LOG.info("=========get dataSource==========={}",dataSource);
    }
}
```

效果如下图所示：

![](https://shirukai.gitee.io/images/e9bbe9a465587185cbdbdc6bea5f46df.jpg)

执行sql的方法的完整代码如下所示：

```
package com.springboot.demo.init;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.datasource.init.DataSourceInitializer;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;

/**
 * Created by shirukai on 2018/7/12
 */
@Component
public class InitProject implements ApplicationRunner {
    private static final Logger LOG = LoggerFactory.getLogger(InitProject.class);

    @Autowired
    DataSource dataSource;

    @Override
    public void run(ApplicationArguments args) throws Exception {
        LOG.info("==========init project===========");
        LOG.info("=========get dataSource==========={}", dataSource);
        //读取sql脚本
        try {
            ClassPathResource recordsSys = new ClassPathResource("create_table_sql.sql");
            DataSourceInitializer dsi = new DataSourceInitializer();
            dsi.setDataSource(dataSource);
            dsi.setDatabasePopulator(new ResourceDatabasePopulator(true, true, "utf-8", recordsSys));
            dsi.setEnabled(true);
            dsi.afterPropertiesSet();
            LOG.info("============init sql success============");
        } catch (Exception e) {
            LOG.error("init sql error={}", e.getMessage());
        }

    }
}
```

效果如下图所示：

![](https://shirukai.gitee.io/images/ef16d44d9c7366dcb29229ff8b57880b.jpg)

## 2 利用spring.datasource.schema=指定SQL初始化

