# 练习：字节流读写 FileInputStream

```
package com.inspur.io;
import java.io.File;
import java.io.FileInputStream;

/**
 * Created by shirukai on 2017/7/26.
 *
 */
public class Fileinputstream {
    public static void main(String[] args){
        Fileinputstream fileinputstream = new Fileinputstream();
        fileinputstream.fileInput();
    }
    public void fileInput(){
        //创建文件对象
        File f = new File("D:\\demo\\test1.txt");
        //创建输入文件流对象
        FileInputStream is = null;
        try{
            is = new FileInputStream(f);
            byte[] bytes = new byte[1024];
            int n ;
            while ((n = is.read(bytes))!=-1){
                String srt = new String(bytes,0,n);
                System.out.println(srt);
            }
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            try{
                is.close();
            }catch (Exception e2){
                e2.printStackTrace();
            }
        }
    }
}
```
