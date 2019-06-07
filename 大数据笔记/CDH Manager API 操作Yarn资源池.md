# CDH Manager API 操作Yarn 资源池

> 版本说明：CDH 5.11.0
>
> API版本：v16

## 1 API 权限认证

在使用REST API 访问 CDH Manager 提供的相关接口的时候，需要进行权限认证。认证的类型是 Basic Auth。在java编程中将如下所示生成authorization，然后将该认证信息添加到请求头信息中即可。

```java
private static String generateAuth(String userName, String password) {
    return "Basic " + new String(Base64.getEncoder().encode((userName + ":" + password).getBytes()));
}
```

在PostMan中测试可以通过如下设置添加认证信息

![](http://shirukai.gitee.io/images/7e0e7f6efa7bb6055cb610375a9d61ec.jpg)

## 2 获取集群信息

API: http://192.168.66.168:7180/api/v16/clusters

请求类型：GET

参数：无

认证方式：Basic Auth

响应：

```json
{
    "items": [
        {
            "name": "cluster",
            "displayName": "Cluster 1",
            "version": "CDH5",
            "fullVersion": "5.11.0",
            "maintenanceMode": false,
            "maintenanceOwners": [],
            "clusterUrl": "http://cdh-manager:7180/cmf/clusterRedirect/cluster",
            "hostsUrl": "http://cdh-manager:7180/cmf/clusterRedirect/cluster/hosts",
            "entityStatus": "CONCERNING_HEALTH",
            "uuid": "2b718bbd-d712-4b63-bd28-35b8f1e6bf35"
        }
    ]
}
```



## 3 获取Yarn的配置信息

API: http://192.168.66.168:7180/api/v16/clusters/{clusterName}/services/yarn/config

请求类型：GET

参数：

| 参数        | 描述     |
| ----------- | -------- |
| clusterName | 集群名称 |

认证方式：无需

响应：

```json
{
    "items": [
        {
            "name": "hdfs_service",
            "value": "hdfs",
            "sensitive": false
        },
        {
            "name": "yarn_fs_scheduled_allocations",
            "value": "{\"defaultFairSharePreemptionThreshold\":null,\"defaultFairSharePreemptionTimeout\":null,\"defaultMinSharePreemptionTimeout\":null,\"defaultQueueSchedulingPolicy\":\"fair\",\"queueMaxAMShareDefault\":null,\"queueMaxAppsDefault\":null,\"queuePlacementRules\":[{\"create\":true,\"name\":\"specified\",\"queue\":null,\"rules\":null},{\"create\":null,\"name\":\"nestedUserQueue\",\"queue\":null,\"rules\":[{\"create\":true,\"name\":\"default\",\"queue\":\"users\",\"rules\":null}]},{\"create\":null,\"name\":\"default\",\"queue\":null,\"rules\":null}],\"queues\":[{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\" \",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"root\",\"queues\":[{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\"*\",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"default\",\"queues\":[],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":null,\"maxRunningApps\":null,\"minResources\":null,\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":null},{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\"*\",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"users\",\"queues\":[],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":null,\"maxRunningApps\":null,\"minResources\":null,\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":\"parent\"},{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\"*\",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"analyst-srk\",\"queues\":[],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":{\"memory\":4194304,\"vcores\":4},\"maxRunningApps\":null,\"minResources\":{\"memory\":2097152,\"vcores\":2},\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":null}],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":null,\"maxRunningApps\":null,\"minResources\":null,\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":null}],\"userMaxAppsDefault\":null,\"users\":[]}",
            "sensitive": false
        },
        {
            "name": "zookeeper_service",
            "value": "zookeeper",
            "sensitive": false
        }
    ]
}
```

将name为"yarn_fs_scheduled_allocations"的value值json化展开，得到如下信息，这些信息就是Yarn的资源池配置信息。

```json
{
    "defaultQueueSchedulingPolicy": "fair",
    "userMaxAppsDefault": null,
    "queueMaxAppsDefault": null,
    "queueMaxAMShareDefault": null,
    "queuePlacementRules": [
        {
            "name": "specified",
            "create": true,
            "rules": null,
            "queue": null
        },
        {
            "name": "nestedUserQueue",
            "create": null,
            "rules": [
                {
                    "name": "default",
                    "create": true,
                    "rules": null,
                    "queue": "users"
                }
            ],
            "queue": null
        },
        {
            "name": "default",
            "create": null,
            "rules": null,
            "queue": null
        }
    ],
    "queues": [
        {
            "fairSharePreemptionThreshold": null,
            "queues": [
                {
                    "fairSharePreemptionThreshold": null,
                    "queues": [],
                    "aclSubmitApps": "*",
                    "schedulablePropertiesList": [
                        {
                            "impalaDefaultQueryMemLimit": null,
                            "scheduleName": "default",
                            "impalaMaxMemory": null,
                            "impalaDefaultQueryOptions": null,
                            "weight": 1,
                            "maxChildResources": null,
                            "minResources": null,
                            "impalaMaxRunningQueries": null,
                            "maxRunningApps": null,
                            "maxAMShare": null,
                            "impalaQueueTimeout": null,
                            "maxResources": null,
                            "impalaMaxQueuedQueries": null
                        }
                    ],
                    "name": "default",
                    "aclAdministerApps": "*",
                    "allowPreemptionFrom": null,
                    "type": null,
                    "fairSharePreemptionTimeout": null,
                    "minSharePreemptionTimeout": null,
                    "schedulingPolicy": "drf"
                },
                {
                    "fairSharePreemptionThreshold": null,
                    "queues": [],
                    "aclSubmitApps": "*",
                    "schedulablePropertiesList": [
                        {
                            "impalaDefaultQueryMemLimit": null,
                            "scheduleName": "default",
                            "impalaMaxMemory": null,
                            "impalaDefaultQueryOptions": null,
                            "weight": 1,
                            "maxChildResources": null,
                            "minResources": null,
                            "impalaMaxRunningQueries": null,
                            "maxRunningApps": null,
                            "maxAMShare": null,
                            "impalaQueueTimeout": null,
                            "maxResources": null,
                            "impalaMaxQueuedQueries": null
                        }
                    ],
                    "name": "users",
                    "aclAdministerApps": "*",
                    "allowPreemptionFrom": null,
                    "type": "parent",
                    "fairSharePreemptionTimeout": null,
                    "minSharePreemptionTimeout": null,
                    "schedulingPolicy": "drf"
                },
                {
                    "fairSharePreemptionThreshold": null,
                    "queues": [],
                    "aclSubmitApps": "*",
                    "schedulablePropertiesList": [
                        {
                            "impalaDefaultQueryMemLimit": null,
                            "scheduleName": "default",
                            "impalaMaxMemory": null,
                            "impalaDefaultQueryOptions": null,
                            "weight": 1,
                            "maxChildResources": null,
                            "minResources": {
                                "memory": 2097152,
                                "vcores": 2
                            },
                            "impalaMaxRunningQueries": null,
                            "maxRunningApps": null,
                            "maxAMShare": null,
                            "impalaQueueTimeout": null,
                            "maxResources": {
                                "memory": 4194304,
                                "vcores": 4
                            },
                            "impalaMaxQueuedQueries": null
                        }
                    ],
                    "name": "analyst-srk",
                    "aclAdministerApps": "*",
                    "allowPreemptionFrom": null,
                    "type": null,
                    "fairSharePreemptionTimeout": null,
                    "minSharePreemptionTimeout": null,
                    "schedulingPolicy": "drf"
                }
            ],
            "aclSubmitApps": " ",
            "schedulablePropertiesList": [
                {
                    "impalaDefaultQueryMemLimit": null,
                    "scheduleName": "default",
                    "impalaMaxMemory": null,
                    "impalaDefaultQueryOptions": null,
                    "weight": 1,
                    "maxChildResources": null,
                    "minResources": null,
                    "impalaMaxRunningQueries": null,
                    "maxRunningApps": null,
                    "maxAMShare": null,
                    "impalaQueueTimeout": null,
                    "maxResources": null,
                    "impalaMaxQueuedQueries": null
                }
            ],
            "name": "root",
            "aclAdministerApps": "*",
            "allowPreemptionFrom": null,
            "type": null,
            "fairSharePreemptionTimeout": null,
            "minSharePreemptionTimeout": null,
            "schedulingPolicy": "drf"
        }
    ],
    "defaultFairSharePreemptionThreshold": null,
    "defaultFairSharePreemptionTimeout": null,
    "defaultMinSharePreemptionTimeout": null,
    "users": []
}
```

从下图可以看出，根资源池root下有三个子资源池。

![](http://shirukai.gitee.io/images/061f131d04b40723cfcf6f3db2105f7d.jpg)

然后展开三个子资源池的数据，可以看到它们分别为：default、users、analyst-srk。

## 4 动态设置Yarn的资源池

动态设置Yarn的资源池，其实就是修改Yarn的config信息，然后刷新资源池。修改yarn的config信息的API与上述查询配置的API相同，只是想请求类型改为PUT，然后添加认证头信息即可。

如，我要添加在root资源池中，创建一个子资源池srk-test，并指定最小的资源：内存为2g核数为2核。最大的资源：内存为4g，核数为4核。其它的参数，可以参考界面设置。需要将如下信息，添加到上述的json中。

```json
{
    "fairSharePreemptionThreshold": null,
    "queues": [],
    "aclSubmitApps": "*",
    "schedulablePropertiesList": [
        {
            "impalaDefaultQueryMemLimit": null,
            "scheduleName": "default",
            "impalaMaxMemory": null,
            "impalaDefaultQueryOptions": null,
            "weight": 1,
            "maxChildResources": null,
            "minResources": {
                "memory": 2097152,
                "vcores": 2
            },
            "impalaMaxRunningQueries": null,
            "maxRunningApps": null,
            "maxAMShare": null,
            "impalaQueueTimeout": null,
            "maxResources": {
                "memory": 4194304,
                "vcores": 4
            },
            "impalaMaxQueuedQueries": null
        }
    ],
    "name": "srk-test",
    "aclAdministerApps": "*",
    "allowPreemptionFrom": null,
    "type": null,
    "fairSharePreemptionTimeout": null,
    "minSharePreemptionTimeout": null,
    "schedulingPolicy": "drf"
}
```



API: http://192.168.66.168:7180/api/v16/clusters/{clusterName}/services/yarn/config

请求类型：PUT

参数：

```json
{
    "items": [
        {
            "name": "hdfs_service",
            "value": "hdfs",
            "sensitive": false
        },
        {
            "name": "yarn_fs_scheduled_allocations_draft",
            "value": {\"defaultQueueSchedulingPolicy\": \"fair\",\"userMaxAppsDefault\": null,\"queueMaxAppsDefault\": null,\"queueMaxAMShareDefault\": null,\"queuePlacementRules\": [{\"name\": \"specified\",\"create\": true,\"rules\": null,\"queue\": null},{\"name\": \"nestedUserQueue\",\"create\": null,\"rules\": [  {\"name\": \"default\",\"create\": true,\"rules\": null,\"queue\": \"users\"  }],\"queue\": null},{\"name\": \"default\",\"create\": null,\"rules\": null,\"queue\": null}],\"queues\": [{\"fairSharePreemptionThreshold\": null,\"queues\": [  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": null,\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": null,\"impalaMaxQueuedQueries\": null  }],\"name\": \"default\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  },  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": null,\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": null,\"impalaMaxQueuedQueries\": null  }],\"name\": \"users\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": \"parent\",\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  },  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": {  \"memory\": 2097152,  \"vcores\": 2},\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": {  \"memory\": 4194304,  \"vcores\": 4},\"impalaMaxQueuedQueries\": null  }],\"name\": \"analyst-srk\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  },  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": {  \"memory\": 2097152,  \"vcores\": 2},\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": {  \"memory\": 4194304,  \"vcores\": 4},\"impalaMaxQueuedQueries\": null  }],\"name\": \"srk-test\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  }],\"aclSubmitApps\": \" \",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": null,\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": null,\"impalaMaxQueuedQueries\": null  }],\"name\": \"root\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"}],\"defaultFairSharePreemptionThreshold\": null,\"defaultFairSharePreemptionTimeout\": null,\"defaultMinSharePreemptionTimeout\": null,\"users\": [] },
            "sensitive": false
        },
        {
            "name": "zookeeper_service",
            "value": "zookeeper",
            "sensitive": false
        }
    ]
}
```

认证方式：Basic Auth

响应：

```json
{
    "items": [
        {
            "name": "hdfs_service",
            "value": "hdfs",
            "sensitive": false
        },
        {
            "name": "yarn_fs_scheduled_allocations",
            "value": "{\"defaultFairSharePreemptionThreshold\":null,\"defaultFairSharePreemptionTimeout\":null,\"defaultMinSharePreemptionTimeout\":null,\"defaultQueueSchedulingPolicy\":\"fair\",\"queueMaxAMShareDefault\":null,\"queueMaxAppsDefault\":null,\"queuePlacementRules\":[{\"create\":true,\"name\":\"specified\",\"queue\":null,\"rules\":null},{\"create\":null,\"name\":\"nestedUserQueue\",\"queue\":null,\"rules\":[{\"create\":true,\"name\":\"default\",\"queue\":\"users\",\"rules\":null}]},{\"create\":null,\"name\":\"default\",\"queue\":null,\"rules\":null}],\"queues\":[{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\" \",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"root\",\"queues\":[{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\"*\",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"default\",\"queues\":[],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":null,\"maxRunningApps\":null,\"minResources\":null,\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":null},{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\"*\",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"users\",\"queues\":[],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":null,\"maxRunningApps\":null,\"minResources\":null,\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":\"parent\"},{\"aclAdministerApps\":\"*\",\"aclSubmitApps\":\"*\",\"allowPreemptionFrom\":null,\"fairSharePreemptionThreshold\":null,\"fairSharePreemptionTimeout\":null,\"minSharePreemptionTimeout\":null,\"name\":\"analyst-srk\",\"queues\":[],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":{\"memory\":4194304,\"vcores\":4},\"maxRunningApps\":null,\"minResources\":{\"memory\":2097152,\"vcores\":2},\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":null}],\"schedulablePropertiesList\":[{\"impalaDefaultQueryMemLimit\":null,\"impalaDefaultQueryOptions\":null,\"impalaMaxMemory\":null,\"impalaMaxQueuedQueries\":null,\"impalaMaxRunningQueries\":null,\"impalaQueueTimeout\":null,\"maxAMShare\":null,\"maxChildResources\":null,\"maxResources\":null,\"maxRunningApps\":null,\"minResources\":null,\"scheduleName\":\"default\",\"weight\":1.0}],\"schedulingPolicy\":\"drf\",\"type\":null}],\"userMaxAppsDefault\":null,\"users\":[]}",
            "sensitive": false
        },
        {
            "name": "yarn_fs_scheduled_allocations_draft",
            "value": "{\"defaultQueueSchedulingPolicy\": \"fair\",\"userMaxAppsDefault\": null,\"queueMaxAppsDefault\": null,\"queueMaxAMShareDefault\": null,\"queuePlacementRules\": [{\"name\": \"specified\",\"create\": true,\"rules\": null,\"queue\": null},{\"name\": \"nestedUserQueue\",\"create\": null,\"rules\": [  {\"name\": \"default\",\"create\": true,\"rules\": null,\"queue\": \"users\"  }],\"queue\": null},{\"name\": \"default\",\"create\": null,\"rules\": null,\"queue\": null}],\"queues\": [{\"fairSharePreemptionThreshold\": null,\"queues\": [  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": null,\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": null,\"impalaMaxQueuedQueries\": null  }],\"name\": \"default\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  },  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": null,\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": null,\"impalaMaxQueuedQueries\": null  }],\"name\": \"users\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": \"parent\",\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  },  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": {  \"memory\": 2097152,  \"vcores\": 2},\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": {  \"memory\": 4194304,  \"vcores\": 4},\"impalaMaxQueuedQueries\": null  }],\"name\": \"analyst-srk\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  },  {\"fairSharePreemptionThreshold\": null,\"queues\": [],\"aclSubmitApps\": \"*\",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": {  \"memory\": 2097152,  \"vcores\": 2},\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": {  \"memory\": 4194304,  \"vcores\": 4},\"impalaMaxQueuedQueries\": null  }],\"name\": \"srk-test\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"  }],\"aclSubmitApps\": \" \",\"schedulablePropertiesList\": [  {\"impalaDefaultQueryMemLimit\": null,\"scheduleName\": \"default\",\"impalaMaxMemory\": null,\"impalaDefaultQueryOptions\": null,\"weight\": 1,\"maxChildResources\": null,\"minResources\": null,\"impalaMaxRunningQueries\": null,\"maxRunningApps\": null,\"maxAMShare\": null,\"impalaQueueTimeout\": null,\"maxResources\": null,\"impalaMaxQueuedQueries\": null  }],\"name\": \"root\",\"aclAdministerApps\": \"*\",\"allowPreemptionFrom\": null,\"type\": null,\"fairSharePreemptionTimeout\": null,\"minSharePreemptionTimeout\": null,\"schedulingPolicy\": \"drf\"}],\"defaultFairSharePreemptionThreshold\": null,\"defaultFairSharePreemptionTimeout\": null,\"defaultMinSharePreemptionTimeout\": null,\"users\": [] }",
            "sensitive": false
        },
        {
            "name": "zookeeper_service",
            "value": "zookeeper",
            "sensitive": false
        }
    ]
}
```

查看CHD manager 可以看出我们的资源池配置已经更新上去了

![](http://shirukai.gitee.io/images/0ce65489bff6d1bf4d44e478d463cae8.jpg)

## 5 刷新动态资源池

配置更新上去之后，我们需要刷新动态资源池，才可以是资源池生效。

API: http://192.168.66.168:7180/api/v16/clusters/{clusterName}/commands/poolsRefresh

请求类型：POST

参数：无

认证方式：Basic Auth

响应：

```json
{
    "id": 1066,
    "name": "RefreshPools",
    "startTime": "2018-10-22T08:13:58.669Z",
    "active": true,
    "clusterRef": {
        "clusterName": "cluster"
    }
}
```

