## Amabri2.6多语言处理

## 1.ambari-web 

在ambari-web/app下新建目录locales，然后在locales目录下创建zh、en目录，分别存放中文、英文语言js文件。

en下的message.js为英文语言，跟app目录下的message.js相同

zh下的使我们要汉化的语言。翻译相对应的字段即可。



### 1.1状态修改 

![](https://shirukai.gitee.io/images/1510818136223clipboard.png)

#### 修改modes/host_component.js 243行 

```
    getTextStatus: function (value) {
        switch (value) {
            case this.installing:
                //return 'Installing...';
                return Em.I18n.t('services.textStatus.installing');
            case this.install_failed:
                //return 'Install Failed';
                return Em.I18n.t('services.textStatus.installFailed');
            case this.stopped:
                //return 'Stopped';
                return Em.I18n.t('services.textStatus.stopped');
            case this.started:
                //return 'Started';
                return Em.I18n.t('services.textStatus.started');
            case this.starting:
                //return 'Starting...';
                return Em.I18n.t('services.textStatus.starting');
            case this.stopping:
                //return 'Stopping...';
                return Em.I18n.t('services.textStatus.stopping');
            case this.unknown:
                //return 'Heartbeat Lost';
                return Em.I18n.t('services.textStatus.upgradeFailed');
            case this.upgrade_failed:
                //return 'Upgrade Failed';
                return Em.I18n.t('services.textStatus.upgradeFailed');
            case this.disabled:
                //return 'Disabled';
                return Em.I18n.t('services.textStatus.disabled');
            case this.init:
                //return 'Install Pending...';
                return Em.I18n.t('services.textStatus.installPending');
        }
        //return 'Unknown';
        return Em.I18n.t('services.textStatus.unknown');
    },
```

#### zh/message.js下添加

```
    'services.textStatus.installing': '安装中...',
    'services.textStatus.installFailed': '安装失败',
    'services.textStatus.stopped': '已停止',
    'services.textStatus.started': '已启动',
    'services.textStatus.starting': '启动中...',
    'services.textStatus.stopping': '停止中...',
    'services.textStatus.heartbeatLost': '心跳丢失',
    'services.textStatus.upgradeFailed': '升级失败',
    'services.textStatus.disabled': '已禁用',
    'services.textStatus.installPending': '安装等待...',
    'services.textStatus.unknown': '未知',
```

#### 在en/message.js中添加

```
'services.textStatus.installing': 'Installing...',
'services.textStatus.installFailed': 'Install Failed',
'services.textStatus.stopped': 'Stopped',
'services.textStatus.started': 'Started',
'services.textStatus.starting': 'Starting...',
'services.textStatus.stopping': 'Stopping...',
'services.textStatus.heartbeatLost': 'Heartbeat Lost',
'services.textStatus.upgradeFailed': 'Upgrade Failed',
'services.textStatus.disabled': 'Disabled',
'services.textStatus.installPending': 'Install Pending...',
'services.textStatus.unknown': 'Unknown',
```

### 1.2登录错误信息汉化

![](https://shirukai.gitee.io/images/201711171545_179.png)

#### 修改app/controllers/login_controller.js下文件

![](https://shirukai.gitee.io/images/201711171634_7.png)

#### 修改en/messages.js

```
/*登录错误信息*/
'login.error.unable':'Unable to sign in. Invalid username/password combination.',
```

#### 修改zh/messages.js

```
/*登录错误信息*/
'login.error.unable':'无法登录，无效的用户名/密码组合。',
```



### 1.3下载所有客户端配置 

![](https://shirukai.gitee.io/images/201711171548_943.png)

#### 在en/messages.js添加

```
/*下载所有客户端配置*/
'services.service.downloadAllClientConfigs': 'Download All Client Configs',
```

#### 在zh/messages.js添加

```
/*下载所有客户端配置*/
'services.service.downloadAllClientConfigs': '下载所有客户端配置',
```

### 1.4警告状态 

![](https://shirukai.gitee.io/images/201711201027_967.png)

#### 修改文件

ambari-web\app\views\main\alerts\alert_definition\alert_definition_summary.js



ambari-web\app\models\alerts\alert_definition.js 258行

大约55行位置

```
/*多语言处理*/
_stateSummary.count = Em.I18n.t('zh_count.'+count);
```

![](https://shirukai.gitee.io/images/201711201029_756.png)

#### 修改en/messages.js 

```
/*count*/
'zh_count.OK':'OK',
'zh_count.WARN':'WARN',
'zh_count.CRIT':'CRIT',
'zh_count.UNKWN':'UNKWN',
'zh_count.NONE':'NONE',
```

#### 修改zh/messages.js 

```
/*count*/
'zh_count.OK':'正常',
'zh_count.WARN':'警告',
'zh_count.CRIT':'严重',
'zh_count.UNKWN':'未知',
'zh_count.NONE':'无',
```

### 1.5 导航警告

![](https://shirukai.gitee.io/images/201711201034_970.png)

#### 修改文件

ambari-web\app\templates\application.hbs

大约在51和55行

![](https://shirukai.gitee.io/images/201711201036_646.png)

#### 修改en/messages.js 

```
'alerts':'alerts',
```

#### 修改en/messages.js 

```
'alerts':'个警告',
```

### 1.6警告状态下拉 

![](https://shirukai.gitee.io/images/201711201038_252.png)

#### 修改文件 

ambari-web\app\views\main\alert_definitions_view.js

大约185行

```
  stateFilterView: filters.createSelectView({
    column: 2,
    fieldType: 'filter-input-width',
    content: [
      {
        value: '',
        label: Em.I18n.t('common.all')
      },
      {
        value: 'OK',
        label: Em.I18n.t('zh_alert_state.OK')
      },
      {
        value: 'WARNING',
        label: Em.I18n.t('zh_alert_state.WARNING')
      },
      {
        value: 'CRITICAL',
        label:Em.I18n.t('zh_alert_state.CRITICAL')
      },
      {
        value: 'UNKNOWN',
        label: Em.I18n.t('zh_alert_state.UNKNOWN')
      },
      {
        value: 'PENDING',
        label: Em.I18n.t('zh_alert_state.NONE')
      }
    ],
```

#### 修改en/messages.js 

```
    /*zh_alert_state*/
    'zh_alert_state.OK':'OK',
    'zh_alert_state.WARNING':'WARNING',
    'zh_alert_state.CRITICAL':'CRITICAL',
    'zh_alert_state.UNKNOWN':'UNKNOWN',
    'zh_alert_state.NONE':'NONE',
```

#### 修改zh/messages.js 

```
    /*zh_alert_state*/
    'zh_alert_state.OK':'正常',
    'zh_alert_state.WARNING':'警告',
    'zh_alert_state.CRITICAL':'严重',
    'zh_alert_state.UNKNOWN':'未知',
    'zh_alert_state.NONE':'无',
```

### 1.7主机警告下拉

![](https://shirukai.gitee.io/images/201711201059_566.png)

#### 修改文件

W:\ambari-web\app\views\main\host\host_alerts_view.js

大约145行

```
  stateFilterView: filters.createSelectView({
    column: 4,
    fieldType: 'filter-input-width',
    content: [
      {
        value: '',
        label: Em.I18n.t('common.all')
      },
        {
            value: 'OK',
            label: Em.I18n.t('zh_alert_state.OK')
        },
        {
            value: 'WARNING',
            label: Em.I18n.t('zh_alert_state.WARNING')
        },
        {
            value: 'CRITICAL',
            label:Em.I18n.t('zh_alert_state.CRITICAL')
        },
        {
            value: 'UNKNOWN',
            label: Em.I18n.t('zh_alert_state.UNKNOWN')
        }
```

### 1.8主机警告状态

![](https://shirukai.gitee.io/images/201711201151_883.png)



#### 修改文件 

ambari-web\app\models\alerts\alert_instance.js大约165行



```
    shortState: {
        'CRITICAL': Em.I18n.t('zh_count.CRIT'),
        'WARNING':  Em.I18n.t('zh_count.WARN'),
        'OK': Em.I18n.t('zh_count.OK'),
        'UNKNOWN':  Em.I18n.t('zh_count.UNKWN'),
        'PENDING':  Em.I18n.t('zh_count.NONE')
    }
```

### 1.9恢复主机 

![](https://shirukai.gitee.io/images/201711201153_417.png)

#### en/messages.js 

```
/*recoverHost*/
'hosts.host.details.recoverHost': 'Recover Host',
```

#### zh/messages.js 

```
/*recoverHost*/
'hosts.host.details.recoverHost': '恢复主机',
```

### 1.10 警告配置信息 

![](https://shirukai.gitee.io/images/201711201459_895.png)

#### 修改文件 

ambari-web\app\models\alerts\alert_config.js 大约 在531、549、568行，添加内容如下：

##### OK

![](https://shirukai.gitee.io/images/201711201504_672.png)

##### WARNING 

![](https://shirukai.gitee.io/images/201711201504_75.png)

##### CRITICAL 

![](https://shirukai.gitee.io/images/201711201505_172.png)

#### 然后修改文件 

ambari-web\app\templates\main\alerts\configs\alert_config_threshold.hbs 大约在20行，将原来的badge换成state

![](https://shirukai.gitee.io/images/201711201506_307.png)



#### 1.11警告配置下拉 

![](https://shirukai.gitee.io/images/201711201517_789.png)

#### 修改文件 

ambari-web\app\views\main\alerts\definition_details_view.js  177行

```
    content: [
      {
        value: '',
        label: Em.I18n.t('common.all')
      },
        {
            value: 'OK',
            label: Em.I18n.t('zh_alert_state.OK')
        },
        {
            value: 'WARNING',
            label: Em.I18n.t('zh_alert_state.WARNING')
        },
        {
            value: 'CRITICAL',
            label:Em.I18n.t('zh_alert_state.CRITICAL')
        },
        {
            value: 'UNKNOWN',
            label: Em.I18n.t('zh_alert_state.UNKNOWN')
        },
        {
            value: 'PENDING',
            label: Em.I18n.t('zh_alert_state.NONE')
        }
    ],
```



#### 服务警告

V:\apache-ambari-2.6.0-src\ambari-web\app\templates\main\service\info\summary.hbs

V:\apache-ambari-2.6.0-src\ambari-web\app\templates\main\service\info\summary\master_components.hbs

![](https://shirukai.gitee.io/images/201711271957_207.png)

#### 进度条隐藏加速 

X:\apache-ambari-2.5.1-src\ambari-web\app\templates\main.hbs

注释25-28行

![](https://shirukai.gitee.io/images/201712041429_305.png)

clusterDataLoadedPercent

X:\apache-ambari-2.5.1-src\ambari-web\app\controllers\global\cluster_controller.js

修改方法

![](https://shirukai.gitee.io/images/201712041431_233.png)



```
      if (item === 'stackComponents') {
          this.set('isLoaded', false);
          //this.set('clusterDataLoadedPercent', 'width:50%');
      } else {
          this.set('isLoaded', true);
          //this.set('clusterDataLoadedPercent', 'width:100%');
      }
```

### 后台运行弹窗 乱码 

![img](https://shirukai.gitee.io/images/201712110853_135.png)

后台运行弹窗乱码的原因是在修改多集群的时候，将存入数据库的值进行了url编码encodeUrl，所以会生成乱码，我们需要在取出数据库值的时候，将其解码。

#### 编码的地方 

X:\apache-ambari-2.5.1-src\ambari-web\app\controllers\main\host\details.js

```
sendComponentCommand: function (component, context, state) {
    var data = {
        hostName: this.get('content.hostName'),
        context: encodeURI(context),
        component: component,
        HostRoles: {
            state: state
        }
    };
    if (Array.isArray(component)) {
        data.query = "HostRoles/component_name.in(" + component.mapProperty('componentName').join(',') + ")";
    } else {
        data.componentName = component.get('componentName');
        data.serviceName = component.get('service.serviceName');
    }
    App.ajax.send({
        name: (Array.isArray(component)) ? 'common.host.host_components.update' : 'common.host.host_component.update',
        sender: this,
        data: data,
        success: 'sendComponentCommandSuccessCallback',
        error: 'ajaxErrorCallback',
        showLoadingPopup: true
    });
},
```

#### 解码的地方：

X:\apache-ambari-2.5.1-src\ambari-web\app\controllers\global\background_operations_controller.js

```
parseRequestContext: function (requestContext) {
  var parsedRequestContext;
  var service;
  var contextCommand;
  if (requestContext) {
    if (requestContext.indexOf(App.BackgroundOperationsController.CommandContexts.PREFIX) !== -1) {
      var contextSplits = requestContext.split('.');
      contextCommand = contextSplits[1];
      service = contextSplits[2];
      switch(contextCommand){
      case "STOP":
      case "START":
        if (service === 'ALL_SERVICES') {
          parsedRequestContext = Em.I18n.t("requestInfo." + contextCommand.toLowerCase()).format(Em.I18n.t('common.allServices'));
        } else {
          parsedRequestContext = Em.I18n.t("requestInfo." + contextCommand.toLowerCase()).format(App.format.role(service, true));
        }
        break;
      case "ROLLING-RESTART":
        parsedRequestContext = Em.I18n.t("rollingrestart.rest.context").format(App.format.role(service, true), contextSplits[3], contextSplits[4]);
        break;
      }
    } else {
      parsedRequestContext = decodeURI(requestContext);
    }
  } else {
    parsedRequestContext = Em.I18n.t('requestInfo.unspecified');
  }
  return {
    requestContext: parsedRequestContext,
    dependentService: service,
    contextCommand: contextCommand
  }
},
```



### 加载安装集群的位置 

X:\apache-ambari-2.5.1-src\ambari-web\app\router.js

```
/**
 * Is true, if cluster.provisioning_state is equal to 'INSTALLED'
 * @type {Boolean}
 */
clusterInstallCompleted: false,
```

### 效果 

![](https://shirukai.gitee.io/images/201711171644_221.png)

### 添加组件  

![](https://shirukai.gitee.io/images/201711280857_132.png)





参考：https://issues.apache.org/jira/secure/attachment/12846157/AMBARI-19376-web.patch

## 2. ambari-admin 

替换/opt/apache-ambari-2.6.0-src/ambari-admin/src/main/resources/ui/admin-web/app/scripts目录下的

i18n.config.js文件即可

### 2.1汉化角色部分

![](https://shirukai.gitee.io/images/201711191709_882.png)

#### 2.1.1修改ClustersManageAccessCtrl.js 

在apache-ambari-2.6.0-src\ambari-admin\src\main\resources\ui\admin-web\app\scripts\controllers\clusters\ClustersManageAccessCtrl.js文件大约40行位置新增如下代码

```
for (var key in orderedRoles) {
	var data = $scope.permissions[orderedRoles[key]];
	data.PermissionInfo.permission_label = $t('zh_orderedRoles.'+orderedRoles[key]);
	data.PermissionInfo.permission_name = $t('zh_orderedRoles.'+orderedRoles[key]);
	pms.push(data);
}
```

![](https://shirukai.gitee.io/images/201711191712_215.png)

#### 2.1.2修改i18n.config.js文件

##### 英文部分

```
'zh_orderedRoles': {
    'CLUSTER.ADMINISTRATOR': 'CLUSTER ADMINISTRATOR',
    'CLUSTER.OPERATOR': 'CLUSTER OPERATOR',
    'SERVICE.ADMINISTRATOR': 'SERVICE.ADMINISTRATOR',
    'SERVICE.OPERATOR': 'SERVICE OPERATOR',
    'CLUSTER.USER': 'CLUSTER USER',
    'AMBARI.ADMINISTRATOR': 'AMBARI ADMINISTRATOR '
},
```

##### 汉语部分

```
'zh_orderedRoles': {
    'CLUSTER.ADMINISTRATOR': '集群管理员',
    'CLUSTER.OPERATOR': '集群操作者',
    'SERVICE.ADMINISTRATOR': '服务管理员',
    'SERVICE.OPERATOR': '服务操作者',
    'CLUSTER.USER': '集群用户',
    'AMBARI.ADMINISTRATOR': 'Ambari管理员'
```

### 2.2汉化角色弹框 

![](https://shirukai.gitee.io/images/201711191716_636.png)

#### 2.2.1修改RoleDetailsModal.js文件 

修改apache-ambari-2.6.0-src\ambari-admin\src\main\resources\ui\admin-web\app\scripts\services\RoleDetailsModal.js文件

首先引入多语言处理，添加下图红框里的代码

![](https://shirukai.gitee.io/images/201711191720_687.png)

然后对两处数据进行重新渲染

第一处是authHash，第二处是roles。大约在76行左右添加如下代码：

```
/*authHash数据重新渲染*/
var zh_authHash = $scope.authHash;
//var aa=[];
angular.forEach(zh_authHash, function (value,key) {
    angular.forEach(value,function (value,key) {
        if(key !== "order"){
            //aa.push('\''+key+'\''+':'+'\''+value.name+'\'')
            value.name = $t('zh_authHash.'+key)
        }
    })
});
$scope.authHash = zh_authHash;

/*roles数据重新渲染*/
var zh_roles = $scope.roles;
angular.forEach(zh_roles, function (value, key) {
    value.permission_label= $t('zh_orderedRoles.' + value.permission_name);
});
$scope.roles = zh_roles;
```

如下图所示:

![](https://shirukai.gitee.io/images/201711191724_489.png)

#### 修改i18n.config.js文件 

##### 英语部分

```
'zh_authHash': {
    'AMBARI.ADD_DELETE_CLUSTERS': 'Create new clusters',
    'AMBARI.ASSIGN_ROLES': 'Assign roles',
    'AMBARI.EDIT_STACK_REPOS': 'Edit stack repository URLs',
    'AMBARI.MANAGE_GROUPS': 'Manage groups',
    'AMBARI.MANAGE_SETTINGS': 'Manage administrative settings',
    'AMBARI.MANAGE_STACK_VERSIONS': 'Manage stack versions',
    'AMBARI.MANAGE_USERS': 'Manage users',
    'AMBARI.MANAGE_VIEWS': 'Manage Ambari Views',
    'AMBARI.RENAME_CLUSTER': 'Rename clusters',
    'AMBARI.RUN_CUSTOM_COMMAND': 'Perform custom administrative actions',
    'CLUSTER.MANAGE_ALERTS': 'Manage cluster-level alerts',
    'CLUSTER.MANAGE_ALERT_NOTIFICATIONS': 'Manage alert notifications configuration',
    'CLUSTER.MANAGE_AUTO_START': 'Manage service auto-start configuration',
    'CLUSTER.MANAGE_CONFIG_GROUPS': 'Manage cluster config groups',
    'CLUSTER.MANAGE_CREDENTIALS': 'Manage external credentials',
    'CLUSTER.MANAGE_USER_PERSISTED_DATA': 'Manage cluster-level user persisted data',
    'CLUSTER.MODIFY_CONFIGS': 'Modify cluster configurations',
    'CLUSTER.RUN_CUSTOM_COMMAND': 'Perform custom cluster-level actions',
    'CLUSTER.TOGGLE_ALERTS': 'Enable/disable cluster-level alerts',
    'CLUSTER.TOGGLE_KERBEROS': 'Enable/disable Kerberos',
    'CLUSTER.UPGRADE_DOWNGRADE_STACK': 'Upgrade/downgrade stack',
    'CLUSTER.VIEW_ALERTS': 'View cluster-level alerts',
    'CLUSTER.VIEW_CONFIGS': 'View configuration',
    'CLUSTER.VIEW_METRICS': 'View metrics',
    'CLUSTER.VIEW_STACK_DETAILS': 'View stack version details',
    'CLUSTER.VIEW_STATUS_INFO': 'View status information',
    'HOST.ADD_DELETE_COMPONENTS': 'Install components',
    'HOST.ADD_DELETE_HOSTS': 'Add/Delete hosts',
    'HOST.TOGGLE_MAINTENANCE': 'Turn on/off maintenance mode',
    'HOST.VIEW_CONFIGS': 'View configuration',
    'HOST.VIEW_METRICS': 'View metrics',
    'HOST.VIEW_STATUS_INFO': 'View status information',
    'SERVICE.ADD_DELETE_SERVICES': 'Add/delete services',
    'SERVICE.COMPARE_CONFIGS': 'Compare configurations',
    'SERVICE.DECOMMISSION_RECOMMISSION': 'Decommission/recommission',
    'SERVICE.ENABLE_HA': 'Enable HA',
    'SERVICE.MANAGE_ALERTS': 'Manage service-level alerts',
    'SERVICE.MANAGE_AUTO_START': 'Manage service auto-start',
    'SERVICE.MANAGE_CONFIG_GROUPS': 'Manage configuration groups',
    'SERVICE.MODIFY_CONFIGS': 'Modify configurations',
    'SERVICE.MOVE': 'Move to another host',
    'SERVICE.RUN_CUSTOM_COMMAND': 'Perform service-specific tasks',
    'SERVICE.RUN_SERVICE_CHECK': 'Run service checks',
    'SERVICE.SET_SERVICE_USERS_GROUPS': 'Set service users and groups',
    'SERVICE.START_STOP': 'Start/Stop/Restart Service',
    'SERVICE.TOGGLE_ALERTS': 'Enable/disable service-level alerts',
    'SERVICE.TOGGLE_MAINTENANCE': 'Turn on/off maintenance mode',
    'SERVICE.VIEW_ALERTS': 'View service-level alerts',
    'SERVICE.VIEW_CONFIGS': 'View configurations',
    'SERVICE.VIEW_METRICS': 'View metrics',
    'SERVICE.VIEW_OPERATIONAL_LOGS': 'View service operational logs',
    'SERVICE.VIEW_STATUS_INFO': 'View status information'
},
```

##### 汉语部分

```
'zh_authHash': {
    'AMBARI.ADD_DELETE_CLUSTERS': '创建新集群',
    'AMBARI.ASSIGN_ROLES': '分配角色',
    'AMBARI.EDIT_STACK_REPOS': '编辑软件栈存储库的URL',
    'AMBARI.MANAGE_GROUPS': '管理组',
    'AMBARI.MANAGE_SETTINGS': '管理行政设置',
    'AMBARI.MANAGE_STACK_VERSIONS': '管理软件栈版本',
    'AMBARI.MANAGE_USERS': '用户管理',
    'AMBARI.MANAGE_VIEWS': '管理 Ambari 视图',
    'AMBARI.RENAME_CLUSTER': '重命名集群',
    'AMBARI.RUN_CUSTOM_COMMAND': '执行自定义管理操作',
    'CLUSTER.MANAGE_ALERTS': '管理群集级别警报',
    'CLUSTER.MANAGE_ALERT_NOTIFICATIONS': '管理配置警报通知',
    'CLUSTER.MANAGE_AUTO_START': '管理服务自动启动配置',
    'CLUSTER.MANAGE_CONFIG_GROUPS': '管理群集配置组',
    'CLUSTER.MANAGE_CREDENTIALS': '管理外部凭证',
    'CLUSTER.MANAGE_USER_PERSISTED_DATA': '管理集群级用户持久数据',
    'CLUSTER.MODIFY_CONFIGS': '修改群集配置',
    'CLUSTER.RUN_CUSTOM_COMMAND': '执行自定义集群级操作',
    'CLUSTER.TOGGLE_ALERTS': '启用/禁用群集级警报',
    'CLUSTER.TOGGLE_KERBEROS': '启用/禁用 Kerberos',
    'CLUSTER.UPGRADE_DOWNGRADE_STACK': '升级/降级软件栈',
    'CLUSTER.VIEW_ALERTS': '查看群集级别警报',
    'CLUSTER.VIEW_CONFIGS': '查看配置',
    'CLUSTER.VIEW_METRICS': '查看指标',
    'CLUSTER.VIEW_STACK_DETAILS': '查看软件栈版本详细信息',
    'CLUSTER.VIEW_STATUS_INFO': '查看视图信息',
    'HOST.ADD_DELETE_COMPONENTS': '安装组件',
    'HOST.ADD_DELETE_HOSTS': '添加/删除主机',
    'HOST.TOGGLE_MAINTENANCE': '打开/关闭维修模式',
    'HOST.VIEW_CONFIGS': '查看配置',
    'HOST.VIEW_METRICS': '查看指标',
    'HOST.VIEW_STATUS_INFO': '查看状态信息',
    'SERVICE.ADD_DELETE_SERVICES': '添加/删除服务',
    'SERVICE.COMPARE_CONFIGS': '比较配置',
    'SERVICE.DECOMMISSION_RECOMMISSION': 'Decommission/recommission',
    'SERVICE.ENABLE_HA': '使用 HA',
    'SERVICE.MANAGE_ALERTS': '管理服务级别警报',
    'SERVICE.MANAGE_AUTO_START': '管理服务自动启动',
    'SERVICE.MANAGE_CONFIG_GROUPS': '管理配置组',
    'SERVICE.MODIFY_CONFIGS': '修改配置',
    'SERVICE.MOVE': '移到另一个主机',
    'SERVICE.RUN_CUSTOM_COMMAND': '执行 service-specific 任务',
    'SERVICE.RUN_SERVICE_CHECK': '运行服务检查',
    'SERVICE.SET_SERVICE_USERS_GROUPS': '设置服务用户和组',
    'SERVICE.START_STOP': '启动/停止/重新启动服务',
    'SERVICE.TOGGLE_ALERTS': '启用/禁用服务级别警报',
    'SERVICE.TOGGLE_MAINTENANCE': '打开/关闭维修模式',
    'SERVICE.VIEW_ALERTS': '查看服务级别警报',
    'SERVICE.VIEW_CONFIGS': '查看配置',
    'SERVICE.VIEW_METRICS': '查看指标',
    'SERVICE.VIEW_OPERATIONAL_LOGS': '查看服务操作日志',
    'SERVICE.VIEW_STATUS_INFO': '查看状态信息'
},
```

注意：angular的foreach循环，Function里面第一个参数是value,第二个参数为key

### 效果

![](https://shirukai.gitee.io/images/201711171642_955.png)



