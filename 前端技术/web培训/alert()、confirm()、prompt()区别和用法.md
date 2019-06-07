# alert()、confirm()、prompt()区别和用法

## 1. 消息警告窗 alert()

alert("这里是字符串")，一般用作对信息提示、或者是开发环境中对获取数据的捕获调试。弹出框中显示的是一个字符串信息。

```
<script type="text/javascript" language="JavaScript">
        window.alert("欢迎访问！")
</script>
```

## 2. 确认消息框confirm()

使用确认消息框可向用户问一个“是-或-否”问题，并且用户可以选择单击“确定”按钮或者单击“取消”按钮。confirm 方法的返回值为 true 或 false。该消息框也是模式对话框：用户必须在响应该对话框（单击一个按钮）将其关闭后，才能进行下一步操作。 

```
<script type="text/javascript" language="JavaScript">
        var confirm = window.confirm("点击确定返回true，点击取消返回false")
        if (confirm){
            alert(confirm)
        }else {
            alert(confirm)
        }
    </script>
```


## 3. 提示消息框prompt()
提示消息框提供了一个文本字段，用户可以在此字段输入一个答案来响应您的提示。该消息框有一个“确定”按钮和一个“取消”按钮。如果您提供了一个辅助字符串参数，则提示消息框将在文本字段显示该辅助字符串作为默认响应。否则，默认文本为 "<undefined>"。 

```
<script type="text/javascript" language="JavaScript">
        var prompt = window.prompt("这是一个提示消息框","这里可以接受用户输入的数据")
        window.alert(prompt)
    </script>
```
