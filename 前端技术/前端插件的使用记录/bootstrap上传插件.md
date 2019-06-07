# Bootstrap上传插件 

引入js

```
<link rel="stylesheet" href="skins/css/bootstrap.css">
<link rel="stylesheet" href="skins/css/fileinput.min.css">
<link rel="stylesheet" href="skins/css/font-awesome.css">

<script src="skins/js/jquery.js"></script>
<script src="skins/js/sortable.min.js"></script>
<script src="skins/js/fileinput.min.js"></script>
<script src="skins/js/popper.min.js"></script>
<script src="skins/js/bootstrap.js"></script>
<script src="skins/js/zh.js"></script>
```

html

```
<div class="container">
    <form enctype="multipart/form-data">
        <div class="file-loading">
            <input id="uploadInput" type="file" multiple>
        </div>
    </form>
</div>
```

js

```
<script type="text/javascript">
    var uploadInput = $('#uploadInput');
    uploadInput.fileinput({
        language: 'zh',
        showUpload: true,
        showCaption: true,
        browseClass: "btn btn-primary",//选择按钮样式
        showPreview: true,//是否开启预览
        uploadUrl: '#',//拖拽同时上传
        overwriteInitial: false,//覆盖初始
        maxFileSize: 1000,//最大文件大小
        maxFilesNum: 10,//最大文件数量
        //fileType: "any",
        allowedFileExtensions: ['jpg', 'png', 'gif'],//允许上传的格式
        //allowedFileTypes: ['image', 'video', 'flash'],//文件类型
    });
    uploadInput.on("fileuploaded", function (event, data, previewId, index) {

    });//上传完成后的事件
    uploadInput.on('fileclear', function (event) {
        console.log("fileclear", event)
    })//当预览被关闭后执行的事件
    uploadInput.on('fileloaded', function (event, file, previewId, index, reade) {
        console.log(file)
    })//上传文件加载完成后执行的事件
</script>
```
