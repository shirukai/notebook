# 用POI实现表格导入导出功能 

maven依赖

```
<!--微软POI依赖-->
<dependency>
  <groupId>org.apache.poi</groupId>
  <artifactId>poi-ooxml</artifactId>
  <version>3.17</version>
</dependency>
```

## 一、表格读取

### HTML

引入jquery、bootstrap

```
<div class="container">
    <div class="panel">
        <div class="panel-heading text-center">
            <h3>利用POI实现表格的读写</h3>
        </div>
        <div class="panel-body">
            <button class="btn btn-primary" id="importExcel">导入表格</button>
            <a class="btn btn-info" href="/plugins/excel/export">导出表格</a>
            <input type="file" style="display: none" id="upFile">
            <hr>
            <h4>表格数据</h4>
            <textarea id="tableContent" class="text" style="width: 40%" readonly rows="10">
            </textarea>
            <hr>
        </div>
    </div>
</div>
<script type="text/javascript">
    $('#importExcel').click(function () {
        $('#upFile').click();
    });
    $('#upFile').change(function () {
        //读取input里的文件
        /* var files = $(this).prop('files');*/
        /* var files = event.target.files;*/
        const files = $(this)[0].files;

        console.log(files[0].name);
        //获取后缀名
        const fileName = files[0].name;
        const fileType = getExpandedName(fileName);
        console.log("_____________" + fileType)
        if (fileType === "xml" || fileType === "xlsx"){
            const formdata = new FormData();
            formdata.append('file', files[0])
            $.ajax({
                url: '/plugins/excel/upload',
                type: 'POST',
                data: formdata,
                // 告诉jQuery不要去处理发送的数据
                processData: false,
                // 告诉jQuery不要去设置Content-Type请求头
                contentType: false,
                success: function (data) {
                    console.log(data.toString())
                    $('#tableContent').val(data.toString())
                }
            })
        }else {
            alert("文件格式为：xml、xlsx！")
        }
    });

    //封装获取扩展名的方法
    function getExpandedName(fileName) {
        const index1 = fileName.lastIndexOf(".");
        const index2 = fileName.length;
        return fileName.substring(index1 + 1, index2);
    }
</script>
```

#### 分析

##### 1.先设置一个button用来做点击按钮，然后设置一个隐藏的type为file的input，用来文件上传。当点击按钮的时候触发input的点击事件。 

    $('#importExcel').click(function () {
        $('#upFile').click();
    });
##### 2.选择文件后，我们要根据input的change事件来触发我们的上传操作。

```
    $('#upFile').change(function () {
      //上传操作
    })
```

##### 3.上传操作只要包括，读取上传文件，存入formdata，然后利用ajax传到后端

a 读取input文件有三种方式

###### jquery 方法一：

```
var files = $(this).prop('files');
```

补充：jquery的prop与attr的区别用法

prop 和attr都是获取jqury选种元素的属性的，如获取a标签的class属性：

```
$('a').prop('class')或者 $('a').attr('class')
```

既然都可以获取那么它们有什么区别呢?

prop可以用来获取DOM里再W3C标准中包含的属性，而attr可以获取自定义的属性:

```
<a id="delete" class="btn" href="#" action="actionToDelete">删除</a>

console.log(aId.attr("action"))
```

action是自定义的属性，这时用prop就获取不到了

另外：像checkbox、radio、select这样的元素，属性对应的"checked"、"selected"这也是固有属性，所以要用prop去获取

###### jquery方法二:

```
var files = $(this)[0].files;
```

###### js原生方法三：

```
var files = event.target.files;
```

b 判断后缀名

```
//获取后缀名
const fileName = files[0].name;
const fileType = getExpandedName(fileName);
if (fileType === "xml" || fileType === "xlsx"){
  
}
//封装获取后缀名的方法
    function getExpandedName(fileName) {
        const index1 = fileName.lastIndexOf(".");
        const index2 = fileName.length;
        return fileName.substring(index1 + 1, index2);
    }
```

c将文件存入form

            const formdata = new FormData();
            formdata.append('file', files[0])
d ajax请求

            $.ajax({
                url: '/plugins/excel/upload',
                type: 'POST',
                data: formdata,
                // 告诉jQuery不要去处理发送的数据
                processData: false,
                // 告诉jQuery不要去设置Content-Type请求头
                contentType: false,
                success: function (data) {
                    console.log(data.toString())
                    $('#tableContent').val(data.toString())
                }
            })
注意一定要把：processData设置为false还有contentType设置为false

### 后端 

### 封装工具类

在 util下创建ExcelUtil工具类

```
private final static String excel2003L = ".xml";//2003-版本的excel
private final static String excel2007U = ".xlsx"; //2007+版本的excel

/*—————————————读取Excel文件—————————————————*/

/**
 * 获取读取Excel并返回list
 *
 * @param inputStream file.getInputStream
 * @param fileName    文件名
 * @return 返回list
 * @throws Exception
 */
public static List<List<Object>> getBankListByExcel(InputStream inputStream, String fileName) throws Exception {
    List<List<Object>> list = null;
    //常见Excel工作簿
    Workbook workbook = getWorkbook(inputStream, fileName);
    if (workbook == null) {
        throw new Exception("创建Excel工作簿为空");
    }
    Sheet sheet = null;
    Row row = null;
    Cell cell = null;
    list = new ArrayList<List<Object>>();
    System.out.println(workbook.getNumberOfSheets());
    //遍历Excel中所有的sheet
    for (int i = 0; i < workbook.getNumberOfSheets(); i++) {
        sheet = workbook.getSheetAt(i);
        if (sheet == null) {
            continue;
        }
        //遍历当前sheet中的所有行
        for (int j = sheet.getFirstRowNum(); j <= sheet.getLastRowNum(); j++) {
            row = sheet.getRow(j);
            if (row == null) {
                continue;
            }
            //遍历所有的列
            List<Object> li = new ArrayList<Object>();
            for (int y = row.getFirstCellNum(); y < row.getLastCellNum(); y++) {
                cell = row.getCell(y);
                li.add(getCellValue(cell));
            }
            list.add(li);
        }
    }
    return list;
}

/**
 * 根据后缀名,自适应上传文件的版本
 *
 * @param inputStream file.InputStream\ FileInputStream
 * @param fileName    文件名
 * @return 返回相应版本的工作表
 * @throws Exception
 */
public static Workbook getWorkbook(InputStream inputStream, String fileName) throws Exception {
    Workbook workbook = null;
    //获取后缀名
    String fileType = fileName.substring(fileName.lastIndexOf("."));
    if (excel2003L.equals(fileType)) {
        workbook = new HSSFWorkbook(inputStream);//2003-
    } else if (excel2007U.equals(fileType)) {
        workbook = new XSSFWorkbook(inputStream);//2007+
    } else {
        //文件格式不正确，前后端都可以做校验，最好在前端做校验
    }
    return workbook;
}

/**
 * 格式化数据
 * @param cell 列
 * @return
 */
public static Object getCellValue(Cell cell) {
    Object value = null;
    DecimalFormat decimalFormat = new DecimalFormat("0");//格式化number String字符
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");//日期格式化
    DecimalFormat decimalFormat1 = new DecimalFormat("0.00"); //格式化数字
    CellType cellType = cell.getCellTypeEnum();
    switch (cellType) {
        case STRING:
            value = cell.getRichStringCellValue().getString();
            break;
        case NUMERIC:
            if ("General".equals(cell.getCellStyle().getDataFormatString())) {
                value = decimalFormat.format(cell.getNumericCellValue());
            } else if ("m/d/yy".equals(cell.getCellStyle().getDataFormatString())) {
                value = simpleDateFormat.format(cell.getDateCellValue());
            } else {
                value = decimalFormat1.format(cell.getNumericCellValue());
            }
            break;
        case BOOLEAN:
            value = cell.getBooleanCellValue();
            break;
        case BLANK:
            value = "";
            break;
        default:
            break;
    }
    return value;
}
```

###  controller层 

```
@RequestMapping("/excel/upload")
@ResponseBody
public List<List<Object>> excelUpload(
        MultipartFile file, HttpServletRequest request
){
    List<List<Object>> lists = new ArrayList<List<Object>>();
    logger.info("_________________________file={}",file.getOriginalFilename());
    if (!file.isEmpty()){
        try {
            InputStream inputStream = file.getInputStream();
            lists = ExcelUtils.getBankListByExcel(inputStream, file.getOriginalFilename());
            inputStream.close();
            logger.info("_________ExcelLIst={}", lists);
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }
    return lists;
}
```

## 表格导出

### 封装工具类 

```
/*—————————————————生成Excel文件—————————————————————*/
public static XSSFWorkbook createExcelFile(Class clazz, List objs, Map<Integer, List<ExcelBean>> map,
                                           String sheetName) throws
        IllegalArgumentException, IllegalAccessException, InvocationTargetException,
        ClassNotFoundException, IntrospectionException, ParseException {
    //创建新的Excel工作簿
    XSSFWorkbook workbook = new XSSFWorkbook();
    //在Excel工作簿中创建一张工作表，其名为缺省值，也可以指定Sheet名称
    XSSFSheet sheet = workbook.createSheet(sheetName);
    //Excel样式配置
    createFont(workbook);
    //创建标题头
   createTableHeader(sheet,map);
    //创建内容
    createTableRows(sheet,map,objs,clazz);
    return workbook;
}

private static XSSFCellStyle headStyle;
private static XSSFCellStyle bodyStyle;

/**
 * 字体样式
 *
 * @param workbook 工作簿
 */
public static void createFont(XSSFWorkbook workbook) {
    //1:表头
    headStyle = workbook.createCellStyle();
    // 1)字体
    XSSFFont headFont = workbook.createFont();
    headFont.setBold(true);
    headFont.setFontName("黑体");
    headFont.setFontHeightInPoints((short) 12);
    headStyle.setFont(headFont);
    // 2)边框
    headStyle.setBorderBottom(BorderStyle.THIN);//下边框
    headStyle.setBorderTop(BorderStyle.THIN);//上边框
    headStyle.setBorderLeft(BorderStyle.THIN);//左边框
    headStyle.setBorderRight(BorderStyle.THIN);//右边框
    headStyle.setAlignment(HorizontalAlignment.CENTER);//字体居中

    //2:内容
    bodyStyle = workbook.createCellStyle();
    //1)字体
    XSSFFont bodyFont = workbook.createFont();
    bodyFont.setFontName("宋体");//字体
    bodyFont.setFontHeightInPoints((short) 10);//字体大小
    bodyStyle.setFont(bodyFont);
    //2)边框
    bodyStyle.setBorderBottom(BorderStyle.THIN);//下边框
    bodyStyle.setBorderTop(BorderStyle.THIN);//上边框
    bodyStyle.setBorderLeft(BorderStyle.THIN);//左边框
    bodyStyle.setBorderRight(BorderStyle.THIN);//右边框
    bodyStyle.setAlignment(HorizontalAlignment.CENTER);//字体居中
}

public static final void createTableHeader(XSSFSheet sheet, Map<Integer, List<ExcelBean>> map) {
    int startIndex = 0;//起始位置
    int endIndex = 0;//终止位置

    for (Map.Entry<Integer, List<ExcelBean>> entry : map.entrySet()) {
        XSSFRow row = sheet.createRow(entry.getKey());
        List<ExcelBean> excelBeans = entry.getValue();
        for (int x = 0; x < excelBeans.size(); x++) {
            //合并单元格
            if (excelBeans.get(x).getCols() > 1) {
                if (x == 0) {
                    endIndex += excelBeans.get(x).getCols() - 1;
                    CellRangeAddress rangeAddress = new CellRangeAddress(0, 0, startIndex, endIndex);
                    sheet.addMergedRegion(rangeAddress);
                    startIndex += excelBeans.get(x).getCols();
                } else {
                    endIndex += excelBeans.get(x).getCols();
                    CellRangeAddress rangeAddress = new CellRangeAddress(0, 0, startIndex, endIndex);
                    sheet.addMergedRegion(rangeAddress);
                    startIndex += excelBeans.get(x).getCols();
                }
                XSSFCell cell = row.createCell(startIndex - excelBeans.get(x).getCols());
                cell.setCellValue(excelBeans.get(x).getHeadTextName());//设置内容
                if (excelBeans.get(x).getCellStyle() != null) {
                    cell.setCellStyle(excelBeans.get(x).getCellStyle());
                }
                cell.setCellStyle(headStyle);
            } else {
                XSSFCell cell = row.createCell(x);
                cell.setCellValue(excelBeans.get(x).getHeadTextName());//设置内容
                if (excelBeans.get(x).getCellStyle() != null) {
                    cell.setCellStyle(excelBeans.get(x).getCellStyle());//设置格式
                }
                cell.setCellStyle(headStyle);
            }
        }
    }
}

@SuppressWarnings("rawtypes")
public static void createTableRows(XSSFSheet sheet, Map<Integer, List<ExcelBean>> map, List objs, Class clazz)
        throws IllegalArgumentException, IllegalAccessException,
        InvocationTargetException, IntrospectionException, ClassNotFoundException {
    int rowIndex = map.size();
    int maxKey = 0;
    List<ExcelBean> excelBeans = new ArrayList<ExcelBean>();
    for (Map.Entry<Integer, List<ExcelBean>> entry : map.entrySet()) {
        if (entry.getKey() > maxKey) {
            maxKey = entry.getKey();
        }
    }
    excelBeans = map.get(maxKey);
    List<Integer> widths = new ArrayList<Integer>(excelBeans.size());
    for (Object object : objs) {
        XSSFRow row = sheet.createRow(rowIndex);
        for (int i = 0; i < excelBeans.size(); i++) {
            ExcelBean em = (ExcelBean) excelBeans.get(i);
            //获得get方法
            PropertyDescriptor pd = new PropertyDescriptor(em.getPropertyName(), clazz);
            Method getMethod = pd.getReadMethod();
            Object rtn = getMethod.invoke(object);
            String value = "";
            //如果是日期类型进行转换
            if (rtn != null) {
                if (rtn instanceof Date) {
                    SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
                    value = format.format(rtn);
                } else if (rtn instanceof BigDecimal) {
                    NumberFormat nf = new DecimalFormat("#,##0.00");
                    value = nf.format((BigDecimal) rtn).toString();
                } else if ((rtn instanceof Integer) && (Integer.valueOf(rtn.toString()) < 0)) {
                    value = "--";
                } else {
                    value = rtn.toString();
                }
            }
            XSSFCell cell = row.createCell(i);
            cell.setCellValue(value);
            cell.setCellType(CellType.STRING);
            cell.setCellStyle(bodyStyle);
            //获得最大列宽
            int width = value.getBytes().length * 300;
            //还未设置，设置当前
            if (widths.size() <= i) {
                widths.add(width);
                continue;
            }
            //比原来大,更新数据
            if (width > widths.get(i)) {
                widths.set(i, width);
            }
        }
        rowIndex++;
    }
    //设置列换
    for (int index = 0; index < widths.size(); index++) {
        Integer width = widths.get(index);
        width = width < 2500 ? 2500 : width + 300;
        width = width > 10000 ? 10000 + 300 : width + 300;
        sheet.setColumnWidth(index,width);
    }
}
```

### controller层 

```
@RequestMapping("/excel/export")
@ResponseBody
public void excelExport(
        HttpServletRequest request,
        HttpServletResponse response
)throws Exception{
            response.reset();
    SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddhhmmssms");
    String dataStr = sdf.format(new Date());
    Map<String,Object> map = new HashMap<String,Object>();

    //指定下载的文件名
    response.setHeader("Content-Disposition","attachment;filename="+dataStr+".xlsx");
    response.setContentType("application/vnd.ms-excel;charset=UTF-8");
    response.setHeader("Pragma","no-cache");
    response.setHeader("Cache-Control","no-cache");
    response.setDateHeader("Expires",0);

    //导出Excel表格
    XSSFWorkbook workbook = null;
    try {
        List<User> userList = mavenssmlrService.queryAll();
        List<ExcelBean> ems = new ArrayList<ExcelBean>();
        Map<Integer,List<ExcelBean>> map1 = new LinkedHashMap<Integer, List<ExcelBean>>();
        //手动设置表头
        Boolean autoHeader = true;
        if (!autoHeader){
            ems.add(new ExcelBean("id","id",0));
            ems.add(new ExcelBean("用户名","uname",0));
            ems.add(new ExcelBean("创建时间","createTime",0));
            ems.add(new ExcelBean("修改时间","modifyTime",0));
            map1.put(0,ems);
        }else {
            User user = new User();
            String fieldName;
            Field[] fields = user.getClass().getDeclaredFields();
            for (int i = 0; i<fields.length;i++){
                fieldName = fields[i].getName();
                ems.add(new ExcelBean(fieldName,fieldName,0));
                logger.info("fieldsName={}",fieldName);
            }
            map1.put(0,ems);
        }
        workbook = ExcelUtils.createExcelFile(User.class,userList,map1,"用户表");

    } catch (Exception e) {
        logger.error(e.getMessage(), e);
    }
    OutputStream outputStream;
    try {
        outputStream = response.getOutputStream();
        BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(outputStream);
        bufferedOutputStream.flush();
        workbook.write(bufferedOutputStream);
        bufferedOutputStream.close();
    } catch (Exception e) {
        logger.error(e.getMessage(), e);
    }

}
```