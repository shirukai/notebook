# java 利用Future做超时任务处理 

```
Callable<String> task = new Callable<String>() {
    @Override
    public String call() throws Exception {
        return HttpRequestUtil.host().doGet(requestUrl);
    }
};
ExecutorService executorService = Executors.newSingleThreadExecutor();
Future<String> future = executorService.submit(task);
String hostInfo = future.get(10,TimeUnit.SECONDS);
```

连接：http://blog.51cto.com/5880861/1714852