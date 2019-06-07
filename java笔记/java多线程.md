# java多线程 

java多线程主要体现在Thread这个类和Runnable这个接口上。他们里面都有一个共同的方法run()

### Thread常用方法 

![](https://shirukai.gitee.io/images/201711271005_84.png)



创建线程的两种方法

第一个是继承Thread类

```
public class Actor extends Thread{
    @Override
    public void run() {
    //TO-DO 线程要执行的方法
    }
    public static void  main(String[] args){
        Thread actor = new Actor();
        actor.setName("Mr.Thread");
        actor.start();
        //也可以直接调用run()方法
        //new Actor().run();
    }
}
```



第二个是Runnable接口

```
public class Actress implements Runnable{
    public void run() {
     //TO-DO 线程要执行的方法
    }
    
    public static void  main(String[] args){
        Thread actress = new Thread(new Actress(),"MS.Runnable");
        actress.start();
        //也可以直接调用run()方法
        //new Actress().run();
    }
}
```



stop()弃用

不用interrupt停止线程

### 例子 

#### ArmyRunnable类 

```
package com.mavenssmlr.threadLean;

/**
 * 军队线程
 * 模拟作战双方的行为
 * Created by shirukai on 2017/11/27.
 */
public class ArmyRunnable implements Runnable {
    //volatile 保证了线程可以正确的去取其他线程写入的值
    volatile boolean keepRunning = true;
    public void run() {
        while (keepRunning){
            //发送五连击
            for (int i=0;i<5;i++){
                System.out.println(Thread.currentThread().getName()+"进攻对方["+i+"]");
                //让出处理器时间
                Thread.yield();
            }
        }
        System.out.println(Thread.currentThread().getName()+"结束了战斗！");
    }

}

```

#### KeyPersonThread类 

```
package com.mavenssmlr.threadLean;


public class KeyPersonThread extends Thread {
    @Override
    public void run() {
        System.out.println(getName()+"开始了战斗！");
        for (int i=0;i<10;i++){
            System.out.println(getName()+"左突右杀，攻击隋军……");
        }
        System.out.println(getName()+"结束了战斗！");
    }
}

```

#### Stage类 

```
package com.mavenssmlr.threadLean;

/**
 *
 * Created by shirukai on 2017/11/27.
 */
public class Stage extends Thread {
    @Override
    public void run() {
        System.out.println("欢迎观看隋唐演义");
        try{
            Thread.sleep(2000);
        }catch (InterruptedException e){
            e.printStackTrace();
        }
        System.out.println("大幕徐徐拉开");
        try{
            Thread.sleep(2000);
        }catch (InterruptedException e){
            e.printStackTrace();
        }
        ArmyRunnable armyTaskOfSuiDynasty = new ArmyRunnable();
        ArmyRunnable armyTaskOfRevolt = new ArmyRunnable();
        //使用Runnable接口创建线程
        Thread armySuiDynasty = new Thread(armyTaskOfSuiDynasty,"隋军");
        Thread armyOfRevolt = new Thread(armyTaskOfRevolt,"农民");

        armySuiDynasty.start();
        armyOfRevolt.start();
        //Stage线程休眠
        try {
            Thread.sleep(50);
        }catch (InterruptedException e){
            e.printStackTrace();
        }
        System.out.println("正当双方激战正酣，半路杀出了个程咬金");

        Thread mrCheng = new KeyPersonThread();
        mrCheng.setName("程咬金");
        //停止作战
        armyTaskOfSuiDynasty.keepRunning = false;
        armyTaskOfRevolt.keepRunning = false;
        try{
            Thread.sleep(2000);
        }catch (InterruptedException e){
            e.printStackTrace();
        }

        mrCheng.start();
        //调用join方法，所有线程等待调用join方法的线程完成
        try{
           mrCheng.join();
        }catch (InterruptedException e){
            e.printStackTrace();
        }

    }
    public static void main(String[] args){
        new Stage().run();
    }
}

```



