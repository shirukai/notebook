# HBase基本概念及知识点

## HBase 写流程

![](http://shirukai.gitee.io/images/b0f204f57713df7a54aaa51028cc7307.jpg)

* Client会县访问zookeeper，得到对应的RegionServer地址
* Clinet对RegionServer发起请求，RegionServer接收数据写入内
* 当MemStore的大小达到一定的值后，flush到StoreFile并存储到HDFS

![](http://shirukai.gitee.io/images/07b7d596a9aa320b48b333afd36195f4.jpg)

HBase中的WAL（预写日志）的实现：https://www.cnblogs.com/ohuang/p/5807543.html

## HBase的读流程

![](http://shirukai.gitee.io/images/0f9b89b3da0fa872b9091e9add63b691.jpg)

* Client会先访问zookeeper，得到对应的RegionServer地址
* Client对RegionServer发起读请求
* 当RegionServer收到client的读请求后，先扫描哦自己的Memstore，再扫描BlockCache（加速读内容缓存区）如果换没找到则StoreFile读取数据，然后将数据返回给Client

## HBase 模块协作

### HBase启动时发生了什么？

* HMaster启动，注册到Zookeeper，等待RegionServer汇报
* RegionServer注册到Zookeeper，并向HMaster汇报
* 对各个RegionServer（包括失效的）的数据进行整理，分配Region和meta信息

### 当RegionServer失效后会发生什么？

* HMaster将失效RegionServer上的Region分配到其他节点
* HMaster更新hbase：meta表以保证数据正常访问

### 当HMaster失效后会发生什么？

* 处于Backup状态的其他HMaster节点推选出一个转为Active状态（配置高可用）
* 数据能正常读写，但是不能创建删除表，也不能更改表结构（未配置高可用）

## HBase操作

### HBase Shell 命令

![](http://shirukai.gitee.io/images/a219b1b1a92e19620bae1c7ecdea7dda.jpg)

#### 1 查看集群状态: status

```shell
hbase(main):001:0> status
1 active master, 0 backup masters, 1 servers, 1 dead, 6.0000 average load
Took 0.7064 seconds
```

#### 2 查看所有表：list

```shell
hbase(main):003:0> list
TABLE                                                                                                         
coures_clickcount                                                                                             
course_search_clickcount                                                                                      
member                                                                                                        
table1                                                                                                        
4 row(s)
Took 0.0236 seconds                                                                                           
=> ["coures_clickcount", "course_search_clickcount", "member", "table1"]
```

#### 3 创建一张表：create  'tableName' 'columnFamily'

创建一张名为FileTable的表，包含两个列族，分别为fileInfo和saveInfo

```shell
hbase(main):004:0> create 'FileTable','fileInfo','saveInfo'
Created table FileTable
Took 0.8806 seconds                                                                                           
=> Hbase::Table - FileTable
```

#### 4 查看表的描述信息：desc 'tableName'

```shell
hbase(main):005:0> desc 'FileTable'
Table FileTable is ENABLED                                                                                    
FileTable                                                                                                     
COLUMN FAMILIES DESCRIPTION                                                                                   
{NAME => 'fileInfo', VERSIONS => '1', EVICT_BLOCKS_ON_CLOSE => 'false', NEW_VERSION_BEHAVIOR => 'false', KEEP_
DELETED_CELLS => 'FALSE', CACHE_DATA_ON_WRITE => 'false', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', MIN
_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', CACHE_INDEX_ON_WRITE => 'false', IN_MEMORY =
> 'false', CACHE_BLOOMS_ON_WRITE => 'false', PREFETCH_BLOCKS_ON_OPEN => 'false', COMPRESSION => 'NONE', BLOCKC
ACHE => 'true', BLOCKSIZE => '65536'}                                                                         
{NAME => 'saveInfo', VERSIONS => '1', EVICT_BLOCKS_ON_CLOSE => 'false', NEW_VERSION_BEHAVIOR => 'false', KEEP_
DELETED_CELLS => 'FALSE', CACHE_DATA_ON_WRITE => 'false', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', MIN
_VERSIONS => '0', REPLICATION_SCOPE => '0', BLOOMFILTER => 'ROW', CACHE_INDEX_ON_WRITE => 'false', IN_MEMORY =
> 'false', CACHE_BLOOMS_ON_WRITE => 'false', PREFETCH_BLOCKS_ON_OPEN => 'false', COMPRESSION => 'NONE', BLOCKC
ACHE => 'true', BLOCKSIZE => '65536'}                                                                         
2 row(s)
Took 0.3854 seconds 
```

#### 5 修改表结构：alter

##### 添加一个列族 alter 'tableName','addColumnFamily'

```shell
alter 'FileTable','test'
+Updating all regions with the new schema...
1/1 regions updated.
Done.
Took 1.8539 seconds        
```

##### 删除一个列族 aleter 'tableName',{NAME=>'columnFamily',METHOD=>'delete'}

```shell
 alter 'FileTable',{NAME=>'test',METHOD=>'delete'}
Updating all regions with the new schema...
1/1 regions updated.
Done.
Took 1.8177 seconds   
```

#### 6 插入数据：put 'tableName','rowkey','columnFamily:field','value'

```shell
hbase(main):008:0> put 'FileTable','rowkey1','fileInfo:name','file1.txt'
Took 0.1394 seconds                                                                                           
hbase(main):009:0> put 'FileTable','rowkey1','fileInfo:type','txt'
Took 0.0041 seconds                                                                                           
hbase(main):010:0> put 'FileTable','rowkey1','fileInfo:size','1024'
Took 0.0048 seconds                                                                                           
hbase(main):011:0> put 'FileTable','rowkey1','saveInfo:path','/home'
Took 0.0052 seconds                                                                                           
hbase(main):012:0> put 'FileTable','rowkey1','saveInfo:creator','srk'
Took 0.0061 seconds     
```

#### 7 查看表有多少行数据：count 'tableName'

```shell
hbase(main):013:0> count 'FileTable'
1 row(s)
Took 0.0676 seconds                                                                                           
=> 1
```

#### 8 查询数据 get

##### 使用get按照rowkey查询: get 'tableName','rowKey'

```shell
hbase(main):005:0> get 'FileTable','rowkey1'
COLUMN                CELL                                                      
 fileInfo:name        timestamp=1542166201745, value=file1.txt                  
 fileInfo:size        timestamp=1542166236481, value=1024                       
 fileInfo:type        timestamp=1542166217417, value=txt                        
 saveInfo:creator     timestamp=1542166283601, value=srk                        
 saveInfo:path        timestamp=1542166258675, value=/home                      
1 row(s)
Took 0.0281 seconds 
```

##### 使用get按照rowkey查询某个列族: get 'tableName','rowKey','cloumnFamily'

```
hbase(main):006:0> get 'FileTable','rowkey1','fileInfo'
COLUMN                CELL                                                      
 fileInfo:name        timestamp=1542166201745, value=file1.txt                  
 fileInfo:size        timestamp=1542166236481, value=1024                       
 fileInfo:type        timestamp=1542166217417, value=txt                        
1 row(s)
Took 0.0260 seconds  
```

##### 使用get按照rowkey查询某个列子的某个字段: get 'tableName','rowKey','cloumnFamily:field'

```
hbase(main):008:0> get 'FileTable','rowkey1','fileInfo:name'
COLUMN                CELL                                                      
 fileInfo:name        timestamp=1542166201745, value=file1.txt                  
1 row(s)
Took 0.0169 seconds 
```

#### 9 查看整张表的数据 scan

##### 查看整张表的所有数据数据： scan 'tableName'

```shell
hbase(main):009:0> scan 'FileTable'
ROW                   COLUMN+CELL                                               
 rowkey1              column=fileInfo:name, timestamp=1542166201745, value=file1
                      .txt                                                      
 rowkey1              column=fileInfo:size, timestamp=1542166236481, value=1024 
 rowkey1              column=fileInfo:type, timestamp=1542166217417, value=txt  
 rowkey1              column=saveInfo:creator, timestamp=1542166283601, value=sr
                      k                                                         
 rowkey1              column=saveInfo:path, timestamp=1542166258675, value=/home
1 row(s)
Took 0.0905 seconds
```

##### 查看某个列族的所有数据：scan 'tableName',{COLUMN=>'columnFamily'}

```shell
hbase(main):010:0> scan 'FileTable',{COLUMN=>'fileInfo'}
ROW                   COLUMN+CELL                                               
 rowkey1              column=fileInfo:name, timestamp=1542166201745, value=file1
                      .txt                                                      
 rowkey1              column=fileInfo:size, timestamp=1542166236481, value=1024 
 rowkey1              column=fileInfo:type, timestamp=1542166217417, value=txt  
1 row(s)
Took 0.0191 seconds 
```

##### 查看某个列族的某个字段的所有数据：scan 'tableName',{COLUMN=>'columnFamily:field'}

```shell
hbase(main):011:0> scan 'FileTable',{COLUMN=>'fileInfo:name'}
ROW                   COLUMN+CELL                                               
 rowkey1              column=fileInfo:name, timestamp=1542166201745, value=file1
                      .txt                                                      
1 row(s)
Took 0.0051 seconds  
```

##### scan 条件：STARTROW、LIMIT、VERSIONS、ENDROW

```shell
hbase(main):015:0> scan 'FileTable',{STARTROW=>'rowkey1',ENDROW=>'rowkey2',LIMIT=>2,VERSIONS=>1}
ROW                   COLUMN+CELL                                               
 rowkey1              column=fileInfo:name, timestamp=1542166201745, value=file1
                      .txt                                                      
 rowkey1              column=fileInfo:size, timestamp=1542166236481, value=1024 
 rowkey1              column=fileInfo:type, timestamp=1542166217417, value=txt  
 rowkey1              column=saveInfo:creator, timestamp=1542166283601, value=sr
                      k                                                         
 rowkey1              column=saveInfo:path, timestamp=1542166258675, value=/home
1 row(s)
Took 0.0093 seconds       
```

#### 10 删除数据

##### 删除某一列的数据：delete 'tableName','rowKey','columnFamily:field'

```shell
hbase(main):016:0> delete 'FileTable','rowkey1','fileInfo:size'
Took 0.0628 seconds                                                             
hbase(main):017:0> get 'FileTable','rowkey1','fileInfo:size'
COLUMN                CELL                                                      
0 row(s)
Took 0.0113 seconds 
```

##### 删除某一行的数据：deleteall 'tableName','rowKey'

```shell
hbase(main):023:0> deleteall 'FileTable','rowkey1'
Took 0.0118 seconds                                                             
hbase(main):024:0> get 'FileTable','rowkey1'
COLUMN                CELL                                                      
0 row(s)
Took 0.0156 seconds
```

#### 11 删除表

先禁用表在删除表 

disable 'tableName'

drop 'tableName'

```shell
hbase(main):025:0> disable 'FileTable'
Took 1.3645 seconds                                                             
hbase(main):026:0> is_enabled 'FileTable'
false                                                                           
Took 0.0067 seconds                                                             
=> false
hbase(main):027:0> is_disabled 'FileTable'
true                                                                            
Took 0.0077 seconds                                                             
=> 1
hbase(main):028:0> drop 'FileTable'
Took 0.4925 seconds  
```

### Java 操作HBase

![](http://shirukai.gitee.io/images/ab5d15aa2f8ba54e3083a72a13f7fbea.jpg)

## HBase进阶

### HBase 优化策略

什么导致HBase性能下降：

* Jvm内存分配与GC回收策略
* 与HBae运行机制相关的部分配置不合理
* 表结构设计及用户使用方式不合理

#### HBase服务端优化

Jvm设置与GC设置

hbase-site.xml部分属性配置

![](http://shirukai.gitee.io/images/fd7ad1cc41d20bc85e57a685cd3ae2f7.jpg)

| HBase properties                        | 简介                                                         | 默认值        |
| --------------------------------------- | ------------------------------------------------------------ | ------------- |
| hbase.regionserver.handler.count        | rpc 请求的线程数量                                           | 10            |
| hbase.hregion.max.filesize              | 当region的大小大于设定值后hbase就会开始split                 | 10G           |
| hbase.hregion.majorcompaction           | major compaction 的执行周期                                  | 1000建议设为0 |
| hbase.hstore.compaction.min             | 一个store里的storefile总数超过该值，会触发默认的合并操作     | 3             |
| hbase.hstore.compaction.max             | 一次最多合并多少个storefile                                  |               |
| hbase.hstore.blockingStorefiles         | 一个region钟的Strore(CoulmnFamily)内有超过xx个storefile时，则block所有的写请求进行compaction |               |
| hfile.block.cache.size                  | regionserver的block cache 的内存大小限制                     |               |
| hbase.hregion.memstore.flush.size       | memstore超过该值将被flush                                    |               |
| hbase.hregion.memstore.block.multiplier | 如果memstore的内存大小超过flush.size*multiplier，会阻塞该memstore的写操作 |               |

#### HBase 常用优化

* 预先分区
* RowKey优化
* Column优化
* Schema优化

##### 预先分区

创建HBase表的时候回自动创建一个Region分区

创建HBase表的时候预先创建一些空的Regions

##### Rowkey优化

* 利用HBase默认排序特点，将一起访问的数据放到一起
* 防止热点问题，避免使用时序或者单调的递增递减等

##### Column优化

* 列族的名称和列的描述命名尽量简短
* 同一张表中ColumnFamily的数量不要超过3个

##### Schema优化

* 宽表：一种“列多行少”的设计
* 高表：一种“列少行多”的设计

#### HBase 写优化策略

* 同步批量提交or异步批量提交
* WAL优化，是否必须，持久化等级

#### HBase读优化策略

* 客户端：Scan缓存设置，批量获取
* 服务端：BlockCache配置是否合理，HFile是否过多
* 表结构的设计问题



#### HBase Coprocessor

HBase协处理受BigTable协处理器的启发，为用户提供类库和运行时环境，使得代码能够在HBase RegionServer和Master上处理

系统协处理器and表协处理器

Observer and Endpoint

系统协处理器：全局加载到RegionServer托管的所有表和Region上

表协处理器：用户可以指定一张表使用协处理器

观察者（Observer）：类似于关系数据库的触发器

终端（Endpoint）：动态的终端有点像存储过程

##### Observer

RegionObserver:提供客户端的数据操纵时间钩子：Get、Put、Delete、Scan等

MasterObserver：提供DDL类型的操作钩子，如创建、删除、修改、数据表等

WALObserver：提供WAL相关操作钩子