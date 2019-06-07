# Springboot异步任务执行及监控

除了自己实现线程外，springboot本身就提供了通过注解的方式，进行异步任务的执行。下面主要记录一下，在Springboot项目中实现异步任务，以及对异步任务进行封装监控。

## 1 开启异步支持

想要使用springboot的注解进行异步任务，首先要开启springboot的异步任务支持。通过集成AsyncConfigurer接口，并实现getAsyncExcutor()方法，如下所示：

```
package com.springboot.demo.asyncTask.conf;

import org.springframework.aop.interceptor.AsyncUncaughtExceptionHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

/**
 * Created by shirukai on 2018/7/30
 * 配置spring boot 多线程支持
 */
@Configuration
@EnableAsync   //开启异步任务支持
public class SpringTaskExecutor implements AsyncConfigurer {

    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor taskExecutor = new ThreadPoolTaskExecutor();
        taskExecutor.setCorePoolSize(5);
        taskExecutor.setMaxPoolSize(10);
        taskExecutor.setQueueCapacity(20);
        taskExecutor.initialize();
        return taskExecutor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return null;
    }
}
```
通过上面方法，就可以实现Spring boot的异步任务支持。然后只需要在想要进行异步的方法前添加@Async注解就可以了，如下图所示：

```
package com.springboot.demo.asyncTask.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

/**
 * Created by shirukai on 2018/7/31
 * 异步任务执行器
 */
@Component
public class AsyncTaskExecutor {
    private static Logger LOG = LoggerFactory.getLogger(AsyncTaskExecutor.class);
    @Async
    public void executor(AsyncTaskConstructor asyncTaskGenerator, String taskInfo) {
        LOG.info("AsyncTaskExecutor is executing async task:{}", taskInfo);
        asyncTaskGenerator.async();
    }
}
```

## 2 异步任务封装监控

### 2.1 封装思路

提供一个异步任务的管理器，管理器可以实现异步任务的提交、保存任务信息、获取任务信息等功能。

提供一个异步任务的监控器，用于监控异步任务执行状况，并把执行信息保存到缓存中，并记录任务执行时间。

提供一个异步任务的构造器，用于构造异步方法。

提供一个异步任务的执行器，用于执行管理器提交的使用构造器构造的异步方法。

### 2.2 效果展示

#### 2.2.1 启动异步任务

![](http://shirukai.gitee.io/images/2d96394ea6ee4b051074be33275f9205.jpg)

#### 2.2.2 查看任务状态

![](http://shirukai.gitee.io/images/432bd3f012c5c58177ae1753054f597d.jpg)

### 2.3  编码实现

#### 2.3.1 conf包

主要是配置springboot的线程池，开启spring boot支持异步支持

##### 2.3.1.1 SpringTaskExcutor.java

```
package com.emcc.hiacloud.analytics.asynctask.conf;

import org.springframework.aop.interceptor.AsyncUncaughtExceptionHandler;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

/**
 * Created by shirukai on 2018/7/30
 * 配置spring boot 多线程支持
 */
@Configuration
@EnableAsync   //开启异步任务支持
public class SpringTaskExecutor implements AsyncConfigurer {
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor taskExecutor = new ThreadPoolTaskExecutor();
        taskExecutor.setCorePoolSize(5);
        taskExecutor.setMaxPoolSize(10);
        taskExecutor.setQueueCapacity(20);
        taskExecutor.initialize();
        return taskExecutor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return null;
    }
}
```

#### 2.3.2 entity包

主要存放TaskInfo实例类用于保存任务信息，TaskStatusEnmu枚举类用来存放任务状态。

##### 2.3.2.1 TaskInfo.java

```
package com.emcc.hiacloud.analytics.asynctask.entity;


import java.util.Date;

/**
 * Created by shirukai on 2018/7/31
 * 任务信息
 */
public class TaskInfo {
    private String taskId;
    private TaskStatusEnum status;
    private Date startTime;
    private Date endTime;
    private String totalTime;

    public TaskStatusEnum getStatus() {
        return status;
    }

    public void setStatus(TaskStatusEnum status) {
        this.status = status;
    }

    public void setTotalTime(String totalTime) {
        this.totalTime = totalTime;
    }

    public String getTaskId() {
        return taskId;
    }

    public void setTaskId(String taskId) {
        this.taskId = taskId;
    }

    public Date getStartTime() {
        return startTime;
    }

    public void setStartTime(Date startTime) {
        this.startTime = startTime;
    }

    public Date getEndTime() {
        return endTime;
    }

    public void setEndTime(Date endTime) {
        this.endTime = endTime;
    }

    public String getTotalTime() {
        return totalTime;
    }

    public void setTotalTime() {
        this.totalTime = (this.endTime.getTime() - this.startTime.getTime()) + "ms";
    }
}
```

##### 2.3.2.2  TaskStatusEnum.java

```
package com.emcc.hiacloud.analytics.asynctask.entity;

/**
 * Created by shirukai on 2018/7/31
 * 任务状态枚举
 */
public enum TaskStatusEnum {

    STARTED(1, "任务已经启动"),
    RUNNING(0, "任务正在运行"),
    SUCCESS(2, "任务执行成功"),
    FAILED(-2, "任务执行失败");
    private int state;
    private String stateInfo;

    TaskStatusEnum(int state, String stateInfo) {
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
#### 2.3.3 manager包

存放要不任务的管理类和监控类

##### 2.3.3.1 AsyncTaskManager.java

```
package com.emcc.hiacloud.analytics.asynctask.manager;


import com.emcc.hiacloud.analytics.asynctask.entity.TaskInfo;
import com.emcc.hiacloud.analytics.asynctask.entity.TaskStatusEnum;
import com.emcc.hiacloud.analytics.asynctask.service.AsyncTaskConstructor;
import com.emcc.hiacloud.analytics.asynctask.service.AsyncTaskExecutor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Created by shirukai on 2018/7/31
 * 异步任务管理器
 */
@Component
public class AsyncTaskManager {
    private Map<String, TaskInfo> taskContainer = new HashMap<>(16);
    @Autowired
    AsyncTaskExecutor asyncTaskExecutor;


    /**
     * 初始化任务
     *
     * @return taskInfo
     */
    public TaskInfo initTask() {
        TaskInfo taskInfo = new TaskInfo();
        taskInfo.setTaskId(getTaskId());
        taskInfo.setStatus(TaskStatusEnum.STARTED);
        taskInfo.setStartTime(new Date());
        setTaskInfo(taskInfo);
        return taskInfo;
    }

    /**
     * 初始化任务
     * @param asyncTaskConstructor 异步任务构造器
     * @return taskInfo
     */
    public TaskInfo submit(AsyncTaskConstructor asyncTaskConstructor) {
        TaskInfo info = initTask();
        String taskId = info.getTaskId();
        asyncTaskExecutor.executor(asyncTaskConstructor,taskId);
        return info;
    }

    /**
     * 保存任务信息
     *
     * @param taskInfo 任务信息
     */
    public void setTaskInfo(TaskInfo taskInfo) {
        taskContainer.put(taskInfo.getTaskId(), taskInfo);
    }

    /**
     * 获取任务信息
     *
     * @param taskId 任务ID
     * @return
     */
    public TaskInfo getTaskInfo(String taskId) {
        return taskContainer.get(taskId);
    }

    /**
     * 获取任务状态
     *
     * @param taskId 任务ID
     * @return
     */
    public TaskStatusEnum getTaskStatus(String taskId) {
        return getTaskInfo(taskId).getStatus();
    }

    /**
     * 生成任务ID
     *
     * @return taskId
     */
    public String getTaskId() {
        return UUID.randomUUID().toString();
    }
}
```

##### 2.3.3.2 AsyncTaskMonitor.java

异步任务的监控主要是利用了spring的AOP面向切面，在异步方法的执行前和执行后进行监控，判断任务状态，并记录任务信息。

```
package com.emcc.hiacloud.analytics.asynctask.manager;


import com.emcc.hiacloud.analytics.asynctask.entity.TaskInfo;
import com.emcc.hiacloud.analytics.asynctask.entity.TaskStatusEnum;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Date;

/**
 * Created by shirukai on 2018/7/31
 * 异步任务监控
 */
@Component
@Aspect
public class AsyncTaskMonitor {
    @Autowired
    AsyncTaskManager manager;
    private static Logger LOG = LoggerFactory.getLogger(AsyncTaskMonitor.class);

    @Around("execution(* com.emcc.hiacloud.analytics.asynctask.service.AsyncTaskExecutor.*(..))")
    public void taskHandle(ProceedingJoinPoint pjp) {
        //获取taskId
        String taskId = pjp.getArgs()[1].toString();
        //获取任务信息
        TaskInfo taskInfo = manager.getTaskInfo(taskId);
        LOG.info("AsyncTaskMonitor is monitoring async task:{}", taskId);
        taskInfo.setStatus(TaskStatusEnum.RUNNING);
        manager.setTaskInfo(taskInfo);
        TaskStatusEnum status = null;
        try {
            pjp.proceed();
            status = TaskStatusEnum.SUCCESS;
        } catch (Throwable throwable) {
            status = TaskStatusEnum.FAILED;
            LOG.error("AsyncTaskMonitor:async task {} is failed.Error info:{}", taskId, throwable.getMessage());
        }
        taskInfo.setEndTime(new Date());
        taskInfo.setStatus(status);
        taskInfo.setTotalTime();
        manager.setTaskInfo(taskInfo);
    }
}
```

#### 2.3.4 service包

主要存放异步任务的方法构造器和执行器。

##### 2.3.4.1 AsyncTaskConstructor

通过该接口可以构建想要实现的异步方法。只要new 一下接口实例，然后重写李曼的async()方法即可。

```
package com.emcc.hiacloud.analytics.asynctask.service;

/**
 * Created by shirukai on 2018/7/31
 * 异步任务构造器
 */
public interface AsyncTaskConstructor {
    public void async();
}
```

##### 2.3.4.2 AsyncTaskExecutor.java

异步任务执行器

```
package com.emcc.hiacloud.analytics.asynctask.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

/**
 * Created by shirukai on 2018/7/31
 * 异步任务执行器
 */
@Component
public class AsyncTaskExecutor {
    private static Logger LOG = LoggerFactory.getLogger(AsyncTaskExecutor.class);
    @Async
    public void executor(AsyncTaskConstructor asyncTaskGenerator, String taskInfo) {
        LOG.info("AsyncTaskExecutor is executing async task:{}", taskInfo);
        asyncTaskGenerator.async();
    }
}

```

## 3 应用

实现两个接口，一个是开启一个异步任务，另一个是查看任务状态。

想要使用我们刚才分装好的异步任务，只需要将AsyncTaskManager注入到程序中。

```
package com.emcc.hiacloud.analytics.orchestrations.controller;

import com.emcc.hiacloud.analytics.asynctask.entity.TaskInfo;
import com.emcc.hiacloud.analytics.asynctask.manager.AsyncTaskManager;
import com.emcc.hiacloud.analytics.common.rest.RestMessage;
import com.emcc.hiacloud.analytics.common.util.RestMessageUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by shirukai on 2018/7/31
 */
@RestController
@RequestMapping(value = "/api/v1/asynctask")
public class AsyncTaskController {
	//注入异步任务管理器
    @Autowired
    AsyncTaskManager asyncTaskManager;

    @RequestMapping(value = "/startTask", method = RequestMethod.GET)
    public RestMessage startAsyncTask() {
        //调用任务管理器中的submit去提交一个异步任务
        TaskInfo taskInfo = asyncTaskManager.submit(() -> {
            System.out.println("__________");
            try {
                //模拟异步，睡眠6秒
                Thread.sleep(30000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("__________");
        });
        return RestMessageUtil.objectToRestMessage(taskInfo);
    }

    @RequestMapping(value = "/getTaskStatus", method = RequestMethod.GET)
    public RestMessage getTaskStatus(
            @RequestParam("taskId") String taskId) {
        return RestMessageUtil.objectToRestMessage(asyncTaskManager.getTaskInfo(taskId));
    }
}

```





