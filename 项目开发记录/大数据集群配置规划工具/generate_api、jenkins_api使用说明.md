# generate_api、jenkins_api使用说明

## 准备 

#### pip安装python_jenkins包

```
pip install python-jenkins
```

#### 复制自定义python包

复制项目中的indata_pack目录到python的site-packages下。

> 位置：indata_dev\indata_tool_api\indata_pack

#### indata_pack说明 

##### 目录结构：

![](https://shirukai.gitee.io/images/201801311507_372.png)

##### config_base目录

主要存放jenkins执行时需要的配置文件config.xml以及其他的一些脚本文件

##### config_template目录

存放生成配置文件的模板

##### generate_api .py

生成配置文件的类

##### jenkins_api.py

调用jenkins的类

##### params.py 

定义相关变量，如生成文件的位置、复制文件位置、目录结构、jenkins的所在ip、端口号、用户名、密码等信息

## 一、generate_api 说明

```
def generate_config():
	# 定义配置生成配置文件的名字
    config_name = 'TestApi'
    # 从本地文件读取json数据
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.json')
    with open(data_path) as f:
        data = f.read()
    # 调用 generate_api
    gr = generate_api.GenerateApi(config_name)
    # 构建生成配置文件的参数
    params = gr.generate_params(json.loads(data))
    # 生成配置文件
    gr.generate_config(params)
    # 输出 文件路径
    print(gr.config_path)
    return gr.config_path
```

需要的json格式：

```
{
  "blueprint": {
    "atlas_rest_address": "indatatest-10-110-13-164.test.com",
    "range_admin_db_name": "ranger",
    "ranger_plugin_kafka_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "db_root_user": "root",
    "range_admin_db_password": "123456Aa?",
    "hbase_rest_kerberos_principal": "TEST.COM",
    "admin_server_host": "10.110.13.166",
    "range_kms_db_name": "rangerkms",
    "ranger_plugin_nifi_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "javax_jdo_option_ConnectionPassword": "hive11111",
    "logsearch_nginx_cluster": "10.110.13.163",
    "nifi_security_encrypt_configuration_password": "1234567890a?",
    "ranger_ks_jpa_jdbc_url": "indatatest-10-110-13-163.test.com",
    "KMS_MASTER_KEY_PASSWD": "123456Aa?",
    "hadoop_kms_key_provider_path": "indatatest-10-110-13-164.test.com",
    "knox_request_hostip": "10.110.13.163",
    "ranger_privelege_user_jdbc_url": "indatatest-10-110-13-163.test.com",
    "nifi_realm": "tenant",
    "range_kms_db_password": "123456Aa?",
    "ranger_admin_password": "123456Aa?",
    "ranger_plugin_knox_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "kdc_hosts": "10.110.13.166",
    "ranger_plugin_hive_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "nifi_security_user_knox_url": "10.110.13.163",
    "blueprint_name": "indata",
    "nifi_nginx_dev": "10.110.13.163",
    "nifi_initial_admin_identity": "nifiadmin-tenant",
    "ranger_plugin_yarn_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "range_kms_db_user": "rangerkms",
    "range_admin_db_user": "rangeradmin",
    "logsearch_auth_jwt_provider_url": "10.110.13.163",
    "nifi_nginx_cluster": "10.110.13.163",
    "keycloak_dev_realm": "tenant",
    "ranger_audit_solr_zookeepers": "indatatest-10-110-13-163.test.com:2181,indatatest-10-110-13-164.test.com:2181,indatatest-10-110-13-165.test.com:2181",
    "ranger_plugin_hdfs_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "ranger_jpa_jdbc_url": "indatatest-10-110-13-163.test.com",
    "host_groups": [
      {
        "cardinality": 1,
        "name": "master1",
        "components": [
          {
            "name": "KERBEROS_CLIENT"
          },
          {
            "name": "LOGSEARCH_LOGFEEDER"
          },
          {
            "name": "ZOOKEEPER_SERVER"
          },
          {
            "name": "KNOX_GATEWAY"
          },
          {
            "name": "ES_SERVER"
          },
          {
            "name": "HBASE_REGIONSERVER"
          },
          {
            "name": "NIFI_CA"
          },
          {
            "name": "METRICS_MONITOR"
          },
          {
            "name": "DATANODE"
          },
          {
            "name": "KAFKA_BROKER"
          },
          {
            "name": "NIFI_MASTER"
          },
          {
            "name": "ATLAS_CLIENT"
          },
          {
            "name": "SQOOP"
          },
          {
            "name": "JOURNALNODE"
          },
          {
            "name": "NODEMANAGER"
          },
          {
            "name": "LOGSEARCH_SERVER"
          }
        ]
      },
      {
        "cardinality": 1,
        "name": "master2",
        "components": [
          {
            "name": "INFRA_SOLR_CLIENT"
          },
          {
            "name": "KERBEROS_CLIENT"
          },
          {
            "name": "LOGSEARCH_LOGFEEDER"
          },
          {
            "name": "METRICS_COLLECTOR"
          },
          {
            "name": "RANGER_TAGSYNC"
          },
          {
            "name": "ZOOKEEPER_SERVER"
          },
          {
            "name": "NAMENODE"
          },
          {
            "name": "HBASE_CLIENT"
          },
          {
            "name": "ES_SERVER"
          },
          {
            "name": "HBASE_REGIONSERVER"
          },
          {
            "name": "METRICS_MONITOR"
          },
          {
            "name": "DATANODE"
          },
          {
            "name": "RANGER_USERSYNC"
          },
          {
            "name": "KAFKA_BROKER"
          },
          {
            "name": "NIFI_MASTER"
          },
          {
            "name": "ATLAS_CLIENT"
          },
          {
            "name": "SQOOP"
          },
          {
            "name": "ZOOKEEPER_CLIENT"
          },
          {
            "name": "JOURNALNODE"
          },
          {
            "name": "MAPREDUCE2_CLIENT"
          },
          {
            "name": "SPARK2_CLIENT"
          },
          {
            "name": "INFRA_SOLR"
          },
          {
            "name": "HDFS_CLIENT"
          },
          {
            "name": "RANGER_KMS_SERVER"
          },
          {
            "name": "RANGER_ADMIN"
          },
          {
            "name": "NODEMANAGER"
          },
          {
            "name": "ZKFC"
          },
          {
            "name": "HCAT"
          },
          {
            "name": "METRICS_GRAFANA"
          },
          {
            "name": "HIVE_METASTORE"
          },
          {
            "name": "RESOURCEMANAGER"
          },
          {
            "name": "HIVE_CLIENT"
          },
          {
            "name": "YARN_CLIENT"
          },
          {
            "name": "WEBHCAT_SERVER"
          },
          {
            "name": "HBASE_MASTER"
          },
          {
            "name": "HIVE_SERVER"
          },
          {
            "name": "ATLAS_SERVER"
          }
        ]
      },
      {
        "cardinality": 1,
        "name": "master3",
        "components": [
          {
            "name": "KERBEROS_CLIENT"
          },
          {
            "name": "LOGSEARCH_LOGFEEDER"
          },
          {
            "name": "HISTORYSERVER"
          },
          {
            "name": "METRICS_COLLECTOR"
          },
          {
            "name": "PIG"
          },
          {
            "name": "ZOOKEEPER_SERVER"
          },
          {
            "name": "NAMENODE"
          },
          {
            "name": "TEZ_CLIENT"
          },
          {
            "name": "ES_SERVER"
          },
          {
            "name": "HBASE_REGIONSERVER"
          },
          {
            "name": "SPARK2_THRIFTSERVER"
          },
          {
            "name": "METRICS_MONITOR"
          },
          {
            "name": "DATANODE"
          },
          {
            "name": "KAFKA_BROKER"
          },
          {
            "name": "NIFI_MASTER"
          },
          {
            "name": "SPARK2_JOBHISTORYSERVER"
          },
          {
            "name": "ATLAS_CLIENT"
          },
          {
            "name": "SQOOP"
          },
          {
            "name": "JOURNALNODE"
          },
          {
            "name": "NODEMANAGER"
          },
          {
            "name": "ZKFC"
          },
          {
            "name": "SLIDER"
          },
          {
            "name": "HIVE_METASTORE"
          },
          {
            "name": "RESOURCEMANAGER"
          },
          {
            "name": "WEBHCAT_SERVER"
          },
          {
            "name": "HBASE_MASTER"
          },
          {
            "name": "APP_TIMELINE_SERVER"
          },
          {
            "name": "HIVE_SERVER"
          }
        ]
      }
    ],
    "keycloak_auth_url": "10.110.13.163",
    "javax_jdo_option_ConnectionURL": "10.110.13.163",
    "nifi_security_user_knox_cookieName": "tenant-jw",
    "policymgr_external_url": "indatatest-10-110-13-164.test.com",
    "nifi_admin_ssl_config_content": "<property name='Node Identity1'>CN=indatatest-10-110-13-163.test.com, OU=NIFI</property>\n<property name='Node Identity2'>CN=indatatest-10-110-13-164.test.com, OU=NIFI</property>\n<property name='Node Identity3'>CN=indatatest-10-110-13-165.test.com, OU=NIFI</property>",
    "db_host": "10.110.13.163",
    "ranger_plugin_hbase_policy_rest_url": "indatatest-10-110-13-164.test.com",
    "db_root_password": "123456Aa?",
    "domains": "TEST.COM",
    "hbase_rest_authentication_kerberos_principal": "TEST.COM",
    "ranger_plugin_atlas_policy_rest_url": "indatatest-10-110-13-164.test.com"
  },
  "new_cluster": {
    "mysql_idap_password": "idap",
    "ambari_nifi_hostip": [
      "10.110.13.163",
      "10.110.13.164",
      "10.110.13.165"
    ],
    "keycloak_dev_realm": "tenant",
    "ambari_logsearch_hostip": "10.110.13.163",
    "ldap_rootdn_password": "123456a?",
    "interface": "eth0",
    "manager_hosts": [
      "10.110.13.163",
      "10.110.13.164"
    ],
    "openldap_base": "dc=test,dc=com",
    "mysql_root_password": "123456Aa?",
    "mysql_keycloak_password": "123456Aa?",
    "ambari_knox_hostip": "10.110.13.163",
    "floating_ip_map": {},
    "blueprint_name": "indata",
    "krb5kdc_admin_principal": "root",
    "mysql_hive_password": "hive11111",
    "virtual_ipaddress": "10.110.13.166",
    "controler_hosts": [
      "10.110.13.163",
      "10.110.13.164",
      "10.110.13.165"
    ],
    "ambari_clustername": "InDataTest",
    "krb5kdc_realm": "TEST.COM",
    "hostinfo": [
      {
        "password": "123456a?",
        "hostname": "indatatest-10-110-13-163.test.com",
        "hostip": "10.110.13.163"
      },
      {
        "password": "123456a?",
        "hostname": "indatatest-10-110-13-164.test.com",
        "hostip": "10.110.13.164"
      },
      {
        "password": "123456a?",
        "hostname": "indatatest-10-110-13-165.test.com",
        "hostip": "10.110.13.165"
      }
    ],
    "ambari_kafka_hostip": "10.110.13.163",
    "virtual_ipfqdn": "indatatest-10-110-13-166.test.com",
    "ambari_ranger_hostip": "10.110.13.164"
  },
  "shell": {
    "root_pwd": "123456a?",
    "ambari_server_ip": "10.110.13.163"
  },
  "node_info": [
    {
      "passwd": "123456a?",
      "ip": "10.110.13.243",
      "hostname": "indatatest-10-110-13-243.test.com"
    },
    {
      "passwd": "123456a?",
      "ip": "10.110.13.243",
      "hostname": "indatatest-10-110-13-243.test.com"
    },
    {
      "passwd": "123456a?",
      "ip": "10.110.13.243",
      "hostname": "indatatest-10-110-13-243.test.com"
    }
  ],
  "host_map": {
    "blueprint": "indata",
    "kerberos_user": "root",
    "kerberos_admin_pwd": "123456a?",
    "cluster_name": "InDataTest",
    "host_groups": [
      {
        "hosts": [
          {
            "fqdn": "indatatest-10-110-13-163.test.com"
          }
        ],
        "name": "master1"
      },
      {
        "hosts": [
          {
            "fqdn": "indatatest-10-110-13-164.test.com"
          }
        ],
        "name": "master2"
      },
      {
        "hosts": [
          {
            "fqdn": "indatatest-10-110-13-165.test.com"
          }
        ],
        "name": "master3"
      }
    ],
    "default_password": "123456a?"
  },
  "disk_partition": []
}
```

## 二、jenkins_api说明

```
# 启动
def start_jenkins():
    # config_path 生成配置文件后返回的路径
    config_path = 'D:\\tmp\indata_config\TestApi1517384088.06'
    # 节点用户名
    username = 'root'
    # root 密码
    password = '123456a?'
    # 节点ip
    node_ip = '10.110.13.243'
    # node_name
    node_name = 'ambari_server' + node_ip
    # job_name 带时间戳的配置名
    job_name = 'TestApi' + str(time.time())
    jenkins = jenkins_api.JenkinsApi()
    # 复制文件，将生成的配置文件复制到 指定节点的/opt目录下
    (sh_state, output) = jenkins.copy_file(config_path)
    # sh_state=0表示执行成功，output为输出信息
    if sh_state == 0:
        # 创建 node
        jenkins.create_node(node_name, job_name, username, password, node_ip)
        # 创建job 并启动
        jenkins.create_job(node_name, job_name, node_ip)
    else:
        print(output)


# 停止
def stop_jenkins():
    job_name = "TestApi1517386158.76"
    jenkins = jenkins_api.JenkinsApi()
    jenkins.stop_job(job_name)


# 重新开始
def restart_jenkins():
    job_name = "TestApi1517386158.76"
    jenkins = jenkins_api.JenkinsApi()
    jenkins.start_job(job_name)
```

