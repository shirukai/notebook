# Hadoop推荐算法-基于用户的协同过滤UserCF

算法思想：给用户推荐和他兴趣相似的其他用户喜欢的物品

## 理论 

### 现有如下用户、商品、行为、权重 

![https://shirukai.gitee.io/images/1510554135635__IZF__1U_Z@XX4R`_UTFEW.png](https://shirukai.gitee.io/images/1510554135635__IZF__1U_Z@XX4R`_UTFEW.png)

### 行为列表 

![https://shirukai.gitee.io/images/1510554230791ESFBEVY70B6_0`__93AC4AB.png](https://shirukai.gitee.io/images/1510554230791ESFBEVY70B6_0`__93AC4AB.png)

### 算法步骤

#### 1.根据用户行为列表计算物品、用户的评分矩阵 

![](https://shirukai.gitee.io/images/1510554331568@Q_K50~~DLCDT__NJSJW_13.png)

#### 2.根据评分矩阵计算用户与用户的相似矩阵 

![](https://shirukai.gitee.io/images/1510554447729V5E@_965_2RNB__UGNX__9G.png)

用户与用户之间的相似度矩阵

![](https://shirukai.gitee.io/images/1510554484395___745A___5NE~`ND3_SLC3.png)

### 3.相似度矩阵 X 评分矩阵 = 推荐列表 

![](https://shirukai.gitee.io/images/1510554577308_`1U3ICG_JJI7X6M_BBT_DU.png)

得到的推荐列表如下

![](https://shirukai.gitee.io/images/1510554657684_XCJ_ZP_7N_JPBESPI_~7_L.png)

#### 4.根据评分矩阵对推荐列表进行过滤 

![](https://shirukai.gitee.io/images/1510554824499Z74_IYEF5R9NBUP@__M_G8F.png)

## 代码实现 

![](https://shirukai.gitee.io/images/15105549099244E__FLA83_DCZX1_HRG350J.png)

### Step1 根据用户行为列表构建评分矩阵 

#### Mapper1

```
package org.hadoop.mrs.userCF.step1;

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

        outKey.set(userID);
        outValue.set(itemID+"_"+score);
        context.write(outKey,outValue);
    }
}

```

#### Reducer1

```
package org.hadoop.mrs.userCF.step1;

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
        String userID = key.toString();
        //<userID,sore>
        Map<String, Integer> map = new HashMap<String, Integer>();
        for (Text value :values){
            String itemId = value.toString().split("_")[0];
            String score = value.toString().split("_")[1];
            if (map.get(itemId) == null){
                map.put(itemId,Integer.valueOf(score));
            }else {
                Integer preScore = map.get(itemId);
                map.put(itemId,preScore+Integer.valueOf(score));
            }
        }
        StringBuilder sBuilder = new StringBuilder();
        for (Map.Entry<String,Integer> entry: map.entrySet()
             ) {
            String itemID = entry.getKey();
            String score = String.valueOf(entry.getValue());
            sBuilder.append(itemID+"_"+score+",");
        }
        String line = null;
        //去掉末尾的“，”
        if (sBuilder.toString().endsWith(",")){
            line = sBuilder.substring(0,sBuilder.length()-1);
        }
        outKey.set(userID);
        outValue.set(line);
        context.write(outKey,outValue);
    }
}

```

#### MR1

```
package org.hadoop.mrs.userCF.step1;

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
    private static String inPath = "/userCF/step1/step1_input/userCF.txt";
    //输出文件的相对路径
    private static String outPath = "/userCF/step1/step1_output";

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

##### 执行step之后得到的结果

```
A	1_1,3_5,4_3
B	2_3,5_3
C	1_5,6_10
D	1_10,5_5
E	3_5,4_1
F	2_5,3_3,6_1
```



### Step2 利用评分矩阵，构建用户与用户的相似度矩阵 

#### Mapper2

```
package org.hadoop.mrs.userCF.step2;

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
        String line = null;
        while ((line = br.readLine()) != null) {
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] mapLine = value.toString().split("\t");
        String mapIndex = mapLine[0];
        String[] mapKeyAndValues = mapLine[1].split(",");

        //遍历缓存
        for (String cache : cacheList
                ) {

            int num = 0;//分子
            Double cacheDen = 0D;
            Double mapDen = 0D;
            Double den;//分母
            Double cos = 0D;//最后结果

            String[] cacheLine = cache.split("\t");
            String cacheIndex = cacheLine[0];
            String[] cacheKeyAndValues = cacheLine[1].split(",");
            for (String cacheKeyAndValue : cacheKeyAndValues
                    ) {
                String cacheScore = cacheKeyAndValue.split("_")[1];
                cacheDen += Double.valueOf(cacheScore) * Double.valueOf(cacheScore);

            }
            //遍历mapKeyAndValues
            for (String mapKeyAndValue : mapKeyAndValues
                    ) {
                String mapUserId = mapKeyAndValue.split("_")[0];
                String mapScore = mapKeyAndValue.split("_")[1];
                //遍历cacheKeyAndValues
                for (String cacheKeyAndValue : cacheKeyAndValues
                        ) {
                    String cacheUserId = cacheKeyAndValue.split("_")[0];
                    String cacheScore = cacheKeyAndValue.split("_")[1];
                    if (mapUserId.equals(cacheUserId)) {
                        //分子
                        num += Integer.valueOf(mapScore) * Integer.valueOf(cacheScore);
                    }
                }

                mapDen += Double.valueOf(mapScore) * Double.valueOf(mapScore);
            }
            den = Math.sqrt(mapDen) * Math.sqrt(cacheDen);
            cos = num / den;
            if (num == 0) {
                continue;
            }
            outKey.set(mapIndex);
            outValue.set(cacheIndex + "_" + df.format(cos));
            context.write(outKey, outValue);
        }
    }
}

```

#### Reducer2

```
package org.hadoop.mrs.userCF.step2;

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

#### MR2

```
package org.hadoop.mrs.userCF.step2;

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
    private static String inPath = "/userCF/step1/step1_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/userCF/step2/step2_output";

    //将step1输出的转置矩阵作为全局缓存
    private static String cache = "/userCF/step1/step1_output/part-r-00000";

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

Step2执行后得到结果:

```
A	A_1.00,C_0.08,D_0.15,E_0.93,F_0.43
B	B_1.00,D_0.32,F_0.60
C	F_0.15,D_0.40,C_1.00,A_0.08
D	D_1.00,C_0.40,B_0.32,A_0.15
E	A_0.93,E_1.00,F_0.50
F	C_0.15,E_0.50,F_1.00,A_0.43,B_0.60
```



### Step3 将评分矩阵转置 

#### Mapper3

```
package org.hadoop.mrs.userCF.step3;

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
        String mapIndex = mapLine[0];
        String[] keyAndValues = mapLine[1].split(",");
        for (String keyAndValue:keyAndValues
             ) {
            String mapKey = keyAndValue.split("_")[0];
            String mapValue = keyAndValue.split("_")[1];
            outKey.set(mapKey);
            outValue.set(mapIndex+"_"+mapValue);
            context.write(outKey,outValue);
        }
    }
}

```

#### Reducer3

```
package org.hadoop.mrs.userCF.step3;

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

#### MR3

```
package org.hadoop.mrs.userCF.step3;

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
    private static String inPath = "/userCF/step1/step1_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/userCF/step3/step3_output";

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

##### Step3执行成功后，得到的结果

```
1	D_10,A_1,C_5
2	F_5,B_3
3	A_5,F_3,E_5
4	E_1,A_3
5	D_5,B_3
6	F_1,C_10
```



### Step4 用户与用户相似度矩阵 X 评分矩阵 

#### Mapper4

```
package org.hadoop.mrs.userCF.step4;

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
        //每一行的格式是：  A  6_5,4_3,2_10,1_2
        String line = null;
        while ((line = br.readLine()) != null) {
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] mapLine = value.toString().split("\t");
        String mapIndex = mapLine[0];
        String[] mapKeyAndValues = mapLine[1].split(",");

        //遍历缓存
        for (String cache : cacheList
                ) {

            Double result = 0D;
            String[] cacheLine = cache.split("\t");
            String cacheIndex = cacheLine[0];
            String[] cacheKeyAndValues = cacheLine[1].split(",");

            //遍历mapKeyAndValues
            for (String mapKeyAndValue : mapKeyAndValues
                    ) {
                String mapKey = mapKeyAndValue.split("_")[0];
                String mapSimilarity = mapKeyAndValue.split("_")[1];
                //遍历cacheUserIdAndScores
                for (String cacheKeyAndValue : cacheKeyAndValues
                        ) {
                    String cacheKey = cacheKeyAndValue.split("_")[0];
                    String cacheSimilarity = cacheKeyAndValue.split("_")[1];
                    if (mapKey.equals(cacheKey)) {
                        result += Double.valueOf(mapSimilarity) * Double.valueOf(cacheSimilarity);
                    }
                }
            }
            if (result == 0) {
                continue;
            }
            outKey.set(mapIndex);
            outValue.set(cacheIndex + "_" + df.format(result));
            context.write(outKey, outValue);
        }
    }
}

```

#### Reducer4

```
package org.hadoop.mrs.userCF.step4;

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

#### MR4

```
package org.hadoop.mrs.userCF.step4;

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
    private static Logger logger = Logger.getLogger("MR4");
    //输入文件的相对路径
    private static String inPath = "/userCF/step2/step2_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/userCF/step4/step4_output";

    //将step3输出的转置矩阵作为全局缓存
    private static String cache = "/userCF/step3/step3_output/part-r-00000";

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

##### Step4执行后的结果：

```
A	1_2.90,2_2.15,3_10.94,4_3.93,5_0.75,6_1.23
B	1_3.20,2_6.00,3_1.80,5_4.60,6_0.60
C	6_10.15,5_2.00,4_0.24,3_0.85,2_0.75,1_9.08
D	1_12.15,6_4.00,5_5.96,4_0.45,3_0.75,2_0.96
E	1_0.93,2_2.50,3_11.15,4_3.79,6_0.50
F	1_1.18,2_6.80,3_7.65,4_1.79,5_1.80,6_2.50
```



### Step5 根据评分矩阵将在步骤4的输出中，用户已经用过行为的商品评分置0

#### Mapper5

```
package org.hadoop.mrs.userCF.step5;

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
        String line = null;
        while ((line = br.readLine()) != null) {
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] mapLine = value.toString().split("\t");
        String mapIndex = mapLine[0];
        String[] mapKeyAndValues = mapLine[1].split(",");

        //遍历缓存
        for (String cache : cacheList
                ) {
            String[] cacheLine = cache.split("\t");
            String cacheIndex = cacheLine[0];
            String[] cacheKeyAndValues = cacheLine[1].split(",");
            if (mapIndex.equals(cacheIndex)){
                for (String mapKeyAndValue : mapKeyAndValues
                        ) {
                    boolean flag = false;
                    String mapKey = mapKeyAndValue.split("_")[0];
                    String mapSimilarity = mapKeyAndValue.split("_")[1];
                    //遍历cacheUserIdAndScores
                    for (String cacheKeyAndValue : cacheKeyAndValues
                            ) {
                        String cacheKey = cacheKeyAndValue.split("_")[0];
                        if (mapKey.equals(cacheKey)) {
                            flag = true;
                        }
                    }
                    if (!flag){
                        outKey.set(mapIndex);
                        outValue.set(mapKey+"_"+mapSimilarity);
                        context.write(outKey,outValue);
                    }
                }
            }

        }
    }
}

```

#### Reducer5

```
package org.hadoop.mrs.userCF.step5;

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

#### MR5

```
package org.hadoop.mrs.userCF.step5;

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
public class MR5 {
    private static Logger logger = Logger.getLogger("MR5");
    //输入文件的相对路径
    private static String inPath = "/userCF/step4/step4_output/part-r-00000";
    //输出文件的相对路径
    private static String outPath = "/userCF/step5/step5_output";

    //将step1输出的转置矩阵作为全局缓存
    private static String cache = "/userCF/step1/step1_output/part-r-00000";

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

##### Step5执行后的结果：

```
A	2_2.15,5_0.75,6_1.23
B	1_3.20,3_1.80,6_0.60
C	2_0.75,3_0.85,4_0.24,5_2.00
D	2_0.96,3_0.75,4_0.45,6_4.00
E	1_0.93,2_2.50,6_0.50
F	1_1.18,4_1.79,5_1.80
```

### 在userCF包下创建RunUserCF类，用户执行各个步骤方法

#### RunUserCF类 

```
package org.hadoop.mrs.userCF;

import org.apache.hadoop.fs.Path;
import org.hadoop.files.Files;
import org.hadoop.mrs.userCF.step1.MR1;
import org.hadoop.mrs.userCF.step2.MR2;
import org.hadoop.mrs.userCF.step3.MR3;
import org.hadoop.mrs.userCF.step4.MR4;
import org.hadoop.mrs.userCF.step5.MR5;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * 运行ItemCF
 * Created by shirukai on 2017/11/12.
 */
public class RunUserCF {
    private static org.apache.log4j.Logger logger = org.apache.log4j.Logger.getLogger("RunUserCF");
    public static void Run() {
        //开始时间
        long startTime = System.currentTimeMillis();
        //创建目录
        try {
            Files.deleteFile("/userCF");
            Files.mkdirFolder("/userCF");
            for (int i = 1; i < 6; i++) {
                Files.mkdirFolder("/userCF/step" + i);
                Files.mkdirFolder("/userCF/step" + i + "/step" + i + "_input");
                Files.mkdirFolder("/userCF/step" + i + "/step" + i + "_output");
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        //上传文件
        Files.uploadFile("D:\\Hadoop\\upload\\", "userCF.txt", "/userCF/step1/step1_input/");

        //执行第一步
        int step1 = MR1.run();
        if (step1 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/userCF/step1/step1_output/part-r-00000");

        }
        //执行第二步
        int step2 = MR2.run();
        if (step2 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/userCF/step2/step2_output/part-r-00000");

        }
        //执行第三步
        int step3 = MR3.run();
        if (step3 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/userCF/step3/step3_output/part-r-00000");
        }
        //执行第四步
        int step4 = MR4.run();
        if (step4 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/userCF/step4/step4_output/part-r-00000");
        }
        //执行第五步
        int step5 = MR5.run();
        if (step5 == 1) {
            //执行成功后打印文件
            Files. readOutFile("/userCF/step5/step5_output/part-r-00000");
        }
        //结束时间
        long endTime = System.currentTimeMillis();
        logger.info("任务用时："+(endTime-startTime)/1000+"秒");
    }

}

```

