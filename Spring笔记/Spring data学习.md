# Spring data 学习 

官网：http://projects.spring.io/spring-data/ 

> Spring Data的使命是为数据访问提供熟悉且一致的基于Spring的编程模型，同时仍保留底层数据存储的特殊特性。 

> 它使得使用数据访问技术，关系数据库和非关系数据库，map-reduce框架以及基于云的数据服务变得很容易。这是一个总括项目，其中包含许多特定于特定数据库的子项目。这些项目是通过与许多支持这些令人兴奋的技术的公司和开发人员合作开发的。



## 一、Spring Data 包含多个子项目： 

### 主要模块

- [Spring Data Commons](https://docs.spring.io/spring-data/commons/docs/current/reference/html/) - 支持每个Spring Data项目的核心Spring概念。
- [Spring Data Gemfire](https://projects.spring.io/spring-data-gemfire) - 从Spring应用程序中轻松配置和访问GemFire。
- [Spring Data JPA](https://projects.spring.io/spring-data-jpa) - 可以轻松实现基于JPA的存储库。
- [Spring Data JDBC](https://projects.spring.io/spring-data-jdbc) - 基于JDBC的存储库。
- [Spring Data KeyValue](https://github.com/spring-projects/spring-data-keyvalue) - `Map`基于存储库和SPI可以轻松为键值存储构建Spring Data模块。
- [Spring Data LDAP](https://projects.spring.io/spring-data-ldap) - 为[Spring LDAP](https://github.com/spring-projects/spring-ldap)提供Spring Data存储库支持。
- [Spring Data MongoDB](https://projects.spring.io/spring-data-mongodb) - 基于Spring的对象文档支持和MongoDB存储库。
- [Spring Data REST](https://projects.spring.io/spring-data-rest) - 将Spring Data存储库导出为超媒体驱动的RESTful资源。
- [Spring Data Redis](https://projects.spring.io/spring-data-redis) - 从Spring应用程序中轻松配置和访问Redis。
- [Apache Cassandra的](https://projects.spring.io/spring-data-cassandra) Spring数据 - [Apache Cassandra的](https://projects.spring.io/spring-data-cassandra) Spring Data模块。
- [Apache Solr的](https://projects.spring.io/spring-data-solr) Spring数据 - [Apache Solr的](https://projects.spring.io/spring-data-solr) Spring Data模块。

### 社区模块

- [Spring Data Aerospike](https://github.com/aerospike/spring-data-aerospike) - [Aerospike的](https://github.com/aerospike/spring-data-aerospike)弹簧数据模块。
- [Spring Data ArangoDB](https://github.com/arangodb/spring-data) - 用于ArangoDB的Spring Data模块。
- [Spring Data Couchbase](https://projects.spring.io/spring-data-couchbase) - [Couchbase的](https://projects.spring.io/spring-data-couchbase) Spring Data模块。
- [Spring Data Azure DocumentDB](https://github.com/Microsoft/spring-data-documentdb) - 用于Microsoft Azure DocumentDB的Spring Data模块。
- [Spring Data DynamoDB](https://github.com/spring-data-dynamodb/spring-data-dynamodb) - [DynamoDB的](https://github.com/spring-data-dynamodb/spring-data-dynamodb) Spring Data模块。
- [Spring Data Elasticsearch](https://projects.spring.io/spring-data-elasticsearch) - [Elasticsearch的](https://projects.spring.io/spring-data-elasticsearch) Spring Data模块。
- [Spring Data Hazelcast](https://github.com/hazelcast/spring-data-hazelcast) - 为Hazelcast提供Spring Data repository支持。
- [Spring Data Jest](https://github.com/VanRoy/spring-data-jest) - 基于Jest REST客户端的Elasticsearch的Spring数据。
- [Spring Data Neo4j](https://projects.spring.io/spring-data-neo4j) - 基于[Spring的Neo4j的](https://projects.spring.io/spring-data-neo4j)对象图支持和存储库。
- [Spring Data Vault](https://projects.spring.io/spring-vault/) - 基于Spring Data KeyValue构建的Vault存储库。

### 相关模块

- [Spring Data JDBC Extensions](https://projects.spring.io/spring-data-jdbc-ext) - 提供Spring Framework中提供的对JDBC支持的扩展。
- [Spring for Apache Hadoop](https://projects.spring.io/spring-hadoop) - 通过提供统一的配置模型和易于使用的API来使用HDFS，MapReduce，Pig和Hive，简化Apache Hadoop。
- [Spring内容](https://paulcwarren.github.io/spring-content/) - 将内容与您的Spring Data Entities相关联，并将其存储在多个不同的商店，包括文件系统，S3，数据库或Mongo的GridFS。

## 二、传统方式访问数据库 

### JDBC 

Connection 

Statement 

ResultSet

Test Case  单元测试

### Spring JdbcTemplate 

### 弊端分析 

![](https://shirukai.gitee.io/images/201803211544_373.png)





