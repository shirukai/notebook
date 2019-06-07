# Set接口及其实现类——HashSet
> ### Set是元素无序并且不可以重复的集合，被称为集
> ### HashSet——哈希集，是Set的一个重要的实现类
## HashSet案例
* #### 提供备选课程
* #### 创建学生对象，并给该学生添加三门课程（添加正在学生的courses——Set类型的属性中）
1. 显示备选课程
2. 循环三次，每次输入课程ID
3. 往学生的courses属性中添加与输入的ID匹配的课程
4. 输出学生选择的课程
## 代码清单
#### 创建学生类

```
public class Student {
    public String sid;
    public String sname;
    public Set<Course> courses;
    public Student(String sid, String sname){
        this.sid = sid;
        this.sname = sname;
        this.courses = new HashSet<Course>();
    }
}
```
#### 创建SetTest类

```
public class SetTest {
    public List<Course> coursesToSelect;
    public SetTest(){
        coursesToSelect  = new ArrayList<Course>();
    }
}
```
#### 在SetTest类中构建 添加元素的方法testAdd()

```
public void testAdd(){
        Course cr1 = new Course("1","数据结构");
        coursesToSelect.add(cr1);

        Course cr2 = new Course("2","C语言");
        coursesToSelect.add(0,cr2);

        Course[] course = {new Course("3","离散数学"),new Course("4","汇编语言")};
        coursesToSelect.addAll(Arrays.asList(course));


        Course[] course2 = {new Course("5","高等数学"),new Course("6","大学英语")};
        coursesToSelect.addAll(2,Arrays.asList(course2));
    }
```
#### 在SetTest中通过for each方法遍历元素

```
ublic void testForEach(){
        System.out.println("有如下课程待选（通过foreach遍历）：");
        for(Object obj:coursesToSelect){
            Course course = (Course) obj;
            System.out.println("课程："+course.cid+":"+course.cname);
        }
    }
```
#### 打印输出，学生所选的课程

```
    public void testForEachForSet(Student student){
        for(Course cr : student.courses){
            System.out.println("选择了课程:"+cr.cid+":"+cr.cname);
        }
    }
```
#### 创建测试类主方法

```
    public static void main(String[] args){
        SetTest st = new SetTest();
        st.testAdd();
        st.testForEach();
        //创建一个学生对象
        Student student = new Student("1","小明");
        System.out.println("欢迎学生："+student.sname+"选课！");
        //创建一个Scanner对象，用来接收从键盘输入的课程ID
        Scanner console = new Scanner(System.in);
        for(int i=0;i<3;i++){
            System.out.println("请输入课程ID");
            String courseId = console.next();
            for (Course cr:st.coursesToSelect){
                if (cr.cid.equals(courseId)){
                    student.courses.add(cr);
                   /* Set中，添加某个对象，无论添加多少次
                   * 最终只会保留一个该对象（的引用），
                   * 并且，保留的是第一次添加的那一个*/
                }
            }
        }
        st.testForEachForSet(student);
    }
```
