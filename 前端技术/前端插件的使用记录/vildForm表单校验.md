# vildForm表单校验

## 一、 HTML部分

```
<!-- 页面结构 -->
<div class="ue-container" id="sandbox-container">
    <!-- 验证信息nowrap -->
    <form class="form-horizontal" id="saveForm" name="saveForm" onsubmit="return false">
        <div class="form-group">
            <label class="col-sm-3 control-label">名称<span class="required">*</span></label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" id="userName"
                       name="userName" value="" placeholder="名称" datatype="s5-16" errormsg="昵称至少5个字符,最多16个字符！" nullmsg="请设置正确名称" />
                <span class="Validform_checktip Validform_span"></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">账号状态</label>
            <div class="col-sm-8">
                <select class="form-control ue-form Validform_input" name="userStatus" datatype="s" nullmsg="请设置账号状态">
                    <option value="">请选择</option>
                    <option value="N">启用</option>
                    <option value="X">停用</option>
                </select>
                <span class="Validform_checktip Validform_span"></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">身份证号<span class="required">*</span></label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" id="id"
                       name="userArchiveId" value=""
                       placeholder="身份证号" datatype="idcard" nullmsg="请填写身份证号" errormsg="请填写合法的身份证号"/>
                <span class="Validform_checktip Validform_span"></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">生日</label>
            <div class="col-sm-8">
                <div class="input-group date Validform_input" >
                    <div id="birthday"><input type="text" class="form-control ue-form"
                                              name="userArchiveBirthday"
                                              placeholder="生日" datatype="*" nullmsg="请设置出生日期"/></div> <span class="input-group-addon ue-form-btn"><i
                        class="fa fa-calendar"></i></span>
                </div>
                <span class="Validform_checktip Validform_span" ></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">学历</label>
            <div class="col-sm-8 text-left radio">
                <label><input type="radio"  name="userArchiveEducation" value="0" datatype="*" nullmsg="请选择学历"/>本科 	</label>
                <label><input type="radio"  name="userArchiveEducation" value="1"/>硕士</label>
                <label><input type="radio"  name="userArchiveEducation" value="2"/>博士</label>
                <span class="Validform_checktip"></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">学校<span class="required">*</span></label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" id="school"
                       name="archivesSchool" value=""
                       placeholder="学校" datatype="s" nullmsg="请填写学校名称"/>
                <span class="Validform_checktip Validform_span"></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">爱好</label>
            <div class="col-sm-8 text-left checkbox">
                <label><input type="checkbox" value="0" name="archivesFavor" datatype="*" nullmsg="请填写兴趣爱好" errormsg="请填写兴趣爱好"/>篮球</label>
                <label><input type="checkbox" value="1" name="archivesFavor"/>足球</label>
                <label><input type="checkbox" value="2" name="archivesFavor"/>排球</label>
                <span class="Validform_checktip" ></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">电子邮件</label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" id="email"
                       name="archivesEmail" value=""
                       placeholder="邮件地址" datatype="email" nullmsg="请填写邮箱地址" errormsg="请填写正确的邮箱地址"/>
                <span class="Validform_checktip Validform_span" ></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">密码</label>
            <div class="col-sm-8">
                <input type="password" class="form-control ue-form Validform_input" id="pwd"
                       name="pwd" value=""
                       placeholder="请输入6-16位密码" datatype="s6-16" nullmsg="密码不能为空" errormsg="请输入6-16位密码"/>
                <span class="Validform_checktip Validform_span" ></span>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-3 control-label">重复密码</label>
            <div class="col-sm-8">
                <input type="password" class="form-control ue-form Validform_input" id="pwd-confirm"
                       name="pwd-confirm" value=""
                       placeholder="重复密码" datatype="s6-16" nullmsg="密码不能为空" errormsg="两次密码不一致，请重新填写" recheck="pwd"/>
                <span class="Validform_checktip Validform_span" ></span>
            </div>
        </div>
        <h4>自定义正则校验</h4>
        <div class="form-group">
            <label class="col-sm-3 control-label">第一个字符为字母</label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" id="inital"
                       name="inital" value=""
                       placeholder="首字母校验" datatype="inital" nullmsg="请填写内容"/>
                <span class="Validform_checktip Validform_span" ></span>
            </div>
        </div>
        <h4>ajax当前表单参数校验</h4>
        <div class="form-group">
            <label class="col-sm-3 control-label">判断用户名是否存在</label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" ajaxurl="data/checkName.json" id="uname"
                       name="uname" value=""
                       placeholder="判断用户名是否存在" datatype="*" nullmsg="输入用户名"/>
                <span class="Validform_checktip Validform_span" ></span>
            </div>
        </div>
        <div class="form-group" >
            <label class="col-sm-3 control-label"></label>
            <div class="col-sm-8">
                <button type="button" class="btn ue-btn-primary" id="validate">
                    保存
                </button>
                <button type="button" class="btn ue-btn" id="cancel">
                    取消
                </button>
                <span id="msgdemo"></span>
            </div>
        </div>
    </form>
</div>
```

说明：
1. input里添加class属性Validform_input，
2. datatype属性是校验的类型，如datatype=“s5-16”意思是5到16个字符，插件分装好的几个正则判断如下：

```
*：检测是否有输入，可以输入任何字符，不留空即可通过验证；
*6-16：检测是否为6到16位任意字符；
n：数字类型；
n6-16：6到16位数字；
s：字符串类型；
s6-18：6到18位字符串；
p：验证是否为邮政编码；
m：手机号码格式；
e：email格式；
url：验证字符串是否为网址。
```
3. errormsg属性是，不符合正则时的显示的字符串

4. nullmsg属性是，当输入为空时显示的字符串


## 二、js部分

```
    <script type="text/javascript">
        $(function () {
            $("#saveForm").uValidform({
                btnSubmit:"#validate",
                datatype:{
                    "idcard": idcard,
                    "email" : email,
                    //自定义校验
                    "inital":function (gets,obj,curform,regxp) {
                        //参数gets是获取到的表单元素值，obj为当前表单元素，curform为当前验证的表单，regxp为内置的一些正则表达式的引用;
                        //首字母校验,这里写正则表达式或者函数
                        var reg1=/^[a-zA-Z]\w*$/ ;
                        //长度校验
                        var reg2=/^\w{6,16}/;
                        var errormsg;
                        if (reg1.test(gets)){
                            if (reg2.test(gets)){
                                return true
                            }else {
                                errormsg = "长度为6-16字符";
                                return errormsg
                            }
                        }else {
                            errormsg = "第一个字符必须为首字母";
                            return errormsg;
                        }
                    }
                },
                callback:function(form){
                    $.dialog({
                        type: 'confirm',
                        content: '您确定要提交表单吗？',
                        ok: function () {save();},
                        cancel: function () {}
                    });
                }
            });
            //日期插件
            $('.input-group.date').datetimepicker({
                container: $("#birthday"),
                language: "zh-CN",
                autoclose: true,
                minView: 2,
                format: "yyyy-mm-dd"
            }).on("changeDate",function(){
                $(this).find("input").blur();
            });
        })
    </script>
```
说明
1. #saveForm 为表单form的id
2. btnSubmit:"#validate"中的#validate 为提交表单的按钮
3. datatype里为自定义正则判断或者函数方法，这里可以自己去写一些正则表达式，或者是方法，甚至可以通过ajax发送数据请求后台数据来判断前端表单数据的合法性。
4. callback里为提交表单前执行的回调函数，return true择执行form表单默认的post请求，return false则不自动执行



## 三、扩展 ajax表单验证的两证方法

1. ajax判断用户名是否存在（当前表单内容为参数）

```
        <div class="form-group">
            <label class="col-sm-3 control-label">用户名<span class="required">*</span></label>
            <div class="col-sm-8">
                <input type="text" class="form-control ue-form Validform_input" id="uname"
                       name="uname" value="" placeholder="邮箱或者手机号" datatype="m|e" ajaxurl="<%=request.getContextPath()%>/service/checkName"  errormsg="注册用户名必须为邮箱或者手机号！" nullmsg="请设置正确用户名" />
                <span class="Validform_checktip Validform_span"></span>
            </div>
        </div>
```

ajaxurl里为请求的链接，当前表单里的内容会以参数的形式发送。
后台返回的数据格式如下：

```
{
"status": "y",
"info": "用户名可用"
}
```
如果用户名不可用status为n，Info是要提示用户的信息，如“用户名已存在”

2. 在js中自定义datatype中可以发送ajax请求，去判断输入的合法性，注意ajax请求必须为同步。


官网文档地址：[http://validform.rjboy.cn/document.html](http://validform.rjboy.cn/document.html)