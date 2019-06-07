## 基础用法


```
 <el-radio class="radio" v-model="radio" label="1">备选项</el-radio>
  <el-radio class="radio" v-model="radio" label="2">备选项</el-radio>
```
## 按钮禁用

```
<el-radio disabled v-model="radio1" label="禁用">备选项</el-radio>
<el-radio disabled v-model="radio1"
label="选中且禁用">备选项</el-radio>
```
## 单选组

```
<el-radio-group v-model="radio2">
    <el-radio :label="3">备选项</el-radio>
    <el-radio :label="6">备选项</el-radio>
    <el-radio :label="9">备选项</el-radio>
  </el-radio-group>
```
## 按钮样式

```
      <el-radio-group v-model="radio3">
        <el-radio-button label="上海"></el-radio-button>
        <el-radio-button label="北京"></el-radio-button>
        <el-radio-button :disabled="isDisabled" label="广州"></el-radio-button>
        <el-radio-button label="深圳"></el-radio-button>
      </el-radio-group>
```
