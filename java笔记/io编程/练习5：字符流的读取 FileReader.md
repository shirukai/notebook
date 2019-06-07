# 练习5：字符流的读取 FileReader

### 实例：
```
package com.inspur.io;

import java.io.File;
import java.io.FileReader;

/**
 * Created by shirukai on 2017/7/26.
 *
 */
public class Filereader {
    public static void main(String[] agrs){
        Filereader filereader = new Filereader();
        filereader.fileReader();
    }
    public void fileReader(){
        FileReader fr = null;
        File f = new File("D:\\demo\\test1.txt");
        try{
            fr = new FileReader("D:\\demo\\test1.txt");
           // fr = new FileReader(f);
            char[] c= new char[1024];
            int n;
            while ((n=fr.read(c))!=-1){
                String str = new String(c,0,n);
                System.out.println(str);
            }
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            try{
                fr.close();
            }catch (Exception e2){
                e2.printStackTrace();
            }
        }
    }
}
```
