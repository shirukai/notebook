# js运算符自动转换规则

### 自动转换成布尔值 

当JavaScript遇到预期为布尔值的地方，会将非布尔值的参数自动转换为布尔值，比如if语句的条件部分。

```
<script type="text/javascript" language="javascript">
        var foo = "abc";
        if(foo){
            alert(foo)
        }
    </script>
```
alert返回结果是 “abc”

### 自动转换为字符串

字符串的自动转换，主要发生在加法运算时，当一个值为字符串，另一个值为非字符串，则后者转换为字符串。

```
<script type="text/javascript" language="JavaScript">
        var foo = "11"+2;
        alert(foo);
        //alert 返回112
        var foo1 = 11+"2";
        alert(foo1);
        //alert返回112
        var foo2 = 11+2+"3";
        alert(foo2)
        //alert 返回133
    </script>
```
### 自动转换为数值

通常在执行算术运算的时候回自动转换成数值类型（加法时注意）

```
<script type="text/javascript" language="JavaScript">
        var foo ="11"-2;
        alert(foo)
    </script>
```

## 相等运算符转换规则

### 如果有个一个操作数是布尔值、则在比较相等性之前先将其转换为数值--false转换成0，而true转换成1

```
<script type="text/javascript" language="JavaScript">
    <script type="text/javascript" language="JavaScript">
        if(true==1){
            alert("true在相等运算时值为1")
        }
        if(false==0){
            alert("false在相等运算时值为0")
        }
    </script>
```
#### 如果一个操作数是一个字符串，另一个操作数是数值，在比较相等性之前先将字符串转换为数值。

```
<script type="text/javascript" language="JavaScript">
        if("1"==1){
            alert("字符串转换成数值了")
        }
    </script>
```

#### 如果一个操作数是对象，另一个操作数不是，则调用对象的value（）方法，用得到的基本类型值按照前面的规则进行比较。

---

valueOf()：返回最适合该对象类型的原始值；

toString(): 将该对象的原始值以字符串形式返回。这两个方法一般是交由JS去隐式调用，以满足不同的运算情况。在数值运算里，会优先调用valueOf()，如a + b；在字符串运算里，会优先调用toString()，如alert(c)。
