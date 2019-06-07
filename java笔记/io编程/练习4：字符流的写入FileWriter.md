# 练习4：字符流的写入

### 实例：
```
package com.inspur.io;

import java.io.FileWriter;

/**
 * Created by shirukai on 2017/7/26.
 *
 */
public class Filewrite {
    public static void main(String[] args){
        Filewrite filewrite = new Filewrite();
        filewrite.fileWrite();
    }
    public void  fileWrite(){
        FileWriter fw = null;
        try{
            fw = new FileWriter("D:\\demo\\test4.txt");
            String str = "输出字符流内容到系统文件";
            fw.write(str.toCharArray());
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            try{
                fw.close();
            }catch (Exception e2){
                e2.printStackTrace();
            }
        }
    }
}
```

