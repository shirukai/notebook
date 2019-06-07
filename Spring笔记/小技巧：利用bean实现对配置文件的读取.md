首先扫描配置文件：

```
<context:property-placeholder location="classpath:redis.properties" ignore-unresolvable="true"/>
```

然后创建bean

```
<bean id="config" class="com.mavenssmlr.entity.Config">
    <constructor-arg name="value1" value="${redis.host}"/>
    <constructor-arg name="value2" value="${redis.maxWaitMillis}"/>
</bean>
```

在com/mavenssmlr/entiry下创建名字为Config的java类

```
package com.mavenssmlr.entity;

/**
 * Created by shirukai on 2017/10/19.
 *
 */
public class Config {
    public Config(String value1,String value2){
        this.rag1 = value1;
        this.rag2 = value2;
    }
    private String rag1;
    private String rag2;


    public String getRag1() {
        return rag1;
    }

    public void setRag1(String rag1) {
        this.rag1 = rag1;
    }

    public String getRag2() {
        return rag2;
    }

    public void setRag2(String rag2) {
        this.rag2 = rag2;
    }

    @Override
    public String toString() {
        return "Config{" +
                "rag1='" + rag1 + '\'' +
                ", rag2='" + rag2 + '\'' +
                '}';
    }
}
```

调用：

```
@Autowired
private Config config;
Map<String,Object> map = new HashMap<String, Object>();
map.put("config",config);
logger.info("________________________________________test={}",map);
```