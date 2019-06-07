# azkaban job类型

## Spark

job

```
type=spark
master=local
execution-jar=azkaban.jar
class=com.azkaban.hollysys.main
params=hdfs://192.168.66.192:8020/user/root/srk/input/words.txt hdfs://192.168.66.192:8020/user/root/srk/output/wordcount
```

jar

```
package com.azkaban.hollysys.spark

import org.apache.hadoop.fs.Path
import org.apache.spark.{SparkConf, SparkContext}

object wordCount {
  def run(input: String, output: String): Unit = {
    val conf = new SparkConf().setAppName("srk_word_count")
    val sc = new SparkContext(conf)
    val textFile = sc.textFile(input)
    val counts = textFile.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey(_ + _)
    //如果目录存在则删除
    val out = new Path(output)
    val hdfs = org.apache.hadoop.fs.FileSystem.get(
      new java.net.URI("hdfs://master:9000"), new org.apache.hadoop.conf.Configuration())
    counts.saveAsTextFile(output)
  }
}
```

