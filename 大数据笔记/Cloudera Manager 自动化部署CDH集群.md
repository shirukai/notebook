# Cloudera Manager 自动化部署CDH集群

>  版本说明：
>
> Python 2.7
>
> Ansible 2.7.2
>
> cm-api1 9.1.1
>
> Cloudera Manger 6.0.0
>
> CDH Parcel  6.0.0-1.cdh6.0.0.p0.537114
>
> 部署环境：CentOS 7.3

## 1 思路

自动化部署CDH集群主要分为两大模块：

模块一：使用Ansible部署基础环境，包括：修改hosts、互信、关闭防火墙、安装Java、安装MySQL、安装 Cloudera Manger、安装Cloudera Agent等操作。

模块二：使用Cloudera API 部署大数据服务，包括：创建集群、部署Cloudera Manger的监控服务 、分发Parcels、部署Zookeeper服务、部署Hdfs 服务、部署Yarn服务、部署HBase服务等。

因为Ansible属于Python的一个包，Cloudera Manger也提供了一个Python包 cm-api，所以这里使用Python作为胶水语言，贯穿整个部署流程，先使用Python 调用Ansible部署基础环境，然后使用Python 调用Cloudera Manager API部署大数据服务。

部署流程如下所示：

![](http://shirukai.gitee.io/images/fc68fcee056d9665e914c68447c62104.jpg)

## 2 部署准备

### 2.1 安装包准备

将本项目的代码及安装包上传到部署主机。

### 2.2 部署环境

在进行部署之前，需要对部署主机进行环境准备，比如安装sshpas、安装pip、安装Ansible包、安装cm-api包等，只需要执行以下安装脚本env.sh即可进行基础环境的准备。

env.sh

```shell
#!/usr/bin/env bash
yum install -y epel-release sshpass python-pip
pip install --no-cache-dir -r virtualenv
```

virtualenv

```
ansible==2.7.2
cm-api==19.1.1
```

### 2.3 部署配置

一键部署服务是根据提供的deployconfig.json进行部署的。配置文件中主要包含两大内容，一个是hosts主机信息、另一个是部署方案（目前只支持一种部署方案），Json结构如下所示：

![](http://shirukai.gitee.io/images/4773279ca26d82e3274433ab7029ba35.jpg)

#### 2.3.1 host主机信息

配置文件中的host主机信息，主要包括主机组，如manager、master、slave等，主机信息如：ip、hostname、ssh_user、ssh_pass等。内容如下：

```json
{
    "hosts": {
        "manager": [
            {
                "ip": "192.168.1.45",
                "hostname": "cdh-manager",
                "ssh_user": "root",
                "ssh_pass": "root",
                "role": "manager"
            }
        ],
        "master": [
            {
                "ip": "192.168.1.74",
                "hostname": "cdh-master",
                "ssh_user": "root",
                "ssh_pass": "root",
                "role": "master"
            }
        ],
        "slave": [
            {
                "ip": "192.168.1.75",
                "hostname": "cdh-slave1",
                "ssh_user": "root",
                "ssh_pass": "root",
                "role": "slave1"
            },
            {
                "ip": "192.168.1.77",
                "hostname": "cdh-slave2",
                "ssh_user": "root",
                "ssh_pass": "root",
                "role": "slave2"
            }
        ]
    }
}
```

#### 2.3.2 部署方案

部署方案中，目前分为两部分：基础环境部署配置、大数据服务部署配置。目前支持的部署方案为：MN、CN&DN方案，此方案MN管理节点（指的是CDH Manager）单独分设，CN控制节点（master节点）和DN数据节点合设，要求最少四台节点。

配置内容如下所示：

```json
{
    "install_plans": {
        "MN_CN&DN": {
            "description": "此方案为MN管理节点（指的是CDH Manager）单独分设，CN控制节点（master节点）和DN数据节点合设，要求最少四台节点。",
            "env_deploy": {
                "extra_vars": {
                    "ssh_key_hosts": [
                        "manager",
                        "master"
                    ],
                    "packages_path": "packages",
                    "yum_http_server": "manager",
                    "cdh_parcel_version": "6.0.0-1.cdh6.0.0.p0.537114"
                },
                "base_env": {
                    "name": "Building a basic environment.",
                    "nodes": [
                        "all"
                    ],
                    "roles": [
                        "hostnames",
                        "firewall",
                        "sshkeys"
                    ]
                },
                "install_yum_repo": {
                    "name": "Install yum repo.",
                    "nodes": [
                        "manager"
                    ],
                    "roles": [
                        "repo"
                    ]
                },
                "copy_repo": {
                    "name": "Copy repo file to hosts.",
                    "nodes": [
                        "all"
                    ],
                    "roles": [
                        "cdhrepo"
                    ]
                },
                "java": {
                    "name": "Install java",
                    "nodes": [
                        "all"
                    ],
                    "roles": [
                        "cdhjava"
                    ]
                },
                "mysql": {
                    "name": "Install mysql.",
                    "nodes": [
                        "manager"
                    ],
                    "roles": [
                        "cdhmysql"
                    ]
                },
                "cdh_manager": {
                    "name": "Install cdh manager.",
                    "nodes": [
                        "manager"
                    ],
                    "roles": [
                        "cdhmanager"
                    ]
                },
                "cdh_agent": {
                    "name": "Install cdh agent.",
                    "nodes": [
                        "all"
                    ],
                    "roles": [
                        "cdhagent"
                    ]
                }
            },
            "cloudera_manager_deploy": {
                "cluster_info": {
                    "cluster_name": "Cluster 1",
                    "cluster_version": "CDH6",
                    "admin_name": "admin",
                    "admin_pass": "admin",
                    "cm_config": {
                        "TSQUERY_STREAMS_LIMIT": 1000
                    },
                    "cmd_timeout": 180
                },
                "management": {
                    "name": "MGMT",
                    "nodes": [
                        "manager"
                    ],
                    "config": {},
                    "components": {
                        "alert_publisher": {
                            "name": "ALERTPUBLISHER",
                            "config": {},
                            "nodes": [
                                "manager"
                            ]
                        },
                        "event_server": {
                            "name": "EVENTSERVER",
                            "config": {
                                "event_server_heapsize": "215964392"
                            },
                            "nodes": [
                                "manager"
                            ]
                        },
                        "host_monitor": {
                            "name": "HOSTMONITOR",
                            "config": {},
                            "nodes": [
                                "manager"
                            ]
                        },
                        "service_monitor": {
                            "name": "SERVICEMONITOR",
                            "config": {},
                            "nodes": [
                                "manager"
                            ]
                        }
                    }
                },
                "parcels": {
                    "name": "PARCEL",
                    "config": [
                        {
                            "name": "CDH",
                            "version": "6.0.0-1.cdh6.0.0.p0.537114"
                        }
                    ]
                },
                "zookeeper": {
                    "name": "ZOOKEEPER",
                    "nodes": [
                        "master",
                        "slave"
                    ],
                    "components": {
                        "zookeeper_server": {
                            "name": "ZOOKEEPERSERVICE",
                            "config": {
                                "quorumPort": 2888,
                                "electionPort": 3888,
                                "dataLogDir": "/var/lib/zookeeper",
                                "dataDir": "/var/lib/zookeeper",
                                "maxClientCnxns": "1024"
                            },
                            "nodes": [
                                "master",
                                "slave"
                            ]
                        }
                    },
                    "config": {
                        "zookeeper_datadir_autocreate": "true"
                    }
                },
                "hdfs": {
                    "name": "HDFS",
                    "nodes": [],
                    "components": {
                        "namenode": {
                            "name": "nn",
                            "nodes": [
                                "master"
                            ],
                            "config": {
                                "dfs_name_dir_list": "/dfs/nn",
                                "dfs_namenode_handler_count": 30
                            }
                        },
                        "secondary_namenode": {
                            "name": "sn",
                            "nodes": [
                                "manager"
                            ],
                            "config": {
                                "fs_checkpoint_dir_list": "/dfs/snn"
                            }
                        },
                        "balancer": {
                            "name": "b",
                            "nodes": [
                                "manager"
                            ],
                            "config": {}
                        },
                        "datanode": {
                            "name": "dn",
                            "nodes": [
                                "master",
                                "slave"
                            ],
                            "config": {
                                "dfs_data_dir_list": "/dfs/dn",
                                "dfs_datanode_handler_count": 30,
                                "dfs_datanode_du_reserved": 1073741824,
                                "dfs_datanode_failed_volumes_tolerated": 0,
                                "dfs_datanode_data_dir_perm": 755
                            }
                        }
                    },
                    "config": {
                        "dfs_replication": 3,
                        "dfs_permissions": "false",
                        "dfs_block_local_path_access_user": "impala,hbase,mapred,spark"
                    }
                },
                "yarn": {
                    "name": "YARN",
                    "nodes": [],
                    "config": {
                        "hdfs_service": "HDFS"
                    },
                    "components": {
                        "job_history_server": {
                            "name": "JOBHISTORYSERVER",
                            "nodes": [
                                "master"
                            ],
                            "config": {}
                        },
                        "resource_manager": {
                            "name": "RESOURCEMANAGER",
                            "nodes": [
                                "master"
                            ],
                            "config": {}
                        },
                        "node_manager": {
                            "name": "NODEMANAGER",
                            "nodes": [
                                "slave"
                            ],
                            "config": {
                                "yarn_nodemanager_local_dirs": "/yarn/nm"
                            }
                        }
                    }
                },
                "hbase": {
                    "name": "HBASE",
                    "nodes": [],
                    "config": {
                        "hdfs_service": "HDFS",
                        "zookeeper_service": "ZOOKEEPER"
                    },
                    "components": {
                        "hbase_master": {
                            "name": "HBASEMASTER",
                            "nodes": [
                                "master"
                            ],
                            "config": {}
                        },
                        "hbase_region_server": {
                            "name": "HBASEREGIONSERVER",
                            "nodes": [
                                "slave"
                            ],
                            "config": {
                                "hbase_hregion_memstore_flush_size": 1024000000,
                                "hbase_regionserver_handler_count": 10,
                                "hbase_regionserver_java_heapsize": 2048000000,
                                "hbase_regionserver_java_opts": ""
                            }
                        }
                    }
                }
            }
        }
    }
}
```

通常情况下，我们只需要修改hosts中的主机清单信息即可。

## 3 部署

使用Python执行项目中的main.py

```shell
python main.py
```