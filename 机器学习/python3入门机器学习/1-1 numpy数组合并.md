

```python
import numpy as np
```


```python
x = np.array([1,2,3])
y = np.array([3,2,1])
```


```python
x
```




    array([1, 2, 3])




```python
y
```




    array([3, 2, 1])



x与y合并


```python
np.concatenate([x,y])
```




    array([1, 2, 3, 3, 2, 1])




```python
z = np.array([666,666,666])
```


```python
np.concatenate([x,y,z])
```




    array([  1,   2,   3,   3,   2,   1, 666, 666, 666])



基于矩阵的操作


```python
A = np.array([[1,2,3],
              [4,5,6]])
```


```python
np.concatenate([A,A])
```




    array([[1, 2, 3],
           [4, 5, 6],
           [1, 2, 3],
           [4, 5, 6]])




```python
np.concatenate([A,A],axis = 1)
```




    array([[1, 2, 3, 1, 2, 3],
           [4, 5, 6, 4, 5, 6]])




```python
np.concatenate([A,z])
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-14-abdc54b54f98> in <module>()
    ----> 1 np.concatenate([A,z])
    

    ValueError: all the input arrays must have same number of dimensions



```python
np.concatenate([A,z.reshape(1,-1)])
```




    array([[  1,   2,   3],
           [  4,   5,   6],
           [666, 666, 666]])




```python
A2 = np.concatenate([A,z.reshape(1,-1)])
```


```python
A2
```




    array([[  1,   2,   3],
           [  4,   5,   6],
           [666, 666, 666]])




```python
np.vstack([A,z])
```




    array([[  1,   2,   3],
           [  4,   5,   6],
           [666, 666, 666]])




```python
B = np.full((2,2),100)
```


```python
np.hstack([A,B])
```




    array([[  1,   2,   3, 100, 100],
           [  4,   5,   6, 100, 100]])



### 分割


```python
x = np.arange(10)
x
```




    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])



将x分别从位置3和位置7进行分割


```python
x1,x2,x3 = np.split(x,[3,7])
```


```python
x1
```




    array([0, 1, 2])




```python
x2
```




    array([3, 4, 5, 6])




```python
x1,x2 = np.split(x,[5])
```


```python
x1
```




    array([0, 1, 2, 3, 4])




```python
x2
```




    array([5, 6, 7, 8, 9])




```python
A = np.arange(16).reshape([4,4])
```


```python
A
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
A1,A2 = np.split(A,[2])
```


```python
A1
```




    array([[0, 1, 2, 3],
           [4, 5, 6, 7]])




```python
A2
```




    array([[ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
A1,A2 = np.split(A,[2],axis = 1)
```


```python
A1
```




    array([[ 0,  1],
           [ 4,  5],
           [ 8,  9],
           [12, 13]])




```python
A2
```




    array([[ 2,  3],
           [ 6,  7],
           [10, 11],
           [14, 15]])




```python
upper,lower = np.vsplit(A,[2])
```


```python
upper
```




    array([[0, 1, 2, 3],
           [4, 5, 6, 7]])




```python
lower
```




    array([[ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
left,right = np.hsplit(A,[2])
```


```python
left
```




    array([[ 0,  1],
           [ 4,  5],
           [ 8,  9],
           [12, 13]])




```python
right
```




    array([[ 2,  3],
           [ 6,  7],
           [10, 11],
           [14, 15]])




```python
data = np.arange(16).reshape((4,4))
```


```python
data
```




    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])




```python
x,y = np.hsplit(data,[-1])
```


```python
x
```




    array([[ 0,  1,  2],
           [ 4,  5,  6],
           [ 8,  9, 10],
           [12, 13, 14]])




```python
y
```




    array([[ 3],
           [ 7],
           [11],
           [15]])




```python
y[:,0]
```




    array([ 3,  7, 11, 15])


