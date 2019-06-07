# select_system选择虚拟化平台页面的实现

## 一、页面描述
> 这也页面主要是让用户去选择虚拟化平台如vsphere等，然后填入相应的平台地址用户名和密码就可以对接虚拟化平台了。

## 二、功能描述
>首先对表单进行校验，这里利用了validform插件对表单进行校验，然后是当用户选择了虚拟化平台环境之后，我们要判断当先用户下这个平台之前有没有填入数据库，请求数据，当请求判断后台已经存在相应记录时，直接获取后台数据，并将相应的平台地址用户名和密码填入到表单中，无需用户再次填写。而当用户是第一次进行操作时，就要手动的去填写相关信息，并且要进行连接测试，只有当测试成功后，我们才可以进行信息提交。

实现代码如下：

```
<!DOCTYPE html>
{% load staticfiles %}
<html lang="zh-CN" >
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>选择虚拟化平台</title>
    <link rel="stylesheet" href="{% static 'css/loushang/bootstrap.css' %}" type="text/css">
    <link rel="stylesheet" href="{% static 'css/loushang/ui.css' %}" type="text/css">
    <link rel="stylesheet" href="{% static 'css/login.css' %}" type="text/css">
	<link rel="stylesheet" href="{% static 'css/loushang/form.css' %}" type="text/css">
	<link rel="stylesheet" href="{% static 'css/loushang/font-awesome.css' %}" type="text/css">
    <style>
        body{
            background: #f0f2f6;
        }
    </style>
	<script src="{% static 'js/loushang/jquery.js' %}" type="text/javascript" charset="utf-8"></script>
	<script src="{% static 'js/loushang/bootstrap.js' %}" type="text/javascript" charset="utf-8"></script>
	<script src="{% static 'js/loushang/ui.js' %}" type="text/javascript" charset="utf-8"></script>
	<script src="{% static 'js/loushang/form.js' %}" type="text/javascript" charset="utf-8"></script>


</head>
<body>
<!--navbar部分-->
<div class="nav_self">
	<div class="container_self">
		<div class="logo"></div>
		<div class="index_user">admin
			<div class="exit">退出</div>
		</div>
	</div>
</div>
<!--内容-->
<div class="container" style="background: white;margin-top: 18px; padding-bottom: 40px">
	<div class="select_system">
		<h3>选择虚拟化平台</h3>

		<a onclick="window.location.href='choose_os.html'">
			<span class="" style=" float: right;position: relative;top: -32px; right: 56px">
				<i class="fa fa-undo"></i>返回
			</span>

		</a>
	</div>
	<div style="background-color:#ddd;height:1px;border:none;width: 96%;margin-bottom: 40px"></div>
	<br>
	<form class="form-horizontal" id="saveForm" name="saveForm" style="width: 100%" onsubmit="return false">
		<div class="form-group">
			<label class="col-xs-3  control-label">虚拟化平台：</label>
			<div class="col-sm-9">
				<select id="system" class="form-control ue-form Validform_input" name="system" datatype="s" nullmsg="请选择虚拟化平台" style="width: 80%">
					<option value="">请选择虚拟化平台</option>
					<!-- <option value="openstack">openstack</option>-->
					<option value="vsphere">vsphere</option>
				</select>   <span class="Validform_checktip Validform_span"></span>

			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-3 control-label">平台地址：<span class="required">*</span>
			</label>
			<div class="col-sm-9">
				<input type="text" class="form-control ue-form Validform_input" id="ip_address" style="width: 80%" name="ip_address" value="" placeholder="输入平台地址" datatype="*" nullmsg=" 请输入正确地址">
				<span class="Validform_checktip Validform_span"></span>

			</div>
		</div>
		<!-- <div class="form-group">
                <label class="col-sm-3 control-label">端口号：<span class="required">*</span></label>
                <div class="col-sm-9">
                    <input type="text" class="form-control ue-form Validform_input" id="port" style="width: 80%"
                           name="port" value="443" placeholder="请输入端口号" datatype="*" nullmsg=" 请输入正确ip" />
                    <span class="Validform_checktip Validform_span"></span>
                </div>
            </div>-->
		<div class="form-group">
			<label class="col-sm-3 control-label">用户名：<span class="required">*</span>
			</label>
			<div class="col-sm-9">
				<input type="text" class="form-control ue-form Validform_input" id="userName" style="width: 80%" name="userName" value="" placeholder="请输入用户名" datatype="*" nullmsg=" 请输入正确用户名">
				<span class="Validform_checktip Validform_span"></span>

			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-3 control-label">密码：<span class="required">*</span>
			</label>
			<div class="col-sm-9">
				<input type="password" class="form-control ue-form Validform_input" id="password" style="width: 80%" name="password" value="" placeholder="请输入密码" datatype="*" nullmsg=" 请输入正确密码">
				<span class="Validform_checktip Validform_span"></span>

			</div>
		</div>
		<button id="test" type="button" class="btn ue-btn  btn-sm" style="margin-left:258px;">测试</button>

		<div style="height: 36px">
			<div id="testAlertInfo" class="alert  alert-dismissable pull-right" role="alert" style="width:57%;margin-right:160px;display:none"> <span></span>
				<button class="close" type="button" id="close">×</button>
			</div>
		</div>
		<!-- <button type="button" id="add_manager_2.html" class="btn ue-btn-warning pull-right" style="margin-right:20px;">测试</button>-->
		<br>
		<br>
		<button type="button" id="next" class="btn ue-btn-primary pull-right" style="margin-right: 56px">下一步</button>
	</form>
</div>

<script type="text/javascript">
    //初始化validform表单校验
    $(function () {
        var isSave = false;
        var isClick = "";

        $("#test").click(function () {
            isClick = true;
        });
        $("#next").click(function () {
            isClick = false;
        });
        $("#saveForm").uValidform({
            btnSubmit: "#next,#test",
            datatype: {},
            callback: function (form) {
                if (isClick) {
                    $("#test").attr('disabled', 'disabled');
                    test();
                } else {
                    if (isSave) {
                        save();
                    } else {
                        $.dialog({
                            type: 'alert',
                            title: '提示：',
                            content: '执行下一步之前，请确保测试连接成功！'
                        })
                    }
                }
            }
        });

        //系统环境选中后判断数据库是否有记录
        $("#system").change(function () {
            var optionValue = $("#system option:selected").val();

            if (optionValue === "vsphere") {
                $.ajax({
                    type: "GET", //or POST
                    url: 'getVMPlatformInfo',
                    data: {
                        'vm_platform': optionValue
                    },
                    beforeSend: function () {
                        //发送请求之前执行的函数
                    },
                    success: function (data) {
                        var jsonData = $.parseJSON(data);
						if(jsonData.vm_info){
						var vm_info_passwd = jsonData.vm_info.vm_info_passwd;
                        var vm_info_host = jsonData.vm_info.vm_info_host;
                        var vm_info_user = jsonData.vm_info.vm_info_user;
                        var vm_info_platform = jsonData.vm_info.vm_info_platform;
                        if (vm_info_platform !== "" && vm_info_platform !== null) {
                            $("#ip_address").attr("readonly", "readonly").val(vm_info_host);
                            $("#userName").attr("readonly", "readonly").val(vm_info_user);
                            $("#password").attr("readonly", "readonly").val(vm_info_passwd);
                            isSave = true;
                        }	
						}
                    },
                    error: function () {
                        //请求错误后执行的函数
                    },
                    complete: function () {
                        //请求完成后执行的函数
                    }
                })
            }
        });
        //警告框关闭按钮
        $("#close").click(function () {
            $("#testAlertInfo").hide();
        });

        function test() {
            //获取系统环境
            var system = $("#system option:selected").val();
            //获取输入ip的值
            var ip = $("#ip_address").val();
            //获取端口号的值
            //var port = $("#port").val();
            //获取用户名
            var userName = $("#userName").val();
            //获取用户密码
            var password = $("#password").val();
            //判断是否隐藏

            function isHide() {
                if ($("#testAlertInfo").css("display") === 'none') {
                    $("#testAlertInfo").show();
                    setTimeout(function () {
                        $("#testAlertInfo").fadeOut(500).removeClass('alert-success alert-danger');
                    }, 3000)
                }
            }
            $.ajax({
                type: 'GET',
                url: '/check_vsphere_connect/',
                data: {
                    "vm_ip": ip,
                    "vm_user": userName,
                    "vm_passwd": password
                },
                success: function (data) {
                    //如果隐藏
                    isHide();
                    if (data.result) {
                        $("#testAlertInfo").addClass('alert-success').children('span').text("测试连接成功！");
                        isSave = true;
                    } else {
                        $("#testAlertInfo").addClass('alert-danger ').children('span').text("测试连接失败，请检查填写信息是否正确！");
                        isSave = false;
                    }
                },
                error: function () {
                    isHide();
                    $("#testAlertInfo").addClass('alert-danger ').children('span').text("测试连接失败，请检查填写信息是否正确！")
                    isSave = false;
                },
                complete: function () {
                    $("#test").removeAttr("disabled")
                }
            })
        }

        function save() {
            //获取系统环境
            var system = $("#system option:selected").val();
            //获取输入ip的值
            var ip = $("#ip_address").val();
            //获取端口号的值
            //var port = $("#port").val();
            //获取用户名
            var userName = $("#userName").val();
            //获取用户密码
            var password = $("#password").val();
            $.ajax({
                type: 'GET',
                url: '/saveManagerInfo/',
                data: {
                    "vm_ip": ip,
                    "vm_user": userName,
                    "vm_passwd": password,
                    "vm_platform": system
                },
                success: function (data) {
                    window.location.href = ('select_config?vm_ip=' + ip + "&vm_user=" + userName + "&vm_passwd=" + password +
                        "&vm_platform=" + system)
                },
                error: function () {}
            })
        }
    });
</script>
</body>
</html>

```
