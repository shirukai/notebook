# hadoop-MapReduce (并行计算框架)

## MapReduce原理 

分而治之，一个大任务分成多个小的子任务(map),并行执行后，合并结果（reduce）

## MaperReduce的运行流程 

### 基本概念

![](https://shirukai.gitee.io/images/201711271304_825.png)

### MapReduce的四个阶段

![](https://shirukai.gitee.io/images/201711271305_812.png)





### MapReduce的容错机制 

①重复执行 （默认重复执行四次之后仍然失败放弃执行）

② 推测执行 

在整个任务执行的过程中，需要map端所有的任务都完成后，才开始执行Reduce端的任务。

map端可能出现某一个任务执行的特别慢，其他的任务都完成了，而它还没有完成。这时候jobTracker就会发现其中有一个节点算的特别慢，说明它出现了问题，这时候，算的慢的还继续算，再找一台TaskTracker去跟他做同样的实行，他们两个，谁先完成，就把另一个给终止掉。

### 控制Map任务个数

![](https://shirukai.gitee.io/images/201711271309_82.png)



在一个Reducer中，所有的数据都会被按照key值升序排序，故如果part输出文件中包含key值，则这个文件一定是有序的。

## MapReduce应用案例 

### 入门程序WordCount单词计数 

计算文件中出现每个单词的频数

输入结果按照字母顺序进行排序

