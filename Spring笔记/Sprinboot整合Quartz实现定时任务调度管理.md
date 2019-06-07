# Sprinboot整合Quartz实现定时任务调度管理

> 版本说明：
>
> springboot版本：2.0.0.RELEASE
>
> quartz版本：2.3.0
>
> github地址：https://github.com/shirukai/quartz-demo.git

Quartz官网：http://www.quartz-scheduler.org/

Quartz是一款开源的定时任务调度框架，本文主要记录一下在工作中使用springboot整合quartz实现定时任务调度管理的用例。内容主要有：springboot整合quartz相关配置、实现基于simpleTrigger的定时任务、实现基于cronTrigger的定时任务。

## 1 springboot整合Quartz相关配置

在之前，先创建一个springboot项目。

### 1.1 引入依赖

springboot整合quartz需要依赖两个包，quartz-jobs和spring-boot-starter-quartz下面我们在pom.xml文件里加入我们所需要的依赖包

```xml
        <!--quartz-->
        <dependency>
            <groupId>org.quartz-scheduler</groupId>
            <artifactId>quartz-jobs</artifactId>
            <version>2.3.0</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-quartz</artifactId>
            <version>2.0.0.RELEASE</version>
        </dependency>
```

### 1.2未整合前使用Quartz

参考官网：http://www.quartz-scheduler.org/documentation/quartz-2.2.x/quick-start.html

在整合spring和quartz之前，我们来看一下，如何以普通的方式使用Quartz。

#### 1.2.1 创建可调度Job

在项目中，创建一个job包用来存放我们使用Quartz调度的job。然后我们创建一个HelloJob.java类，来写我们的Job里的逻辑。HelloJob类需要继承org.quartz.Job接口并实现接口里的execute方法，这里我们只是简单的输出了一句话。代码如下：

```java
package com.example.quartz.job;

import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

/**
 * Created by shirukai on 2018/9/6
 */
public class HelloJob implements Job {
    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        System.out.println("这里可以执行我们的业务逻辑");
    }
}
```

#### 1.2.2 使用Quartz调度HelloJob

如上我们已经创建了一个HelloJob类，现在我们要写一个main方法，使用Quartz对HelloJob进行定时调度。

实现步骤如下：

第一步：使用StdSchedulerFactory工厂创建一个Scheduler实例

第二步：创建一个JobDetail并绑定HelloJob，设置jobName和group

第三步：创建一个Trigger，用以设置定时任务的时间、周期等属性

第四步：将JobDetail和Trigger传出Scheduler进行调度

代码如下：

```java
package com.example.quartz;

import com.example.quartz.job.HelloJob;
import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.Trigger;
import org.quartz.impl.StdSchedulerFactory;

import static org.quartz.JobBuilder.newJob;
import static org.quartz.SimpleScheduleBuilder.simpleSchedule;
import static org.quartz.TriggerBuilder.newTrigger;

/**
 * Created by shirukai on 2018/9/6
 */
public class QuartzTest {
    public static void main(String[] args) throws Exception {
        //从工厂创建scheduler实例
        Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();
        //开启scheduler
        scheduler.start();
        //定义一个job，并绑定我们的HelloJob
        JobDetail jobDetail = newJob(HelloJob.class)
                .withIdentity("job1", "group1")
                .build();
        //定义一个simple trigger,设置重复次数为10次，周期为2秒
        Trigger trigger = newTrigger()
                .withIdentity("job1", "group1")
                .startNow()
                .withSchedule(simpleSchedule().withIntervalInSeconds(1).withRepeatCount(10)).build();
        //使用scheduler进行job调度
        scheduler.scheduleJob(jobDetail, trigger);
    }
}

```

执行上述main方法，效果如下；

![](http://shirukai.gitee.io/images/403c4b99b44ce0f0e3d909c52fbed95a.gif)

#### 1.2.3 在HelloJob中使用Spring IOC容器

下面我们改写HelloJob，看看我们的定时任务能不能调用我们注册到Spring中的业务。

首先创建一个service包，用于存放我们spring中业务逻辑，并创建一个QuartzService类。

```java
package com.example.quartz.service;

import org.quartz.JobDetail;
import org.quartz.JobExecutionContext;
import org.springframework.stereotype.Service;

/**
 * Created by shirukai on 2018/9/6
 */
@Service
public class QuartzService {
    public void printJobInfo(JobExecutionContext context) {
        //从上下文中获取JobDetail
        JobDetail jobDetail = context.getJobDetail();
        String jobName = jobDetail.getKey().getName();
        String group = jobDetail.getKey().getGroup();
        System.out.println("Schedule job name is:" + jobName);
        System.out.println("Schedule job group is:" + group);
    }
}
```

修改HelloJob类

```java
package com.example.quartz.job;

import com.example.quartz.service.QuartzService;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Created by shirukai on 2018/9/6
 */
public class HelloJob implements Job {
    @Autowired
    QuartzService quartzService;

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        System.out.println("这里可以执行我们的业务逻辑");
        quartzService.printJobInfo(context);
    }
}
```

然后执行main方法，发现报错，这是因为我们使用了spring的IOC容器，所以我们要启动spring才能进行测试。否则我们获取不到我们注入到spring里的bean，会得到空指针异常。

![](http://shirukai.gitee.io/images/c42f65be402d33416a54c9d208052dc3.jpg)

创建上面main方法的junit单元测试类，并启用spring如下所示：

```java
package com.example.quartz;

import com.example.quartz.job.HelloJob;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.Trigger;
import org.quartz.impl.StdSchedulerFactory;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import static org.quartz.JobBuilder.newJob;
import static org.quartz.SimpleScheduleBuilder.simpleSchedule;
import static org.quartz.TriggerBuilder.newTrigger;

/**
 * Created by shirukai on 2018/9/6
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class QuartzTestTest {

    @Test
    public void main() throws Exception {
        //从工厂创建scheduler实例
        Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();
        //开启scheduler
        scheduler.start();
        //定义一个job，并绑定我们的HelloJob
        JobDetail jobDetail = newJob(HelloJob.class)
                .withIdentity("job1", "group1")
                .build();
        //定义一个simple trigger,设置重复次数为10次，周期为2秒
        Trigger trigger = newTrigger()
                .withIdentity("job1", "group1")
                .startNow()
                .withSchedule(simpleSchedule().withIntervalInSeconds(1).withRepeatCount(10)).build();
        //使用scheduler进行job调度
        scheduler.scheduleJob(jobDetail, trigger);
    }
}
```

执行单元测试之后，发现仍然报空指针异常，这是为什么呢，因为我们没有与spring整合，我们的job里是没法注入spring ioc管理的bean的，也就是说，没法在job里调用spring里的业务逻辑。所以接下来我们来看一下spring如何整合Quartz。

![](http://shirukai.gitee.io/images/b1b60314b4a4cec8d2e899223dacf174.jpg)

### 1.3 Springboot整合Quartz

在项目目录下创建一个conf包用来存放我们Quartz的相关配置。

然后创建一个JobFactory类，用于将JobFactory注入到spring里。如下所示：

```java
package com.example.quartz.conf;

import org.quartz.spi.TriggerFiredBundle;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.AutowireCapableBeanFactory;
import org.springframework.scheduling.quartz.AdaptableJobFactory;
import org.springframework.stereotype.Component;

/**
 * Created by shirukai on 2018/9/4
 */
@Component
public class JobFactory extends AdaptableJobFactory {
    @Autowired
    private AutowireCapableBeanFactory capableBeanFactory;

    @Override
    protected Object createJobInstance(TriggerFiredBundle bundle) throws Exception {
        //调用父类的方法
        Object jobInstance = super.createJobInstance(bundle);
        //进行注入
        capableBeanFactory.autowireBean(jobInstance);
        return jobInstance;
    }
}

```

在创建一个QuartzConfig类，用于注入Scheduler相关的Bean

```java
package com.example.quartz.conf;

import org.quartz.Scheduler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.PropertiesFactoryBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.scheduling.quartz.SchedulerFactoryBean;

import javax.sql.DataSource;
import java.io.IOException;
import java.util.Properties;

/**
 * Created by shirukai on 2018/9/4
 */
@Configuration
public class QuartzConfig {
    @Autowired
    private JobFactory jobFactory;
    
    @Bean
    public SchedulerFactoryBean schedulerFactoryBean() throws IOException {
        SchedulerFactoryBean schedulerFactoryBean = new SchedulerFactoryBean();
        schedulerFactoryBean.setOverwriteExistingJobs(true);
        schedulerFactoryBean.setJobFactory(jobFactory);
        return schedulerFactoryBean;
    }


    // 创建schedule
    @Bean(name = "scheduler")
    public Scheduler scheduler() throws IOException {
        return schedulerFactoryBean().getScheduler();
    }
}
```

这时我们已经将Quartz与Springboot简单的整合到一起，下面我们再次修改一下单元测试类里的方法，不再使用工厂类去创建Scheduler实例，而是通过注解从spring的ioc容器里拿到对应的实例，代码如下：

```java
package com.example.quartz;

import com.example.quartz.job.HelloJob;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.Trigger;
import org.quartz.impl.StdSchedulerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import static org.quartz.JobBuilder.newJob;
import static org.quartz.SimpleScheduleBuilder.simpleSchedule;
import static org.quartz.TriggerBuilder.newTrigger;

/**
 * Created by shirukai on 2018/9/6
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class QuartzTestTest {
    @Autowired
    Scheduler scheduler;
    @Test
    public void main() throws Exception {
        //开启scheduler
        scheduler.start();
        //定义一个job，并绑定我们的HelloJob
        JobDetail jobDetail = newJob(HelloJob.class)
                .withIdentity("job1", "group1")
                .build();
        //定义一个simple trigger,设置重复次数为10次，周期为2秒
        Trigger trigger = newTrigger()
                .withIdentity("job1", "group1")
                .startNow()
                .withSchedule(simpleSchedule().withIntervalInSeconds(1).withRepeatCount(10)).build();
        //使用scheduler进行job调度
        scheduler.scheduleJob(jobDetail, trigger);
    }
}
```

运行测试类，成功执行。效果如下：

![](http://shirukai.gitee.io/images/0bd7447948ce33bbf00c4c9e3a2595f2.jpg)

### 1.4 自定义配置文件与持久化

这一小节主要记录一下Springboot与Quartz的深度整合，一个是自定义Quartz的配置文件、另一个是Quartz定时任务的持久化。

#### 1.4.1 自定义Quartz的配置文件

在项目resources目录下创建一个quartz.properties配置文件，内容如下:

```properties
#使用自己的配置文件
org.quartz.jobStore.useProperties:true

#默认或是自己改名字都行
org.quartz.scheduler.instanceName: DefaultQuartzScheduler
#如果使用集群，instanceId必须唯一，设置成AUTO
org.quartz.scheduler.instanceId = AUTO


org.quartz.threadPool.class: org.quartz.simpl.SimpleThreadPool
org.quartz.threadPool.threadCount: 10
org.quartz.threadPool.threadPriority: 5
org.quartz.threadPool.threadsInheritContextClassLoaderOfInitializingThread: true
```

在上面我们创建的QuartzConfig类中注入我们的配置文件

```java
    @Bean
    public Properties quartzProperties() throws IOException {
        PropertiesFactoryBean propertiesFactoryBean = new PropertiesFactoryBean();
        propertiesFactoryBean.setLocation(new ClassPathResource("quartz.properties"));
        propertiesFactoryBean.afterPropertiesSet();
        return propertiesFactoryBean.getObject();
    }
    @Bean
    public SchedulerFactoryBean schedulerFactoryBean() throws IOException {
        SchedulerFactoryBean schedulerFactoryBean = new SchedulerFactoryBean();
        schedulerFactoryBean.setOverwriteExistingJobs(true);
        schedulerFactoryBean.setQuartzProperties(quartzProperties());
        schedulerFactoryBean.setJobFactory(jobFactory);
        return schedulerFactoryBean;
    }
```

这样我们就可以使用自定义的配置文件了。

#### 1.4.2 Quartz定时任务的持久化

默认情况下，Quartz是将我们的定时任务的记录保存到内存里，等我们再次启动项目的时候，我们之前设置的定时任务都会被清空，无法持久化。当然Quartz可以将记录持久化到数据库中，下面将从自定义DataSource持久化数据和使用Springboot的DataSource两方面来持久化Quartz的数据。

##### 1.4.2.1 自定义DataSource

首先在配置文件中添加如下内容，用以配置数据库相关信息：

```properties
#存储方式使用JobStoreTX，也就是数据库
org.quartz.jobStore.class:org.quartz.impl.jdbcjobstore.JobStoreTX
org.quartz.jobStore.driverDelegateClass:org.quartz.impl.jdbcjobstore.StdJDBCDelegate
#是否使用集群（如果项目只部署到 一台服务器，就不用了）
org.quartz.jobStore.isClustered = false
org.quartz.jobStore.clusterCheckinInterval=20000
org.quartz.jobStore.tablePrefix = QRTZ_
org.quartz.jobStore.dataSource = myDS

#配置数据源
#数据库中quartz表的表名前缀

org.quartz.dataSource.myDS.driver = com.mysql.jdbc.Driver
org.quartz.dataSource.myDS.URL = jdbc:mysql://localhost:3306/springboot?characterEncoding=utf-8
org.quartz.dataSource.myDS.user = root
org.quartz.dataSource.myDS.password = hollysys
org.quartz.dataSource.myDS.maxConnections = 5
```

这样配置之后我们就可以将Quartz数据持久化到我们指定的数据库了，但是仅仅是这样操作是不行的，回报如下错误：

![](http://shirukai.gitee.io/images/d08f935c5653c1c54862882ae676a1e2.jpg)

从错误信息可以看出，与Quartz相关的表不存在。我们需要创建相应的表，建表脚本在官网都可以download。

官网地址：http://www.quartz-scheduler.org/downloads/

到官网下载源码，然后在源码quartz-2.3.0/docs/dbTables目录下可以找到所有数据库的建表语句，

这里提供一下2.3.0版mysql innoDB的建表脚本：

```mysql
DROP TABLE IF EXISTS QRTZ_FIRED_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_PAUSED_TRIGGER_GRPS;
DROP TABLE IF EXISTS QRTZ_SCHEDULER_STATE;
DROP TABLE IF EXISTS QRTZ_LOCKS;
DROP TABLE IF EXISTS QRTZ_SIMPLE_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_SIMPROP_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_CRON_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_BLOB_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_TRIGGERS;
DROP TABLE IF EXISTS QRTZ_JOB_DETAILS;
DROP TABLE IF EXISTS QRTZ_CALENDARS;

CREATE TABLE QRTZ_JOB_DETAILS(
SCHED_NAME VARCHAR(120) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
JOB_CLASS_NAME VARCHAR(250) NOT NULL,
IS_DURABLE VARCHAR(1) NOT NULL,
IS_NONCONCURRENT VARCHAR(1) NOT NULL,
IS_UPDATE_DATA VARCHAR(1) NOT NULL,
REQUESTS_RECOVERY VARCHAR(1) NOT NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
NEXT_FIRE_TIME BIGINT(13) NULL,
PREV_FIRE_TIME BIGINT(13) NULL,
PRIORITY INTEGER NULL,
TRIGGER_STATE VARCHAR(16) NOT NULL,
TRIGGER_TYPE VARCHAR(8) NOT NULL,
START_TIME BIGINT(13) NOT NULL,
END_TIME BIGINT(13) NULL,
CALENDAR_NAME VARCHAR(200) NULL,
MISFIRE_INSTR SMALLINT(2) NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,JOB_NAME,JOB_GROUP)
REFERENCES QRTZ_JOB_DETAILS(SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_SIMPLE_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
REPEAT_COUNT BIGINT(7) NOT NULL,
REPEAT_INTERVAL BIGINT(12) NOT NULL,
TIMES_TRIGGERED BIGINT(10) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_CRON_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
CRON_EXPRESSION VARCHAR(120) NOT NULL,
TIME_ZONE_ID VARCHAR(80),
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_SIMPROP_TRIGGERS
  (          
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    STR_PROP_1 VARCHAR(512) NULL,
    STR_PROP_2 VARCHAR(512) NULL,
    STR_PROP_3 VARCHAR(512) NULL,
    INT_PROP_1 INT NULL,
    INT_PROP_2 INT NULL,
    LONG_PROP_1 BIGINT NULL,
    LONG_PROP_2 BIGINT NULL,
    DEC_PROP_1 NUMERIC(13,4) NULL,
    DEC_PROP_2 NUMERIC(13,4) NULL,
    BOOL_PROP_1 VARCHAR(1) NULL,
    BOOL_PROP_2 VARCHAR(1) NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP) 
    REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_BLOB_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
BLOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
INDEX (SCHED_NAME,TRIGGER_NAME, TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_CALENDARS (
SCHED_NAME VARCHAR(120) NOT NULL,
CALENDAR_NAME VARCHAR(200) NOT NULL,
CALENDAR BLOB NOT NULL,
PRIMARY KEY (SCHED_NAME,CALENDAR_NAME))
ENGINE=InnoDB;

CREATE TABLE QRTZ_PAUSED_TRIGGER_GRPS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE QRTZ_FIRED_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
ENTRY_ID VARCHAR(95) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
FIRED_TIME BIGINT(13) NOT NULL,
SCHED_TIME BIGINT(13) NOT NULL,
PRIORITY INTEGER NOT NULL,
STATE VARCHAR(16) NOT NULL,
JOB_NAME VARCHAR(200) NULL,
JOB_GROUP VARCHAR(200) NULL,
IS_NONCONCURRENT VARCHAR(1) NULL,
REQUESTS_RECOVERY VARCHAR(1) NULL,
PRIMARY KEY (SCHED_NAME,ENTRY_ID))
ENGINE=InnoDB;

CREATE TABLE QRTZ_SCHEDULER_STATE (
SCHED_NAME VARCHAR(120) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
LAST_CHECKIN_TIME BIGINT(13) NOT NULL,
CHECKIN_INTERVAL BIGINT(13) NOT NULL,
PRIMARY KEY (SCHED_NAME,INSTANCE_NAME))
ENGINE=InnoDB;

CREATE TABLE QRTZ_LOCKS (
SCHED_NAME VARCHAR(120) NOT NULL,
LOCK_NAME VARCHAR(40) NOT NULL,
PRIMARY KEY (SCHED_NAME,LOCK_NAME))
ENGINE=InnoDB;

CREATE INDEX IDX_QRTZ_J_REQ_RECOVERY ON QRTZ_JOB_DETAILS(SCHED_NAME,REQUESTS_RECOVERY);
CREATE INDEX IDX_QRTZ_J_GRP ON QRTZ_JOB_DETAILS(SCHED_NAME,JOB_GROUP);

CREATE INDEX IDX_QRTZ_T_J ON QRTZ_TRIGGERS(SCHED_NAME,JOB_NAME,JOB_GROUP);
CREATE INDEX IDX_QRTZ_T_JG ON QRTZ_TRIGGERS(SCHED_NAME,JOB_GROUP);
CREATE INDEX IDX_QRTZ_T_C ON QRTZ_TRIGGERS(SCHED_NAME,CALENDAR_NAME);
CREATE INDEX IDX_QRTZ_T_G ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_GROUP);
CREATE INDEX IDX_QRTZ_T_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_STATE);
CREATE INDEX IDX_QRTZ_T_N_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP,TRIGGER_STATE);
CREATE INDEX IDX_QRTZ_T_N_G_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_GROUP,TRIGGER_STATE);
CREATE INDEX IDX_QRTZ_T_NEXT_FIRE_TIME ON QRTZ_TRIGGERS(SCHED_NAME,NEXT_FIRE_TIME);
CREATE INDEX IDX_QRTZ_T_NFT_ST ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_STATE,NEXT_FIRE_TIME);
CREATE INDEX IDX_QRTZ_T_NFT_MISFIRE ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME);
CREATE INDEX IDX_QRTZ_T_NFT_ST_MISFIRE ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME,TRIGGER_STATE);
CREATE INDEX IDX_QRTZ_T_NFT_ST_MISFIRE_GRP ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME,TRIGGER_GROUP,TRIGGER_STATE);

CREATE INDEX IDX_QRTZ_FT_TRIG_INST_NAME ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,INSTANCE_NAME);
CREATE INDEX IDX_QRTZ_FT_INST_JOB_REQ_RCVRY ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,INSTANCE_NAME,REQUESTS_RECOVERY);
CREATE INDEX IDX_QRTZ_FT_J_G ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,JOB_NAME,JOB_GROUP);
CREATE INDEX IDX_QRTZ_FT_JG ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,JOB_GROUP);
CREATE INDEX IDX_QRTZ_FT_T_G ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP);
CREATE INDEX IDX_QRTZ_FT_TG ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,TRIGGER_GROUP);

commit; 

```

手动执行sql建表脚本，将所需要的表创建到数据库里，关于如何自动初始化建表脚本，后面将会补充到。

##### 1.4.2.2 使用Springboot的DataSource

除了使用我们在配置文件中指定的数据源外，我们话可以使用springboot项目中配置的数据源。

首先需要注释掉配置文件中与数据源相关的配置，如下所示：

```properties
#存储方式使用JobStoreTX，也就是数据库
#org.quartz.jobStore.class:org.quartz.impl.jdbcjobstore.JobStoreTX
#org.quartz.jobStore.driverDelegateClass:org.quartz.impl.jdbcjobstore.StdJDBCDelegate
##是否使用集群（如果项目只部署到 一台服务器，就不用了）
#org.quartz.jobStore.isClustered = false
#org.quartz.jobStore.clusterCheckinInterval=20000
#org.quartz.jobStore.tablePrefix = QRTZ_
#org.quartz.jobStore.dataSource = myDS
#
##配置数据源
##数据库中quartz表的表名前缀
#
#org.quartz.dataSource.myDS.driver = com.mysql.jdbc.Driver
#org.quartz.dataSource.myDS.URL = jdbc:mysql://localhost:3306/springboot?characterEncoding=utf-8
#org.quartz.dataSource.myDS.user = root
#org.quartz.dataSource.myDS.password = hollysys
#org.quartz.dataSource.myDS.maxConnections = 5
```

然后再QuartzConfig类中设置我们的数据源，分为两步;

第一步 从spring的ioc容器中获取datasource

```java
    @Autowired
    DataSource dataSource;
```

第二步 将获取到的datasource设置到SchedulerFactoryBean里

```java
        schedulerFactoryBean.setDataSource(dataSource);
```

这样我们就可以使用项目中的datasource了。

## 2 实现基于simpleTrigger的定时任务

先讲一下我们将Quartz与Springboot整合实现定时任务管理的实现思路：

1. 使用自己的表来保存定时任务相关信息
2. 封装Quartz相关操作提供基于simpleTrigger和cronTrigger的定时任务设置接口
3. 对外提供相关操作的API

### 2.1 创建Schedule表

利用springboot创建Schedule表，用以来保存我们定时任务相关的信息。

#### 2.1.1 创建ScheduleStatusEnum.java枚举类

在项目entity包下创建定时任务状态枚举类，用来映射定时任务的状态

```java
package com.example.quartz.entity;

/**
 * Created by shirukai on 2018/9/4
 */
public enum ScheduleStatusEnum {
    ACTIVATED(1, "已激活"),
    INACTIVATED(0, "未激活");
    private int state;
    private String stateInfo;

    ScheduleStatusEnum(int state, String stateInfo) {
        this.state = state;
        this.stateInfo = stateInfo;
    }

    public int getState() {
        return state;
    }

    public String getStateInfo() {
        return stateInfo;
    }
}

```

#### 2.1.2 创建Schedule.java的实体类

在项目entity包下创建Sechedule.java实体类

```java
package com.example.quartz.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Date;

/**
 * Created by shirukai on 2018/9/3
 */
@Entity
public class Schedule implements Serializable {
    @Id
    private String id;
    private String triggerInfo;
    @Enumerated(EnumType.STRING)
    private ScheduleStatusEnum status;
    private String groupName; 
    private String jobName;

    private int record;//运行记录
    @Temporal(TemporalType.TIMESTAMP)
    @Column(updatable = false)
    @CreationTimestamp
    private Date createdTimestamp;
    @JsonIgnore
    @Temporal(TemporalType.TIMESTAMP)
    @Column(insertable = false)
    @UpdateTimestamp
    private Date updatedTimestamp;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTriggerInfo() {
        return triggerInfo;
    }

    public void setTriggerInfo(String triggerInfo) {
        this.triggerInfo = triggerInfo;
    }

    public ScheduleStatusEnum getStatus() {
        return status;
    }

    public void setStatus(ScheduleStatusEnum status) {
        this.status = status;
    }

    public String getGroupName() {
        return groupName;
    }

    public void setGroupName(String groupName) {
        this.groupName = groupName;
    }

    public String getJobName() {
        return jobName;
    }

    public void setJobName(String jobName) {
        this.jobName = jobName;
    }

    public int getRecord() {
        return record;
    }

    public void setRecord(int record) {
        this.record = record;
    }

    public Date getCreatedTimestamp() {
        return createdTimestamp;
    }

    public void setCreatedTimestamp(Date createdTimestamp) {
        this.createdTimestamp = createdTimestamp;
    }

    public Date getUpdatedTimestamp() {
        return updatedTimestamp;
    }

    public void setUpdatedTimestamp(Date updatedTimestamp) {
        this.updatedTimestamp = updatedTimestamp;
    }
}

```

#### 2.1.3 创建 ScheduleRepository.java

在项目repository包下创建ScheduleRepository.java，用以使用jpa对数据库表进行相关的操作。

```java
package com.example.quartz.repository;

import com.example.quartz.entity.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Created by shirukai on 2018/9/4
 */
public interface ScheduleRepository extends JpaRepository<Schedule, String> {
    Schedule findScheduleByJobNameAndGroupName(String jobName, String groupName);

    Schedule findScheduleById(String scheduleId);
}

```

 至此我们Schedule表相关的操作就已经完成了，启动项目后，我们的表会被自动创建。

### 2.2 基于SimpleTrigger封装Quartz相关操作

#### 2.2.1 创建SimpleScheduleDTO.java实体类

创建DTO类是为了方便我们对象之间的数据传输，格式如下所示；

```json
{
    "startTime":0,
    "repeatCount": 100,
    "period": {
        "time": "5",
        "unit": "minutes"
    },
    "endTime":0
}
```

在项目dto包想创建ScheduleDTO.java实体类

```java
package com.example.quartz.dto;

/**
 * Created by shirukai on 2018/9/7
 */
public class ScheduleDTO {
    private String jobName;
    private String group;
    private long startTime;
    private long endTime;

    public String getJobName() {
        return jobName;
    }

    public void setJobName(String jobName) {
        this.jobName = jobName;
    }

    public String getGroup() {
        return group;
    }

    public void setGroup(String group) {
        this.group = group;
    }

    public long getStartTime() {
        return startTime;
    }

    public void setStartTime(long startTime) {
        this.startTime = startTime;
    }

    public long getEndTime() {
        return endTime;
    }

    public void setEndTime(long endTime) {
        this.endTime = endTime;
    }
}

```

同目录下创建Period类映射JSON中的period字段

```java
package com.example.quartz.dto;

/**
 * Created by shirukai on 2018/9/7
 */
public class Period {

    private long time;
    private String unit;

    public long getTime() {
        return time;
    }

    public void setTime(long time) {
        this.time = time;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }
}

```

同目录下创建SimpleScheduleDTO类继承上面的ScheduleDTO类

```java
package com.example.quartz.dto;

/**
 * Created by shirukai on 2018/9/7
 */
public class SimpleScheduleDTO extends ScheduleDTO {
    private int repeatCount;
    private Period period;

    public int getRepeatCount() {
        return repeatCount;
    }

    public void setRepeatCount(int repeatCount) {
        this.repeatCount = repeatCount;
    }


    public Period getPeriod() {
        return period;
    }

    public void setPeriod(Period period) {
        this.period = period;
    }
}
```

#### 2.2.2 创建ScheduleManager

创建定时任务管理器ScheduleManager用以封装Quartz相关的操作。

##### 2.2.2.1 在项目manager包下创建ScheduleManager.java类

创建ScheduleManager类，从spring ioc中注入Quartz的Scheduler，并将ScheduleManager类使用@Component注解注册到Spring里。

```java
package com.example.quartz.manager;

import org.quartz.Scheduler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Created by shirukai on 2018/9/7
 * 定时任务管理器
 */
@Component
public class ScheduleManager {
    @Autowired
    Scheduler scheduler;
    //todo
}

```

##### 2.2.2.2 构建SimpleScheduleBuilder

根据周期参数

```json
"period": {
        "time": "5",
        "unit": "minutes"
    },
```

构建SimpleScheduleBuilder。如参数表示每5分钟为一个周期，所以我们编写getSimpleScheduleBuilder方法，传入如上的参数，构建相应的SimpleSchedulerBuilder，代码如下

```java
    /**
     * 构建 SimpleScheduleBuilder
     *
     * @param period 周期参数
     * @return SimpleScheduleBuilder
     */
    private SimpleScheduleBuilder getSimpeScheduleBuilder(Period period, int repeatCount) {
        SimpleScheduleBuilder ssb = SimpleScheduleBuilder.simpleSchedule();
        String unit = period.getUnit();
        long time = period.getTime();
        switch (unit) {
            case "milliseconds":
                ssb.withIntervalInMilliseconds(time);
                break;
            case "seconds":
                ssb.withIntervalInSeconds((int) time);
                break;
            case "minutes":
                ssb.withIntervalInMinutes((int) time);
                break;
            case "hours":
                ssb.withIntervalInHours((int) time);
                break;
            case "days":
                ssb.withIntervalInHours((int) time * 24);
                break;
            default:
                break;
        }
        ssb.withRepeatCount(repeatCount);
        return ssb;
    }
```

##### 2.2.2.3 构建SimpleTrigger

利用上述生成的SimpleScheduleBuilder和传入的参数，这里用SimpleScheduleDTO封装，构建相应的SimpleTrigger。代码如下：

```java
    /**
     * 构建 SimpleTrigger
     *
     * @param ssd 参数
     * @return Trigger
     */
    private Trigger getSimpleTrigger(SimpleScheduleDTO ssd) {
        String jobName = ssd.getJobName();
        String group = ssd.getGroup();
        int repeatCount = ssd.getRepeatCount();
        TriggerBuilder triggerBuilder = TriggerBuilder.newTrigger()
                //设置jobName和group
                .withIdentity(jobName, group)
                //设置Schedule方式
                .withSchedule(getSimpeScheduleBuilder(ssd.getPeriod(), repeatCount));
        if (ssd.getStartTime() != 0) {
            //设置起始时间
            triggerBuilder.startAt(new Date(ssd.getStartTime()));
        } else {
            triggerBuilder.startNow();
        }
        if (ssd.getEndTime() != 0) {
            //设置终止时间
            triggerBuilder.endAt(new Date(ssd.getEndTime()));
        }
        return triggerBuilder.build();
    }
```

##### 2.2.2.4 创建ScheduleJob

Quartz创建定时任务，通过JobDetail 和Trigger就可以创建，我们编写createJob方法，通过传入相应参数来实现创建定时任务的功能，代码如下:

```java
/**
     * 创建Job
     * @param jobClass 要调度的类名
     * @param sd 调度参数
     * @param jobDataMap 数据
     * @param trigger trigger
     * @return Schedule
     */
    private Schedule createJob(
            Class<? extends Job> jobClass,
            ScheduleDTO sd,
            JobDataMap jobDataMap,
            Trigger trigger
    ){
        String jobName = sd.getJobName();
        String group = sd.getGroup();
        //判断记录在数据库是否存在
        Schedule schedule = scheduleRepository.findScheduleByJobNameAndGroupName(jobName, group);
        if (schedule == null) {
            schedule = new Schedule();
        } else {
            throw new RuntimeException("Schedule job already exists.");
        }
        String scheduleId = UUID.randomUUID().toString();
        try {
            if (jobDataMap == null) {
                jobDataMap = new JobDataMap();
            }
            jobDataMap.put("id", scheduleId);
            //创建JobDetail
            JobDetail jobDetail = JobBuilder.newJob(jobClass).withIdentity(jobName, group).usingJobData(jobDataMap).build();
            schedule.setId(scheduleId);
            schedule.setStatus(ScheduleStatusEnum.ACTIVATED);
            schedule.setJobName(jobName);
            schedule.setGroupName(group);
            schedule.setTriggerInfo(JSON.toJSONString(sd));
            schedule.setRecord(0);
            //保存记录信息
            schedule = scheduleRepository.save(schedule);
            //调度执行定时任务
            scheduler.scheduleJob(jobDetail, trigger);
        } catch (Exception e) {
            log.error("Create schedule job error:{}", e.getMessage());
            throw new RuntimeException(e);
        }
        return schedule;
    }
```

编写一个createSimpleJob方法，用于创建SimpleTrigger类型的Job

```java
/**
     * 创建 simple schedule job
     *
     * @param jobClass   job class
     * @param ssd        参数
     * @param jobDataMap 数据
     * @return Schedule
     */
    public Schedule createSimpleJob(Class<? extends Job> jobClass,
                                    SimpleScheduleDTO ssd,
                                    JobDataMap jobDataMap) {
        Trigger trigger = getSimpleTrigger(ssd);
        return createJob(jobClass, ssd, jobDataMap, trigger);
    }
```

##### 2.2.2.5 更新Simple Schedule Job

```java
/**
 * 更新simple job
 *
 * @param scheduleId scheduleId
 * @param ssd        ssv
 * @return Schedule
 */
public Schedule updateSimpleJob(String scheduleId, SimpleScheduleDTO ssd) {
    Schedule schedule = getSchedule(scheduleId);
    return updateSimpleJob(schedule, ssd);
}

public Schedule updateSimpleJob(Schedule schedule, SimpleScheduleDTO ssd) {
    try {
        String jobName = schedule.getJobName();
        String groupName = schedule.getGroupName();
        JobKey jobKey = new JobKey(jobName, groupName);
        JobDetail jobDetail = scheduler.getJobDetail(jobKey);
        //先删除
        scheduler.deleteJob(jobKey);
        //重新创建
        Trigger trigger = getSimpleTrigger(ssd);
        scheduler.scheduleJob(jobDetail, trigger);
        //更新元数据
        schedule.setRecord(0);
        schedule.setTriggerInfo(JSON.toJSONString(ssd));
        scheduleRepository.save(schedule);
    } catch (SchedulerException e) {
        log.error("Update simple schedule job error:{}", e.getMessage());
    }
    return schedule;
}

public Schedule getSchedule(String scheduleId) {
    Schedule schedule = scheduleRepository.findScheduleById(scheduleId);
    if (schedule == null) {
        throw new RuntimeException("Schedule job does not exist");
    }
    return schedule;
}
```

##### 2.2.2.6 暂停job

```java
s/**
 * 暂停某个job
 *
 * @param scheduleId id
 */
public Schedule pauseJob(String scheduleId) {
    Schedule schedule = getSchedule(scheduleId);
    return pauseJob(schedule);
}

public Schedule pauseJob(Schedule schedule) {
    JobKey jobKey = new JobKey(schedule.getJobName(), schedule.getGroupName());
    try {
        scheduler.pauseJob(jobKey);
        schedule.setStatus(ScheduleStatusEnum.INACTIVATED);
        scheduleRepository.save(schedule);
    } catch (SchedulerException e) {
        log.error("Pause schedule job error:{}", e.getMessage());
    }
    return schedule;
}
```

##### 2.2.2.7 恢复job

```java
/**
 * 恢复某个job
 *
 * @param scheduleId id
 */
public Schedule resumeJob(String scheduleId) {
    Schedule schedule = getSchedule(scheduleId);
    return resumeJob(schedule);
}

public Schedule resumeJob(Schedule schedule) {
    JobKey jobKey = new JobKey(schedule.getJobName(), schedule.getGroupName());
    try {
        scheduler.resumeJob(jobKey);
        schedule.setStatus(ScheduleStatusEnum.ACTIVATED);
        scheduleRepository.save(schedule);
    } catch (SchedulerException e) {
        log.error("Resume schedule job error:{}", e.getMessage());
    }
    return schedule;
}
```

##### 2.2.2.8 删除job

```java
/**
 * 删除 job
 *
 * @param scheduleId id
 */
public void deleteJob(String scheduleId) {
    Schedule schedule = getSchedule(scheduleId);
    deleteJob(schedule);
}

public void deleteJob(Schedule schedule) {
    JobKey jobKey = new JobKey(schedule.getJobName(), schedule.getGroupName());
    try {
        scheduler.deleteJob(jobKey);
        scheduleRepository.delete(schedule);
    } catch (SchedulerException e) {
        log.error("Delete schedule job error:{}", e.getMessage());
    }
}
```

### 2.3 对外提供相关API

#### 2.3.1 创建ScheduleService

创建ScheduleService，调用ScheduleManager分装的接口。

```java
package com.example.quartz.service;

import com.example.quartz.dto.SimpleScheduleDTO;
import com.example.quartz.entity.Schedule;
import com.example.quartz.job.HelloJob;
import com.example.quartz.manager.ScheduleManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Created by shirukai on 2018/9/7
 */
@Service
public class ScheduleService {
    private final static String GROUP = "TEST_GROUP";
    @Autowired
    ScheduleManager scheduleManager;
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    /**
     * 设置编排定时任务
     *
     * @param ssd 定时参数
     * @return schedule
     */
    public Schedule setSchedule(String joName, SimpleScheduleDTO ssd) {
        ssd.setJobName(joName);
        ssd.setGroup(GROUP);
        return scheduleManager.createSimpleJob(HelloJob.class, ssd, null);
    }


    /**
     * 更新编排定时任务
     *
     * @param ssd 参数
     * @return schedule
     */
    public Schedule modifySchedule(String jobName, SimpleScheduleDTO ssd) {
        Schedule schedule = scheduleManager.getJobByNameAndGroup(jobName, GROUP);
        ssd.setJobName(jobName);
        ssd.setGroup(GROUP);
        return scheduleManager.updateSimpleJob(schedule, ssd);
    }

    /**
     * 获取编排定时信息
     *
     * @param joName id
     * @return schedule
     */
    public Schedule getSchedule(String joName) {
        return scheduleManager.getJobByNameAndGroup(joName, GROUP);
    }

    /**
     * 暂停编排定时任务
     *
     * @param joName joName
     * @return schedule
     */
    public Schedule pauseSchedule(String joName) {
        Schedule schedule = scheduleManager.getJobByNameAndGroup(joName, GROUP);
        return scheduleManager.pauseJob(schedule);
    }

    /**
     * 恢复编排定时任务
     *
     * @param joName joName
     * @return schedule
     */
    public Schedule resumeSchedule(String joName) {
        Schedule schedule = scheduleManager.getJobByNameAndGroup(joName, GROUP);
        return scheduleManager.resumeJob(schedule);
    }

    /**
     * 删除编排定时任务
     *
     * @param joName joName
     * @return str
     */
    public String removerSchedule(String joName) {
        Schedule schedule = scheduleManager.getJobByNameAndGroup(joName, GROUP);
        scheduleManager.deleteJob(schedule);
        return "Delete schedule job succeed.";
    }
}

```

#### 2.3.2 创建SceduleController

创建SceduleCOntroller对外提供可访问API

```java
package com.example.quartz.controller;


import com.example.quartz.common.rest.RestMessage;
import com.example.quartz.common.util.RestMessageUtil;
import com.example.quartz.dto.SimpleScheduleDTO;
import com.example.quartz.service.ScheduleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * Created by shirukai on 2018/9/7
 */
@RestController
@RequestMapping(value = "/api/v1/schedule/")
public class ScheduleController {
    @Autowired
    ScheduleService scheduleService;
    @PostMapping(value = "/{jobName}/simple")
    public RestMessage schedule(
            @PathVariable("jobName") String jobName,
            @RequestBody SimpleScheduleDTO simpleScheduleDTO
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.setSchedule(jobName, simpleScheduleDTO));
    }

    @PutMapping(value = "/{jobName}/simple")
    public RestMessage modifySchedule(
            @PathVariable("jobName") String jobName,
            @RequestBody SimpleScheduleDTO simpleScheduleDTO
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.modifySchedule(jobName, simpleScheduleDTO));
    }

    @DeleteMapping(value = "/{jobName}")
    public RestMessage removeSchedule(
            @PathVariable("jobName") String jobName
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.removerSchedule(jobName));
    }

    @PostMapping(value = "/{jobName}/pause")
    public RestMessage pauseSchedule(
            @PathVariable("jobName") String jobName
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.pauseSchedule(jobName));
    }

    @PostMapping(value = "/{jobName}/resume")
    public RestMessage resumeSchedule(
            @PathVariable("jobName") String jobName
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.resumeSchedule(jobName));
    }

    @GetMapping(value = "/{jobName}")
    public RestMessage scheduleInfo(
            @PathVariable("jobName") String jobName
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.getSchedule(jobName));
    }
}

```

#### 2.3.3 测试提供的API

在这之前先修改我们的HelloJob类，用以记录我们执行的条数

```java
package com.example.quartz.job;

import com.example.quartz.entity.Schedule;
import com.example.quartz.repository.ScheduleRepository;
import org.quartz.Job;
import org.quartz.JobDataMap;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Created by shirukai on 2018/9/7
 */
public class HelloJob implements Job {
    @Autowired
    ScheduleRepository scheduleRepository;
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        //获取上下文数据
        JobDataMap dataMap = context.getMergedJobDataMap();
        String scheduleId = dataMap.getString("id");

        Schedule schedule = scheduleRepository.findScheduleById(scheduleId);
        log.info("定时任务执行了：{}", scheduleId);
        //更新执行条数
        schedule.setRecord(schedule.getRecord() + 1);
        scheduleRepository.save(schedule);
    }
}

```

##### 2.3.3.1 设置定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/simple

请求类型：POST

请求参数：

```json
{
    "repeatCount": 100,
    "period": {
        "time": "5",
        "unit": "seconds"
    }
}
```

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": {
        "id": "218a3db4-e2e6-480e-b520-bac138b6c403",
        "triggerInfo": "{\"endTime\":0,\"group\":\"TEST_GROUP\",\"jobName\":\"8aaabdfc659f74620165b2ad36b50030\",\"period\":{\"time\":5,\"unit\":\"seconds\"},\"repeatCount\":100,\"startTime\":0}",
        "status": "ACTIVATED",
        "groupName": "TEST_GROUP",
        "jobName": "8aaabdfc659f74620165b2ad36b50030",
        "record": 0,
        "createdTimestamp": "2018-09-07T06:50:15.521+0000"
    }
}
```

##### 2.3.3.2 查看定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/

请求类型：GET

请求参数：无

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": {
        "id": "218a3db4-e2e6-480e-b520-bac138b6c403",
        "triggerInfo": "{\"endTime\":0,\"group\":\"TEST_GROUP\",\"jobName\":\"8aaabdfc659f74620165b2ad36b50030\",\"period\":{\"time\":5,\"unit\":\"seconds\"},\"repeatCount\":100,\"startTime\":0}",
        "status": "ACTIVATED",
        "groupName": "TEST_GROUP",
        "jobName": "8aaabdfc659f74620165b2ad36b50030",
        "record": 9,
        "createdTimestamp": "2018-09-07T06:50:16.000+0000"
    }
}
```

##### 2.3.3.3 暂停定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/pause

请求类型：POST

请求参数：无

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": {
        "id": "218a3db4-e2e6-480e-b520-bac138b6c403",
        "triggerInfo": "{\"endTime\":0,\"group\":\"TEST_GROUP\",\"jobName\":\"8aaabdfc659f74620165b2ad36b50030\",\"period\":{\"time\":5,\"unit\":\"seconds\"},\"repeatCount\":100,\"startTime\":0}",
        "status": "INACTIVATED",
        "groupName": "TEST_GROUP",
        "jobName": "8aaabdfc659f74620165b2ad36b50030",
        "record": 23,
        "createdTimestamp": "2018-09-07T06:50:16.000+0000"
    }
}
```

##### 2.3.3.4 恢复定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/resume

请求类型：POST

请求参数：无

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": {
        "id": "218a3db4-e2e6-480e-b520-bac138b6c403",
        "triggerInfo": "{\"endTime\":0,\"group\":\"TEST_GROUP\",\"jobName\":\"8aaabdfc659f74620165b2ad36b50030\",\"period\":{\"time\":5,\"unit\":\"seconds\"},\"repeatCount\":100,\"startTime\":0}",
        "status": "ACTIVATED",
        "groupName": "TEST_GROUP",
        "jobName": "8aaabdfc659f74620165b2ad36b50030",
        "record": 23,
        "createdTimestamp": "2018-09-07T06:50:16.000+0000"
    }
}
```

##### 2.3.3. 5 删除定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/

请求类型：DELETE

请求参数：无

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": "Delete schedule job succeed."
}
```

## 3 实现基于CronTrigger的定时任务

上面我们已经实现了基于SimpleTrigger的定时任务管理，从Quartz封装，到对外提供RESTful接口。实现了的定时任务的添加、暂停、恢复、查看、删除等功能。接下来我们在此基础上，继续对Quartz进行分装，实现基于CronTrigger的定时任务。

### 3.1 基于CronTrigger分装Quartz相关操作

#### 3.1.1 创建CronScheduleDTO.java实体类

与SimpleScheduleDTO一样需要继承ScheduleDTO类，代码如下：

```java
package com.example.quartz.dto;

/**
 * Created by shirukai on 2018/9/7
 */
public class CronScheduleDTO extends ScheduleDTO {
    private String cronExpression;

    public String getCronExpression() {
        return cronExpression;
    }

    public void setCronExpression(String cronExpression) {
        this.cronExpression = cronExpression;
    }
}
```

#### 3.1.2 构建CronTrigger

在ScheduleManager类里添加getCronTrigger方法，用于构建CronTrigger

```java
    private Trigger getCronTrigger(CronScheduleDTO csd) {
        CronScheduleBuilder scb = CronScheduleBuilder.cronSchedule(csd.getCronExpression());
        TriggerBuilder triggerBuilder = TriggerBuilder.newTrigger()
                .withIdentity(csd.getJobName(), csd.getGroup())
                .withSchedule(scb);
        if (csd.getStartTime() != 0) {
            triggerBuilder.startAt(new Date(csd.getStartTime()));
        } else {
            triggerBuilder.startNow();
        }
        if (csd.getEndTime() != 0) {
            triggerBuilder.endAt(new Date(csd.getEndTime()));
        }
        return triggerBuilder.build();
    }
```

#### 3.1.3 构建Cron Schedule Job

在ScheduleManager类里添加createCronJob方法

```java
/**
 * 创建 cron schedule job
 *
 * @param jobClass   可执行job class
 * @param csd        定时参数
 * @param jobDataMap 数据
 * @return Schedule
 */
public Schedule createCronJob(Class<? extends Job> jobClass, CronScheduleDTO csd, JobDataMap jobDataMap) {
    Trigger trigger = getCronTrigger(csd);
    return createJob(jobClass, csd, jobDataMap, trigger);
}
```

#### 3.1.4 更新Job

在ScheduleManager类里添加updateCronJob方法

```java
public Schedule updateCronJob(String scheduleId, CronScheduleDTO csd) {
    Schedule schedule = getSchedule(scheduleId);
    return updateCronJob(schedule, csd);
}

public Schedule updateCronJob(Schedule schedule, CronScheduleDTO csd) {
    try {
        String jobName = schedule.getJobName();
        String groupName = schedule.getGroupName();
        JobKey jobKey = new JobKey(jobName, groupName);
        JobDetail jobDetail = scheduler.getJobDetail(jobKey);
        //先删除
        scheduler.deleteJob(jobKey);
        //重新创建
        Trigger trigger = getCronTrigger(csd);
        scheduler.scheduleJob(jobDetail, trigger);
        //更新元数据
        schedule.setRecord(0);
        schedule.setTriggerInfo(JSON.toJSONString(csd));
        scheduleRepository.save(schedule);
    } catch (SchedulerException e) {
        log.error("Update cron schedule job error:{}", e.getMessage());
    }
    return schedule;
}
```

### 3.2 对外提供相关API

#### 3.3.1 修改ScheduleService

在ScheduleService类里添加cron相关的操作，主要是添加Cron定时任务和更新Cron定时任务，代码如下：

```java
    public Schedule setSchedule(String jobName, CronScheduleDTO csd) {
        csd.setJobName(jobName);
        csd.setGroup(GROUP);
        return scheduleManager.createCronJob(HelloJob.class, csd, null);
    }
    public Schedule modifySchedule(String jobName, CronScheduleDTO csd) {
        Schedule schedule = scheduleManager.getJobByNameAndGroup(jobName, GROUP);
        csd.setJobName(jobName);
        csd.setGroup(GROUP);
        return scheduleManager.updateCronJob(schedule, csd);
    }
```

#### 3.3.2 修改ScheduleController

同样在ScheduleController下添加cron相应的接口

```java
    @PostMapping(value = "/{jobName}/cron")
    public RestMessage schedule(
            @PathVariable("jobName") String jobName,
            @RequestBody CronScheduleDTO cronScheduleDTO
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.setSchedule(jobName, cronScheduleDTO));
    }

    @PutMapping(value = "/{jobName}/cron")
    public RestMessage modifySchedule(
            @PathVariable("jobName") String jobName,
            @RequestBody CronScheduleDTO cronScheduleDTO
    ) {
        return RestMessageUtil.objectToRestMessage(scheduleService.modifySchedule(jobName, cronScheduleDTO));
    }
```

#### 3.3.3 测试提供的API

##### 3.3.3.1 设置cron格式的定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/cron

请求类型：POST

请求参数：

```json
{
	"cronExpression":"0 0/5 * * * ? *"
}
```

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": {
        "id": "2d876e3e-f1e1-4ad7-bc64-5a107387cd3f",
        "triggerInfo": "{\"cronExpression\":\"0 0/5 * * * ? *\",\"endTime\":0,\"group\":\"TEST_GROUP\",\"jobName\":\"8aaabdfc659f74620165b2ad36b50030\",\"startTime\":0}",
        "status": "ACTIVATED",
        "groupName": "TEST_GROUP",
        "jobName": "8aaabdfc659f74620165b2ad36b50030",
        "record": 0,
        "createdTimestamp": "2018-09-07T07:32:40.238+0000"
    }
}
```

##### 3.3.3.2 更新cron格式的定时任务

请求API：{{hostIP}}/api/v1/schedule/8aaabdfc659f74620165b2ad36b50030/cron

请求类型：PUT

请求参数：

```json
{
	"cronExpression":"0/1 * * * * ? "
}
```

响应：

```json
{
    "success": true,
    "code": 0,
    "msg": "操作成功",
    "data": {
        "id": "2d876e3e-f1e1-4ad7-bc64-5a107387cd3f",
        "triggerInfo": "{\"cronExpression\":\"0/1 * * * * ? \",\"endTime\":0,\"group\":\"TEST_GROUP\",\"jobName\":\"8aaabdfc659f74620165b2ad36b50030\",\"startTime\":0}",
        "status": "ACTIVATED",
        "groupName": "TEST_GROUP",
        "jobName": "8aaabdfc659f74620165b2ad36b50030",
        "record": 0,
        "createdTimestamp": "2018-09-07T07:32:40.000+0000"
    }
}
```

![](http://shirukai.gitee.io/images/82d21c899ea25350cf85cf73d3fd25e8.gif)

## 4 Springboot整合Quartz进阶

### 4.1 自动初始化Quartz建表SQL

#### 4.1.1 使用Springboot的DataSource时，初始化Quartz建表SQL

使用springboot的DataSource初始化SQL我这里提供了两种方式，一种是基于配置的SQL初始化、另一种是基于编程的SQL初始化。下面将分别记录一下这两种初始化SQL的方式。

##### 4.1.1.1 基于配置的SQL初始化

基于配置的SQL初始化很简单，只需要在springboot中添加几个配置项即可。

首先列一下我们的初始化脚本：

```sql
CREATE TABLE IF NOT EXISTS QRTZ_JOB_DETAILS(
SCHED_NAME VARCHAR(120) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
JOB_CLASS_NAME VARCHAR(250) NOT NULL,
IS_DURABLE VARCHAR(1) NOT NULL,
IS_NONCONCURRENT VARCHAR(1) NOT NULL,
IS_UPDATE_DATA VARCHAR(1) NOT NULL,
REQUESTS_RECOVERY VARCHAR(1) NOT NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
NEXT_FIRE_TIME BIGINT(13) NULL,
PREV_FIRE_TIME BIGINT(13) NULL,
PRIORITY INTEGER NULL,
TRIGGER_STATE VARCHAR(16) NOT NULL,
TRIGGER_TYPE VARCHAR(8) NOT NULL,
START_TIME BIGINT(13) NOT NULL,
END_TIME BIGINT(13) NULL,
CALENDAR_NAME VARCHAR(200) NULL,
MISFIRE_INSTR SMALLINT(2) NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,JOB_NAME,JOB_GROUP)
REFERENCES QRTZ_JOB_DETAILS(SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_SIMPLE_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
REPEAT_COUNT BIGINT(7) NOT NULL,
REPEAT_INTERVAL BIGINT(12) NOT NULL,
TIMES_TRIGGERED BIGINT(10) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_CRON_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
CRON_EXPRESSION VARCHAR(120) NOT NULL,
TIME_ZONE_ID VARCHAR(80),
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_SIMPROP_TRIGGERS
  (          
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    STR_PROP_1 VARCHAR(512) NULL,
    STR_PROP_2 VARCHAR(512) NULL,
    STR_PROP_3 VARCHAR(512) NULL,
    INT_PROP_1 INT NULL,
    INT_PROP_2 INT NULL,
    LONG_PROP_1 BIGINT NULL,
    LONG_PROP_2 BIGINT NULL,
    DEC_PROP_1 NUMERIC(13,4) NULL,
    DEC_PROP_2 NUMERIC(13,4) NULL,
    BOOL_PROP_1 VARCHAR(1) NULL,
    BOOL_PROP_2 VARCHAR(1) NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP) 
    REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_BLOB_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
BLOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
INDEX (SCHED_NAME,TRIGGER_NAME, TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_CALENDARS (
SCHED_NAME VARCHAR(120) NOT NULL,
CALENDAR_NAME VARCHAR(200) NOT NULL,
CALENDAR BLOB NOT NULL,
PRIMARY KEY (SCHED_NAME,CALENDAR_NAME))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_PAUSED_TRIGGER_GRPS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_FIRED_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
ENTRY_ID VARCHAR(95) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
FIRED_TIME BIGINT(13) NOT NULL,
SCHED_TIME BIGINT(13) NOT NULL,
PRIORITY INTEGER NOT NULL,
STATE VARCHAR(16) NOT NULL,
JOB_NAME VARCHAR(200) NULL,
JOB_GROUP VARCHAR(200) NULL,
IS_NONCONCURRENT VARCHAR(1) NULL,
REQUESTS_RECOVERY VARCHAR(1) NULL,
PRIMARY KEY (SCHED_NAME,ENTRY_ID))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_SCHEDULER_STATE (
SCHED_NAME VARCHAR(120) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
LAST_CHECKIN_TIME BIGINT(13) NOT NULL,
CHECKIN_INTERVAL BIGINT(13) NOT NULL,
PRIMARY KEY (SCHED_NAME,INSTANCE_NAME))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS  QRTZ_LOCKS (
SCHED_NAME VARCHAR(120) NOT NULL,
LOCK_NAME VARCHAR(40) NOT NULL,
PRIMARY KEY (SCHED_NAME,LOCK_NAME))
ENGINE=InnoDB;
```

可以看出，我们的初始化脚本，是基于官网提供的建表脚本进行了改造。改造有两点：第一点是去掉原有的如果表存在则删除的脚本，改为如果表不存在则创建。第二点是去掉索引脚本，因为索引重复创建会报错。这个可以利用存储过程的方式去解决，后面会提到。下面将我们的初始化SQL的脚本配置到springboot的配置文件中。在application.yml配置文件中，添加如下内容：

```yaml
spring:
 #配置数据库
 datasource:
   driver-class-name: com.mysql.jdbc.Driver
   url: jdbc:mysql://localhost:3306/springboot?useSSL=false&characterEncoding=utf-8
   username: root
   password: hollysys
   schema-username: root
   schema-password: hollysys
   schema: classpath:quartz_tables.sql
   initialization-mode: always
```

这样的话，系统就会默认初始化我们的sql了。

注意：在springboot2.0之前不需要指定schema-username、schema-password、initialization-mode这三个属性就可以初始化sql，但是在2.0之后必须要设置这三个属性，否则spring.datasource.schema属性无法正常执行。

##### 补充配置带存储过程的SQL脚本：

带添加索引的SQL脚本：

```sql

CREATE TABLE IF NOT EXISTS  QRTZ_JOB_DETAILS (
SCHED_NAME VARCHAR(120) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
JOB_CLASS_NAME VARCHAR(250) NOT NULL,
IS_DURABLE VARCHAR(1) NOT NULL,
IS_NONCONCURRENT VARCHAR(1) NOT NULL,
IS_UPDATE_DATA VARCHAR(1) NOT NULL,
REQUESTS_RECOVERY VARCHAR(1) NOT NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
NEXT_FIRE_TIME BIGINT(13) NULL,
PREV_FIRE_TIME BIGINT(13) NULL,
PRIORITY INTEGER NULL,
TRIGGER_STATE VARCHAR(16) NOT NULL,
TRIGGER_TYPE VARCHAR(8) NOT NULL,
START_TIME BIGINT(13) NOT NULL,
END_TIME BIGINT(13) NULL,
CALENDAR_NAME VARCHAR(200) NULL,
MISFIRE_INSTR SMALLINT(2) NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,JOB_NAME,JOB_GROUP)
REFERENCES QRTZ_JOB_DETAILS(SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_SIMPLE_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
REPEAT_COUNT BIGINT(7) NOT NULL,
REPEAT_INTERVAL BIGINT(12) NOT NULL,
TIMES_TRIGGERED BIGINT(10) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_CRON_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
CRON_EXPRESSION VARCHAR(120) NOT NULL,
TIME_ZONE_ID VARCHAR(80),
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_SIMPROP_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    STR_PROP_1 VARCHAR(512) NULL,
    STR_PROP_2 VARCHAR(512) NULL,
    STR_PROP_3 VARCHAR(512) NULL,
    INT_PROP_1 INT NULL,
    INT_PROP_2 INT NULL,
    LONG_PROP_1 BIGINT NULL,
    LONG_PROP_2 BIGINT NULL,
    DEC_PROP_1 NUMERIC(13,4) NULL,
    DEC_PROP_2 NUMERIC(13,4) NULL,
    BOOL_PROP_1 VARCHAR(1) NULL,
    BOOL_PROP_2 VARCHAR(1) NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
    REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_BLOB_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
BLOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
INDEX (SCHED_NAME,TRIGGER_NAME, TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_CALENDARS (
SCHED_NAME VARCHAR(120) NOT NULL,
CALENDAR_NAME VARCHAR(200) NOT NULL,
CALENDAR BLOB NOT NULL,
PRIMARY KEY (SCHED_NAME,CALENDAR_NAME))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_PAUSED_TRIGGER_GRPS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_FIRED_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
ENTRY_ID VARCHAR(95) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
FIRED_TIME BIGINT(13) NOT NULL,
SCHED_TIME BIGINT(13) NOT NULL,
PRIORITY INTEGER NOT NULL,
STATE VARCHAR(16) NOT NULL,
JOB_NAME VARCHAR(200) NULL,
JOB_GROUP VARCHAR(200) NULL,
IS_NONCONCURRENT VARCHAR(1) NULL,
REQUESTS_RECOVERY VARCHAR(1) NULL,
PRIMARY KEY (SCHED_NAME,ENTRY_ID))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_SCHEDULER_STATE (
SCHED_NAME VARCHAR(120) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
LAST_CHECKIN_TIME BIGINT(13) NOT NULL,
CHECKIN_INTERVAL BIGINT(13) NOT NULL,
PRIMARY KEY (SCHED_NAME,INSTANCE_NAME))
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS QRTZ_LOCKS (
SCHED_NAME VARCHAR(120) NOT NULL,
LOCK_NAME VARCHAR(40) NOT NULL,
PRIMARY KEY (SCHED_NAME,LOCK_NAME))
ENGINE=InnoDB;


DROP PROCEDURE IF EXISTS schema_change;
CREATE PROCEDURE schema_change()
DELIMITER $$
BEGIN
DECLARE  CurrentDatabase VARCHAR(100);
SELECT DATABASE() INTO CurrentDatabase;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_JOB_DETAILS' AND index_name = 'IDX_QRTZ_J_REQ_RECOVERY') THEN
  CREATE INDEX IDX_QRTZ_J_REQ_RECOVERY ON QRTZ_JOB_DETAILS(SCHED_NAME,REQUESTS_RECOVERY);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_JOB_DETAILS' AND index_name = 'IDX_QRTZ_J_GRP') THEN
  CREATE INDEX IDX_QRTZ_J_GRP ON QRTZ_JOB_DETAILS(SCHED_NAME,JOB_GROUP);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_J') THEN
  CREATE INDEX IDX_QRTZ_T_J ON QRTZ_TRIGGERS(SCHED_NAME,JOB_NAME,JOB_GROUP);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_JG') THEN
  CREATE INDEX IDX_QRTZ_T_JG ON QRTZ_TRIGGERS(SCHED_NAME,JOB_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_C') THEN
  CREATE INDEX IDX_QRTZ_T_C ON QRTZ_TRIGGERS(SCHED_NAME,CALENDAR_NAME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_G') THEN
  CREATE INDEX IDX_QRTZ_T_G ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_STATE') THEN
  CREATE INDEX IDX_QRTZ_T_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_N_STATE') THEN
  CREATE INDEX IDX_QRTZ_T_N_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_N_G_STATE') THEN
  CREATE INDEX IDX_QRTZ_T_N_G_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_GROUP,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NEXT_FIRE_TIME') THEN
  CREATE INDEX IDX_QRTZ_T_NEXT_FIRE_TIME ON QRTZ_TRIGGERS(SCHED_NAME,NEXT_FIRE_TIME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_ST') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_ST ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_STATE,NEXT_FIRE_TIME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_MISFIRE') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_MISFIRE ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_ST_MISFIRE') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_ST_MISFIRE ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_ST_MISFIRE_GRP') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_ST_MISFIRE_GRP ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME,TRIGGER_GROUP,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_TRIG_INST_NAME') THEN
  CREATE INDEX IDX_QRTZ_FT_TRIG_INST_NAME ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,INSTANCE_NAME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_INST_JOB_REQ_RCVRY') THEN
  CREATE INDEX IDX_QRTZ_FT_INST_JOB_REQ_RCVRY ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,INSTANCE_NAME,REQUESTS_RECOVERY);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_J_G') THEN
  CREATE INDEX IDX_QRTZ_FT_J_G ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,JOB_NAME,JOB_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_JG') THEN
  CREATE INDEX IDX_QRTZ_FT_JG ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,JOB_GROUP);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_T_G') THEN
  CREATE INDEX IDX_QRTZ_FT_T_G ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_TG') THEN
  CREATE INDEX IDX_QRTZ_FT_TG ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,TRIGGER_GROUP);
END IF;

END $$
DELIMITER;
CALL schema_change();
```

刚才说到基于配置的初始化SQL脚本不能去执行存储过程，原因是，springboot默认的SQL分隔符为;，也就是说，当它读到脚本中的;时就会默认为这是一条可执行的语句，所以我们的存储过程就没有办法执行，就会报如下错误：

```
Caused by: com.mysql.jdbc.exceptions.jdbc4.MySQLSyntaxErrorException: You have an error in your SQL syntax; 
check the manual that corresponds to your MySQL server version for the right syntax to use near
'$$ BEGIN DECLARE CurrentDatabase VARCHAR(100)' at line 1
```

显然就是说我们的SQL语法有问题，实际上就是上面我所提到的问题导致的，那么如何解决呢，这里参考了网上一种解决方法就是修改springboot默认的SQL分隔符。这里我们修改分隔符为$$。在配置文件中添加：

```yaml
spirng.datasource.separator: $$
```

然后就是修改我们的SQL脚本，将原来的;改为;$$，存储过程中的;不变。

脚本如下所示：

```sql
CREATE TABLE IF NOT EXISTS  QRTZ_JOB_DETAILS (
SCHED_NAME VARCHAR(120) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
JOB_CLASS_NAME VARCHAR(250) NOT NULL,
IS_DURABLE VARCHAR(1) NOT NULL,
IS_NONCONCURRENT VARCHAR(1) NOT NULL,
IS_UPDATE_DATA VARCHAR(1) NOT NULL,
REQUESTS_RECOVERY VARCHAR(1) NOT NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
JOB_NAME VARCHAR(200) NOT NULL,
JOB_GROUP VARCHAR(200) NOT NULL,
DESCRIPTION VARCHAR(250) NULL,
NEXT_FIRE_TIME BIGINT(13) NULL,
PREV_FIRE_TIME BIGINT(13) NULL,
PRIORITY INTEGER NULL,
TRIGGER_STATE VARCHAR(16) NOT NULL,
TRIGGER_TYPE VARCHAR(8) NOT NULL,
START_TIME BIGINT(13) NOT NULL,
END_TIME BIGINT(13) NULL,
CALENDAR_NAME VARCHAR(200) NULL,
MISFIRE_INSTR SMALLINT(2) NULL,
JOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,JOB_NAME,JOB_GROUP)
REFERENCES QRTZ_JOB_DETAILS(SCHED_NAME,JOB_NAME,JOB_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_SIMPLE_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
REPEAT_COUNT BIGINT(7) NOT NULL,
REPEAT_INTERVAL BIGINT(12) NOT NULL,
TIMES_TRIGGERED BIGINT(10) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_CRON_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
CRON_EXPRESSION VARCHAR(120) NOT NULL,
TIME_ZONE_ID VARCHAR(80),
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_SIMPROP_TRIGGERS
  (
    SCHED_NAME VARCHAR(120) NOT NULL,
    TRIGGER_NAME VARCHAR(200) NOT NULL,
    TRIGGER_GROUP VARCHAR(200) NOT NULL,
    STR_PROP_1 VARCHAR(512) NULL,
    STR_PROP_2 VARCHAR(512) NULL,
    STR_PROP_3 VARCHAR(512) NULL,
    INT_PROP_1 INT NULL,
    INT_PROP_2 INT NULL,
    LONG_PROP_1 BIGINT NULL,
    LONG_PROP_2 BIGINT NULL,
    DEC_PROP_1 NUMERIC(13,4) NULL,
    DEC_PROP_2 NUMERIC(13,4) NULL,
    BOOL_PROP_1 VARCHAR(1) NULL,
    BOOL_PROP_2 VARCHAR(1) NULL,
    PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
    FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
    REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_BLOB_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
BLOB_DATA BLOB NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP),
INDEX (SCHED_NAME,TRIGGER_NAME, TRIGGER_GROUP),
FOREIGN KEY (SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP)
REFERENCES QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_CALENDARS (
SCHED_NAME VARCHAR(120) NOT NULL,
CALENDAR_NAME VARCHAR(200) NOT NULL,
CALENDAR BLOB NOT NULL,
PRIMARY KEY (SCHED_NAME,CALENDAR_NAME))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_PAUSED_TRIGGER_GRPS (
SCHED_NAME VARCHAR(120) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
PRIMARY KEY (SCHED_NAME,TRIGGER_GROUP))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_FIRED_TRIGGERS (
SCHED_NAME VARCHAR(120) NOT NULL,
ENTRY_ID VARCHAR(95) NOT NULL,
TRIGGER_NAME VARCHAR(200) NOT NULL,
TRIGGER_GROUP VARCHAR(200) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
FIRED_TIME BIGINT(13) NOT NULL,
SCHED_TIME BIGINT(13) NOT NULL,
PRIORITY INTEGER NOT NULL,
STATE VARCHAR(16) NOT NULL,
JOB_NAME VARCHAR(200) NULL,
JOB_GROUP VARCHAR(200) NULL,
IS_NONCONCURRENT VARCHAR(1) NULL,
REQUESTS_RECOVERY VARCHAR(1) NULL,
PRIMARY KEY (SCHED_NAME,ENTRY_ID))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_SCHEDULER_STATE (
SCHED_NAME VARCHAR(120) NOT NULL,
INSTANCE_NAME VARCHAR(200) NOT NULL,
LAST_CHECKIN_TIME BIGINT(13) NOT NULL,
CHECKIN_INTERVAL BIGINT(13) NOT NULL,
PRIMARY KEY (SCHED_NAME,INSTANCE_NAME))
ENGINE=InnoDB;$$

CREATE TABLE IF NOT EXISTS QRTZ_LOCKS (
SCHED_NAME VARCHAR(120) NOT NULL,
LOCK_NAME VARCHAR(40) NOT NULL,
PRIMARY KEY (SCHED_NAME,LOCK_NAME))
ENGINE=InnoDB;$$

DROP PROCEDURE IF EXISTS schema_change;$$
CREATE PROCEDURE schema_change()
BEGIN
DECLARE  CurrentDatabase VARCHAR(100);
SELECT DATABASE() INTO CurrentDatabase;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_JOB_DETAILS' AND index_name = 'IDX_QRTZ_J_REQ_RECOVERY') THEN
  CREATE INDEX IDX_QRTZ_J_REQ_RECOVERY ON QRTZ_JOB_DETAILS(SCHED_NAME,REQUESTS_RECOVERY);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_JOB_DETAILS' AND index_name = 'IDX_QRTZ_J_GRP') THEN
  CREATE INDEX IDX_QRTZ_J_GRP ON QRTZ_JOB_DETAILS(SCHED_NAME,JOB_GROUP);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_J') THEN
  CREATE INDEX IDX_QRTZ_T_J ON QRTZ_TRIGGERS(SCHED_NAME,JOB_NAME,JOB_GROUP);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_JG') THEN
  CREATE INDEX IDX_QRTZ_T_JG ON QRTZ_TRIGGERS(SCHED_NAME,JOB_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_C') THEN
  CREATE INDEX IDX_QRTZ_T_C ON QRTZ_TRIGGERS(SCHED_NAME,CALENDAR_NAME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_G') THEN
  CREATE INDEX IDX_QRTZ_T_G ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_STATE') THEN
  CREATE INDEX IDX_QRTZ_T_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_N_STATE') THEN
  CREATE INDEX IDX_QRTZ_T_N_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_N_G_STATE') THEN
  CREATE INDEX IDX_QRTZ_T_N_G_STATE ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_GROUP,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NEXT_FIRE_TIME') THEN
  CREATE INDEX IDX_QRTZ_T_NEXT_FIRE_TIME ON QRTZ_TRIGGERS(SCHED_NAME,NEXT_FIRE_TIME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_ST') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_ST ON QRTZ_TRIGGERS(SCHED_NAME,TRIGGER_STATE,NEXT_FIRE_TIME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_MISFIRE') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_MISFIRE ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_ST_MISFIRE') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_ST_MISFIRE ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_TRIGGERS' AND index_name = 'IDX_QRTZ_T_NFT_ST_MISFIRE_GRP') THEN
  CREATE INDEX IDX_QRTZ_T_NFT_ST_MISFIRE_GRP ON QRTZ_TRIGGERS(SCHED_NAME,MISFIRE_INSTR,NEXT_FIRE_TIME,TRIGGER_GROUP,TRIGGER_STATE);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_TRIG_INST_NAME') THEN
  CREATE INDEX IDX_QRTZ_FT_TRIG_INST_NAME ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,INSTANCE_NAME);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_INST_JOB_REQ_RCVRY') THEN
  CREATE INDEX IDX_QRTZ_FT_INST_JOB_REQ_RCVRY ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,INSTANCE_NAME,REQUESTS_RECOVERY);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_J_G') THEN
  CREATE INDEX IDX_QRTZ_FT_J_G ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,JOB_NAME,JOB_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_JG') THEN
  CREATE INDEX IDX_QRTZ_FT_JG ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,JOB_GROUP);
END IF;

IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_T_G') THEN
  CREATE INDEX IDX_QRTZ_FT_T_G ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,TRIGGER_NAME,TRIGGER_GROUP);
END IF;
IF NOT EXISTS (SELECT * FROM information_schema.statistics WHERE table_schema=CurrentDatabase AND table_name = 'QRTZ_FIRED_TRIGGERS' AND index_name = 'IDX_QRTZ_FT_TG') THEN
  CREATE INDEX IDX_QRTZ_FT_TG ON QRTZ_FIRED_TRIGGERS(SCHED_NAME,TRIGGER_GROUP);
END IF;

END $$
CALL schema_change();$$
```

如上修改完我们的SQL脚本之后，就可以在启动项目的时候自动初始化项目了 。

##### 4.1.1.2 基于编程的SQL初始化

基于编程的SQL初始化就是手动加载DataSource和SQL脚本，然后去执行脚本。因为我们之前将Quartz与Spring整合，需要将Scheduler以Bean的形式注入到IOC容器中，所以我们的初始化脚本要在这之前执行。这里我们将在之前的QuartzConfig类里添加相应修改。

注释掉之前的基于配置的SQL初始化配置

```yaml
#   schema-username: root
#   schema-password: hollysys
#   schema: classpath:quartz_tables.sql
#   initialization-mode: always
#   separator: $$
```

在QuartzConfig类里注入Springboot的DataSource

```java
    @Autowired
    DataSource dataSource;
```

在QuartzConfig类创建初始化数据库方法initDataBase()

```java
public void initDataBase(DataSource dataSource) {
        log.info("============== init quartz database started ==============");
        try {
            //加载SQL
            ClassPathResource recordsSys = new ClassPathResource("quartz_tables.sql");
            //使用DataSourceInitializer初始化
            DataSourceInitializer dsi = new DataSourceInitializer();
            dsi.setDataSource(dataSource);
            dsi.setDatabasePopulator(new ResourceDatabasePopulator(true, true, "utf-8", recordsSys));
            dsi.setEnabled(true);
            dsi.afterPropertiesSet();
            log.info("============== init quartz database succeed ==============");
        } catch (Exception e) {
            log.error("init quartz database failed:{}", e.getMessage());
        }
    }
```

在创建SchedulerFactoryBean的时候，去初始化数据库

```java
    @Bean
    public SchedulerFactoryBean schedulerFactoryBean() throws IOException {
        //初始化数据库
        initDataBase(dataSource);
        SchedulerFactoryBean schedulerFactoryBean = new SchedulerFactoryBean();
        schedulerFactoryBean.setOverwriteExistingJobs(true);
        schedulerFactoryBean.setQuartzProperties(quartzProperties());
        schedulerFactoryBean.setJobFactory(jobFactory);
        return schedulerFactoryBean;
    }
```

这样我们就完成基于编程的SQL初始化。

#### 4.1.2 使用Quartz自定义DataSource时，初始化Quartz建表SQL

上面我们介绍了两种方式实现使用Springboot的DataSource去初始化Quartz的建表SQL。这里我们来讲一下，使用自定义的DataSource该如何初始化呢？其实原理与上面的基于编程的方式一样，只不过不能通过注解的方式注入DataSource，而是需要我们手动创建DataSource，然后传入上面编写的initDataBase(）方法。

首先在quartz.properties配置文件中开启我们的数据库相关配置

```
#存储方式使用JobStoreTX，也就是数据库
org.quartz.jobStore.class:org.quartz.impl.jdbcjobstore.JobStoreTX
org.quartz.jobStore.driverDelegateClass:org.quartz.impl.jdbcjobstore.StdJDBCDelegate
#是否使用集群（如果项目只部署到 一台服务器，就不用了）
org.quartz.jobStore.isClustered = false
org.quartz.jobStore.clusterCheckinInterval=20000
org.quartz.jobStore.tablePrefix = QRTZ_
org.quartz.jobStore.dataSource = myDS

#配置数据源
#数据库中quartz表的表名前缀
org.quartz.dataSource.myDS.driver = com.mysql.jdbc.Driver
org.quartz.dataSource.myDS.URL = jdbc:mysql://localhost:3306/springboot?characterEncoding=utf-8&useSSL=false
org.quartz.dataSource.myDS.user = root
org.quartz.dataSource.myDS.password = hollysys
org.quartz.dataSource.myDS.maxConnections = 5
```

在QuartzConfig类里添加创建DataSource的方法 quartzSource()如下所示：

```java
    @Bean
    public DataSource quartzSource() throws IOException {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        Properties properties = quartzProperties();
        dataSource.setDriverClassName(properties.getProperty("org.quartz.dataSource.myDS.driver"));
        dataSource.setUrl(properties.getProperty("org.quartz.dataSource.myDS.URL"));
        dataSource.setUsername(properties.getProperty("org.quartz.dataSource.myDS.user"));
        dataSource.setPassword(properties.getProperty("org.quartz.dataSource.myDS.password"));
        return dataSource;
    }
```

然后同样在创建SchedulerFactoryBean的时候，去初始化数据库

```java
    @Bean
    public SchedulerFactoryBean schedulerFactoryBean() throws IOException {
        //初始化数据库,这时候DataSource就要使用上面的quartzSource()方法创建了
        initDataBase(quartzSource());
        SchedulerFactoryBean schedulerFactoryBean = new SchedulerFactoryBean();
        schedulerFactoryBean.setOverwriteExistingJobs(true);
        schedulerFactoryBean.setQuartzProperties(quartzProperties());
        schedulerFactoryBean.setJobFactory(jobFactory);
        return schedulerFactoryBean;
    }
```

这样我们就可以实现基于自定义DataSource的SQL初始化。

### 4.2 关于实现多租户的几点思路

#### 4.2.1 租户独享服务模式的实现

这里所说的租户独享服务包含两种情景：一种是一个租户对应一个服务，另一种是一个租户对应多个服务(服务集群）即一个租户对应一个集群。这两种场景的实现方式都可以用一种方案解决。我的思路是使用Scheduler容器来区分租户，即一个租户对应一个Scheduler容器或一个Scheduler容器集群。该租户的Scheduler容器，只会管理在该Scheduler实例中创建的定时任务。生产中，我们的租户以服务作为隔离级别，租户各自有自己的服务。Quartz集群以Scheduler容器作为隔离级别，租户各自的定时任务在自己的Scheduler容器和Scheduler集群里执行。

那么如何通过Scheduler去做租户隔离呢？其实很简单，只需要在创建SchedulerFactoryBean的时候，指定一下SchedulerName即可，这个地方我们用租户ID来做SchedulerName，从而实现基于Scheduler容器的多租户。

```java
    @Bean
    public SchedulerFactoryBean schedulerFactoryBean() throws IOException {
        //初始化数据库
        initDataBase(dataSource);
        SchedulerFactoryBean schedulerFactoryBean = new SchedulerFactoryBean();
        schedulerFactoryBean.setOverwriteExistingJobs(true);
        schedulerFactoryBean.setQuartzProperties(quartzProperties());
        schedulerFactoryBean.setJobFactory(jobFactory);
        //通过租户ID来设置SchedulerName从而实现多租户
        schedulerFactoryBean.setSchedulerName(tenant_id);
        return schedulerFactoryBean;
    }
```

这样我们租户下的服务只会执行自己租户ID对应的Scheduler容器中的定时任务。

#### 4.2.1 租户共享服务模式的实现

租户共享服务模式是指一个服务对应多个租户，或者一个服务集群对应多个租户。这样的服务模式原本隔离性就很差。这样的多租户实现，可以使用JobGroup来进行隔离。使用同一个Scheduler容器或者一个Scheduler集群来共同调度所有的定时任务，只不过是通过JobGroup来区分，哪个定时任务对应哪个租户。这时候我们就可以使用租户ID来作为group名就能实现。具体实现，根据自己的业务场景定制，这里不做演示。

## 5 总结

至此，已经完成了所有Springboot整合Quartz实现定时任务调度管理的内容。项目的实现我也是从0到1，从接触Quartz调度框架到整合到自己的项目中，其中一些思路来自于强大的网络，另一些是自己不成熟的见解。希望记录整合过程，对以后开发有所帮助。

