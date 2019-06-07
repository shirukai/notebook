# List类案例
> 通过案例实现对list类的增删改查
## 创建课程类

```
public class Course
{
    //设置属性课程编号为cid
    public String cid;
    //设置属性课程名为cname
    public String cname;
    //构造有参方法给cid、cname赋值
    public Course(String cid,String cname){
        this.cid = cid;
        this.cname = cname;
    }
}
```
## 创建ListTest类

```
public class ListTest {
    /*用于存放备选课程*/
    public List coursesToSelect;
    public ListTest(){
        this.coursesToSelect = new ArrayList();
    }
}
```
#### 在ListTest类中构造testAdd方法用于测试add、addAll方法

```
public void testAdd(){
        Course cr1 = new Course("1","数据结构");
        coursesToSelect.add(cr1);
        Course temp =(Course) coursesToSelect.get(0);
        System.out.println("添加了课程："+temp.cid+":"+temp.cname);

        Course cr2 = new Course("2","C语言");
        coursesToSelect.add(0,cr2);
        Course temp2 = (Course)coursesToSelect.get(0);
        System.out.println("添加了课程："+temp2.cid+":"+temp2.cname);

        /*抛出数组下标越界异常*/
/*        Course cr3 = new Course("3","PHP");
        coursesToSelect.add(3,cr3);*/

        /*addAll方法*/
        Course[] course = {new Course("3","离散数学"),new Course("4","汇编语言")};
        coursesToSelect.addAll(Arrays.asList(course));
        Course temp3 = (Course) coursesToSelect.get(2);
        Course temp4 = (Course) coursesToSelect.get(3);
        System.out.println("添加了两门课程："+temp3.cid+":"+temp3.cname+";"+temp4.cid+":"+temp4.cname);

        Course[] course2 = {new Course("5","高等数学"),new Course("6","大学英语")};
        coursesToSelect.addAll(2,Arrays.asList(course2));
        Course temp5 = (Course)coursesToSelect.get(2);
        Course temp6 = (Course)coursesToSelect.get(3);
        System.out.println("又添加了两门课程："+temp5.cid+":"+temp5.cname+";"+temp6.cid+":"+temp6.cname);
    }
```
### 取得List中的元素的方法
> for循环遍历、迭代器遍历、for each 遍历
#### for循环

```
    public void testGet(){
        //获取List的长度
        int size = coursesToSelect.size();
        System.out.println("有如下课程待选：");
        for(int i=0;i<size;i++){
            Course cr = (Course)coursesToSelect.get(i);
            System.out.println("课程："+cr.cid+":"+cr.cname);
        }
    }
```
#### 通过迭代器遍历list元素

```
    public void testIterator(){
        Iterator iterator = coursesToSelect.iterator();
        System.out.println("有如下课程待选（通过迭代器访问）：");
        while (iterator.hasNext()){
            Course course = (Course) iterator.next();
            System.out.println("课程："+course.cid+":"+course.cname);
        }
    }
```
#### 通过for each方法遍历元素

```
    public void testForEach(){
        System.out.println("有如下课程待选（通过foreach遍历）：");
        for(Object obj:coursesToSelect){
            Course course = (Course) obj;
            System.out.println("课程："+course.cid+":"+course.cname);
        }
    }
```
### 修改list里的元素

```
    public void testModify(){
        coursesToSelect.set(4,new Course("7","毛概"));
        testForEach();
    }
```
### 删除list里的元素

```
    public void testRemove(){
/*        Course course = (Course)coursesToSelect.get(4);
        System.out.println("我是课程："+course.cid+":"+course.cname+"，我即将被删除");
        coursesToSelect.remove(course);*/
        /*或者用 coursesToSelect.remove(4);*/
        Course[] courses = {(Course) coursesToSelect.get(4),(Course) coursesToSelect.get(5)};
        coursesToSelect.removeAll(Arrays.asList(courses));
        System.out.println("成功删除");
        testForEach();
    }
```
## 测试方法

```
    public static void main(String[] args){
        ListTest listTest = new ListTest();
        listTest.testAdd();
        listTest.testGet();
        listTest.testIterator();
        listTest.testForEach();
        listTest.testModify();
        listTest.testRemove();
    }
```
