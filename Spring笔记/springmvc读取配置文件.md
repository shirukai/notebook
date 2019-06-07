# springmvc读取配置文件 

## 工具类 

简单的工具类

PropertiesUtil

```
package com.mavenssmlr.util;

import java.io.InputStream;
import java.util.Properties;

/**
 * 读取配置文件工具类
 * Created by shirukai on 2017/12/18.
 */
public class PropertiesUtil {
    private static Properties getProperties(String properties) {
        try {
            InputStream in = PropertiesUtil.class.getClassLoader().getResourceAsStream(properties);
            Properties p = new Properties();
            p.load(in);
            return p;
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }
    public static String getValue(String properties,String key){
        Properties p = getProperties(properties);
        return p.getProperty(key);
    }
}
```

## 配置文件

在resource目录下创建config.properties文件

```
test="this is test !"
```

## 测试类 

```
package com.mavenssmlr.util;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 *
 * Created by shirukai on 2017/12/18.
 */
public class PropertiesUtilTest {
    @Test
    public void getValue() throws Exception {
        System.out.println(PropertiesUtil.getValue("config.properties","test"));
    }

}
```



## 多功能读取配置文件的工具类 

```
package com.inspur.tax.common.util;

import java.io.IOException;
import java.io.InputStream;
import java.util.NoSuchElementException;
import java.util.Properties;

import org.springframework.core.io.DefaultResourceLoader;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;

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
     * @since 2016年9月21日 下午3:46:33
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
     * @since 2016年9月21日 下午3:51:45
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
     * @since 2016年9月21日 下午3:52:35
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
     * @since 2016年9月21日 下午3:53:27
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
     * @since 2016年9月21日 下午3:54:00
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
     * @since 2016年9月21日 下午3:54:35
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
     * @since 2016年9月21日 下午3:55:17
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
     * @since 2016年9月21日 下午3:43:55
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
     * @since 2016年9月21日 下午3:45:28
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
     * @since 2016年9月21日 下午3:49:43
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
     * @since 2016年9月21日 下午3:48:32
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
     * @since 2016年9月21日 下午3:48:12
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

