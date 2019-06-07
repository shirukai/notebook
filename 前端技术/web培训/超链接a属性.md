
# <a> 超链接
主要属性：

* href：设置链接的URL,相对路径或绝对路径
* target：显示连接的窗口或框架

    _blank:在新窗口中打开链接
    
    _self:在当前窗口打开链接
    
    _parent:在父窗口中打开链接
    
    _top:在定级窗口中打开链接
    
    framename：窗口名称
    
* name：超链接，创建文档内的书签
* title：设置超链接的文字说明（鼠标悬停时显示）

```
<body>
<ul type="circle">
    <li>
        <a href="http://www.baidu.com" title="百度" target="_blank">百度blank</a>
        <a href="http://www.baidu.com" title="百度" target="_self">百度self</a>
        <a href="http://www.baidu.com" title="百度" target="iframe">百度self</a>
    </li>
</ul>
<iframe name="iframe" width="400" height="400"></iframe>
</body>
```
