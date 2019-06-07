# Java遍历map、list 

## Java遍历map的四种方法 

> 补充：将javabean封装成map

```
package com.mavenssmlr.util;

import java.beans.BeanInfo;
import java.beans.Introspector;
import java.beans.PropertyDescriptor;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

/**
 * 将java bean封装成map
 * Created by shirukai on 2017/11/1.
 */
public class TransBeanToMap {
     public static Map<String, Object> trans(Object object) {
        Map<String, Object> map = new HashMap<String, Object>();
        if (object == null) {
            return null;
        }
        try {
            BeanInfo beanInfo = Introspector.getBeanInfo(object.getClass());
            PropertyDescriptor[] propertyDescriptors = beanInfo.getPropertyDescriptors();
            for (PropertyDescriptor propertyDescriptor : propertyDescriptors) {
                String key = propertyDescriptor.getName();
                if (!key.equals("class")) {
                    //得到property对应的getter方法
                    Method getter = propertyDescriptor.getReadMethod();
                    Object value = getter.invoke(object);
                    map.put(key, value);
                }
            }
        } catch (Exception e) {
          System.out.println(e.getMessage());
        }

        return map;
    }
}
```

遍历map的四种方法：map.keySet()、迭代器、map.entrySet、map.values

```
public void traverseMap() throws Exception {
    User user = userDao.queryById(1);
    Map<String,Object> map = TransBeanToMap.trans(user);
    logger.info("map={}",map);
    //遍历map的四种方法
    //方法一：普遍使用、二次取值
    for (String key:map.keySet()
         ) {
        logger.info("key={}",key);
        logger.info("value={}",map.get(key));
    }
    //方法二：迭代器
    Iterator<Map.Entry<String,Object>> iterator = map.entrySet().iterator();
    while (iterator.hasNext()){
        Map.Entry<String,Object> entry = iterator.next();
        logger.info("key={}",entry.getKey());
        logger.info("value={}",entry.getValue());
    }

    //方法三：推荐，尤其是容量大时（通过Map.entrySet遍历key和value）
    for (Map.Entry<String,Object> entry : map.entrySet()
         ) {
        logger.info("key={}",entry.getKey());
        logger.info("value={}",entry.getValue());
    }
    //方法四：通过Map.values()遍历所有的value,但不能遍历key
    for (Object value : map.values()
         ) {
        logger.info("value={}",value);
    }

}
```

##  java遍历list的三种方法

```
List<String> list = new ArrayList<String>();
list.add("aaa");
list.add("bbb");
list.add("ccc");
方法一：
超级for循环遍历
for(String attribute : list) {
  System.out.println(attribute);
}
方法二：
对于ArrayList来说速度比较快, 用for循环, 以size为条件遍历:
for(int i = 0 ; i < list.size() ; i++) {
  system.out.println(list.get(i));
}
方法三：
集合类的通用遍历方式, 从很早的版本就有, 用迭代器迭代
Iterator it = list.iterator();
while(it.hasNext()) {
  System.ou.println(it.next);
}
```