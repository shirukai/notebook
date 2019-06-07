# Hadoop推荐算法-基于物品的协同过滤ItemCF

算法思想：给用户推荐那些和他们之前喜欢的物品相似的物品 

## 用户行为与权重 

1. 点击——1.0分
2. 搜索——3.0分
3. 收藏——5.0分
4. 付款——10.0分

## 实例

### 现有如下用户、商品、行为、权重: 

用户:A、B、C

商品:1、2、3、4、5、6

行为:点击(1)、搜索（2）、收藏（5）、付款（10）

### 用户行为列表 

| 用户   | 物品   | 行为   |
| ---- | ---- | ---- |
| A    | 1    | 点击   |
| C    | 3    | 收藏   |
| B    | 2    | 搜索   |
| B    | 5    | 搜索   |
| B    | 6    | 收藏   |
| A    | 2    | 付款   |
| C    | 3    | 付款   |
| C    | 4    | 收藏   |
| C    | 1    | 收藏   |
| A    | 1    | 点击   |
| A    | 6    | 收藏   |
| A    | 4    | 搜索   |

### 步骤 

1.根据用户行为列表计算用户、物品的评分矩阵

![https://shirukai.gitee.io/images/1510464415461W9DA_SUE~_JF8KHM8__DS0Y.png](https://shirukai.gitee.io/images/1510464415461W9DA_SUE~_JF8KHM8__DS0Y.png)

2.根据用户、物品的评分矩阵计算物品与物品的相似度矩阵

![https://shirukai.gitee.io/images/1510464508136C_B4JV_NJ41`HGY9_ZKY90H.png](https://shirukai.gitee.io/images/1510464508136C_B4JV_NJ41`HGY9_ZKY90H.png)



![https://shirukai.gitee.io/images/1510464812670`7Y9Q__RP`HPE4S3`C11_@9.png](https://shirukai.gitee.io/images/1510464812670`7Y9Q__RP`HPE4S3`C11_@9.png)

3.相似度矩阵X评分矩阵 = 推荐列表

![https://shirukai.gitee.io/images/1510464967129CKAQL8JCA`_LLIK_W_Z_TZ0.png](https://shirukai.gitee.io/images/1510464967129CKAQL8JCA`_LLIK_W_Z_TZ0.png)

4.将之前用户已经发生过的的行为置零，得到推荐列表。

## 代码实现 

代码实现是在《IDEA向hadoop集群提交MapReduce环境搭建》文章中搭建的项目基础上实现的。以下配置Hadoop连接、对HDFS文件操作的代码没有贴出，详情参考上一篇文章。

![https://shirukai.gitee.io/images/1510465483735A_4U_YD@LN1_RQD_`MCRS7L.png](https://shirukai.gitee.io/images/1510465483735A_4U_YD@LN1_RQD_`MCRS7L.png)

### 项目结构

![https://shirukai.gitee.io/images/1510544170486__9FF5`EZP`_9HB@F_7K_4D.png](https://shirukai.gitee.io/images/1510544170486__9FF5`EZP`_9HB@F_7K_4D.png)

### Step1 根据用户行为列表构建评分矩阵 

输入：用户ID，物品ID，分值

```
A,1,1
C,3,5
B,2,3
B,5,3
B,6,5
A,2,10
C,3,10
C,4,5
C,1,5
A,1,1
A,6,5
A,4,3
```

输出：物品ID，用户ID分值

```
1	A_2,C_5
2	A_10,B_3
3	C_15
4	A_3,C_5
5	B_3
6	A_5,B_5
```

#### 分析：

Mapper部分

按行读取输入文件，然后以逗号拆分数据，输出key为itemId，value为 userId_score

Reducer部分

读取Mapper后的结果，然后for循环values得到userIdAndScore，然后以"_"分割，得到userId和score

将userId和socre以map容器存保存，保存之前先判断userId是否为空，如果为空，说明之前没有出现过，直接保存到map里，如果不为空，说明userId之前出现过，这时候就要获取之前的score值加上当前的score值，依次类推得到最后的总分。

然后遍历map输出Reducer

#### 代码实现：

##### mapper1

```
package org.hadoop.mrs.itemCF.step1;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/12.
 */
public class Mapper1 extends Mapper<LongWritable, Text, Text, Text> {
    //定义输出key
    private Text outKey = new Text();
    //定义输出value
    private Text outValue = new Text();

    /**
     *
     * @param key 行号 1 2 3
     * @param value 输入文件文本的值 A,1,1（用户ID，物品ID，分值)
     * @param context context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] values = value.toString().split(",");
        String userID = values[0];
        String itemID = values[1];
        String score = values[2];

        outKey.set(itemID);
        outValue.set(userID+"_"+score);
        context.write(outKey,outValue);
    }
}

```

#### Reducer1 

```
package org.hadoop.mrs.itemCF.step1;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Reducer1
 * Created by shirukai on 2017/11/12.
 */
public class Reducer1 extends Reducer<Text, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        String itemID = key.toString();
        //<userID,sore>
        Map<String, Integer> map = new HashMap<String, Integer>();
        for (Text value :values){
            String userID = value.toString().split("_")[0];
            String score = value.toString().split("_")[1];
            if (map.get(userID) == null){
                map.put(userID,Integer.valueOf(score));
            }else {
                Integer preScore = map.get(userID);
                map.put(userID,preScore+Integer.valueOf(score));
            }
        }
        StringBuilder sBuilder = new StringBuilder();
        for (Map.Entry<String,Integer> entry: map.entrySet()
             ) {
            String userID = entry.getKey();
            String score = String.valueOf(entry.getValue());
            sBuilder.append(userID+"_"+score+",");
        }
        String line = null;
        //去掉末尾的“，”
        if (sBuilder.toString().endsWith(",")){
            line = sBuilder.substring(0,sBuilder.length()-1);
        }
        outKey.set(itemID);
        outValue.set(line);
        context.write(outKey,outValue);
    }
}

```

##### MR1

```
package org.hadoop.mrs.itemCF.step1;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.log4j.Logger;
import org.hadoop.conf.Conf;


import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/12.
 */
public class MR1 {
    private static Logger logger = Logger.getLogger("MR1");
    //输入文件的相对路径
    private static String inPath = "/itemCF/step1/step1_input/itemCF.txt";
    //输出文件的相对路径
    private static String outPath = "/itemCF/step1/step1_output";

    public static int run(){
        try {
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step1");

            //设置job的主类
            job.setJarByClass(MR1.class);
            //设置job的Mapper类和Reducer类
            job.setMapperClass(Mapper1.class);
            job.setReducerClass(Reducer1.class);

            //设置Mapper的输出类型
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);

            //设置Reducer的输出类型
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            //设置输入和输出路径
            FileSystem fs = FileSystem.get(conf);
            Path inputPath = new Path(inPath);
            if (fs.exists(inputPath)){
                FileInputFormat.addInputPath(job,inputPath);
            }
            Path outputPath = new Path(outPath);
            fs.delete(outputPath,true);

            FileOutputFormat.setOutputPath(job,outputPath);
            return job.waitForCompletion(true)?1:-1;
        }catch (IOException e){
            logger.error(e.getMessage());
        }catch (ClassNotFoundException e){
            logger.error(e.getMessage());
        }catch (InterruptedException e){
            logger.error(e.getMessage());
        }
        return -1;
    }
}
```

### Step2 利用评分矩阵，求出物品与物品的相似度矩阵

输入：step1的输出

```
1	A_2,C_5
2	A_10,B_3
3	C_15
4	A_3,C_5
5	B_3
6	A_5,B_5
```

缓存：step1的输出

```
1	A_2,C_5
2	A_10,B_3
3	C_15
4	A_3,C_5
5	B_3
6	A_5,B_5
```

输出：

```
1	1_1.00,2_0.36,3_0.93,4_0.99,6_0.26
2	1_0.36,2_1.00,4_0.49,5_0.29,6_0.88
3	4_0.86,3_1.00,1_0.93
4	1_0.99,4_1.00,6_0.36,3_0.86,2_0.49
5	2_0.29,5_1.00,6_0.71
6	1_0.26,5_0.71,6_1.00,2_0.88,4_0.36
```

#### 分析：

Mapper2 首先读取缓存，并存入list里。然后遍历缓存，遍历输入。利用公式求出相似度，然后输出

Reducer2处理数据后输出

#### 代码实现

##### Mapper2

```
package org.hadoop.mrs.itemCF.step2;

import org.apache.commons.math3.analysis.function.Acos;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

/**
 * 根据用户、物品的评分矩阵计算物品与物品的相似度矩阵 评分矩阵*评分矩阵
 * Created by shirukai on 2017/11/12.
 */
public class Mapper2 extends Mapper<LongWritable, Text, Text, Text> {
    private static Logger logger = Logger.getLogger("Mapper2");
    private Text outKey = new Text();
    private Text outValue = new Text();
    private List<String> cacheList = new ArrayList<String>();
    private DecimalFormat df = new DecimalFormat("0.00");

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        //通过输入流将全局缓存中的右侧矩阵读入List<String>
        FileReader fr = new FileReader("itemUserScore1");
        BufferedReader br = new BufferedReader(fr);
        //每一行的格式是： 1	A_2,C_5
        String line = null;
        while ((line = br.readLine()) != null) {
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // value = 1	A_2,C_5
        String[] mapLine = value.toString().split("\t"); // ["1","A_2,C_5"]
        String mapItemId = mapLine[0]; // "1"
        String[] mapUserIdAndScores = mapLine[1].split(",");// ["A_2","C_5"]

        //遍历缓存
        for (String cache : cacheList
                ) {

            int num = 0;//分子
            Double cacheDen = 0D;
            Double mapDen = 0D;
            Double den;//分母
            Double cos = 0D;//最后结果

            String[] cacheLine = cache.split("\t"); // ["1","A_2,C_5"]
            String cacheItemId = cacheLine[0];// "1"
            String[] cacheUserIdAndScores = cacheLine[1].split(",");// ["A_2","C_5"]
            for (String cacheUserIdAndScore : cacheUserIdAndScores
                    ) {
                String cacheScore = cacheUserIdAndScore.split("_")[1];//"2"
                cacheDen += Double.valueOf(cacheScore) * Double.valueOf(cacheScore);//2*2

            }
            //遍历mapUserIdAndScores
            for (String mapUserIdAndScore : mapUserIdAndScores
                    ) {
                String mapUserId = mapUserIdAndScore.split("_")[0]; //"A"
                String mapScore = mapUserIdAndScore.split("_")[1];//"2"
                //遍历cacheUserIdAndScores
                for (String cacheUserIdAndScore : cacheUserIdAndScores
                        ) {
                    String cacheUserId = cacheUserIdAndScore.split("_")[0];//"A"
                    String cacheScore = cacheUserIdAndScore.split("_")[1];//"2"
                    if (mapUserId.equals(cacheUserId)) {
                        //分子
                        num += Integer.valueOf(mapScore) * Integer.valueOf(cacheScore); //2*2
                    }
                }

                mapDen += Double.valueOf(mapScore) * Double.valueOf(mapScore);//2*2
            }
            den = Math.sqrt(mapDen) * Math.sqrt(cacheDen);
            cos = num / den;
            if (num == 0) {
                continue;
            }
            outKey.set(mapItemId);
            outValue.set(cacheItemId + "_" + df.format(cos));
            context.write(outKey, outValue);
        }
    }
}

```

##### Reducer2 

```
package org.hadoop.mrs.itemCF.step2;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by shirukai on 2017/11/12.
 */
public class Reducer2 extends Reducer<Text, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        StringBuilder sb = new StringBuilder();
        for (Text value : values) {
            sb.append(value + ",");
        }
        String result = null;
        if (sb.toString().endsWith(",")) {
            result = sb.substring(0, sb.length() - 1);
        }
        outKey.set(key);
        outValue.set(result);
        context.write(outKey, outValue);
    }
}

```

##### MR2 

```
package org.hadoop.mrs.itemCF.step2;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.log4j.Logger;
import org.hadoop.conf.Conf;

import java.net.URI;

/**
 *
 * Created by shirukai on 2017/11/12.
 */
public class MR2 {
    private static Logger logger = Logger.getLogger("MR2");
    //输入文件的相对路径
    private static String inPath = "/itemCF/step1/step1_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/itemCF/step2/step2_output";

    //将step1输出的转置矩阵作为全局缓存
    private static String cache = "/itemCF/step1/step1_output/part-r-00000";

    public static int run(){
        try {
            //创建job配置类
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step2");

            //添加分布式缓存文件
            job.addCacheArchive(new URI(cache+"#itemUserScore1"));
            //设置job的主类
            job.setJarByClass(org.hadoop.mrs.matrix.step2.MR2.class);
            //设置job的Mapper类和Reducer类
            job.setMapperClass(Mapper2.class);
            job.setReducerClass(Reducer2.class);

            //设置Mapper的输出类型
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);

            //设置Reducer的输出类型
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            //设置输入和输出路径
            FileSystem fs = FileSystem.get(conf);
            Path inputPath = new Path(inPath);
            if (fs.exists(inputPath)){
                FileInputFormat.addInputPath(job,inputPath);
            }
            Path outputPath = new Path(outPath);
            fs.delete(outputPath,true);

            FileOutputFormat.setOutputPath(job,outputPath);
            return job.waitForCompletion(true)?1:-1;
        }catch (Exception e){
            logger.error(e.getMessage());
        }
        return -1;
    }
}

```

### Step3 将评分矩阵转置

##### Mapper3

```
package org.hadoop.mrs.itemCF.step3;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * 将评分列表转置
 * Created by shirukai on 2017/11/13.
 */
public class Mapper3 extends Mapper<LongWritable,Text,Text,Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] mapLine = value.toString().split("\t");
        String itemId = mapLine[0];
        String[] userIdAndScores = mapLine[1].split(",");
        for (String userIdAndScore:userIdAndScores
             ) {
            String userId = userIdAndScore.split("_")[0];
            String score = userIdAndScore.split("_")[1];
            outKey.set(userId);
            outValue.set(itemId+"_"+score);
            context.write(outKey,outValue);
        }
    }
}

```

#### Reducer3

```
package org.hadoop.mrs.itemCF.step3;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/13.
 */
public class Reducer3 extends Reducer<Text, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();
    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        StringBuilder sb = new StringBuilder();
        for (Text value : values){
            sb.append(value+",");
        }
        String result = null;
        if (sb.toString().endsWith(",")){
            result = sb.substring(0,sb.length()-1);
        }
        //outKey:行 outValue:列_值
        outKey.set(key);
        outValue.set(result);
        context.write(outKey,outValue);
    }
}

```

##### MR3 

```
package org.hadoop.mrs.itemCF.step3;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.log4j.Logger;
import org.hadoop.conf.Conf;

import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/13.
 */
public class MR3 {
    private static Logger logger = Logger.getLogger("MR3");
    //输入文件的相对路径
    private static String inPath = "/itemCF/step1/step1_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/itemCF/step3/step3_output";

    public static int run(){
        try {
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step3");

            //设置job的主类
            job.setJarByClass(MR3.class);
            //设置job的Mapper类和Reducer类
            job.setMapperClass(Mapper3.class);
            job.setReducerClass(Reducer3.class);

            //设置Mapper的输出类型
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);

            //设置Reducer的输出类型
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            //设置输入和输出路径
            FileSystem fs = FileSystem.get(conf);
            Path inputPath = new Path(inPath);
            if (fs.exists(inputPath)){
                FileInputFormat.addInputPath(job,inputPath);
            }
            Path outputPath = new Path(outPath);
            fs.delete(outputPath,true);

            FileOutputFormat.setOutputPath(job,outputPath);
            return job.waitForCompletion(true)?1:-1;
        }catch (IOException e){
            logger.error(e.getMessage());
        }catch (ClassNotFoundException e){
            logger.error(e.getMessage());
        }catch (InterruptedException e){
            logger.error(e.getMessage());
        }
        return -1;
    }
}
```

### Step4 物品相似度矩阵* 转置后的评分矩阵求出推荐列表

##### Mapper4

```
package org.hadoop.mrs.itemCF.step4;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * Created by shirukai on 2017/11/13.
 */
public class Mapper4 extends Mapper<LongWritable,Text,Text,Text> {
    private static Logger logger = Logger.getLogger("Mapper4");
    private Text outKey = new Text();
    private Text outValue = new Text();
    private List<String> cacheList = new ArrayList<String>();
    private DecimalFormat df = new DecimalFormat("0.00");

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        //通过输入流将全局缓存中的右侧矩阵读入List<String>
        FileReader fr = new FileReader("itemUserScore4");
        BufferedReader br = new BufferedReader(fr);
        //每一行的格式是：  A	6_5,4_3,2_10,1_2
        String line = null;
        while ((line = br.readLine()) != null) {
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // value = 1	1_1.00,2_0.36,3_0.93,4_0.99,6_0.26
        String[] mapLine = value.toString().split("\t");
        String itemId = mapLine[0];
        String[] mapUserIdAndScores = mapLine[1].split(",");

        //遍历缓存
        for (String cache : cacheList
                ) {

            Double result = 0D;//最后结果
            //cache A	6_5,4_3,2_10,1_2
            String[] cacheLine = cache.split("\t");
            String cacheUserId = cacheLine[0];
            String[] cacheUserIdAndScores = cacheLine[1].split(",");

            //遍历mapUserIdAndScores
            for (String mapUserIdAndScore : mapUserIdAndScores
                    ) {
                String mapItemId = mapUserIdAndScore.split("_")[0];
                String mapSimilarity = mapUserIdAndScore.split("_")[1];
                //遍历cacheUserIdAndScores
                for (String cacheUserIdAndScore : cacheUserIdAndScores
                        ) {
                    String cacheItemId = cacheUserIdAndScore.split("_")[0];
                    String cacheSimilarity = cacheUserIdAndScore.split("_")[1];
                    if (mapItemId.equals(cacheItemId)) {
                        result += Double.valueOf(mapSimilarity) * Double.valueOf(cacheSimilarity);
                    }
                }
            }
            if (result == 0) {
                continue;
            }
            outKey.set(itemId);
            outValue.set(cacheUserId + "_" + df.format(result));
            context.write(outKey, outValue);
        }
    }
}

```

##### Reducer4

```
package org.hadoop.mrs.itemCF.step4;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by shirukai on 2017/11/13.
 */
public class Reducer4 extends Reducer<Text, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        StringBuilder sb = new StringBuilder();
        for (Text value : values) {
            sb.append(value + ",");
        }
        String result = null;
        if (sb.toString().endsWith(",")) {
            result = sb.substring(0, sb.length() - 1);
        }
        outKey.set(key);
        outValue.set(result);
        context.write(outKey, outValue);
    }
}

```

##### MR4

```
package org.hadoop.mrs.itemCF.step4;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.log4j.Logger;
import org.hadoop.conf.Conf;

import java.net.URI;

/**
 * Created by shirukai on 2017/11/13.
 */
public class MR4 {
    private static Logger logger = Logger.getLogger("MR2");
    //输入文件的相对路径
    private static String inPath = "/itemCF/step2/step2_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/itemCF/step4/step4_output";

    //将step3输出的转置矩阵作为全局缓存
    private static String cache = "/itemCF/step3/step3_output/part-r-00000";

    public static int run(){
        try {
            //创建job配置类
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step4");

            //添加分布式缓存文件
            job.addCacheArchive(new URI(cache+"#itemUserScore4"));
            //设置job的主类
            job.setJarByClass(MR4.class);
            //设置job的Mapper类和Reducer类
            job.setMapperClass(Mapper4.class);
            job.setReducerClass(Reducer4.class);

            //设置Mapper的输出类型
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);

            //设置Reducer的输出类型
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            //设置输入和输出路径
            FileSystem fs = FileSystem.get(conf);
            Path inputPath = new Path(inPath);
            if (fs.exists(inputPath)){
                FileInputFormat.addInputPath(job,inputPath);
            }
            Path outputPath = new Path(outPath);
            fs.delete(outputPath,true);

            FileOutputFormat.setOutputPath(job,outputPath);
            return job.waitForCompletion(true)?1:-1;
        }catch (Exception e){
            logger.error(e.getMessage());
        }
        return -1;

    }
}

```

### Step5过滤推荐列表 将step1中已有的用户行为过滤掉

##### Mapper5

```
package org.hadoop.mrs.itemCF.step5;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * Created by shirukai on 2017/11/13.
 */
public class Mapper5 extends Mapper<LongWritable,Text,Text,Text> {
    private static Logger logger = Logger.getLogger("Mapper4");
    private Text outKey = new Text();
    private Text outValue = new Text();
    private List<String> cacheList = new ArrayList<String>();
    private DecimalFormat df = new DecimalFormat("0.00");
    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        //通过输入流将全局缓存中的右侧矩阵读入List<String>
        FileReader fr = new FileReader("itemUserScore5");
        BufferedReader br = new BufferedReader(fr);
        //每一行的格式是： 1   A_2,C_5
        String line = null;
        while ((line = br.readLine()) != null) {
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        // value = 1   A_9.87,B_2.38,C_23.90
        String[] mapLine = value.toString().split("\t");
        String mapItemId = mapLine[0];
        String[] mapUserIdAndScores = mapLine[1].split(",");

        //遍历缓存
        for (String cache : cacheList
                ) {
            String[] cacheLine = cache.split("\t");
            String cacheItemId = cacheLine[0];
            String[] cacheUserIdAndScores = cacheLine[1].split(",");
            if (mapItemId.equals(cacheItemId)){
                //遍历mapUserIdAndScores
                for (String mapUserIdAndScore : mapUserIdAndScores
                        ) {
                    boolean flag = false;
                    String mapUserId = mapUserIdAndScore.split("_")[0];
                    String mapSimilarity = mapUserIdAndScore.split("_")[1];
                    //遍历cacheUserIdAndScores
                    for (String cacheUserIdAndScore : cacheUserIdAndScores
                            ) {
                        String cacheUserId = cacheUserIdAndScore.split("_")[0];
                        if (mapUserId.equals(cacheUserId)) {
                            flag = true;
                        }
                    }
                    if (!flag){
                        outKey.set(mapUserId);
                        outValue.set(mapItemId+"_"+mapSimilarity);
                        context.write(outKey,outValue);
                    }
                }
            }

        }
    }
}

```

##### Reducer5 

```
package org.hadoop.mrs.itemCF.step5;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by shirukai on 2017/11/13.
 */
public class Reducer5 extends Reducer<Text, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        StringBuilder sb = new StringBuilder();
        for (Text value : values) {
            sb.append(value + ",");
        }
        String result = null;
        if (sb.toString().endsWith(",")) {
            result = sb.substring(0, sb.length() - 1);
        }
        outKey.set(key);
        outValue.set(result);
        context.write(outKey, outValue);
    }
}

```

##### MR5 

```
package org.hadoop.mrs.itemCF.step5;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.log4j.Logger;
import org.hadoop.conf.Conf;
import org.hadoop.mrs.itemCF.step4.Mapper4;
import org.hadoop.mrs.itemCF.step4.Reducer4;

import java.net.URI;

/**
 * Created by shirukai on 2017/11/13.
 */
public class MR5 {
    private static Logger logger = Logger.getLogger("MR5");
    //输入文件的相对路径
    private static String inPath = "/itemCF/step4/step4_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/itemCF/step5/step5_output";

    //将step1输出的转置矩阵作为全局缓存
    private static String cache = "/itemCF/step1/step1_output/part-r-00000";

    public static int run(){
        try {
            //创建job配置类
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step5");

            //添加分布式缓存文件
            job.addCacheArchive(new URI(cache+"#itemUserScore5"));
            //设置job的主类
            job.setJarByClass(MR5.class);
            //设置job的Mapper类和Reducer类
            job.setMapperClass(Mapper5.class);
            job.setReducerClass(Reducer5.class);

            //设置Mapper的输出类型
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);

            //设置Reducer的输出类型
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);

            //设置输入和输出路径
            FileSystem fs = FileSystem.get(conf);
            Path inputPath = new Path(inPath);
            if (fs.exists(inputPath)){
                FileInputFormat.addInputPath(job,inputPath);
            }
            Path outputPath = new Path(outPath);
            fs.delete(outputPath,true);

            FileOutputFormat.setOutputPath(job,outputPath);
            return job.waitForCompletion(true)?1:-1;
        }catch (Exception e){
            logger.error(e.getMessage());
        }
        return -1;

    }
}
```

### 在itemCF包创建运行方法 

##### RunItemCF 

```
package org.hadoop.mrs.itemCF;

import org.apache.hadoop.fs.Path;
import org.hadoop.files.Files;
import org.hadoop.mrs.itemCF.step1.MR1;
import org.hadoop.mrs.itemCF.step2.MR2;
import org.hadoop.mrs.itemCF.step3.MR3;
import org.hadoop.mrs.itemCF.step4.MR4;
import org.hadoop.mrs.itemCF.step5.MR5;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * 运行ItemCF
 * Created by shirukai on 2017/11/12.
 */
public class RunItemCF {
    private static org.apache.log4j.Logger logger = org.apache.log4j.Logger.getLogger("RunItemCF");
    public static void Run() {
        //开始时间
        long startTime = System.currentTimeMillis();
        //创建目录
        try {
            Files.deleteFile("/itemCF");
            Files.mkdirFolder("/itemCF");
            for (int i = 1; i < 6; i++) {
                Files.mkdirFolder("/itemCF/step" + i);
                Files.mkdirFolder("/itemCF/step" + i + "/step" + i + "_input");
                Files.mkdirFolder("/itemCF/step" + i + "/step" + i + "_output");
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        //上传文件
        Files.uploadFile("D:\\Hadoop\\upload\\", "itemCF.txt", "/itemCF/step1/step1_input/");

        //执行第一步
        MR1.run();
        //执行第二步
        int step2 = MR2.run();
        if (step2 == 1) {
            //执行成功后打印文件
            readOutFile("/itemCF/step2/step2_output/part-r-00000");

        }
        //执行第三步
        int step3 = MR3.run();
        if (step3 == 1) {
            //执行成功后打印文件
            readOutFile("/itemCF/step3/step3_output/part-r-00000");
        }
        //执行第四步
        int step4 = MR4.run();
        if (step4 == 1) {
            //执行成功后打印文件
            readOutFile("/itemCF/step4/step4_output/part-r-00000");
        }
        //执行第五步
        int step5 = MR5.run();
        if (step5 == 1) {
            //执行成功后打印文件
            readOutFile("/itemCF/step5/step5_output/part-r-00000");
        }
        //结束时间
        long endTime = System.currentTimeMillis();
        logger.info("任务用时："+(endTime-startTime)/1000+"秒");
    }

    public static void readOutFile(String filePath) {
        try {
            InputStream inputStream = Files.getFiles().open(new Path(filePath));
            BufferedReader bf = new BufferedReader(new InputStreamReader(inputStream, "GB2312"));//防止中文乱码
            String line = null;
            while ((line = bf.readLine()) != null) {
                logger.info(line);
            }

        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }
}

```

##### 将RunItemCF添加进main方法中执行

```
package org.hadoop.run;
import org.apache.log4j.Logger;
import org.hadoop.mrs.itemCF.RunItemCF;
import org.hadoop.mrs.matrix.RunMatrix;
import org.hadoop.mrs.wordcount.WordCountRun;

/**
 *
 * Created by shirukai on 2017/11/8.
 */
public class RunHadoop {
    private static Logger logger = Logger.getLogger("RunHadoop");
    public static void main(String[] args) {
        RunItemCF.Run();
    }
}
```

##### 运行main方法：

最终结果

```
A	5_6.45,3_4.44
B	4_3.27,1_2.38
C	6_3.10,2_4.25
```



