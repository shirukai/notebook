# spring项目整合redis

之前利用xml配置过spring-data-redis，但是在实际的项目中，兼容性不是很好。先在看一个实际项目中整合redis的案例。

### 1 首先pom.xml引入依赖

```
        <!--redis客户端 jedis-->
        <dependency>
            <groupId>redis.clients</groupId>
            <artifactId>jedis</artifactId>
            <version>2.8.1</version>
        </dependency>
        <!--spring-data-redis jedis-->
        <dependency>
            <groupId>org.springframework.data</groupId>
            <artifactId>spring-data-redis</artifactId>
            <version>1.6.4.RELEASE</version>
        </dependency>
        <!--json、javabean、xml转换-->
        <dependency>
            <groupId>de.odysseus.staxon</groupId>
            <artifactId>staxon</artifactId>
            <version>1.3</version>
        </dependency>
```

### 2 在resources包下创建配置文件

config.properties

```
#是否使用redis(true或false)
system.redis.isUseRedis=true

#redis模式(哨兵模式:sentinel;单机模式:standalone)
system.redis.mode=standalone

#spring cache集成模式(redisCache或ehcache)
system.cache.mode=redisCache

#缓存选择redis时的超时时间(单位:秒)
system.cache.redis.timeout=3000

```

redis.properties

```
#redis standalone配置
redis.host=10.110.13.243
redis.port=6379
redis.password=shirukai

#redis sentinel配置

#redis 连接池配置
#最大连接数(默认:8)
redis.pool.maxTotal=600
#最大空闲数(默认:8)
redis.pool.maxIdle=300
#当连接池资源耗尽时,调用者最大阻塞时间,超时将抛出异常.单位:毫秒,默认:-1,表示永不超时.
redis.pool.maxWaitMillis=1000
#指明是否在从池中取出连接前进行检验,如果检验失败,则从池中去除连接并尝试取出另一个 (默认:false)
redis.pool.testOnBorrow=true
```

### 3 创建包目录

在controller、dao层的同级目录下，创建redis包。

在redis包下创建

entity包

redisDao包

util包

目录结构如图

![](https://shirukai.gitee.io/images/201712021455_193.png)

### 4 创建包扫描自动创建bean

在spring的配置文件中添加包扫描 (如果项目中之前在这个目录下创建过包扫描，则不需要再次设置，否则会报错。)

loushagn框架已经扫描，所以无需添加

```
<context:component-scan base-package="kb.redis.redisDao" />
```



### 5 创建SpringContexHolder上下文类

默认loushang已经创建

```
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package org.loushang.framework.util;

import org.loushang.framework.i18n.MessageSourceExt;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;

public class SpringContextHolder implements ApplicationContextAware, DisposableBean {
    private static ApplicationContext applicationContext = null;
    private static Logger logger = LoggerFactory.getLogger(SpringContextHolder.class);

    public SpringContextHolder() {
    }

    public static ApplicationContext getApplicationContext() {
        assertContextInjected();
        return applicationContext;
    }

    public static <T> T getBean(String name) {
        assertContextInjected();
        return applicationContext.getBean(name);
    }

    public static void clearHolder() {
        applicationContext = null;
    }

    public void setApplicationContext(ApplicationContext applicationContext) {
        if (applicationContext != null) {
            logger.warn(MessageSourceExt.getLocaleMessage("framework.util.034", "SpringContextHolder中的ApplicationContext被覆盖, 原有ApplicationContext为:") + applicationContext);
        }

        applicationContext = applicationContext;
    }

    public void destroy() throws Exception {
        clearHolder();
    }

    private static void assertContextInjected() {
        if (applicationContext == null) {
            logger.error(MessageSourceExt.getLocaleMessage("framework.util.035", "applicaitonContext属性未注入, 请在WEB-INF/spring/spring-context.xml中定义SpringContextHolder."));
            throw new RuntimeException(MessageSourceExt.getLocaleMessage("framework.util.035", "applicaitonContext属性未注入, 请在WEB-INF/spring/spring-context.xml中定义SpringContextHolder."));
        }
    }
}
```

### 6 配置SpringContexHolder

楼上配置文件中默认已经启用

```
     <!-- spring上下文工具 -->                
    <bean class="org.loushang.framework.util.SpringContextHolder" lazy-init="false" />
```

非loushang的话可以自己在spring配置文件中，配置bean。创建一个类，然后选择类路径即可。

### 7 创建redis工具类

#### 7.1 在redis/utils包下创建

##### 7.1.1 JsonInput类

JsonInput.java

```
package kb.redis.util;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

/**
 * json输入对象
 */
public class JsonInput implements Serializable {
	private static final long serialVersionUID = 6479304251080435277L;

	private String appKey;
	private String secretKey;
	private String appType;
	private String signatureInfo;
	private String timeStamp;
	private String tranSeq;
	private String tranId;
	private int queueId;
	private List<Map<String, Object>> body;

	public JsonInput() {

	}

	public JsonInput(String appKey, String secretKey, String appType, String signatureInfo, String timeStamp,
			String tranSeq, String tranId, int queueId, List<Map<String, Object>> body) {
		super();
		this.appKey = appKey;
		this.secretKey = secretKey;
		this.appType = appType;
		this.signatureInfo = signatureInfo;
		this.timeStamp = timeStamp;
		this.tranSeq = tranSeq;
		this.tranId = tranId;
		this.queueId = queueId;
		this.body = body;
	}

	public String getAppKey() {
		return appKey;
	}

	public void setAppKey(String appKey) {
		this.appKey = appKey;
	}

	public String getSecretKey() {
		return secretKey;
	}

	public void setSecretKey(String secretKey) {
		this.secretKey = secretKey;
	}

	public String getAppType() {
		return appType;
	}

	public void setAppType(String appType) {
		this.appType = appType;
	}

	public String getSignatureInfo() {
		return signatureInfo;
	}

	public void setSignatureInfo(String signatureInfo) {
		this.signatureInfo = signatureInfo;
	}

	public String getTimeStamp() {
		return timeStamp;
	}

	public void setTimeStamp(String timeStamp) {
		this.timeStamp = timeStamp;
	}

	public String getTranSeq() {
		return tranSeq;
	}

	public void setTranSeq(String tranSeq) {
		this.tranSeq = tranSeq;
	}

	public List<Map<String, Object>> getBody() {
		return body;
	}

	public void setBody(List<Map<String, Object>> body) {
		this.body = body;
	}

	public String test(String json) {

		return json;
	}

	public String getTranId() {
		return tranId;
	}

	public void setTranId(String tranId) {
		this.tranId = tranId;
	}

	public int getQueueId() {
		return queueId;
	}

	public void setQueueId(int queueId) {
		this.queueId = queueId;
	}

}

```

##### 7.1.2 JsonOutput类

JsonOutput.java

```
package kb.redis.util;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * json输出对象
 */
public class JsonOutput implements Serializable {
   private static final long serialVersionUID = -8836237657941280022L;

   private String timeStamp;
   private String tranSeq;
   private String tranId;

   private String rtnCode;
   private String code;
   private String message;
   private String signatureInfo;
   private List<Map<String, Object>> body;

   public JsonOutput() {

   }

   public JsonOutput(String rtnCode, String code, String message) {
      super();
      this.rtnCode = rtnCode;
      this.code = code;
      this.message = message;
      this.timeStamp = "";
      this.tranSeq = "";
      this.tranId = "";
      this.signatureInfo = "";
      this.body = new ArrayList<Map<String, Object>>();
   }

   public JsonOutput(String timeStamp, String tranSeq, String tranId, String rtnCode, String code, String message,
         String signatureInfo, List<Map<String, Object>> body) {
      super();
      this.timeStamp = timeStamp;
      this.tranSeq = tranSeq;
      this.tranId = tranId;
      this.rtnCode = rtnCode;
      this.code = code;
      this.message = message;
      this.signatureInfo = signatureInfo;
      this.body = body;
   }

   public String getTimeStamp() {
      return timeStamp;
   }

   public void setTimeStamp(String timeStamp) {
      this.timeStamp = timeStamp;
   }

   public String getTranSeq() {
      return tranSeq;
   }

   public void setTranSeq(String tranSeq) {
      this.tranSeq = tranSeq;
   }

   public String getRtnCode() {
      return rtnCode;
   }

   public void setRtnCode(String rtnCode) {
      this.rtnCode = rtnCode;
   }

   public String getCode() {
      return code;
   }

   public void setCode(String code) {
      this.code = code;
   }

   public String getMessage() {
      return message;
   }

   public void setMessage(String message) {
      this.message = message;
   }

   public List<Map<String, Object>> getBody() {
      return body;
   }

   public void setBody(List<Map<String, Object>> body) {
      this.body = body;
   }

   public String getTranId() {
      return tranId;
   }

   public void setTranId(String tranId) {
      this.tranId = tranId;
   }

   public String getSignatureInfo() {
      return signatureInfo;
   }

   public void setSignatureInfo(String signatureInfo) {
      this.signatureInfo = signatureInfo;
   }

}
```



##### 7.1.3  JsonUtil类

JsonUtil.java

```
package kb.redis.util;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.odysseus.staxon.json.JsonXMLConfig;
import de.odysseus.staxon.json.JsonXMLConfigBuilder;
import de.odysseus.staxon.json.JsonXMLInputFactory;
import de.odysseus.staxon.json.JsonXMLOutputFactory;
import de.odysseus.staxon.xml.util.PrettyXMLEventWriter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLEventWriter;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLOutputFactory;
import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.Map;

/**
 * json工具类
 */
public final class JsonUtil {

    private JsonUtil() {
    }

    private static final Logger LOG = LoggerFactory.getLogger(JsonUtil.class);

    /**
     * object转换为json字符串
     *
     * @param object 要转换的对象
     * @return 转换后的json字符串
     */
    public static String objectToJsonStr(Object object) {
        ObjectMapper om = new ObjectMapper();
        try {
            return om.writeValueAsString(object);
        } catch (JsonProcessingException e) {
            LOG.error(e.getMessage());
            return null;
        }
    }

    /**
     * json字符串转换为指定类型的对象
     *
     * @param <T>       Type Java类
     * @param jsonStr   要转换的json字符串
     * @param valueType 指定的对象类型
     * @return 转换后的对象
     */
    public static <T> T jsonStrToObject(String jsonStr, Class<T> valueType) {
        ObjectMapper om = new ObjectMapper();
        try {
            return om.readValue(jsonStr, valueType);
        } catch (JsonParseException e) {
            LOG.error(e.getMessage());
            return null;
        } catch (JsonMappingException e) {
            LOG.error(e.getMessage());
            return null;
        } catch (IOException e) {
            LOG.error(e.getMessage());
            return null;
        } catch (NullPointerException e) {
            LOG.error(e.getMessage());
            return null;
        }
    }

    /**
     * 将xml字符串转换为json字符串
     *
     * @param xmlStr 要转换的xml字符串
     * @return 转换后的json字符串
     */
    public static String xmlStrToJsonStr(String xmlStr) {
        StringReader input = new StringReader(xmlStr);
        StringWriter output = new StringWriter();
        JsonXMLConfig config = new JsonXMLConfigBuilder().autoArray(true).autoPrimitive(true).prettyPrint(true).build();
        try {
            XMLEventReader reader = XMLInputFactory.newInstance().createXMLEventReader(input);
            XMLEventWriter writer = new JsonXMLOutputFactory(config).createXMLEventWriter(output);
            writer.add(reader);
            reader.close();
            writer.close();
        } catch (Exception e) {
            LOG.error(e.getMessage());
        } finally {
            try {
                output.close();
                input.close();
            } catch (IOException e) {
                LOG.error(e.getMessage());
            }
        }
        return output.toString();
    }

    /**
     * 将json字符串转换为xml字符串
     *
     * @param jsonStr 要转换的json字符串
     * @return 转换后的xml字符串
     */
    public static String jsonStrToXmlStr(String jsonStr) {
        StringReader input = new StringReader(jsonStr);
        StringWriter output = new StringWriter();
        JsonXMLConfig config = new JsonXMLConfigBuilder().multiplePI(false).repairingNamespaces(false).build();
        try {
            XMLEventReader reader = new JsonXMLInputFactory(config).createXMLEventReader(input);
            XMLEventWriter writer = XMLOutputFactory.newInstance().createXMLEventWriter(output);
            writer = new PrettyXMLEventWriter(writer);
            writer.add(reader);
            reader.close();
            writer.close();
        } catch (Exception e) {
            LOG.error(e.getMessage());
        } finally {
            try {
                output.close();
                input.close();
            } catch (IOException e) {
                LOG.error(e.getMessage());
            }
        }
        /**
         * remove <?xml version='1.0'?> return output.toString().substring(22);
         */
        return output.toString();
    }

    /**
     * JsonInput对象完整性校验
     *
     * @param jsonInput 要检验的JsonInput对象
     * @return JsonOutput
     */
    public static JsonOutput validateJson(JsonInput jsonInput) {
        String rtnCode = "3";
        String code = "3000";
        String message = "fail";
        if (jsonInput == null) {
            message = "inputJson not received.";
        } else if (jsonInput.getAppKey() == null) {
            message = "appKey is required.";
        } else if (jsonInput.getAppType() == null) {
            message = "appType is required.";
        } else if (jsonInput.getBody() == null) {
            message = "body is required.";
        } else if (jsonInput.getSecretKey() == null) {
            message = "secretKey is required.";
        } else if (jsonInput.getSignatureInfo() == null) {
            message = "signatureInfo is required.";
        } else if (jsonInput.getTimeStamp() == null) {
            message = "timeStamp is required.";
        } else if (jsonInput.getTranId() == null) {
            message = "tranId is required.";
        } else if (jsonInput.getTranSeq() == null) {
            message = "tranSeq is required.";
        } else {
            rtnCode = "0";
            code = "0000";
            message = "success";
        }
        JsonOutput jo = new JsonOutput(rtnCode, code, message);
        return jo;
    }

    /**
     * json字符串转换为map
     *
     * @param jsonStr 要转换的json字符串
     * @return 转换后的map
     */
    public static Map<?, ?> jsonStrToMap(String jsonStr) {
        try {
            ObjectMapper om = new ObjectMapper();
            return om.readValue(jsonStr, Map.class);
        } catch (Exception e) {
            LOG.error(e.getMessage());
            return null;
        }
    }

    /**
     * 格式化json字符串
     *
     * @param jsonStr 要格式化的json字符串
     * @return 格式化后的json字符串
     */
    public static String formatJsonStr(String jsonStr) {
        try {
            ObjectMapper om = new ObjectMapper();
            return om.writerWithDefaultPrettyPrinter().writeValueAsString(jsonStrToMap(jsonStr));
        } catch (Exception e) {
            LOG.error(e.getMessage());
            return null;
        }
    }

}
```

##### 7.1.4 PropertiesLoader类

用于加载resources包的配置文件的

PropertiesLoader.java

```
package kb.redis.util;

import org.springframework.core.io.DefaultResourceLoader;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;

import java.io.IOException;
import java.io.InputStream;
import java.util.NoSuchElementException;
import java.util.Properties;

/**
 * 用以加载配置文件
 */
public class PropertiesLoader {
    private static ResourceLoader resourceLoader = new DefaultResourceLoader();

    private final Properties properties;

    public PropertiesLoader(String... resourcesPaths) {
        properties = loadProperties(resourcesPaths);
    }

    public Properties getProperties() {
        return properties;
    }

    /**
     * 取出Property,但以System的Property优先.取不到返回空字符串
     *
     * @param key Property键
     * @return String类型的Property值
     */
    private String getValue(String key) {
        String systemProperty = System.getProperty(key);
        if (systemProperty != null) {
            return systemProperty;
        }
        if (properties.containsKey(key)) {
            return properties.getProperty(key);
        }
        return "";
    }

    /**
     * 取出String类型的Property,但以System的Property优先,如果都为Null则抛出异常
     *
     * @param key Property键
     * @return String类型的Property值
     */
    public String getProperty(String key) {
        String value = getValue(key);
        if (value == null) {
            throw new NoSuchElementException();
        }
        return value;
    }

    /**
     * 取出String类型的Property,但以System的Property优先.如果都为Null则返回Default值
     *
     * @param key          Property键
     * @param defaultValue Default值
     * @return String类型的Property值
     */
    public String getProperty(String key, String defaultValue) {
        String value = getValue(key);
        return value != null ? value : defaultValue;
    }

    /**
     * 取出Integer类型的Property,但以System的Property优先.如果都为Null或内容错误则抛出异常
     *
     * @param key Property键
     * @return Integer类型的Property值
     */
    public Integer getInteger(String key) {
        String value = getValue(key);
        if (value == null) {
            throw new NoSuchElementException();
        }
        return Integer.valueOf(value);
    }

    /**
     * 取出Integer类型的Property,但以System的Property优先.如果都为Null则返回Default值,如果内容错误则抛出异常
     *
     * @param key          Property键
     * @param defaultValue Default值
     * @return Integer类型的Property值
     */
    public Integer getInteger(String key, Integer defaultValue) {
        String value = getValue(key);
        return value != null ? Integer.valueOf(value) : defaultValue;
    }

    /**
     * 取出Long类型的Property,但以System的Property优先.如果都为Null或内容错误则抛出异常
     *
     * @param key Property键
     * @return Long类型的Property值
     */
    public Long getLong(String key) {
        String value = getValue(key);
        if (value == null) {
            throw new NoSuchElementException();
        }
        return Long.valueOf(value);
    }

    /**
     * 取出Long类型的Property,但以System的Property优先.如果都为Null则返回Default值,如果内容错误则抛出异常
     *
     * @param key          Property键
     * @param defaultValue Default值
     * @return Long类型的Property值
     */
    public Long getLong(String key, Long defaultValue) {
        String value = getValue(key);
        return value != null ? Long.valueOf(value) : defaultValue;
    }

    /**
     * 取出Double类型的Property,但以System的Property优先.如果都为Null或内容错误则抛出异常
     *
     * @param key Property键
     * @return Double类型的Property值
     */
    public Double getDouble(String key) {
        String value = getValue(key);
        if (value == null) {
            throw new NoSuchElementException();
        }
        return Double.valueOf(value);
    }

    /**
     * 取出Double类型的Property,但以System的Property优先.如果都为Null则返回Default值,如果内容错误则抛出异常
     *
     * @param key          Property键
     * @param defaultValue Default值
     * @return Double类型的Property值
     */
    public Double getDouble(String key, Integer defaultValue) {
        String value = getValue(key);
        return value != null ? Double.valueOf(value) : defaultValue;
    }

    /**
     * 取出Boolean类型的Property,但以System的Property优先.如果都为Null抛出异常,如果内容不是true/
     * false则返回false
     *
     * @param key Property键
     * @return Boolean类型的Property值
     */
    public Boolean getBoolean(String key) {
        String value = getValue(key);
        if (value == null) {
            throw new NoSuchElementException();
        }
        return Boolean.valueOf(value);
    }

    /**
     * 取出Boolean类型的Property,但以System的Property优先.如果都为Null则返回Default值,如果内容不为true/
     * false则返回false
     *
     * @param key          Property键
     * @param defaultValue Default值
     * @return Boolean类型的Property值
     */
    public Boolean getBoolean(String key, boolean defaultValue) {
        String value = getValue(key);
        return value != null ? Boolean.valueOf(value) : defaultValue;
    }

    /**
     * 载入多个文件,文件路径使用Spring Resource格式
     *
     * @param resourcesPaths 文件路径
     * @return Properties
     */
    private Properties loadProperties(String... resourcesPaths) {
        Properties props = new Properties();

        for (String location : resourcesPaths) {
            InputStream is = null;
            try {
                Resource resource = resourceLoader.getResource(location);
                is = resource.getInputStream();
                props.load(is);
            } catch (IOException ex) {
                ex.printStackTrace();
            } finally {
                // IOUtils.closeQuietly(is);
            }
        }
        return props;
    }
}

```

#### 7.2在redis/utils/redis包下创建

##### 7.2.1 redis连接类

提供两种连接模式：哨兵模式和单机模式

RedisConfig.java

```
package kb.redis.utils.redis;

import kb.redis.utils.PropertiesLoader;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisSentinelConfiguration;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.serializer.JdkSerializationRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;
import org.springframework.util.StringUtils;
import redis.clients.jedis.JedisPoolConfig;

/**
 * @ClassName: RedisConfig
 * @Description: redis配置
 */
@Configuration
public class RedisConfig {

    private final PropertiesLoader redisProperties = new PropertiesLoader("redis.properties");

    /**
     * redis的模式（哨兵模式:sentinel;单机模式:standalone）
     */
    @Value("${system.redis.mode}")
    private String redisMode;

    /**
     * @return
     * @Title: jedisPoolConfig
     * @Description: 配置连接池
     */
    @Bean
    public JedisPoolConfig jedisPoolConfig() {

        JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();

        jedisPoolConfig.setMaxIdle(redisProperties.getInteger("redis.pool.maxIdle"));
        jedisPoolConfig.setMaxTotal(redisProperties.getInteger("redis.pool.maxTotal"));
        jedisPoolConfig.setMaxWaitMillis(redisProperties.getLong("redis.pool.maxWaitMillis"));
        jedisPoolConfig.setTestOnBorrow(redisProperties.getBoolean("redis.pool.testOnBorrow"));

        return jedisPoolConfig;
    }

    /**
     * @param jpc
     * @return
     * @Title: jedisConnectionFactory
     * @Description: 配置连接工厂
     */
    @Bean
    public JedisConnectionFactory jedisConnectionFactory(JedisPoolConfig jpc) {

        /**
         * 根据config.properties中system.redis.mode配置连接工厂(哨兵模式:sentinel;单机模式: standalone)
         */
        if ("sentinel".equals(redisMode)) {

            RedisSentinelConfiguration sentinelConfig = new RedisSentinelConfiguration(
                    redisProperties.getProperty("redis.sentinel.master"),
                    StringUtils.commaDelimitedListToSet(redisProperties.getProperty("redis.sentinel.hostAndPost")));
            return new JedisConnectionFactory(sentinelConfig, jpc);
        } else {

            JedisConnectionFactory jedisConnectionFactory = new JedisConnectionFactory();
            jedisConnectionFactory.setHostName(redisProperties.getProperty("redis.host"));
            jedisConnectionFactory.setPort(redisProperties.getInteger("redis.port"));
            jedisConnectionFactory.setPassword(redisProperties.getProperty("redis.password"));
            jedisConnectionFactory.setPoolConfig(jpc);

            return jedisConnectionFactory;
        }
    }

    /**
     * @param jcf
     * @return
     * @Title: stringRedisTemplate
     * @Description: 配置redis模板，用于操作redis
     */
    @Bean
    public StringRedisTemplate stringRedisTemplate(JedisConnectionFactory jcf) {
        StringRedisTemplate stringRedisTemplate = new StringRedisTemplate();
        stringRedisTemplate.setConnectionFactory(jcf);
        stringRedisTemplate.setKeySerializer(new StringRedisSerializer());
        stringRedisTemplate.setValueSerializer(new JdkSerializationRedisSerializer());
        return stringRedisTemplate;
    }

}
```

##### 7.2.1 redis基本操作类

RedisBaseDao.java

```
package kb.redis.utils.redis;
import kb.redis.utils.JsonUtil;
import kb.redis.utils.PropertiesLoader;
import org.loushang.framework.util.SpringContextHolder;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.concurrent.TimeUnit;

/**
 * @ClassName: RedisBaseDao
 * @Description: 提供操作redis的方法
 */
public abstract class RedisBaseDao {

    private static PropertiesLoader configProperties = new PropertiesLoader("config.properties");

    private static boolean isUseRedis = configProperties.getBoolean("system.redis.isUseRedis");

    private static StringRedisTemplate stringRedisTemplate = null;

    static {
        if (isUseRedis) {
            stringRedisTemplate = SpringContextHolder.getBean("stringRedisTemplate");
        }
    }

    /**
     * 向redis中插入永不过期的数据
     *
     * @param key    键
     * @param object 要存入的对象
     * @return 是否成功
     */
    protected boolean insert(String key, Object object) {
        if (isUseRedis) {
            stringRedisTemplate.opsForValue().set(key, JsonUtil.objectToJsonStr(object));
        }
        return isUseRedis;
    }

    /**
     * 向redis中插入含过期时间的数据(单位:秒)
     *
     * @param key     键
     * @param object  要存入的对象
     * @param timeout 超时时间
     * @return 是否成功3
     */
    protected boolean insert(String key, Object object, Long timeout) {
        if (isUseRedis) {
            stringRedisTemplate.opsForValue().set(key, JsonUtil.objectToJsonStr(object), timeout, TimeUnit.SECONDS);
        }
        return isUseRedis;
    }

    /**
     * 向redis中插入含过期时间的数据,需指定时间单位
     *
     * @param key     键
     * @param object  要存入的对象
     * @param timeout 超时时间
     * @param unit    时间单位
     * @return 是否成功
     */
    protected boolean insert(String key, Object object, Long timeout, TimeUnit unit) {
        if (isUseRedis) {
            stringRedisTemplate.opsForValue().set(key, JsonUtil.objectToJsonStr(object), timeout, unit);
        }
        return isUseRedis;
    }

    /**
     * 删除redis中指定的数据
     *
     * @param key 键
     * @return 是否成功
     */
    protected boolean delete(String key) {
        if (isUseRedis) {
            stringRedisTemplate.delete(key);
        }
        return isUseRedis;
    }

    /**
     * 获取redis中指定的数据，并以指定类型返回
     *
     * @param <T>       Type Java类
     * @param key       键
     * @param valueType redis中对象的类型
     * @return 在redis中对象
     */
    protected <T> T select(String key, Class<T> valueType) {
        if (isUseRedis) {
            String value = stringRedisTemplate.opsForValue().get(key);
            return value == null ? null : JsonUtil.jsonStrToObject(value, valueType);
        } else {
            return null;
        }
    }

    /**
     * 是否使用redis
     *
     * @return 是否使用redis
     */
    public boolean isUseRedis() {
        return isUseRedis;
    }

}

```

### 8 创建RedisDao层

#### 8.1 在redis包下创建redisDao包

#### 8.2 在redisDao包下创建TestRedisByListDao接口

TestRedisByListDao.java

```
package kb.redis.redisDao;

import java.util.List;

/**
 * 测试 插入、删除、获取 list格式
 * Created by shirukai on 2017/12/2.
 */
public interface TestRedisByListDao {
    Boolean setListToRedis(String key,List list);

    Boolean delListFromRedis(String key);

    List getListFromRedis(String key);
}

```

#### 8.3 创建TestRedisByListDao的实现类

TestRedisByListDaoImpl.java

```
package kb.redis.redisDao;
import kb.redis.utils.redis.RedisBaseDao;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * List操作
 * Created by shirukai on 2017/12/2.
 */
@Repository
public class TestRedisByListDaoImpl extends RedisBaseDao implements TestRedisByListDao {
    public static final String KEY = "INSPUR:KB";

    /**
     * 保存List
     *
     * @param key  key
     * @param list list
     * @return boolean
     */
    @Override
    public Boolean setListToRedis(String key, List list) {
        return insert(KEY + ":" + key, list);
    }

    /**
     * 删除key
     *
     * @param key key
     * @return boolean
     */
    @Override
    public Boolean delListFromRedis(String key) {
        return delete(KEY + ":" + key);

    }

    /**
     * 获取list
     *
     * @param key key
     * @return list
     */
    @Override
    public List getListFromRedis(String key) {
        return select(KEY + ":" + key,List.class);
    }
}

```

### 9.单元测试

```
package kb.redis.redisDao;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.*;

/**
 * 测试保存list到redis
 * Created by shirukai on 2017/12/2.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath*:spring-context.xml", "classpath*:mybatis-config.xml"})
public class TestRedisByListDaoImplTest {
    @Autowired
    private TestRedisByListDao testRedisByListDao;

    @Test
    public void setListToRedis() throws Exception {
        List<Map<String,String>> list = new ArrayList<Map<String,String>>();
        Map<String,String> map = new HashMap<String,String>();
        map.put("key1","value1");
        map.put("key2","value2");
        list.add(map);
        list.add(map);
        String key = "list1";
        Boolean resulet = testRedisByListDao.setListToRedis(key,list);
        if (resulet){
            System.out.println("保存redis成功！");
        }else {
            System.out.println("保存失败！");
        }

    }

    @Test
    public void delListFromRedis() throws Exception {
    }

    @Test
    public void getListFromRedis() throws Exception {
        String key = "list1";
        List list = testRedisByListDao.getListFromRedis(key);
        if (list != null){
            System.out.println(list);
        }else {
            System.out.println("获取失败！");
        }
    }

}
```



### 附加配置redis

下载redis后解压然后执行make命令进行编译

#### 设置redis可以远程访问：

修改redis目录下的redis.conf文件中的两处地方

第一处

69行注释掉 #bind 127.0.0.0

第二处

88行设置 protected-mode no

#### 设置redis密码

500行  requirepass shirukai