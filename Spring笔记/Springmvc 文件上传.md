# Spring mvc 单文件、多文件上传、列表展示、删除 、下载

## Spring mvc 单文件上传 

jsp

```
<!DOCTYPE html>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <%--引入meta标签--%>
    <%@include file="common/meta.jsp" %>
    <title>bootstrap上传</title>
    <%--引入css、js--%>
    <%@include file="common/upload.jsp" %>
</head>
<body>
<div class="container">
    <form enctype="multipart/form-data">
        <div class="file-loading">
            <input id="uploadInput" type="file" multiple name="file">
        </div>
    </form>
</div>
<script type="text/javascript">
    var uploadInput = $('#uploadInput');
    uploadInput.fileinput({
        language: 'zh',
        showUpload: true,
        showCaption: true,
        browseClass: "btn btn-primary",//选择按钮样式
        showPreview: true,//是否开启预览
        uploadUrl: '/plugins/upload/up',//拖拽同时上传
        overwriteInitial: false,//覆盖初始
        maxFileSize: 1000,//最大文件大小
        maxFilesNum: 10,//最大文件数量
        //fileType: "any",
        allowedFileExtensions: ['jpg', 'png', 'gif'],//允许上传的格式
        //allowedFileTypes: ['image', 'video', 'flash'],//文件类型
    });
    uploadInput.on("fileuploaded", function (event, data, previewId, index) {
        console.log(data.response)
    });//上传完成后的事件
    uploadInput.on('fileclear', function (event) {
        console.log("fileclear", event)
    })//当预览被关闭后执行的事件
    uploadInput.on('fileloaded', function (event, file, previewId, index, reade) {
        console.log(file)
    })//上传文件加载完成后执行的事件
</script>
</body>
</html>
```

配置依赖

```
<!--配置上传依赖-->
<dependency>
  <groupId>commons-fileupload</groupId>
  <artifactId>commons-fileupload</artifactId>
  <version>1.3.1</version>
</dependency>
```

上传配置

```
<bean id="multipartResolver"
      class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
    <property name="maxUploadSize" value="209715200" />
    <property name="defaultEncoding" value="UTF-8" />
    <property name="resolveLazily" value="true" />
</bean>
```

Controller

```
@RequestMapping("/upload/up")
@ResponseBody
public Map<String, String> uploadUp(
        MultipartFile file, HttpServletRequest request
) {
    //开始时间
    long startTime = System.currentTimeMillis();
    String timeString = String.valueOf(startTime);
    logger.info("______________开始时间:={}", startTime);
    Map<String, String> map = new HashMap<String, String>();
    logger.info("______________文件名:={}", file.getOriginalFilename());
    //获取当前路径
    String uploadPath = request.getServletContext().getRealPath("WEB-INF/classes/upload");
    //判断目录是否存在
    File file1 = new File(uploadPath);
    if (!file1.exists()) {
        //不存在创建目录
        file1.mkdirs();
        logger.info("_____________创建目录={}", "ok");
    }
    logger.info("______________路径:={}", uploadPath);

    if (!file.isEmpty()) {
        String fileName = timeString + file.getOriginalFilename();
        try {
            String path = uploadPath + "\\" + fileName;
            file.transferTo(new File(path));
            map.put("state", "0");
            map.put("fileName", fileName);
            map.put("fileUrl", path);
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }
    //结束时间
    long endTime = System.currentTimeMillis();
    logger.info("______________用时:={}", endTime - startTime + "ms");
    return map;
}
```

## Spring mvc 文件列表显示 

controller

```
@RequestMapping("/upload/list")
public String uploadList(
        Model model,
        HttpServletRequest request
) {
    Map<String, Object> map = new HashMap<String, Object>();
    List<Map> list = new ArrayList<Map>();
    //获取上传路径
    String path = request.getServletContext().getRealPath("WEB-INF/classes/upload");
    File file = new File(path);
    //获取目录下的所有文件和绝对路径
    File[] fs = file.listFiles();
    for (File f : fs
            ) {
        map.put("fileName", f.getName());
        map.put("filePath", f.getAbsolutePath());
        list.add(map);
        logger.info("_______file={}", f);
    }
    model.addAttribute("fileList", list);
    return "uploadlist";

}
```

jsp

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <%--引入meta标签--%>
    <%@include file="common/meta.jsp" %>
    <title>上传文件列表</title>
    <%--引入jsp标签--%>
    <%@include file="common/tag.jsp" %>
    <%--引入css、js--%>
    <%@include file="common/head.jsp" %>
</head>
<body>
<table class="table table-bordered">
    <thead>
    <tr>
        <th>文件名</th>
        <th>路径</th>
        <th>操作</th>
    </tr>
    </thead>
    <tbody>
    <c:forEach var="file" items="${fileList}">
        <tr>
            <td>${file.fileName}</td>
            <td>${file.filePath}</td>
            <td><a href="/plugins/download?fileName=${file.fileName}" class="btn btn-info btn-sm">下载</a>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <button class="btn btn-danger btn-sm" onclick="deleteFile('${file.fileName}')">删除</button>
            </td>
        </tr>
    </c:forEach>
    </tbody>
</table>
<script type="text/javascript">
    var context = '<%=request.getContextPath()%>';
    function deleteFile(fileName) {
        $.ajax({
            type:"POST",
            data:{"fileName":fileName},
            url:context+"/plugins/upload/delete",
            success:function (data) {
                console.log(data);
                if (data.state = 1){
                    window.location.reload();
                }
            }
        })
    }
</script>
</body>
</html>
```

## 文件删除 

```
@RequestMapping("/upload/delete")
@ResponseBody
public Map<String, Object> uploadDelete(
        @RequestParam("fileName") String fileName,
        HttpServletRequest request
) {
    Map<String, Object> map = new HashMap<String, Object>();
    //文件路径
    String path = request.getServletContext().getRealPath("WEB-INF/classes/upload");
    File file = new File(path, fileName);
    //如果文件存在删除
    if (file.exists()) {
        file.delete();
        map.put("state", 1);
        map.put("info", "删除成功");
    } else {
        map.put("state", 0);
        map.put("info", "文件不存在");
    }
    return map;
}
```

## 文件下载 

```
@RequestMapping("/download")
@ResponseBody
public void download(
        @RequestParam("fileName") String fileName,
        HttpServletRequest request,
        HttpServletResponse response
){
    Map<String,Object> map = new HashMap<String,Object>();
    //设置响应投和客户端保存文件名
    response.setCharacterEncoding("utf-8");
    response.setContentType("multipart/form-data");
    response.setHeader("Content-Disposition", "attachment;fileName=" + fileName);
    //用于记录以完成的下载的数据量，单位是byte
    long downloadedLength = 0l;
    String filePath = request.getServletContext().getRealPath("WEB-INF/classes/upload/")+fileName;
    try {
        //打开本地文件流
        InputStream inputStream = new FileInputStream(filePath);
        //激活下载操作
        OutputStream os = response.getOutputStream();
        //循环写入输出流
        byte[] bytes = new byte[2048];
        int length;
        while ((length = inputStream.read(bytes))>0){
            os.write(bytes,0,length);
            downloadedLength += bytes.length;
        }
        map.put("downLength",downloadedLength);
        //关闭输出流
        os.close();
        inputStream.close();
    } catch (IOException e) {
        logger.error(e.getMessage(), e);
    }
}
```