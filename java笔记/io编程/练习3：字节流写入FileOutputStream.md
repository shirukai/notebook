# 练习3：字节流写入FileOutputStream


```
package com.inspur.io;

import java.io.File;
import java.io.FileOutputStream;

/**
 * Created by shirukai on 2017/7/26.
 *
 */
public class Fileoutstream {
    public static void main(String[] args){
        Fileoutstream fileoutstream = new Fileoutstream();
        fileoutstream.fileOutput();
    }
    public void fileOutput(){
        //创建文件对象
        File f1 = new File("D:\\demo\\test2.txt");
        //创建输出文件流对象
        FileOutputStream os = null;
        try{
            os= new FileOutputStream(f1);
            String str = "输出内容到系统文件中";
            os.write(str.getBytes());
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            try{
                os.close();
            }catch (Exception e2){
                e2.printStackTrace();
            }
        }
    }
}
```
