# js/jQuery实现iframe高度自适应

虽然现在前端框架很多，但是有时候还是会需要用到iframe的，在使用iframe的时候，为了美观一点，会尽量避免在父窗口中出现滚动条，在notebook这个项目案例中，也是大量使用了iframe，其中也有高度自适应，下面将用原生js和jQuery两种方法去实现高度自适应。
### js代码写在iframe子页面中

```
	//初始化方法
	adjIframe();   
	//调整父ifram的高度
   var tmpHeight = 0;
   var adjHeight=0;
   function adjIframe() {
   //设置父页面iframe高度为0
       window.parent.document.getElementById("viewDetails").height =0;
	//设置iframe高度=滚动条高度
       window.parent.document.getElementById("viewDetails").height =
           window.parent.document.getElementById("viewDetails").contentWindow.document.body.scrollHeight;
   //考虑到页面有时候加载图片，会影响到高度，所以加一个延时循环，直到高度不变时停止循环        
       setTimeout(function () {
           tmpHeight = window.parent.document.getElementById("viewDetails").contentWindow.document.body.scrollHeight;
           if(tmpHeight>adjHeight){
               adjHeight=tmpHeight;
               adjIframe();
           }
       },1000)
   }
```

### jQuery 方法写在子页面中

```
	//初始化方法
	adjIframe();   
	//调整父ifram的高度
   var tmpHeight = 0;
   var adjHeight=0;
   function adjIframe() {
   //jQuery获取iframe对象
   var parentIframe = $("#viewDetails"，window.parent.document)
   //设置iframe高度=0；
   parentIframe.height(0);
	//设置iframe高度=滚动条高度
	var tmHeight = parentIframe[0].contentWindow.document.body.scrollHeight
	parentIframe.height(tmHeight)
     
   //考虑到页面有时候加载图片，会影响到高度，所以加一个延时循环，直到高度不变时停止循环        
       setTimeout(function () {
           if(tmpHeight>adjHeight){
               adjHeight=tmpHeight;
               adjIframe();
           }
       },1000)
   }
```

###  jQuery一些获取高度的用法
获取窗口可视区域高度

```
$(window).height();
```

获取文档高度

```
$(document).height();
```