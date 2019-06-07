# java中枚举的使用 

> 在JAVA SE5之前，我们要使用枚举类型时，通常会使用static final定义一组int常量来标识，代码如下:

```
public static final int MAN = 0;
public static final int WOMAN = 1;
```

现在我们可以用枚举来表示

```
enum Sex{
  MAN,
  WOMAN
}
```



## 枚举的使用：

```
package com.mavenssmlr.enumLearn;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

/**
 * 枚举学习
 * Created by shirukai on 2017/11/6.
 */

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration({"classpath:spring/spring-dao.xml"})
public class enumLearn {
    private Logger logger = LoggerFactory.getLogger(this.getClass());

    /**
     * 枚举的基本方法
     */
    //定义枚举
    enum Color {
        RED, GREEN, BLUE
    }

    enum Size {
        BIG, MIDDLE, SMALL
    }

    @Test
    public void enumBasisFunction() {
        logger.info("============Print all Color===========");
        for (Color color : Color.values()
                ) {
            logger.info("{},{}:{}", color, "ordinal", color.ordinal());
        }
        logger.info("============Print all Size===========");
        for (Size size : Size.values()
                ) {
            logger.info("{},{}:{}", size, "ordinal", size.ordinal());
        }

        Color green = Color.GREEN;
        logger.info(green.name());
    }

    /**
     * 枚举中添加普通方法、静态方法、抽象方法、构造方法
     */

    public enum SeckillStateEnum {
        SUCCESS(1, "秒杀成功"),
        END(0, "秒杀结束"),
        REPEAT_KILL(-1, "重复秒杀"),
        INNER_ERROR(-2, "系统异常"),
        DATA_REWRITE(-3, "数据篡改");
        private int state;
        private String stateInfo;

        SeckillStateEnum(int state, String stateInfo) {
            this.state = state;
            this.stateInfo = stateInfo;
        }

        public int getState() {
            return state;
        }

        public String getStateInfo() {
            return stateInfo;
        }

        public static String stateOf(int index) {
            for (SeckillStateEnum state : values()) {
                if (state.getState() == index) {
                    return state.getStateInfo();
                }
            }
            return null;
        }
    }

    @Test
    public void ErrorCodeEnTest() {
        //遍历枚举
        for (SeckillStateEnum seckillEnum:SeckillStateEnum.values()
             ) {
            //输出枚举的名字
            logger.info("name={}",seckillEnum.name());
            logger.info("state={}",seckillEnum.getState());
            logger.info("stateInfo={}",seckillEnum.getStateInfo());
        }
        //获取SUCCESS的state
        logger.info("success state={}",SeckillStateEnum.SUCCESS.getState());
        //获取SUCCESS的stateInfo
        logger.info("success stateInfo={}",SeckillStateEnum.SUCCESS.getStateInfo());
        //根据状态找到状态信息
        logger.info("stateInfo = {}",SeckillStateEnum.stateOf(-1));

    }

    enum SexEnum{
        MAN(0,"男"),
        WOMAN(1,"女");

        private int index;
        private String sex;

        SexEnum(int index,String sex){
            this.index = index;
            this.sex = sex;
        }
        public int getIndex(){
            return this.index;
        }

        public String getSex(){
            return this.sex;
        }

        public static String getSexByIndex(int index){
            for (SexEnum sexEnum:SexEnum.values()
                 ) {
                if (sexEnum.getIndex() == index){
                    return sexEnum.getSex();
                }
            }
            return null;
        }
    }

    @Test
    public void sexEnumTest(){
        logger.info(SexEnum.getSexByIndex(0));
    }
}

```

