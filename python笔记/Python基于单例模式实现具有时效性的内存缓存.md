# Python基于单例模式实现具有时效性的内存缓存

> 版本说明：Python 2.7

Python有不少第三方的缓存库，如[cacheout](https://pypi.org/project/cacheout/)、[memcached](http://memcached.org/)等。因为项目需求，这里不使用第三方库，自己实现具有时效性的内存缓存，用来缓存重复利用的数据。

## 1 设计实现

### 1.1 思路

采用dict()作为缓存介质，数据以key、value的形式进行保存。key为cache_id，用来标识不同的缓存数据。value是要进行缓存的数据。并且使用单例的设计模式，保障缓存数据的原子性。在时效性控制上，对每一个缓存数据进行单独控制，使用threading.Timer进行延时销毁缓存数据。

### 1.2 设计单例模式

本例子使用`__new__`关键字实现单例模式。如下所示：

```python
# encoding: utf-8
"""
Created by shirukai on 2018/11/7
"""
import threading


class DataCache(object):
    # 添加线程锁，保证多线程安全
    __instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):

        if not hasattr(DataCache, "_instance"):
            with DataCache.__instance_lock:
                if not hasattr(DataCache, "_instance"):
                    DataCache._instance = object.__new__(cls)
        return DataCache._instance
```

测试：

```python
if __name__ == '__main__':
    for i in xrange(10):
        print DataCache()

```

![](http://shirukai.gitee.io/images/d6fcea9c166c3e4ee471ba96a385ef12.jpg)

### 1.3 时效性控制

在时效性控制上，选用了threading.Timer进行延时执行方法。例如我要延时执行一个打印方法，可以使用如下的代码.

```python
# encoding: utf-8
"""
Created by shirukai on 2018/11/7
"""
import threading
import time


def print_str(string):
    print string


if __name__ == '__main__':
    timer = threading.Timer(2, print_str, ['test timer'])
    timer.start()
    time.sleep(10)
```

Timer(延时时间,执行函数,参数)

## 2 实现代码

```python
# encoding: utf-8
"""
Created by shirukai on 2018/11/5
基于单例模式实现具有时效性的内存缓存
"""
import threading
import uuid


class DataCache(object):
    """
    _cache 的数据结构如下所示：
    _cache:{
        "cache_id_1":{
            "value":"cache_value",
            "expired":"60s",
            "timer":"定时清理器实例",
        }
    }
    """

    # 默认 expired = 2*60*60s
    EXPIRED = 2 * 60 * 60

    # 添加线程锁，保证多线程安全
    __instance_lock = threading.Lock()

    # 初始化dict(）用来缓存数据
    __CACHE = dict()

    def __init__(self):
        self.__cache = DataCache.__CACHE

    def __new__(cls, *args, **kwargs):

        if not hasattr(DataCache, "_instance"):
            with DataCache.__instance_lock:
                if not hasattr(DataCache, "_instance"):
                    DataCache._instance = object.__new__(cls)
        return DataCache._instance

    def set(self, value, cache_id=None, expired=EXPIRED):
        """
        保存缓存
        :param value: 缓存数据
        :param cache_id: cache_id 默认值：None
        :param expired: 过期时间 默认值：EXPIRED
        :return: cache_id
        """
        if cache_id is None or cache_id == "":
            cache_id = str(uuid.uuid4())

        self._set_cache(value, cache_id, expired)

        return cache_id

    def delete(self, cache_id):
        """
        删除缓存
        :param cache_id: 缓存ID
        :return: None
        """
        self._clean_cache(cache_id)

    def get(self, cache_id):
        """
        获取缓存
        :param cache_id:缓存ID
        :return:
        """
        if self.__cache.has_key(cache_id):
            return self.__cache[cache_id]['value']
        else:
            return None

    def values(self):
        """
        获取所有值
        :return: {
        “cache_id_1”:"value1",
        “cache_id_2”:"value2"
        }
        """
        return {key: item['value'] for key, item in self.__cache.items()}

    def clear(self):
        """
        清空缓存
        :return: None
        """
        for cache_id in self.__cache.keys():
            self._clean_cache(cache_id)

    def _set_cache(self, value, cache_id, expired):
        # 删除缓存
        self._clean_cache(cache_id)
        # 设置时效监控线程
        timer = threading.Timer(expired, self._clean_cache, [cache_id])
        timer.start()
        self.__cache[cache_id] = {
            'timer': timer,
            'value': value
        }

    def _clean_cache(self, cache_id):
        if self.__cache.has_key(cache_id):
            timer = self.__cache[cache_id]['timer']
            timer.cancel()
            self.__cache.pop(cache_id)

```

### 3 测试

测试代码:

```python
# encoding: utf-8
"""
Created by shirukai on 2018/11/7
"""
from src.api.v1.cache.data_cache import DataCache
import time

if __name__ == '__main__':
    cache = DataCache()
    # 保存一个字符串，并设置时效性为6秒
    cache_id = cache.set(value="test cache!", expired=6)

    # 每隔一秒打印一次数据
    for i in xrange(10):
        print cache.get(cache_id)
        time.sleep(1)

```

效果：

![](http://shirukai.gitee.io/images/e98e34634fd539eb0bb0559923aaaf8a.gif)