## springmvc整合七牛云存储实现文件上传(java篇) 

在springmvc上传文件到本地的基础上，整合七牛云存储，实现简单的上传功能。

首先maven配置依赖

```
<!--七牛依赖-->
<dependency>
  <groupId>com.qiniu</groupId>
  <artifactId>sdk</artifactId>
  <version>6.1.7</version>
</dependency>
<dependency>
  <groupId>com.qiniu</groupId>
  <artifactId>qiniu-java-sdk</artifactId>
  <version>7.2.6</version>
  <scope>compile</scope>
</dependency>
<dependency>
  <groupId>com.squareup.okhttp3</groupId>
  <artifactId>okhttp</artifactId>
  <version>3.3.1</version>
  <scope>compile</scope>
</dependency>
<dependency>
  <groupId>com.google.code.gson</groupId>
  <artifactId>gson</artifactId>
  <version>2.6.2</version>
  <scope>compile</scope>
</dependency>
<dependency>
  <groupId>com.qiniu</groupId>
  <artifactId>happy-dns-java</artifactId>
  <version>0.1.4</version>
  <scope>compile</scope>
</dependency>
```

直接贴代码：

文件上传到本地后，然后上传到七牛云，成功上传后删除本地文件。

```
/**
 * java-sdk 上传到七牛
 */

@RequestMapping("/qiniu/java/upload")
public String javaUpload() {
    return "qiniujavaupload";
}
@RequestMapping("/qiniu/java/upload/up")
@ResponseBody
public Map<String,String> qiniuUpload(
        MultipartFile file, HttpServletRequest request
){
    //设置好账号的ACCESS_KEY和SECRET_KEY
    String ACCESS_KEY = "kT93RyyRfkVBgned_N-xLjAlB3kobwGyt7aykgx3";
    String SECRET_KEY = "MVOQB-Nz2q55UA7p9H_MSJ9XkJrGrPyv_oSnbJtX";
    //要上传的空间
    String bucketname = "notebook";
    //上传到七牛后保存的文件名
    String key;
    //上传文件的路径
    String FilePath;
    //密钥配置
    Auth auth = Auth.create(ACCESS_KEY, SECRET_KEY);
    //自动识别要上传的空间的初村区域是华东、华北、华南
    Zone z = Zone.autoZone();
    com.qiniu.storage.Configuration  c  = new com.qiniu.storage.Configuration(z);
    //创建上传对象
    UploadManager uploadManager = new UploadManager(c);
    //外链域名
    String domian = "http://ov1a6etyz.bkt.clouddn.com/";
    //获取upToken
    String upToken = auth.uploadToken(bucketname);
    //开始时间
    long  startTime=System.currentTimeMillis();
    String timeString = String.valueOf(startTime);
    logger.info("______________开始时间:={}",startTime);
    Map<String ,String> map = new HashMap<String, String>();
    logger.info("______________文件名:={}",file.getOriginalFilename());
    //获取当前路径
    String uploadPath = request.getServletContext().getRealPath("WEB-INF/classes/upload");
    logger.info("______________路径:={}",uploadPath);

    if (!file.isEmpty()){
        String fileName = timeString+file.getOriginalFilename();
        try {
            String path=uploadPath+"\\"+fileName;
            file.transferTo(new File(path));
            key = fileName;
            FilePath = path;
            //上传到七牛
            //调用put方法
            try {
                Response response = uploadManager.put(FilePath,key,upToken);
                logger.info("___________________response={}",response.bodyString());
                map.put("state","1");
                map.put("info","上传七牛成功");
                map.put("fileName",fileName);
                map.put("qiniuUrl",domian+"/"+fileName);

            }catch (QiniuException e){
                map.put("state","0");
                map.put("info","上传七牛失败");
                Response r = e.response;
                logger.error("上传七牛异常={}",r.toString());

            }finally {
                //上传七牛完成后删除本地文件
                File deleteFile = new File(path,fileName);
                if (deleteFile.exists()){
                    deleteFile.delete();
                }
            }

        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }
    //结束时间
    long endTime=System.currentTimeMillis();
    logger.info("______________用时:={}",endTime-startTime+"ms");
    return map;
}
```