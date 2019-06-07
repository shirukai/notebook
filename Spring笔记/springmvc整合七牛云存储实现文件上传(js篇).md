# springmvc整合七牛云存储实现文件上传(js篇) 

所谓js实现，是指在客户端进行上传，而不是在服务器端进行上传，这样可以极大的提高上传速率。要想利用js实现七牛上传，同样需要后台获取uptoken，得到验证后才允许上传。

## 官方dome

![http://ov1a6etyz.bkt.clouddn.com//1508744617834qiniuupload.gif](http://ov1a6etyz.bkt.clouddn.com//1508744617834qiniuupload.gif)

需要引入css、js

七牛下载链接:http://ov1a6etyz.bkt.clouddn.com/qiniu.rar

```
<%--引入css--%>
<link href="<%=request.getContextPath()%>/skins/qiniu/css/bootstrap.css" rel="stylesheet">
<link href="<%=request.getContextPath()%>/skins/qiniu/css/main.css" rel="stylesheet">
<link href="<%=request.getContextPath()%>/skins/qiniu/css/highlight.css" rel="stylesheet">
```

```
<%--引入js文件--%>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/jquery.min.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/bootstrap.min.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/moxie.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/plupload.dev.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/zh_CN.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/ui.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/qiniu.min.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/highlight.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/main.js"></script>
<script type="text/javascript">hljs.initHighlightingOnLoad();</script>
```

html

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <%--引入meta标签--%>
    <%@include file="common/meta.jsp" %>
    <title>七牛js上传</title>
    <%--引入css--%>
    <link href="<%=request.getContextPath()%>/skins/qiniu/css/bootstrap.css" rel="stylesheet">
    <link href="<%=request.getContextPath()%>/skins/qiniu/css/main.css" rel="stylesheet">
    <link href="<%=request.getContextPath()%>/skins/qiniu/css/highlight.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-default navbar-fixed-top">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                    data-target="#bs-example-navbar-collapse-6" aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">js上传文件到七牛</a>
        </div>
    </div>
</nav>

<div class="container" style="padding-top: 60px;">
    <ul class="nav nav-tabs" role="tablist">
        <li role="presentation" class="active">
            <a href="#demo" id="demo-tab" role="tab" data-toggle="tab" aria-controls="demo" aria-expanded="true">示例</a>
        </li>
        <li role="presentation">
            <a href="#log" id="log-tab" role="tab" data-toggle="tab" aria-controls="log">日志</a>
        </li>
    </ul>
    <div class="tab-content">
        <div role="tabpanel" class="tab-pane fade in active" id="demo" aria-labelledby="demo-tab">

            <div class="row" style="margin-top: 20px;">
                <input type="hidden" id="domain" value="http://ov1a6etyz.bkt.clouddn.com/">
                <input type="hidden" id="uptoken_url" value="/plugins/uptoken">
                <ul class="tip col-md-12 text-mute">
                    <li>
                        <small>
                            JavaScript SDK 基于 Plupload 开发，可以通过 Html5 或 Flash 等模式上传文件至七牛云存储。
                        </small>
                    </li>
                    <li>
                        <small>临时上传的空间不定时清空，请勿保存重要文件。</small>
                    </li>
                    <li>
                        <small>Html5模式大于4M文件采用分块上传。</small>
                    </li>
                    <li>
                        <small>上传图片可查看处理效果。</small>
                    </li>
                    <li>
                        <small>本示例限制最大上传文件100M。</small>
                    </li>
                </ul>
                <div class="col-md-12">
                    <div id="container">
                        <a class="btn btn-default btn-lg " id="pickfiles" href="#">
                            <i class="glyphicon glyphicon-plus"></i>
                            <span>选择文件</span>
                        </a>
                    </div>
                </div>
                <div style="display:none" id="success" class="col-md-12">
                    <div class="alert-success">
                        队列全部文件处理完毕
                    </div>
                </div>
                <div class="col-md-12 ">
                    <table class="table table-striped table-hover text-left" style="margin-top:40px;display:none">
                        <thead>
                        <tr>
                            <th class="col-md-4">Filename</th>
                            <th class="col-md-2">Size</th>
                            <th class="col-md-6">Detail</th>
                        </tr>
                        </thead>
                        <tbody id="fsUploadProgress">
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
        <div role="tabpanel" class="tab-pane fade" id="code" aria-labelledby="code-tab">
            <div role="tabpanel" class="tab-pane fade" id="log" aria-labelledby="log-tab">
                <pre id="qiniu-js-sdk-log"></pre>
            </div>
        </div>
    </div>

    <div class="modal fade body" id="myModal-img" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
         aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title" id="myModalLabel">图片效果查看</h4>
                </div>
                <div class="modal-body">
                    <div class="modal-body-wrapper text-center">
                        <a href="" target="_blank">
                            <img src="" alt="" data-key="" data-h="">
                        </a>
                    </div>
                    <div class="modal-body-footer">
                        <div class="watermark">
                            <span>水印控制：</span>
                            <a href="#" data-watermark="NorthWest" class="btn btn-default">
                                左上角
                            </a>
                            <a href="#" data-watermark="SouthWest" class="btn btn-default">
                                左下角
                            </a>
                            <a href="#" data-watermark="NorthEast" class="btn btn-default">
                                右上角
                            </a>
                            <a href="#" data-watermark="SouthEast" class="btn btn-default disabled">
                                右下角
                            </a>
                            <a href="#" data-watermark="false" class="btn btn-default">
                                无水印
                            </a>
                        </div>
                        <div class="imageView2">
                            <span>缩略控制：</span>
                            <a href="#" data-imageview="large" class="btn btn-default disabled">
                                大缩略图
                            </a>
                            <a href="#" data-imageview="middle" class="btn btn-default">
                                中缩略图
                            </a>
                            <a href="#" data-imageview="small" class="btn btn-default">
                                小缩略图
                            </a>
                        </div>
                        <div class="imageMogr2">
                            <span>高级控制：</span>
                            <a href="#" data-imagemogr="left" class="btn btn-default no-disable-click">
                                逆时针
                            </a>
                            <a href="#" data-imagemogr="right" class="btn btn-default no-disable-click">
                                顺时针
                            </a>
                            <a href="#" data-imagemogr="no-rotate" class="btn btn-default">
                                无旋转
                            </a>
                        </div>
                        <div class="text-warning">
                            备注：小图片水印效果不明显，建议使用大图片预览水印效果
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <span class="pull-left">本示例仅演示了简单的图片处理效果，了解更多请点击</span>

                    <a href="https://github.com/SunLn/qiniu-js-sdk" target="_blank" class="pull-left">本SDK文档</a>
                    <span class="pull-left">或</span>

                    <a href="http://developer.qiniu.com/docs/v6/api/reference/fop/image/" target="_blank"
                       class="pull-left">七牛官方文档</a>

                    <button type="button" class="btn btn-primary" data-dismiss="modal">关闭</button>
                </div>
            </div>
        </div>
    </div>
</div>

<%--引入js文件--%>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/jquery.min.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/bootstrap.min.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/moxie.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/plupload.dev.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/zh_CN.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/ui.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/qiniu.min.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/highlight.js"></script>
<script src="<%=request.getContextPath()%>/skins/qiniu/js/main.js"></script>
<script type="text/javascript">hljs.initHighlightingOnLoad();</script>
</body>
</html>
```

后台：

maven配置七牛获取token的依赖

```
<dependency>
  <groupId>com.qiniu</groupId>
  <artifactId>sdk</artifactId>
  <version>6.1.7</version>
</dependency>
```

Controller

```
@RequestMapping("uptoken")
@ResponseBody
public ResponseEntity<Object> makeToken() {
    Config.ACCESS_KEY = "kT93RyyRfkVBgned_N-xLjAlB3kobwGyt7aykgx3";
    Config.SECRET_KEY = "MVOQB-Nz2q55UA7p9H_MSJ9XkJrGrPyv_oSnbJtX";
    Mac mac = new Mac(Config.ACCESS_KEY, Config.SECRET_KEY);
    String bucketName = "notebook";
    PutPolicy putPolicy = new PutPolicy(bucketName);
    Map<String,String> map  = new HashMap<String, String>();
    try {
        String uptoken = putPolicy.token(mac);
        logger.info("___________uptoken={}",uptoken);
        map.put("uptoken",uptoken);
        return new ResponseEntity(map, HttpStatus.OK);
    } catch (AuthException e) {
        e.printStackTrace();
        return new ResponseEntity(null, HttpStatus.BAD_REQUEST);
    } catch (JSONException e) {
        e.printStackTrace();
        return new ResponseEntity(null, HttpStatus.BAD_REQUEST);
    }
}
```

![https://shirukai.gitee.io/images/2017%E5%B9%B410%E6%9C%8823%E6%97%A5155233.png](https://shirukai.gitee.io/images/2017%E5%B9%B410%E6%9C%8823%E6%97%A5155233.png)

注意这个地方，这就是我们后台返回得uptoken。domain是我们储存空间的外链地址。



## formdata 

直接在表单中的js上传到七牛的方法

![<http://ov1a6etyz.bkt.clouddn.com/qiniuuformdatapload.gif>](<http://ov1a6etyz.bkt.clouddn.com/qiniuuformdatapload.gif>)

html

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>formdata</title>
    <link href="<%=request.getContextPath()%>/skins/qiniu/css/formdata.css" rel="stylesheet">
    <script src="<%=request.getContextPath()%>/skins/qiniu/js/jquery.min.js"></script>
    <script src="<%=request.getContextPath()%>/skins/qiniu/js/formdata.js"></script>
    <script>
        var domain = "http://ov1a6etyz.bkt.clouddn.com/"; // you bucket domain  eg: http://xxx.bkt.clouddn.com
    </script>
</head>
<body>
<div class="container">
    <div class="title">Formdata 上传 demo</div>

    <!-- Document：https://developer.qiniu.com/kodo/manual/form-upload -->
    <form id="testform" method="post" enctype="multipart/form-data">
        <input name="key" id="key" type="hidden" value="">
        <input name="token" type="hidden" value="${uptoken}">
        <input id="userfile" name="file" type="file" />

        <!-- take photo with phone -->
        <!-- <input id="userfile" name="file" accept="image/*" type="file" /> -->

        <!-- take video with phone -->
        <!-- <input id="userfile" name="file" type="file" accept="video/*"/> -->

        <input name="accept" type="hidden" />
    </form>

    <!-- add file -->
    <label for="userfile">
        <span></span>
        <em>添加文件</em>
    </label>

    <!-- upload info -->
    <div class="selected-file"></div>
    <div class="progress"></div>
    <div class="uploaded-result"></div>
</div>
</body>
</html>
```

controller

```
@RequestMapping("formdata")
public String formData(Model model){
    Config.ACCESS_KEY = "kT93RyyRfkVBgned_N-xLjAlB3kobwGyt7aykgx3";
    Config.SECRET_KEY = "MVOQB-Nz2q55UA7p9H_MSJ9XkJrGrPyv_oSnbJtX";
    Mac mac = new Mac(Config.ACCESS_KEY, Config.SECRET_KEY);
    String bucketName = "notebook";
    PutPolicy putPolicy = new PutPolicy(bucketName);
    try {
        String uptoken = putPolicy.token(mac);
        logger.info("___________uptoken={}",uptoken);
        model.addAttribute("uptoken",uptoken);
    } catch (AuthException e) {
        e.printStackTrace();
    } catch (JSONException e) {
        e.printStackTrace();
    }
    return "formdata";
}
```

