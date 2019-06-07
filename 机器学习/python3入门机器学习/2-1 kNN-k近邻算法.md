
# kNN-k近邻算法

* 思想季度简单
* 应用数学只是少
* 效果好
* 可以解释机器学习算法使用过程中的很多细节问题
* 更完整的刻画机器学习应用的流程

![](https://shirukai.gitee.io/images/696e19e91f8344244a71ab620e8717fa.jpg)

假如k=3，就是寻找与该样本最近的3个样本来投票，票数多的样本就认为该待测样本与多数多的样本相似


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
raw_data_X = [[3.393533211,2.331273381],
             [3.110073483,1.781539368],
             [1.343808831,3.368360954],
             [3.582294042,4.679179110],
             [2.280362439,2.866990263],
             [7.423436942,4.696522875],
             [5.745051997,3.533989803],
             [9.172168622,2.511101045],
             [7.792783481,3.424088941],
             [7.939820817,0.791637231]]
raw_data_y = [0,0,0,0,0,1,1,1,1,1]
```


```python
X_train = np.array(raw_data_X)
y_train = np.array(raw_data_y)
```


```python
plt.scatter(X_train[y_train==0,0],X_train[y_train==0,1],color="g")
plt.scatter(X_train[y_train==1,0],X_train[y_train==1,1],color="r")
plt.show()
```


![](https://shirukai.gitee.io/images/79a66d7722b8b80ef3f56caafc70dc8a.jpg)



```python
x = np.array([8.093607318,3.365731514])
```


```python
plt.scatter(X_train[y_train==0,0],X_train[y_train==0,1],color="g")
plt.scatter(X_train[y_train==1,0],X_train[y_train==1,1],color="r")
plt.scatter(x[0],x[1],color="b")
plt.show()
```


![](https://shirukai.gitee.io/images/1860b9c8f18428d5d3a63ab4eef210bb.jpg)


### kNN过程


```python
from math import sqrt
distance = []
for x_train in X_train:
    d = sqrt(np.sum((x_train -x )**2))
    distance.append(d)
```


```python
distance
```




    [4.812566907609877,
     5.2292709090309994,
     6.749798999160064,
     4.6986266144110695,
     5.83460014556857,
     1.4900114024329525,
     2.354574897431513,
     1.3761132675144652,
     0.3064319992975,
     2.5786840957478887]




```python
# 求所有点与待测点之间的距离
distances = [sqrt(np.sum((x_train - x)**2)) for x_train in X_train]
```


```python
# 将距离排序并获得相应的索引
np.argsort(distances)
```




    array([8, 7, 5, 6, 9, 3, 0, 1, 4, 2])




```python
nearest = np.argsort(distances)
```


```python
k = 6
```


```python
# 取前六个对应的y值
topK_y = [y_train[i] for i in nearest[:k]]
```


```python
topK_y
```




    [1, 1, 1, 1, 1, 0]




```python
from collections import Counter
Counter(topK_y)
```




    Counter({0: 1, 1: 5})




```python
votes = Counter(topK_y)
```


```python
predict_y = votes.most_common(1)[0][0]
predict_y
```




    1



### 使用scikit-learn中的kNN


```python
from sklearn.neighbors import KNeighborsClassifier
```


```python
kNN_clssifier = KNeighborsClassifier(n_neighbors=6)
```


```python
kNN_clssifier.fit(X_train,y_train)
```


    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=6, p=2,
               weights='uniform')


```python
kNN_clssifier.predict(x.reshape(1,-1))
```


    array([1])


