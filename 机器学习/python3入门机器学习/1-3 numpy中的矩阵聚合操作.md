

```python
import numpy as np
```


```python
L = np.random.random(100)
L
```




    array([0.25119175, 0.92977429, 0.99646455, 0.01350068, 0.10785383,
           0.13216408, 0.53743682, 0.2362282 , 0.43276904, 0.88723033,
           0.32363798, 0.7736106 , 0.30140572, 0.70171898, 0.23628926,
           0.11465989, 0.57768914, 0.90286834, 0.44965853, 0.17556582,
           0.32730562, 0.95484208, 0.5746498 , 0.96157915, 0.0786129 ,
           0.84205856, 0.06806985, 0.54740028, 0.51743019, 0.65094052,
           0.78537948, 0.31981498, 0.2084024 , 0.83275363, 0.73754856,
           0.40333091, 0.10272513, 0.71517294, 0.8921517 , 0.46988545,
           0.4046783 , 0.51339148, 0.05850318, 0.16110959, 0.21776947,
           0.44930324, 0.88457981, 0.05811443, 0.10390823, 0.22241806,
           0.55889435, 0.84595252, 0.6193869 , 0.00144356, 0.46580483,
           0.60804701, 0.42649072, 0.51240559, 0.60706584, 0.21786643,
           0.06466162, 0.57357243, 0.79564165, 0.91033563, 0.85622919,
           0.3801982 , 0.83295689, 0.19339375, 0.71351958, 0.74930296,
           0.3444482 , 0.23071657, 0.99059839, 0.02886684, 0.72539377,
           0.56155781, 0.31669104, 0.36856242, 0.88366868, 0.17844751,
           0.86080859, 0.67557473, 0.71354475, 0.23548466, 0.35971581,
           0.70263272, 0.11505366, 0.18399087, 0.68843181, 0.69321406,
           0.80155443, 0.03234361, 0.80893791, 0.24386097, 0.47227101,
           0.88669931, 0.08692295, 0.45551693, 0.6882757 , 0.2721928 ])




```python
sum(L)
```




    48.68469591211663




```python
np.sum(L)
```




    48.68469591211662




```python
big_array = np.random.rand(1000000)
%timeit sum(big_array)
%timeit np.sum(big_array)
```

    93 ms ± 2.17 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
    644 µs ± 50.8 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)



```python
np.min(big_array)
```




    5.496309696262358e-08




```python
np.max(big_array)
```




    0.9999996218965496




```python
big_array.max()
```




    0.9999996218965496




```python
big_array.min()
```




    5.496309696262358e-08




```python
X = np.arange(16).reshape(4,-1)
```


```python
X
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
np.sum(X)
```




    120




```python
# axis = 0 按照行的方向进行运算，就是每一列相加
np.sum(X,axis =0)
```




    array([24, 28, 32, 36])




```python
# axis = 1 按照列的方向进行运算，就是每一行相加
np.sum(X,axis =1)
```




    array([ 6, 22, 38, 54])




```python
# 乘积
np.prod(X)
```




    0




```python
np.prod(X + 1)
```




    20922789888000




```python
# mean 平均值
np.mean(X)
```




    7.5




```python
# 中位数
np.median(X)
```




    7.5




```python
v = np.array([1,1,2,2,10])
np.mean(v)
```




    3.2




```python
np.median(v)
```




    2.0




```python
# 百分位
np.percentile(big_array,q = 50)
```




    0.49954378380757225




```python
np.median(big_array)
```




    0.49954378380757225




```python
for percent in [0,25,50,75,100]:
    print(np.percentile(big_array,q = percent))
```

    5.496309696262358e-08
    0.250017903329254
    0.49954378380757225
    0.749635503268846
    0.9999996218965496



```python
# 方差
np.var(big_array)
```




    0.08327182928486565




```python
# 标准差
np.std(big_array)
```




    0.2885685867950038




```python
x = np.random.normal(0,1,size=1000000)
```


```python
np.mean(x)
```




    6.617905019805358e-05




```python
np.std(x)
```




    1.0004066392846953




```python
x
```




    array([ 1.35701725, -0.10555276,  0.16454334, ..., -0.52624124,
            1.1788963 , -0.53829805])



### 索引


```python
np.min(x)
```




    -4.997660514468604




```python
# 获取最小值索引位置
np.argmin(x)
```




    230204




```python
np.argmax(x)
```




    727824




```python
x[727824]
```




    4.606518805643649



### 排序和使用索引


```python
x = np.arange(16)
```


```python
x
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
np.random.shuffle(x)
x
```




    array([11,  3,  6,  0, 10, 15, 13,  2,  5,  8, 14,  4,  1, 12,  9,  7])




```python
np.sort(x)
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
x.sort()
```


```python
x
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
X = np.random.randint(10,size=(4,4))
X
```




    array([[2, 1, 2, 3],
           [8, 2, 0, 7],
           [7, 6, 1, 9],
           [6, 3, 9, 8]])




```python
# 默认是将每一行进行排序 axis 默认值是1
np.sort(X)
```




    array([[1, 2, 2, 3],
           [0, 2, 7, 8],
           [1, 6, 7, 9],
           [3, 6, 8, 9]])




```python
np.sort(X,axis = 1)
```




    array([[1, 2, 2, 3],
           [0, 2, 7, 8],
           [1, 6, 7, 9],
           [3, 6, 8, 9]])




```python
np.sort(X,axis = 0)
```




    array([[2, 1, 0, 3],
           [6, 2, 1, 7],
           [7, 3, 2, 8],
           [8, 6, 9, 9]])




```python
x
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
np.random.shuffle(x)
```


```python
# 索引数组
np.argsort(x)
```




    array([ 3,  8,  6,  9, 14,  4, 10,  2, 12,  7, 11,  5,  0,  1, 13, 15])




```python
# 寻找标定点，小于标定点放在左侧，大于标定点放在右侧
np.partition(x,3)
```




    array([ 0,  1,  2,  3,  4,  5,  9,  8,  7,  6, 10, 11, 12, 14, 13, 15])




```python
# 获取标定点的索引
np.argpartition(x,3)
```




    array([ 3,  8,  6,  9, 14,  4,  7, 12,  2, 10, 11,  5,  0, 13,  1, 15])




```python
X
```




    array([[2, 1, 2, 3],
           [8, 2, 0, 7],
           [7, 6, 1, 9],
           [6, 3, 9, 8]])




```python
np.argsort(X,axis=1)
```




    array([[1, 0, 2, 3],
           [2, 1, 3, 0],
           [2, 1, 0, 3],
           [1, 0, 3, 2]])




```python
np.argsort(X,axis=0)
```




    array([[0, 0, 1, 0],
           [3, 1, 2, 1],
           [2, 3, 0, 3],
           [1, 2, 3, 2]])




```python
np.argpartition(X,2,axis = 1)
```




    array([[1, 0, 2, 3],
           [2, 1, 3, 0],
           [2, 1, 0, 3],
           [1, 0, 3, 2]])


