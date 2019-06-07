# Django分页查询（整合vue）

## 一、django部分

在view.py里添加分页查询方法

```
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# 分页查询
def show_page(request):
    page = request.GET.get('page')
    pageSize = int(request.GET.get('pageSize'))
    response = {}
    book_list = Book.objects.all()
    paginator = Paginator(book_list, pageSize)
    response['total'] = paginator.count
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    response['list'] = json.loads(serializers.serialize("json", books))
    return JsonResponse(response)
```

接受前端传来的值：page为要显示的页数，pageSize为每页显示的数量

返回值类型：

```
{
"total": 14,
"list": [
{
"pk": 45,
"model": "myapp.book",
"fields": {
"book_name": "122323123231",
"add_time": "2017-09-25T07:15:57.946Z"
}
},
{
"pk": 46,
"model": "myapp.book",
"fields": {
"book_name": "12232312323112",
"add_time": "2017-09-25T07:16:00.553Z"
}
},
{
"pk": 47,
"model": "myapp.book",
"fields": {
"book_name": "12232312323112",
"add_time": "2017-09-25T07:16:00.730Z"
}
},
{
"pk": 48,
"model": "myapp.book",
"fields": {
"book_name": "12232312323112",
"add_time": "2017-09-25T07:16:00.904Z"
}
},
{
"pk": 49,
"model": "myapp.book",
"fields": {
"book_name": "12232312323112",
"add_time": "2017-09-25T07:16:01.074Z"
}
}
]
}
```

## 二、vue部分

HTML代码：

```
<template>
  <div class="table">
    <h1>数据增删改查</h1>
    <el-row type="flex">
      <el-col :span="12">
        <el-input v-model="input" placeholder="请输入书名"></el-input>
      </el-col>
      <el-col :span="2">
        <el-button type="primary" @click="addBook()">新增</el-button>
      </el-col>
    </el-row>
    <el-row type="flex">
      <el-col :span="12">
        <el-input v-model="SearchInput" placeholder="要查询的书名"></el-input>
      </el-col>
      <el-col :span="2">
        <el-button type="primary" @click="searchBook()">查询</el-button>
      </el-col>
    </el-row>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column label="日期" width="280">
        <template scope="scope">
          <el-icon name="time"></el-icon>
          <span style="margin-left: 10px">{{ scope.row.fields.add_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="书名" width="280">
        <template scope="scope">
          <el-input v-show="scope.row.edit" size="small" v-model="scope.row.fields.book_name"></el-input>
          <span v-show="!scope.row.edit">{{ scope.row.fields.book_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template scope="scope">
          <el-button
            size="small"
            @click="handleEdit(scope.$index, scope.row)">{{ scope.row.edit ? '完成' : '编辑'}}
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[5,15,20,25]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
  </div>
</template>
```

script代码：

数据data部分

```
data() {
  return {
    input: '',
    SearchInput: '',
    //一共多少条数据
    total: 0,
    //每页显示多少条数据
    pageSize: 5,
    //当前第几页
    page: 1,
    tableData: [],
    currentPage: 1
  }
},
```

获取数据的方法：

```
showBooks() {
  this.$http.get(requestUrl + '/api/show_page?page=' + this.page + '&pageSize=' + this.pageSize)
    .then((response) => {
      let res = JSON.parse(response.bodyText);
      console.log(res);
      this.total = res.total;
      this.tableData = res.list.map(v => {
      	//在返回的数据里增加一条数据
        this.$set(v, 'edit', false)
        return v
      })
    })
}
```

当每页显数量改变时执行的方法

```
handleSizeChange(pageSize) {
  //每页显示多少条数据
  this.pageSize = pageSize;
  console.log(pageSize);
  this.showBooks()
},
```

当点第几页时执行的方法

```
handleCurrentChange(val) {
  this.page = val;
  this.showBooks();
  console.log(`当前页: ${val}`);
}
```