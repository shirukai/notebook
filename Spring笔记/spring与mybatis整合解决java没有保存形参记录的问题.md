# spring与mybatis整合解决java没有保存形参记录的问题

接口方法：

```
List<Seckill> queryAll(int offset,int limit);
```

SQL:

```
    <select id="queryAll" resultType="Seckill">
        SELECT seckill_id,name,number,start_time,end_time,create_time
        FROM seckill
        ORDER BY create_time DESC
        limit #{offset},#{limit}
    </select>
```

单元测试：

```
    @Test
    public void queryAll() throws Exception {
        List<Seckill> seckills = seckillDao.queryAll(10, 1000);
        for (Seckill seckill : seckills) {
            System.out.println(seckill);
        }
    }
```

错误提示：

```
org.mybatis.spring.MyBatisSystemException: nested exception is org.apache.ibatis.binding.BindingException: Parameter 'offset' not found. Available parameters are [1, 0, param1, param2]
```

错误原因：

java是没有保存形象的记录，当执行这个queryAll(int offset,int limit)方法时，里面的参数会被转化成queryAll(arg0,arg1)，所以我们sql离通过#{offset}，#{limit}是获取不到参数的，因此会报错。

解决方法：

一、修改sql：

    <select id="queryAll" resultType="Seckill">
        SELECT seckill_id,name,number,start_time,end_time,create_time
        FROM seckill
        ORDER BY create_time DESC
        limit #{0},#{1}
    </select>
0代表第一个参数，1代表第二个参数。

二、利用注解的方式设置形参

```
List<Seckill> queryAll(@Param("offset") int offset, @Param("limit") int limit);
```

