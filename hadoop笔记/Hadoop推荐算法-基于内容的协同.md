# Hadoop推荐算法-基于内容的推荐算法contentCF 

算法思想：给用户推荐和他们之前喜欢的物品在内容上相似的其他物品

物品特征建模 Item Profile

## 算法步骤

### 1 构建Item Profile矩阵

![](https://shirukai.gitee.io/images/201711221614_322.png)

### 2构建Item User 评分矩阵

### ![](http://ov1a6etyz.bkt.clouddn.com/201711221615_947.png)

### 3 Item User *  Item Profile = User Profile 

![](https://shirukai.gitee.io/images/201711221616_781.png)

### 4 对Item Profile 和User Profile 求余弦相似度 

![](https://shirukai.gitee.io/images/201711221618_180.png)

## 代码实现

![](https://shirukai.gitee.io/images/201711221620_164.png)

### step1 

#### mapper1

```
package org.hadoop.mrs.contentCF.step1;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * 将矩阵转置
 * Created by shirukai on 2017/11/22.
 */
public class Mapper1 extends Mapper<LongWritable,Text,Text,Text> {
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

#### Reducer1

```
package org.hadoop.mrs.contentCF.step1;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/22.
 */
public class Reducer1 extends Reducer<Text, Text, Text, Text> {
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

#### MR1 

```
package org.hadoop.mrs.contentCF.step1;

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
 * Created by shirukai on 2017/11/22.
 */
public class MR1 {
    private static Logger logger = Logger.getLogger("MR3");
    //输入文件的相对路径
    private static String inPath = "/contentCF/step1/step1_input/contentCF.txt";
    //输出文件的相对路径
    private static String outPath = "/contentCF/step1/step1_output";

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

### Step2 

#### mapper2 

```
package org.hadoop.mrs.contentCF.step2;

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
public class Mapper2 extends Mapper<LongWritable,Text,Text,Text> {
    private static Logger logger = Logger.getLogger("Mapper3");
    private Text outKey = new Text();
    private Text outValue = new Text();
    private List<String> cacheList = new ArrayList<String>();
    private DecimalFormat df = new DecimalFormat("0.00");

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        //通过输入流将全局缓存中的右侧矩阵读入List<String>
        FileReader fr = new FileReader("cache2");
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
                //遍历cacheKeyAndValues
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

#### Reducer2 

```
package org.hadoop.mrs.contentCF.step2;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by shirukai on 2017/11/13.
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
package org.hadoop.mrs.contentCF.step2;

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
public class MR2 {
    private static Logger logger = Logger.getLogger("MR3");
    //输入文件的相对路径
    private static String inPath = "/contentCF/step2/step2_input/contentUserCF.txt";
    //输出文件的相对路径
    private static String outPath = "/contentCF/step2/step2_output";

    //将step3输出的转置矩阵作为全局缓存
    private static String cache = "/contentCF/step1/step1_output/part-r-00000";

    public static int run(){
        try {
            //创建job配置类
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step2");

            //添加分布式缓存文件
            job.addCacheArchive(new URI(cache+"#cache2"));
            //设置job的主类
            job.setJarByClass(MR2.class);
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

### Step3 

#### mapper3 

```
package org.hadoop.mrs.contentCF.step3;

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
public class Mapper3 extends Mapper<LongWritable, Text, Text, Text> {
    private static Logger logger = Logger.getLogger("Mapper3");
    private Text outKey = new Text();
    private Text outValue = new Text();
    private List<String> cacheList = new ArrayList<String>();
    private DecimalFormat df = new DecimalFormat("0.00");

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        //通过输入流将全局缓存中的右侧矩阵读入List<String>
        FileReader fr = new FileReader("cache3");
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

            Double num = 0D;//分子
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
                        num += Double.valueOf(mapScore) * Double.valueOf(cacheScore);
                    }
                }

                mapDen += Double.valueOf(mapScore) * Double.valueOf(mapScore);
            }
            den = Math.sqrt(mapDen) * Math.sqrt(cacheDen);
            cos = num / den;
            if (num == 0) {
                continue;
            }
            outKey.set(cacheIndex);
            outValue.set(mapIndex + "_" + df.format(cos));
            context.write(outKey, outValue);
        }
    }
}

```

####  Reducer3 

```
package org.hadoop.mrs.contentCF.step3;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by shirukai on 2017/11/12.
 */
public class Reducer3 extends Reducer<Text, Text, Text, Text> {
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

#### MR3 

```
package org.hadoop.mrs.contentCF.step3;

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
public class MR3 {
    private static Logger logger = Logger.getLogger("MR3");
    //输入文件的相对路径
    private static String inPath = "/contentCF/step1/step1_input/contentCF.txt";
    //输出文件的相对路径
    private static String outPath = "/contentCF/step3/step3_output";

    //将step1输出的转置矩阵作为全局缓存
    private static String cache = "/contentCF/step2/step2_output/part-r-00000";

    public static int run(){
        try {
            //创建job配置类
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step3");

            //添加分布式缓存文件
            job.addCacheArchive(new URI(cache+"#cache3"));
            //设置job的主类
            job.setJarByClass(org.hadoop.mrs.matrix.step2.MR2.class);
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
        }catch (Exception e){
            logger.error(e.getMessage());
        }
        return -1;

    }
}

```

### RunContentCF 

```
package org.hadoop.mrs.contentCF;

import org.hadoop.files.Files;
import org.hadoop.mrs.contentCF.step1.MR1;
import org.hadoop.mrs.contentCF.step2.MR2;
import org.hadoop.mrs.contentCF.step3.MR3;

/**
 * 运行contentCF
 * Created by shirukai on 2017/11/22.
 */
public class RunContentCF {
    private static org.apache.log4j.Logger logger = org.apache.log4j.Logger.getLogger("RunUserCF");
    public static void Run() {
        //开始时间
        long startTime = System.currentTimeMillis();
        //创建目录
        try {
            Files.deleteFile("/contentCF");
            Files.mkdirFolder("/contentCF");
            for (int i = 1; i < 3; i++) {
                Files.mkdirFolder("/contentCF/step" + i);
                Files.mkdirFolder("/contentCF/step" + i + "/step" + i + "_input");
                Files.mkdirFolder("/contentCF/step" + i + "/step" + i + "_output");
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
        //上传文件
        Files.uploadFile("D:\\Hadoop\\upload\\", "contentCF.txt", "/contentCF/step1/step1_input/");
        Files.uploadFile("D:\\Hadoop\\upload\\", "contentUserCF.txt", "/contentCF/step2/step2_input/");
        //执行第一步
        int step1 = MR1.run();
        if (step1 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/contentCF/step1/step1_output/part-r-00000");
        }
        //执行第二步
        int step2 = MR2.run();
        if (step2 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/contentCF/step2/step2_output/part-r-00000");
        }
        //执行第三步
        int step3 = MR3.run();
        if (step3 == 1) {
            //执行成功后打印文件
            Files.readOutFile("/contentCF/step3/step3_output/part-r-00000");
        }
        //结束时间
        long endTime = System.currentTimeMillis();
        logger.info("任务用时："+(endTime-startTime)/1000+"秒");
    }
}

```

#### 运行结果： 

![](https://shirukai.gitee.io/images/201711221841_4.png)