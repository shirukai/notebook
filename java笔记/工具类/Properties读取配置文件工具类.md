# Properties读取配置文件工具类

PropertiesUtil.java

```
package com.springboot.demo.utils;

import org.springframework.core.io.ClassPathResource;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Created by shirukai on 2018/8/13
 * 读取配置文件
 */
public class PropertiesUtil {
    public static Properties getProperties(String name) {
        Properties properties = new Properties();
        try {
            ClassPathResource resource = new ClassPathResource(name);
            InputStream in = resource.getInputStream();
            properties.load(in);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return properties;
    }
}
```

使用

```
 private static Properties properties = PropertiesUtil.getProperties("kafka.properties");
 //方法里
 	properties.get("key")
```

