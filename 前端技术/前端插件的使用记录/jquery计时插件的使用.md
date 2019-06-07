# jquery 计时插件的使用

引入jquery.js和jquery.countdown.js

```
<script src="jquery.js"></script>
<script src="jquery.countdown.js"></script>
```

html代码：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>countdown</title>
    <script src="jquery.js"></script>
    <script src="jquery.countdown.js"></script>
</head>
<body>
<h1 id="time"></h1>
<script type="text/javascript">
    //获取当前时间戳
    var nowTime = $.now();
    var timebox = $('#time');
    var countTime = new Date(nowTime + 1000*60*6);
    timebox.countdown(countTime,function (event) {
        //控制时间格式
        var format = event.strftime('秒杀倒计时:%D天 %H时 %M分 %S秒');
        timebox.html(format)
    }).on('finish.countdown',function () {
        alert("计时完成后执行的函数")
    });
    console.log(nowTime);
</script>
</body>
</html>
```