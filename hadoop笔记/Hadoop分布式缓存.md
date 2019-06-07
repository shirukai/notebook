# Hadoop分布式缓存 

> 背景：在执行MapReduce时，可能Mapper之间需要共享一些信息，如果信息量不大，可以将其从HDFS加载到内存中，这就是Hadoop分布式缓存机制



## 矩阵相乘的例子



![https://shirukai.gitee.io/images/15101022384539Y_J62__RMA_55~DYK6T4HI.png](https://shirukai.gitee.io/images/15101022384539Y_J62__RMA_55~DYK6T4HI.png)

### 需求及思路

> 需求：给出两个矩阵，要利用MapReduce做矩阵相乘操作
>
> 思路：
>
> 矩阵相乘：左矩阵的列数 = 右矩阵的行数
>
> 相乘得到新的矩阵：行数 = 左矩阵的行 
>
> ​				   列数 = 右矩阵的列  
>
> step1：
>
> 将矩阵以固定的格式加上行号和列号保存到两个文件中。
>
> 因为MapReduce是按行读取文件，所以我们要利用MapReduce将右侧矩阵转置处理
>
> 将转置后的矩阵输出到指定文件
>
> step2：
>
> 获取step1的输出文件并存入HDFS的分布式缓存中
>
> 在进行mapper操作的setup方法中，读取缓存文件，并存入java的List容器中
>
> mapper左侧矩阵，并遍历右侧矩阵，然后相乘
>
> Reducer 操作得到新的矩阵并输出到指定文件中
>
> 

### 矩阵文件及表示方式 

![https://shirukai.gitee.io/images/1510101926767微信图片_20171108084342.png](https://shirukai.gitee.io/images/1510101926767微信图片_20171108084342.png)

matrix1.txt

```
1	1_1,2_2,3_-2,4_0
2	1_3,2_3,3_4,4_-3
3	1_-2,2_0,3_2,4_3
4	1_5,2_3,3_-1,4_2
5	1_-4,2_2,3_0,4_2
```

matrix2.txt

```
1	1_0,2_3,3_-1,4_2,5_-3
2	1_1,2_3,3_5,4_-2,5_-1
3	1_0,2_1,3_4,4_-1,5_2
4	1_-2,2_2,3_-1,4_1,5_2
```

## 编码 

### step1 

在之前的IDEA向hadoop集群提交MapReduce作业那一篇文章我们创建的项目中，继续创建利用分布式缓存进行矩阵相乘的案例。

在org.hadoop.mrs下创建matrix.step1包。

在step1包下

#### 创建Mapper1类

```
package org.hadoop.mrs.matrix.step1;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * 将右侧矩阵转置
 * LongWritable 行号类型
 * Text value 类型
 * Text 输出key类型
 * Text 输出Value类型
 * Created by shirukai on 2017/11/9.
 */
public class Mapper1 extends Mapper<LongWritable, Text, Text, Text> {
    //定义输出key
    private Text outKey = new Text();
    //定义输出value
    private Text outValue = new Text();

    /**
     * map
     *
     * @param key     行号
     * @param value   值 1 1_0,2_3,3_-1,4_2,5_-3
     * @param context 输出
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] rowAndLine = value.toString().split("\t");
        //矩阵的行号
        String row = rowAndLine[0];
        //将1_0,2_3,3_-1,4_2,5_-3以逗号分隔并添加到数组中
        String[] lines = rowAndLine[1].split(",");
        //lines = [1_0,2_3,3_-1,4_2,5_-3]
        for (int i = 0; i < lines.length; i++) {
            //列号
            String column = lines[i].split("_")[0];
            //值
            String valueStr = lines[i].split("_")[1];
            outKey.set(column);
            outValue.set(row + "_" + valueStr);
            context.write(outKey,outValue);
        }
    }
}

```

#### 创建Reducer1类

```
package org.hadoop.mrs.matrix.step1;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Reducer1
 * Created by shirukai on 2017/11/9.
 */
public class Reducer1 extends Reducer<Text, Text, Text, Text> {
    private Text outKey = new Text();
    private Text outValue = new Text();

    /**
     * @param key    map key 列号
     * @param values  map values 1_0 2_1 3_0 4_-2
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
        StringBuilder sb = new StringBuilder();
        for (Text text : values) {
            //text:行号_值
            sb.append(text + ",");
        }
        String line = null;
        if (sb.toString().endsWith(",")) {
            line = sb.substring(0, sb.length() - 1);
        }
        outKey.set(key);
        outValue.set(line);
        context.write(outKey, outValue);
    }
}

```

#### 创建MR1类

```
package org.hadoop.mrs.matrix.step1;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.hadoop.conf.Conf;

import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/7.
 */
public class MR1 {
    //输入文件的相对路径
    private static String inPath = "/matrix/step1_input/matrix2.txt";
    //输出文件的相对路径
    private static String outPath = "/matrix/step1_output";

    public int run(){
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
            e.printStackTrace();
        }catch (ClassNotFoundException e){
            e.printStackTrace();
        }catch (InterruptedException e){
            e.printStackTrace();
        }
        return -1;
    }

}

```

### step2 

在org.hadoop.mrs下创建matrix.step2包。

#### 创建Mapper2类

```
package org.hadoop.mrs.matrix.step2;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * Created by shirukai on 2017/11/7.
 */
public class Mapper2 extends Mapper<LongWritable,Text,Text,Text> {
    private static Logger logger = Logger.getLogger("this.class");
    private Text outKey = new Text();
    private Text outValue = new Text();
    private List<String> cacheList= new ArrayList<String>();
    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
        super.setup(context);
        //通过输入流将全局缓存中的右侧矩阵读入List<String>
        FileReader fr = new FileReader("matrix2");
        BufferedReader br = new BufferedReader(fr);
        //每一行的格式是： 行 tab 列_值
        String line = null;
        while ((line = br.readLine())!=null){
            cacheList.add(line);
        }
        fr.close();
        br.close();
    }


    /**
     *
     * @param key 行号
     * @param value 行 tab 列_值
     * @param context c
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
       //行
        String row_matrix1 = value.toString().split("\t")[0];
        String[] column_value_array_matrix1 = value.toString().split("\t")[1].split(",");
        for (String line : cacheList){
            //右侧矩阵的行
            //格式：行 tab 列_值
            String row_matrix2 = line.split("\t")[0];
            String[] column_value_array_matrix2 = line.split("\t")[1].split(",");

            //矩阵两行相乘得到的结果
            int result = 0;
            //遍历左矩阵的每一行每一列
            for (String column_value_matrix1 : column_value_array_matrix1){
                String column_matrix1 = column_value_matrix1.split("_")[0];
                String value_matrix1 = column_value_matrix1.split("_")[1];

                //遍历右矩阵的每一行每一列

                for (String column_value_matrix2: column_value_array_matrix2){
                    if (column_value_matrix2.startsWith(column_matrix1+"_")){
                        String value_matrix2 = column_value_matrix2.split("_")[1];
                        //将两列相乘并累加
                        result += Integer.valueOf(value_matrix1)* Integer.valueOf(value_matrix2);
                    }
                }
            }

            //result 是结果矩阵中的某个元素，坐标为 行：row_matrix1 列： row_matrix2(因为矩阵已经转置)
            outKey.set(row_matrix1);
            outValue.set(row_matrix2+"_"+result);
            //输出格式 key 行 value 列_值
            context.write(outKey,outValue);
        }
    }
}

```

#### 创建Reducer2类 

```
package org.hadoop.mrs.matrix.step2;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 *
 * Created by shirukai on 2017/11/7.
 */
public class Reducer2 extends Reducer<Text,Text,Text,Text>{
    private Text outKey = new Text();
    private Text outValue = new Text();


    /**
     *
     * @param key
     * @param values
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
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

#### 创建MR2类 

```
package org.hadoop.mrs.matrix.step2;

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
import java.net.URI;
import java.net.URISyntaxException;

/**
 *
 * Created by shirukai on 2017/11/7.
 */
public class MR2 {
    private static Logger logger = Logger.getLogger("this.class");
    //输入文件的相对路径
    private static String inPath = "/matrix/step2_input/matrix1.txt";
    //输出文件的相对路径
    private static String outPath = "/matrix/output";

    //将step1输出的转置矩阵作为全局缓存
    private static String cache = "/matrix/step1_output/part-r-00000";

    public int run(){
        try {
            //创建job配置类
            Configuration conf = Conf.get();
            //创建一个job实例
            Job job = Job.getInstance(conf,"step2");

            //添加分布式缓存文件
            job.addCacheArchive(new URI(cache+"#matrix2"));
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

#### 在matrix包下创建RunMatrix类 

```
package org.hadoop.mrs.matrix;


import org.apache.hadoop.fs.Path;
import org.apache.log4j.Logger;
import org.hadoop.files.Files;
import org.hadoop.mrs.matrix.step1.MR1;
import org.hadoop.mrs.matrix.step2.MR2;

/**
 *
 * Created by shirukai on 2017/11/7.
 */
public class RunMatrix {
    private static Logger logger = Logger.getLogger("this.class");
    public static void Run() {

        //创建文件夹
        try {
            Files.getFiles().delete(new Path("/matrix/step1_input"),true);
            Files.getFiles().delete(new Path("/matrix/step2_input"),true);
            Files.getFiles().delete(new Path("/matrix/step1_output"),true);
            Files.getFiles().delete(new Path("/matrix/output"),true);

            Files.mkdirFolder("/matrix/step1_input");
            Files.mkdirFolder("/matrix/step2_input");
            Files.mkdirFolder("/matrix/step1_output");
            Files.mkdirFolder("/matrix/output");
        }catch (Exception e){
            logger.error(e.getMessage());
        }
        //上传文件
        Files.uploadFile("D:\\Hadoop\\upload\\","matrix2.txt","/matrix/step1_input/");
        Files.uploadFile("D:\\Hadoop\\upload\\","matrix1.txt","/matrix/step2_input/");

        int resultStep1 = -1;
        resultStep1 = new MR1().run();
        if (resultStep1 == 1) {
            logger.info("step1执行成功了");
        } else {
            logger.error("step1执行失败了");
        }

        int resultStep2 = -1;
        resultStep2 = new MR2().run();
        if (resultStep2 == 1) {
            logger.info("step2执行成功了");
        } else {
            logger.error("step2执行失败了");
        }
    }
}

```

在主方法RunHadoop中添加RunMatrix方法

```
public class RunHadoop {
    private static Logger logger = Logger.getLogger("this.class");
    public static void main(String[] args) {
        RunMatrix.Run();
    }
}
```

### 运行主方法

运行结果

```
1	2_7,3_1,1_2,4_0,5_-9
2	1_9,2_16,3_31,4_-7,5_-10
3	3_7,5_16,4_-3,2_2,1_-6
4	1_-1,2_27,3_4,4_7,5_-16
5	1_-2,2_-2,3_12,4_-10,5_14

```

