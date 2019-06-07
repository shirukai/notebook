# ElementUI之button
## 基础用法

```
        <el-button type="primary">primary</el-button>
        <el-button type="success">success</el-button>
        <el-button type="warning">warning</el-button>
        <el-button type="danger">danger</el-button>
        <el-button type="info">info</el-button>
        <el-button type="text">text</el-button>
```
## 禁用状态

```
<el-button :disabled="true">按钮</el-button>
```
## hover 显示颜色
:plain属性控制
```
 <span class="wrapper">
    <el-button :plain="true" type="success">成功按钮</el-button>
    <el-button :plain="true" type="warning">警告按钮</el-button>
    <el-button :plain="true" type="danger">危险按钮</el-button>
    <el-button :plain="true" type="info">信息按钮</el-button>
  </span>
```
## 图标按钮
icon=“ ”属性控制

```
<el-button type="primary" icon="edit"></el-button>
<el-button type="primary" icon="share"></el-button>
<el-button type="primary" icon="delete"></el-button>
<el-button type="primary" icon="search">搜索</el-button>
<el-button type="primary">上传<i class="el-icon-upload el-icon--right"></i></el-button>
```
## 按钮组

```
<el-button-group>
    <el-button type="primary" icon="arrow-left">上一页</el-button>
    <el-button type="primary">下一页<i class="el-icon-arrow-right el-icon--right"></i></el-button>
</el-button-group>
<el-button-group>
    <el-button type="primary" icon="edit"></el-button>
    <el-button type="primary" icon="share"></el-button>
    <el-button type="primary" icon="delete"></el-button>
</el-button-group>
```
## 按钮加载中
:loading="true"属性
```
 <el-button type="primary" :loading="true">加载中</el-button>
```

## 按钮尺寸
