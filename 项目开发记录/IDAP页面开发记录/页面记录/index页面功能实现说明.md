# index页面功能实现说明

## 一、页面描述
> 这个页面有两个表格，分别展示manager列表，主机列表。
### manager列表里的功能有：
1. 展示manger信息包括：manager ip、agent数量、manger状态等
2. 部署日志详情
3. 查看当前集群主机列表

### 所有主机列表的功能有：
1. 展示主机信息包括：主机地址、所属manager、主机状态等
2. 主机部署日志
3. 重新部署 
4. 查看主机配置


## 二、功能实现记录
### 1. 展示manager、主机列表信息
> 这里主要用到的是datatables插件来渲染表格

#### a 定制后台数据

```
{
"aaData": [
            {
            "status": "0",
            "exist_db_port": "",
            "count": 2,
            "exist_db_user": "",
            "os_version": "7",
            "db_type": "1",
            "host_name_pre": "idap",
            "mysql_slave": "10.110.18.59",
            "domain_name": "idap.com",
            "nginx": "10.110.18.80",
            "create_mysql_pwd": "123456a?",
            "server_ip": "10.110.18.59",
            "db_source": "1",
            "id": 1,
            "operation_id": "75a3e53a-8963-11e7-8b1c-000c29fc8a00",
            "exist_db_pwd": "",
            "jdk_version": "8",
            "vm_info_platform": "vsphere",
            "os_type": "CentOS",
            "exist_db_host": "",
            "mysql_master": "10.110.18.58"
            }
          ],
"iTotalRecords": 1,
"iTotalDisplayRecords": 1
```
注意：后台数据格式一定要是这样，而且主要数据对象的key必须是aaData

#### b.表格HTML代码

```
        <table id="hostsList" class="table table-bordered table-hover table-striped">
            <thead>
            <tr>
                <th width="5%" style="text-align: center;">编号</th>
                <th width="20%" style="text-align: center;">主机地址</th>
                <th width="20%" style="text-align: center;">所属IDAP Manager</th>
                <th width="15%" style="text-align: center;">主机状态</th>
                <th width="15%" style="text-align: center;">日志</th>
                <th width="25%" style="text-align: center;">操作</th>
            </tr>
            </thead>
        </table>
```
我们只需要写出表头以及给这个table一个id即可
#### c. JS初始化表格

```
    //初始化manger列表
    var ManagerTable;
    function initManagerTable() {
        ManagerTable =$("#managerList").dtable({
            //显示“正在加载”的图标
            "processing": true,
            "serverSide": false,//开启服务器服务，开启之后将不能进前端分页
            "paging": true,//是否分页
            "iDisplayLength": 5, //显示五行数据
            "bInfo":true,//是否显示底部信息，默认开启
            "ordering": false,
            "pagingType": "simple_numbers",//翻页栏样式
            "ajax": "getManagerList",

            "columns": [
                {
                    "data": "null"
                },
                {
                    "data": "server_ip"
                },
                {
                    "data": "count"
                },
                {
                    "data": "status"
                }
            ],
            "columnDefs": [
                {
                    "targets": 0,
                    "data": "id",
                    "render": function (data, type, row, meta) {
                        return meta.row + meta.settings._iDisplayStart + 1;
                    }
                },
                {
                    "targets": 3,
                    "data": "status",
                    "render": function (data, type, full) {
                        if (data !== "" || data !== null) {
                            if (data === "0") {
                                data = "部署中";
                            }
                            if (data === "1") {
                                data = "部署完成";
                            }
                            if (data === "2") {
                                data = "部署失败";
                            }
                            if (data === "3") {
                                data = "已接入";
                            }
                        }
                        return data;
                    }
                },
                {
                    "targets": 4,
                    "data": "status",
                    "render": function (data, type, full) {
                        var logOptions = '<div><span class="options" onclick="managerLog(' + "'" + full.id + "'" + ')" href="#">详情</span></div>';
                        return logOptions
                    }
                },
                {
                    "targets": 5,
                    "data": "status",
                    "render": function (data, type, full) {
                        var optionHtml = "";
                        var optionList='<span class="options" onclick="managerList(' + "'" + full.id + "'" + "," +
                            "'" + full.server_ip + "'" + "," + "'" + full.vm_info_platform + "'" + "," + "'" + full.os_type + "'" + "," + "'" + full.os_version + "'"  + ')" href="#">主机列表</span>';
                        var optionsRestart = '<span class="options" onclick="managerOption(' + "'" + full.id + "'"  + ')" href="#">' + '重新部署' + '</span>';
                        if(data === "2"){
                            var nbsp = "    ";
                            optionHtml = optionsRestart + nbsp + optionList
                        }else {
                            optionHtml = optionList
                        }
                        return optionHtml
                    }
                }
            ]
        });
        return ManagerTable;
    }
```
注意，这里面用到了几个技巧：
1. 表格自动编号，根据数据，自动给每一行加一个编号：

实现代码：

```
                {
                    "targets": 0,
                    "data": "id",
                    "render": function (data, type, row, meta) {
                        return meta.row + meta.settings._iDisplayStart + 1;
                    }
                }
```
2. 表格里按钮功能的操作：
加一个点击事件，然后把相应的参数传到点击方法里。如 onclick="managerList(' + "'" + full.id + "'" + "," +"'" + full.server_ip + "'" + "," + "'" +full.vm_info_platform + "'" + "," + "'" + full.os_type + "'" + "," + "'" + full.os_version + "'"  + ')"
这里面full是所有aaData对象里的值。

### 2. 查看部署日志


```
    function managerLog(manager_id){
        var task;
        $.get("/m_status/", {
            "manager_id": manager_id
        }, function (m_status) {
            if (m_status.m_status === "0") {
                tmp = 0;
                task = setInterval(function () {
                    $.get("/read/", {
                        "manager_id": manager_id,
                    }, function (read_data) {
                        $(".ManagerDeploy_log").val(read_data.read_d);
                        $(".ManagerDeploy_log").scrollTop($(".ManagerDeploy_log")[0].scrollHeight);
                    });
                }, 2000);
            } else {
                $.get("read", {
                    "manager_id": manager_id
                }, function (read_data) {
                    $(".ManagerDeploy_log").val(read_data.read_d);
                });
            }
        });
        $.dialog({
            type: 'iframe',
            title: '部署日志',
            width: '580',
            height: '320',
            okValue: '确定',
            content: '<textarea class="ManagerDeploy_log"></textarea>',
            onshow: function () {
                $(".ManagerDeploy_log").css({
                    "width": "580px",
                    "height": "290px",
                    "border": "1px solid #ddd",
                    "background": "#ddd",
                    "margin-bottom": "10px"
                });
                $(".deploy_title").css({
                    "font-family": "Microsoft YaHei",
                    "font-size": "20px",
                    "margin-bottom": "8px"
                })
            },
            onclose: function () {
                clearInterval(task);
            },
            ok: function () {
                clearInterval(task);
            }
        });
    }
```
### 3. 查看配置
查看配置这个地方没有从后台获取数据，而是拿到的表格渲染的数据。首先在script标签里写一个html模板如下：

```
<script type="text/html" id="showConfig">
    <div class="container">
        <div class="">
            <table class="table table-hover table-striped">
                <tbody>
                <tr>
                    <td width="50%">主机名称：</td>
                    <td>[vm_host_name]</td>
                </tr>
                <!-- <tr>
                    <td width="50%">root密码：</td>
                    <td>[]</td>
                </tr>-->
                <tr>
                    <td width="50%">数据中心：</td>
                    <td>[vm_host_datacenter]</td>
                </tr>
                <tr>
                    <td width="50%">集群：</td>
                    <td>[vm_host_cluster]</td>
                </tr>
                <tr>
                    <td width="50%">虚拟机位置：</td>
                    <td>[vm_host_host]</td>
                </tr>
                <tr>
                    <td width="50%">CPU：</td>
                    <td>[vm_host_cpu]核</td>
                </tr>
                <tr>
                    <td width="50%">内存：</td>
                    <td>[vm_host_memory]MB</td>
                </tr>
                <tr>
                    <td width="50%">储存器名称：</td>
                    <td>[vm_host_disk]</td>
                </tr>
                <tr>
                    <td width="50%">网络标签：</td>
                    <td>[vm_host_network]</td>
                </tr>
                <tr>
                    <td width="50%">IPv4：</td>
                    <td>[vm_host_ip]</td>
                </tr>
                <tr>
                    <td width="50%">网关：</td>
                    <td>[vm_host_gateway]</td>
                </tr>
                <tr>
                    <td width="50%">子网掩码：</td>
                    <td>[vm_host_netmask]</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</script>
```
script标签里的html在页面显示的时候是不会主动渲染的，我们可以通过js获取页面内容，然后手动渲染到dom里，代码中[]里的内容是我们js渲染时重新赋的值。具体操作日下：


```
    function viewConfig(vm_host_name, vm_host_network, vm_host_status, vm_host_gateway, vm_host_datacenter,
                        vm_host_host, vm_host_disk, vm_host_cpu, vm_info_host, vm_host_memory, idap_manager_id,
                        vm_host_data_disk, vm_info_passwd, vm_info_user, vm_host_ip, vm_host_netmask, vm_host_cluster,
                        operation_id, vm_info_platform, id) {
        //从id为showConfig的标签里读取html内容
        var html = document.getElementById("showConfig").innerHTML;
        var reg = new RegExp("\\[([^\\[\\]]*?)\\]", 'igm'); //i g m是指分别用于指定区分大小写的匹配、全局匹配和多行匹配。
        //重新渲染数据
        var source = html.replace(reg, function (node, key) {
            return {
                'vm_host_name': vm_host_name,
                'vm_host_datacenter': vm_host_datacenter,
                'vm_host_cluster': vm_host_cluster,
                'vm_host_host': vm_host_host,
                'vm_host_cpu': vm_host_cpu,
                'vm_host_memory': vm_host_memory,
                'vm_host_disk': vm_host_disk,
                'vm_host_network': vm_host_network,
                'vm_host_ip': vm_host_ip,
                'vm_host_gateway': vm_host_gateway,
                'vm_host_netmask': vm_host_netmask
            }[key]
        });
        //dialog加载数据
        $.dialog({
            title: "配置信息",
            type: "confirm",
            content: source
        })
    }
```
### 特殊功能:实时监测部署状态，进行刷新
>需求：以主机列表为例，主机部署时有四个状态分别是：states=0表示主机部署中、states=1表示部署成功、states=2表示部署失败、states=3表示主机已接入。现在的需求是当主机完成部署时，后台数据库states的状态会从0变为1部署成功、或者变为2部署失败，我们要监测状态的改变去刷新页面数据。

>不完美解决方案：利用setTimeoUt来间隔的刷新数据

>思路：利用setTimeout来间隔刷新，为了避免不必要的刷新，也就是说，只有当状态改变的时候进行刷新。我们先发送ajax请求，然后遍历所有主机状态，并且计算出状态为0的主机个数。然后设置时间间隔5s后再次发送ajax请求，同样去判断主机状态，记录状态为0的主机个数，当这次状态为0 的主机个数与上一次状态为0的主机个数不一样的时候，说明其中有一个主机状态发生了改变，这时候我们就要执行一次刷新（注意：这里的刷新不是刷新页面，而是重新渲染表格，这也是不完美的地方之一，虽然这样比刷新整个页面要好，但是仍然会影响用户体验，理想的解决方法是：只刷新改变的那一行数据，目前没有实现）

实现代码如下：


```
    //manager、主机状态状态改变时刷新
    var tmpManagerTotal=0;
    var tmpHostsTotal = 0;
    function adjRefresh() {
        var managerTotal = 0;
        var hostsTotal=0;
        $.ajax({
            type:'GET',
            url:"getManagerList",
            success:function (data) {
                var aa = JSON.parse(data);
                var states = "";
                //for循环得到部署中的状态个数
                for(var ii in aa.aaData){
                    我= aa.aaData[ii].status;
                    if(states==="0"){
                        managerTotal=managerTotal+1;
                    }
                }
                if(managerTotal !==tmpManagerTotal){
                    tmpManagerTotal=managerTotal;
                    ManagerTable.destroy();
                    initManagerTable();
                }
            }
        });
        $.ajax({
            type:'GET',
            url:"getVMInfo",
            success:function (data) {
                var aa = JSON.parse(data);
                var hostsStates = "";
                //for循环得到部署中的状态个数
                for(var ii in aa.aaData){
                    hostsStates= aa.aaData[ii].vm_host_status;
                    if(hostsStates==="0"){
                        hostsTotal=hostsTotal+1;
                    }
                }
                if(hostsTotal !==tmpHostsTotal){
                    tmpHostsTotal=hostsTotal;
                    hostsTable.destroy();
                    initHostsTable();
                }
            }
        });
        setTimeout(function() {
            adjRefresh();
        },10000)
    }
```


