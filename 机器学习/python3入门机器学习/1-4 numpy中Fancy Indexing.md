

```python
import numpy as np
```


```python
x = np.arange(16)
x
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
x[3]
```




    3




```python
x[3:9]
```




    array([3, 4, 5, 6, 7, 8])




```python
x[3:9:2]
```




    array([3, 5, 7])




```python
[x[3],x[5],x[8]]
```




    [3, 5, 8]




```python
ind = [3,5,8]
```


```python
x[ind]
```




    array([3, 5, 8])




```python
ind = np.array([[0,2],[1,3]])
```


```python
x[ind]
```




    array([[0, 2],
           [1, 3]])




```python
X = x.reshape(4,-1)
```


```python
X
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
row = np.array([0,1,2])
col = np.array([1,2,3])
```


```python
X[row,col]
```




    array([ 1,  6, 11])




```python
X[0,col]
```




    array([1, 2, 3])




```python
X[:2,col]
```




    array([[1, 2, 3],
           [5, 6, 7]])




```python
col = [True,False,True,True]
```


```python
X[1:3,col]
```




    array([[ 4,  6,  7],
           [ 8, 10, 11]])



### numpy.array的比较


```python
x
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
x <3
```




    array([ True,  True,  True, False, False, False, False, False, False,
           False, False, False, False, False, False, False])




```python
x > 3 
```




    array([False, False, False, False,  True,  True,  True,  True,  True,
            True,  True,  True,  True,  True,  True,  True])




```python
X <=3
```




    array([[ True,  True,  True,  True],
           [False, False, False, False],
           [False, False, False, False],
           [False, False, False, False]])




```python
x>=3
```




    array([False, False, False,  True,  True,  True,  True,  True,  True,
            True,  True,  True,  True,  True,  True,  True])




```python
x==3
```




    array([False, False, False,  True, False, False, False, False, False,
           False, False, False, False, False, False, False])




```python
2 * x == 24 - 4 * x
```




    array([False, False, False, False,  True, False, False, False, False,
           False, False, False, False, False, False, False])




```python
X
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
X < 6
```




    array([[ True,  True,  True,  True],
           [ True,  True, False, False],
           [False, False, False, False],
           [False, False, False, False]])




```python
x
```




    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])




```python
np.sum(x <=3)
```




    4




```python
# 只要有一个满足条件，就会返回true
np.any(x==0)
```




    True




```python
np.all(x>=0)
```




    True




```python
X
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
np.sum(X %2 ==0)
```




    8




```python
np.sum(X%2 ==0,axis = 0)
```




    array([4, 0, 4, 0])




```python
np.sum(X%2==0,axis = 1)
```




    array([2, 2, 2, 2])




```python
np.sum((x>3)&(x<10))
```




    6


