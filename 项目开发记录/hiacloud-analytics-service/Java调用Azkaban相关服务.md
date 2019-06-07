# Java调用Azkaban相关服务

项目里主要使用远程调用azkaban提供的api进行相关任务的执行，下面主要从基础接口封装和调用实例来记录相关代码。

## 基础接口封装

参考官网ajax-api:http://azkaban.github.io/azkaban/docs/latest/#ajax-api

对于azkaban基础接口的封装主要是利用java调用azkaban官网提供的ajax-api，通过springframework提供的restTemplate进行http请求。封装接口主要包括：登录、创建project、删除project、上传zip、执行flow、查询project中的flow、查询execution信息、查询执行job日志、查询flow执行情况等。

### 代码部分：

```
**
 * Created by shirukai on 2018/4/24.
 */
@Component
public class AzkabanAdapter {
    private static Logger log = LoggerFactory.getLogger(AzkabanHandle.class);
    private String URI;
    private String userName;
    private String password;
    private static RestTemplate restTemplate;
    private static String SESSION_ID;

    static {
        SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
        requestFactory.setConnectTimeout(2000);
        requestFactory.setReadTimeout(2000);
        restTemplate = new RestTemplate(requestFactory);
    }

    AzkabanAdapter(@Value("${azkaban.url}") String URI,
                   @Value("${azkaban.username}") String userName,
                   @Value("${azkaban.password}") String password) {
        this.URI = URI;
        this.userName = userName;
        this.password = password;
        SESSION_ID = "b1d4f665-f4b9-4e7d-b83a-b928b41cc323";
    }

    /**
     * 登录
     */
    public void login() {
        HttpHeaders hs = new HttpHeaders();
        hs.add("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");
        hs.add("X-Requested-With", "XMLHttpRequest");
        LinkedMultiValueMap<String, String> linkedMultiValueMap = new LinkedMultiValueMap<String, String>();
        linkedMultiValueMap.add("action", "login");
        linkedMultiValueMap.add("username", userName);
        linkedMultiValueMap.add("password", password);

        HttpEntity<LinkedMultiValueMap<String, String>> httpEntity = new HttpEntity<>(linkedMultiValueMap, hs);
        String responsResultString = restTemplate.postForObject(URI, httpEntity, String.class);
        responsResultString = responsResultString.replace(".", "_");
        JSONObject resJson = JSON.parseObject(responsResultString);
        if (resJson.getString("status").equals("success")) {
            SESSION_ID = resJson.getString("session_id");
            log.info("azkaban login success:{}", resJson);
        } else {
            log.warn("azkabna login failure:{}", resJson);
        }
    }

    /**
     * 创建项目
     *
     * @param projectName project 名称
     * @param description 描述
     * @return str
     */
    public String createProject(String projectName, String description) {
        HttpHeaders hs = new HttpHeaders();
        hs.add("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");
        hs.add("X-Requested-With", "XMLHttpRequest");
        LinkedMultiValueMap<String, String> linkedMultiValueMap = new LinkedMultiValueMap<String, String>();
        linkedMultiValueMap.add("session.id", SESSION_ID);
        linkedMultiValueMap.add("action", "create");
        linkedMultiValueMap.add("name", projectName);
        linkedMultiValueMap.add("description", description);
        HttpEntity<LinkedMultiValueMap<String, String>> httpEntity = new HttpEntity<>(linkedMultiValueMap, hs);
        deleteProject(projectName);
        String res = restTemplate.postForObject(URI + "/manager", httpEntity, String.class);
        log.info("azkaban create project:{}", res);
        return res;
    }

    /**
     * 删除项目
     *
     * @param projectName project名称
     * @return str
     */
    public boolean deleteProject(String projectName) {
        HttpHeaders hs = new HttpHeaders();
        hs.add("Content-Type", "application/x-www-form-urlencoded; charset=utf-8");
        hs.add("X-Requested-With", "XMLHttpRequest");
        hs.add("Accept", "text/plain;charset=utf-8");
        Map<String, String> map = new HashMap<>();
        map.put("id", SESSION_ID);
        map.put("project", projectName);
        ResponseEntity<String> exchange = restTemplate.exchange(URI + "/manager?session.id={id}&delete=true&project={project}", HttpMethod.GET,
                new HttpEntity<String>(hs), String.class, map);
        log.info("azkaban delete project:{}", 200 == exchange.getStatusCodeValue());
        return 200 == exchange.getStatusCodeValue();
    }

    /**
     * 上传zip
     *
     * @param zipFilePath zip 路径
     * @param projectName project 名称
     * @return str
     */
    public String uploadZip(String zipFilePath, String projectName) {
        FileSystemResource resource = new FileSystemResource(new File(zipFilePath));
        LinkedMultiValueMap<String, Object> linkedMultiValueMap = new LinkedMultiValueMap<String, Object>();
        linkedMultiValueMap.add("session.id", SESSION_ID);
        linkedMultiValueMap.add("ajax", "upload");
        linkedMultiValueMap.add("project", projectName);
        linkedMultiValueMap.add("file", resource);
        String res = restTemplate.postForObject(URI + "/manager", linkedMultiValueMap, String.class);
        log.info("azkaban upload zip:{}", res);
        return res;
    }

    /**
     * 执行Flow
     *
     * @param projectName project 名称
     * @param flowName    flow 名称
     * @return str
     */
    public String startFlow(String projectName, String flowName) {
        LinkedMultiValueMap<String, Object> linkedMultiValueMap = new LinkedMultiValueMap<String, Object>();
        linkedMultiValueMap.add("session.id", SESSION_ID);
        linkedMultiValueMap.add("ajax", "executeFlow");
        linkedMultiValueMap.add("project", projectName);
        linkedMultiValueMap.add("flow", flowName);
        String res = restTemplate.postForObject(URI + "/executor", linkedMultiValueMap, String.class);
        log.info("azkaban start flow:{}", res);
        return JSON.parseObject(res).getString("execid");

    }

    /**
     * 查询项目的flow
     *
     * @param projectName project name
     * @return str
     */
    public String fetchProjectFlows(String projectName) {
        String res = restTemplate
                .getForObject(URI + "/manager?ajax=fetchprojectflows&session.id={1}&project={2}"
                        , String.class, SESSION_ID, projectName
                );
        log.info("azkban fetch project flows:{}", res);
        return res;
    }

    /**
     * azkaban执行信息
     *
     * @param execId 执行id
     * @return str
     */
    public String executionInfo(String execId) {
        LinkedMultiValueMap<String, Object> linkedMultiValueMap = new LinkedMultiValueMap<String, Object>();
        linkedMultiValueMap.add("session.id", SESSION_ID);
        linkedMultiValueMap.add("ajax", "fetchexecflow");
        linkedMultiValueMap.add("execid", execId);
        String res = restTemplate.postForObject(URI + "/executor", linkedMultiValueMap, String.class);
        log.info("azkaban execution info:{}", res);
        return res;
    }

    /**
     * 查询执行job日志
     *
     * @param execId 执行ID
     * @param jobId  jobID
     * @param offset 起始位置
     * @param length 长度
     * @return str
     */
    public String fetchExecutionJobLogs(String execId, String jobId, int offset, int length) {
        String res = restTemplate
                .getForObject(URI + "/executor?ajax=fetchExecJobLogs&session.id={1}&execid={2}&jobId={3}&offset={4}&length={5}"
                        , String.class, SESSION_ID, execId, jobId, offset, length
                );
        log.info("azkban execution job logs:{}", res);
        return res;
    }

    /**
     * 查询flow执行情况
     *
     * @param execId execId
     * @return str
     */
    public String fetchFlowExecution(String execId) {
        String res = restTemplate
                .getForObject(URI + "/executor?ajax=fetchexecflow&session.id={1}&execid={2}"
                        , String.class, SESSION_ID, execId
                );
        log.info("azkban execution flow:{}", res);

        return res;
    }

    public FlowExecutionDetailVO fetchFlowExecutionObject(String execId) {

        FlowExecutionDetailVO res = restTemplate
                .getForObject(URI + "/executor?ajax=fetchexecflow&session.id={1}&execid={2}"
                        , FlowExecutionDetailVO.class, SESSION_ID, execId
                );
        log.info("azkban execution flow:{}", res);

        //return responseHandle(res);

        return res;
    }
}
```

## 调用实例

在项目中将AzkabanAdapter注入到spring里，使用单例运行。对于azkaban执行任务的流程如下：分析编排任务、拉取算法物件、生成job、打包zip、创建azkaban项目、上传zip、执行任务、返回任务信息。

```
/**
 * azkaban任务执行相关服务
 */
@Service
public class AzkabanService {
    //临时目录
    @Value("${" + Constants.ANALYTICS_SERVICE_TEMP_ORCHESTRATIONS_PATH + "}")
    private String tempPath;

    @Value("${fs.defaultFS}")
    private String fs_defaultFS;
    //租户ID
    @Value("${tenantId}")
    private String tenant_id;
    @Value("${analyticService.analyticsArtifacts.baseDir}")
    private String analyticsArtifacts_baseDir;

    @Autowired
    OrchestrationRepository orchestrationRepository;

    @Autowired
    AnalyticsService analyticsService;
    @Autowired
    ExecutionRepository executionRepository;
    @Autowired
    AzkabanAdapter azkabanAdapter;
    @Autowired
    AnalyticsRepository analyticsRepository;
    @Autowired
    AlgorithmParamUtil algorithmParamUtil;

    /**
     * 执行编排
     *
     * @param orchestrationId 编排ID
     */
    public JSONObject executeOrchestration(String orchestrationId) {
        //获取编排信息
        Orchestration orchestration = orchestrationRepository.findOne(orchestrationId);
        Project project = orchestration.getProject();
        if (isRunning(orchestration)) {
            throw new RuntimeException("有正在执行的任务，请等待执行完成后重试！");
        }
        //azkaban base name
        String baseName = tenant_id + "_" + project.getId(),
                //azkaban project name
                azProjectName = "project_" + baseName;
        //判断是否需要重新编排
        if (!isAnalysis(orchestration)) {
            JSONObject azResultJson = startAzkaban(azProjectName);
            azResultJson.put("orchestrationId", orchestrationId);
            return azResultJson;
        } else {
            //azkaban zip name
            String zipName = baseName + ".zip";
            //初始化临时编排目录
            String otp = initOrchestrationTempPath(orchestrationId);
            //本地物件列表
            ArrayList<String> localAlgorithms = new ArrayList<>(),
                    //job 列表
                    jobsPath = new ArrayList<>();
            //获取编排任务
            String algorithms = orchestration.getAlgorithms();
            //分析编排
            JSONArray algorithmArray = analysisOrchestrations(algorithms);
            algorithmArray.forEach(row -> {
                //编排任务
                JSONObject algorithmJson = JSON.parseObject(row.toString());
                //保存物件列表
                String hdfsAlgorithm = generatePath(algorithmJson.getString("analyticsId"));
                //获取算法params
                String params = algorithmJson.getString("params");
                //拉取物件
                String artifactLocalPath = pullArtifactsFromHdfs(hdfsAlgorithm, otp);
                localAlgorithms.add(artifactLocalPath);
                algorithmJson.put("artifactLocalPath", artifactLocalPath);
                //生成job
                //String jobName = algorithmJson.getString("jobName").equals("") ? azLastJobName : algorithmJson.getString("jobName");
                String jobPath = constructJob(algorithmJson, otp);
                jobsPath.add(jobPath);
            });
            localAlgorithms.addAll(jobsPath);
            //生成zip
            String zipPath = packageZip(localAlgorithms, otp, zipName);
            //启动Azkaban任务
            JSONObject azResultJson = startAzkaban(zipPath, azProjectName, orchestration.getDescription());
            azResultJson.put("orchestrationId", orchestrationId);
            //清除临时目录
            cleanTemp(otp);
            return azResultJson;
        }

    }

    /**
     * 编排是否在执行
     *
     * @param orchestration 编排
     * @return boolean
     */
    public boolean isRunning(Orchestration orchestration) {
        Execution execution = executionRepository.getFirstByOrchestrationOrderByCreatedTimestampDesc(orchestration);
        if (execution != null) {
            String execid = execution.getAzExecutionId();
            String res = azkabanAdapter.executionInfo(execid);
            return "RUNNING".equals(JSON.parseObject(res).getString("status"));
        }
        return false;
    }

    /**
     * 是否需要编排
     *
     * @param orchestration 编排实体
     * @return boolean
     */
    public boolean isAnalysis(Orchestration orchestration) {
        Execution execution = executionRepository.getFirstByOrchestrationOrderByCreatedTimestampDesc(orchestration);
        if (orchestration.getUpdatedTimestamp() != null && execution != null) {
            long orchestrationTime = orchestration.getUpdatedTimestamp().getTime();
            long executionTime = execution
                    .getCreatedTimestamp()
                    .getTime();
            return orchestrationTime > executionTime;
        } else {
            return execution == null;
        }
    }

    /**
     * 分析编排
     *
     * @param algorithmJsonStr 待分析JSON
     * @return 编排任务
     */
    public JSONArray analysisOrchestrations(String algorithmJsonStr) {
        ArrayList<String> jobNames = new ArrayList<>();
        JSONArray resArrays = new JSONArray();
        String resStr = "{'analyticsId':'%s','jobName':'%s','param':'%s','type':'%s','language':'%s'}";
        JSONArray ajArrays = JSON.parseArray(algorithmJsonStr);
        ajArrays.forEach(row -> {
            JSONObject ajo = JSON.parseObject(row.toString());
            String analyticsId = ajo.getString("analyticsId");
            //生成算法参数
            String algorithmParam = algorithmParamUtil.convertSingleAlgorithmParam(ajo.getString("param"));
            //获取分析信息
            Analytics analytics = analyticsRepository.findOne(analyticsId);
            String type = analytics.getType();
            String language = analytics.getSupportedLanguage();
            int index = jobNames.lastIndexOf(analyticsId);
            String jobName;
            if (index > -1) {
                jobName = analyticsId + "_" + String.valueOf(index + 2) + ".job";
            } else {
                jobName = analyticsId + "_" + "1.job";
            }
            jobNames.add(analyticsId);
            resArrays.add(String.format(resStr,
                    analyticsId, jobName, algorithmParam, type, language));
        });
        return resArrays;
    }


    /**
     * 构造job
     *
     * @param algorithmJson 参数列表
     * @return job路径
     */
    public String constructJob(JSONObject algorithmJson, String orchestrationTempPath) {
        //获取spark master
        String sparkMaster = "yarn",
                sparkJar = "type=spark\r\nmaster=%s\r\nexecution-jar=%s\r\nclass=%s\r\nparams='%s'\r\n",
                sprakPy = "type=spark\r\nmaster=%\r\nsexecution-jar=%s\r\nparams=%s\r\nparams=%s\r\n",
                sparkPyCommand = "type=command\r\ncommand=spark-submit --master %s %s '%s'",
                sparkJarCommand = "type=command\r\ncommand=spark-submit --master %s --class %s %s '%s'",
                javaCommand = "",
                pythonCommand = "",
                shellCommand = "",
                filePath = algorithmJson.getString("artifactLocalPath"),
                fileName = FileUtils.getFileName(filePath, true),
                fileType = FileUtils.getExtensionName(fileName),
                jarClass = "", job = "",
                param = algorithmJson.getString("param"),
                language = algorithmJson.getString("language");
        if (fileType.equals("jar")) {
            //获取class
            jarClass = String.valueOf(JarFileUtil.getClassEntryMap(filePath).get("className"));
        }
        switch (algorithmJson.getString("type")) {
            case "spark":
                switch (language) {
                    case "java":
                    case "scala":
                        job = String.format(sparkJarCommand, sparkMaster, jarClass, fileName, param);
                        break;
                    case "python":
                        job = String.format(sparkPyCommand, sparkMaster, fileName, param);
                        break;
                    default:
                        break;
                }
                break;
            case "single":
                switch (language) {
                    case "java":
                        //todo
                        break;
                    case "python":
                        //todo
                        break;
                    case "shell":
                        //todo
                        break;
                    default:
                        break;
                }
            default:
                break;
        }
        //生成job文件
        return generateJob(job, orchestrationTempPath, algorithmJson.getString("jobName"));

    }

    /**
     * 生成HDFS地址
     *
     * @param analyticsId 算法ID
     * @return hdfs地址
     */
    public String generatePath(String analyticsId) {
        AnalyticsArtifacts artifacts = analyticsService.findExecutableArtifacts(analyticsId);
        return analyticsArtifacts_baseDir + "/" + analyticsId + "/" + artifacts.getFilename();
    }

    /**
     * 初始化 编排临时目录
     *
     * @param orchestrationID 编排ID
     * @return 临时目录
     */
    public String initOrchestrationTempPath(String orchestrationID) {
        //编排临时目录
        String orchestrationTempPath = tempPath + "/" + orchestrationID;
        File folder = new File(orchestrationTempPath);
        //如果目录不存在创建
        if (!folder.exists()) {
            folder.mkdirs();
        }
        return orchestrationTempPath;
    }

    /**
     * 拉取物件
     *
     * @param artifactPath          HDFS物件路径
     * @param orchestrationTempPath 临时目录
     * @return 本地物件路径
     */
    public String pullArtifactsFromHdfs(String artifactPath, String orchestrationTempPath) {
        String[] arrays = artifactPath.split("/");
        String fileName = arrays[arrays.length - 1];
        String savePath = orchestrationTempPath + "/" + fileName;
        HdfsUtil.downloadFile(fs_defaultFS, artifactPath, savePath);
        return savePath;
    }

    /**
     * 生成job
     *
     * @param params                job 参数
     * @param orchestrationTempPath 临时目录
     * @param jobName               job 名字
     * @return job路径
     */
    public String generateJob(String params, String orchestrationTempPath, String jobName) {
        String jobPath = orchestrationTempPath + "/" + jobName;
        AzkabanZipUtil.generateJob(params, new File(jobPath));
        return jobPath;
    }

    /**
     * 打包zip
     *
     * @param localArtifacts        需要打包的文件列表
     * @param orchestrationTempPath 临时目录
     * @param zipName               zip名字
     * @return zip目录
     */
    public String packageZip(ArrayList<String> localArtifacts, String orchestrationTempPath, String zipName) {
        String zipPath = orchestrationTempPath + "/" + zipName;
        AzkabanZipUtil.generateZip(localArtifacts, zipPath);
        return zipPath;
    }

    /**
     * 清空临时目录
     *
     * @param orchestrationTempPath 临时目录
     */
    public void cleanTemp(String orchestrationTempPath) {
        System.out.println(orchestrationTempPath);
        File dir = new File(orchestrationTempPath);
        AzkabanZipUtil.removeTemptDir(dir);
    }


    /**
     * 执行azkaban任务
     *
     * @param jobPath     文件获取路径
     * @param projectName project名称
     * @param description 描述信息
     */
    public JSONObject startAzkaban(String jobPath, String projectName, String description) {
        azkabanAdapter.createProject(projectName, description);
        azkabanAdapter.uploadZip(jobPath, projectName);
        String flows = azkabanAdapter.fetchProjectFlows(projectName);
        String flowName = JSON.parseObject(flows)
                .getJSONArray("flows")
                .getJSONObject(0)
                .getString("flowId");
        String execid = azkabanAdapter.startFlow(projectName, flowName);
        return JSON.parseObject(azkabanAdapter.executionInfo(execid));
    }

    /**
     * 执行azkaban任务
     *
     * @param projectName project名称
     * @return json
     */
    public JSONObject startAzkaban(String projectName) {
        String flows = azkabanAdapter.fetchProjectFlows(projectName);
        String flowName = JSON.parseObject(flows)
                .getJSONArray("flows")
                .getJSONObject(0)
                .getString("flowId");
        String execid = azkabanAdapter.startFlow(projectName, flowName);
        return JSON.parseObject(azkabanAdapter.executionInfo(execid));
    }
}
```