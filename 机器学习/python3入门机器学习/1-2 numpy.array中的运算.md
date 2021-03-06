

```python
import numpy as np
```

给定一个向量，让向量中每一个数乘以2
a = (0,1,2)
a*2 = (0,2,4)

普通python中


```python
n = 10
```


```python
L = [i for i in range(n)]
```


```python
L
```




    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]




```python
2 * L
```




    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]




```python
A = []
for e in L:
    A.append(2*e)
```


```python
A
```




    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]




```python
n = 1000000
L = [i for i in range(n)]
```


```python
%%time
A = []
for e in L:
    A.append(2*e)
A    
```

    CPU times: user 175 ms, sys: 19.8 ms, total: 195 ms
    Wall time: 195 ms



```python
%%time
A = [2*e for e in L]
```

    CPU times: user 75.8 ms, sys: 24.4 ms, total: 100 ms
    Wall time: 99.8 ms


使用numpy


```python
L = np.arange(n)
```


```python
%%time
A = np.array(2*e for e in L)
```

    CPU times: user 11.4 ms, sys: 5.27 ms, total: 16.7 ms
    Wall time: 17 ms



```python
%%time
A = 2 * L
```

    CPU times: user 3.27 ms, sys: 3.95 ms, total: 7.22 ms
    Wall time: 5.48 ms



```python
A
```




    array([      0,       2,       4, ..., 1999994, 1999996, 1999998])




```python
n = 10 
L = np.arange(n)
2 * L
```




    array([ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18])



### Universal Functions


```python
X = np.arange(1,16).reshape((3,5))
X
```




    array([[ 1,  2,  3,  4,  5],
           [ 6,  7,  8,  9, 10],
           [11, 12, 13, 14, 15]])




```python
X + 1
```




    array([[ 2,  3,  4,  5,  6],
           [ 7,  8,  9, 10, 11],
           [12, 13, 14, 15, 16]])




```python
X - 1
```




    array([[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14]])




```python
X * 2
```




    array([[ 2,  4,  6,  8, 10],
           [12, 14, 16, 18, 20],
           [22, 24, 26, 28, 30]])




```python
# 浮点数除法
X / 2
```




    array([[0.5, 1. , 1.5, 2. , 2.5],
           [3. , 3.5, 4. , 4.5, 5. ],
           [5.5, 6. , 6.5, 7. , 7.5]])




```python
# 整数除法
X // 2
```




    array([[0, 1, 1, 2, 2],
           [3, 3, 4, 4, 5],
           [5, 6, 6, 7, 7]])




```python
# 乘方
X ** 2
```




    array([[  1,   4,   9,  16,  25],
           [ 36,  49,  64,  81, 100],
           [121, 144, 169, 196, 225]])




```python
# 取余
X % 2
```




    array([[1, 0, 1, 0, 1],
           [0, 1, 0, 1, 0],
           [1, 0, 1, 0, 1]])




```python
# 取倒数
1 / X
```




    array([[1.        , 0.5       , 0.33333333, 0.25      , 0.2       ],
           [0.16666667, 0.14285714, 0.125     , 0.11111111, 0.1       ],
           [0.09090909, 0.08333333, 0.07692308, 0.07142857, 0.06666667]])




```python
# 取绝对值
np.abs(X)
```




    array([[ 1,  2,  3,  4,  5],
           [ 6,  7,  8,  9, 10],
           [11, 12, 13, 14, 15]])




```python
# 取sin
np.sin(X)
```




    array([[ 0.84147098,  0.90929743,  0.14112001, -0.7568025 , -0.95892427],
           [-0.2794155 ,  0.6569866 ,  0.98935825,  0.41211849, -0.54402111],
           [-0.99999021, -0.53657292,  0.42016704,  0.99060736,  0.65028784]])




```python
# 取cos
np.cos(X)
```




    array([[ 0.54030231, -0.41614684, -0.9899925 , -0.65364362,  0.28366219],
           [ 0.96017029,  0.75390225, -0.14550003, -0.91113026, -0.83907153],
           [ 0.0044257 ,  0.84385396,  0.90744678,  0.13673722, -0.75968791]])




```python
# 取tan
np.tan(X)
```




    array([[ 1.55740772e+00, -2.18503986e+00, -1.42546543e-01,
             1.15782128e+00, -3.38051501e+00],
           [-2.91006191e-01,  8.71447983e-01, -6.79971146e+00,
            -4.52315659e-01,  6.48360827e-01],
           [-2.25950846e+02, -6.35859929e-01,  4.63021133e-01,
             7.24460662e+00, -8.55993401e-01]])




```python
# 取 e的x次方
np.exp(X)
```




    array([[2.71828183e+00, 7.38905610e+00, 2.00855369e+01, 5.45981500e+01,
            1.48413159e+02],
           [4.03428793e+02, 1.09663316e+03, 2.98095799e+03, 8.10308393e+03,
            2.20264658e+04],
           [5.98741417e+04, 1.62754791e+05, 4.42413392e+05, 1.20260428e+06,
            3.26901737e+06]])




```python
# 3的x次方
np.power(3,X)
```




    array([[       3,        9,       27,       81,      243],
           [     729,     2187,     6561,    19683,    59049],
           [  177147,   531441,  1594323,  4782969, 14348907]])




```python
3 **X
```




    array([[       3,        9,       27,       81,      243],
           [     729,     2187,     6561,    19683,    59049],
           [  177147,   531441,  1594323,  4782969, 14348907]])




```python
# 以e为底x的对数
np.log(X)
```




    array([[0.        , 0.69314718, 1.09861229, 1.38629436, 1.60943791],
           [1.79175947, 1.94591015, 2.07944154, 2.19722458, 2.30258509],
           [2.39789527, 2.48490665, 2.56494936, 2.63905733, 2.7080502 ]])




```python
np.log2(X)
```




    array([[0.        , 1.        , 1.5849625 , 2.        , 2.32192809],
           [2.5849625 , 2.80735492, 3.        , 3.169925  , 3.32192809],
           [3.45943162, 3.5849625 , 3.70043972, 3.80735492, 3.9068906 ]])




```python
np.log10(X)
```




    array([[0.        , 0.30103   , 0.47712125, 0.60205999, 0.69897   ],
           [0.77815125, 0.84509804, 0.90308999, 0.95424251, 1.        ],
           [1.04139269, 1.07918125, 1.11394335, 1.14612804, 1.17609126]])



### 矩阵运算


```python
A  = np.arange(4).reshape(2,2)
```


```python
B = np.full((2,2),10)
B
```




    array([[10, 10],
           [10, 10]])




```python
A + B
```




    array([[10, 11],
           [12, 13]])




```python
A-B
```




    array([[-10,  -9],
           [ -8,  -7]])




```python
# A和B对应元素的相乘，并不是矩阵相乘
A * B
```




    array([[ 0, 10],
           [20, 30]])




```python
# 矩阵相乘
# A中的每一行，和B中的每一列相乘再相加
A.dot(B)
```




    array([[10, 10],
           [50, 50]])




```python
# 矩阵的转置
# 行转列，列转行
A.T
```




    array([[0, 2],
           [1, 3]])




```python
C = np.full((3,3),6)
```


```python
C
```




    array([[6, 6, 6],
           [6, 6, 6],
           [6, 6, 6]])




```python
A.dot(C)
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-46-36f3f9c6ed4d> in <module>()
    ----> 1 A.dot(C)
    

    ValueError: shapes (2,2) and (3,3) not aligned: 2 (dim 1) != 3 (dim 0)


### 向量和矩阵运算


```python
v = np.array([1,2])
```


```python
v
```




    array([1, 2])




```python
A
```




    array([[0, 1],
           [2, 3]])




```python
# 数学上没有意义
v+A
```




    array([[1, 3],
           [3, 5]])




```python
np.vstack([v] * A.shape[0])+A
```




    array([[1, 3],
           [3, 5]])




```python
# tile 行堆叠两次，列堆叠一次
np.tile(v,(2,1)) +A
```




    array([[1, 3],
           [3, 5]])




```python
v
```




    array([1, 2])




```python
A
```




    array([[0, 1],
           [2, 3]])




```python
v * A
```




    array([[0, 2],
           [2, 6]])




```python
v.dot(A)
```




    array([4, 7])




```python
A.dot(v)
```




    array([2, 8])



### 矩阵的逆


```python
A
```




    array([[0, 1],
           [2, 3]])




```python
np.linalg.inv(A)
```




    array([[-1.5,  0.5],
           [ 1. ,  0. ]])




```python
invA = np.linalg.inv(A)
```


```python
# 矩阵乘以它的逆矩阵得到的是单位矩阵，对角线为1
# 方阵才有逆矩阵
A.dot(invA)
```




    array([[1., 0.],
           [0., 1.]])




```python
invA.dot(A)
```




    array([[1., 0.],
           [0., 1.]])




```python
# 伪逆矩阵
X = np.arange(16).reshape(2,8)
pinvX = np.linalg.pinv(X)
pinvX
```




    array([[-1.35416667e-01,  5.20833333e-02],
           [-1.01190476e-01,  4.16666667e-02],
           [-6.69642857e-02,  3.12500000e-02],
           [-3.27380952e-02,  2.08333333e-02],
           [ 1.48809524e-03,  1.04166667e-02],
           [ 3.57142857e-02, -1.04083409e-17],
           [ 6.99404762e-02, -1.04166667e-02],
           [ 1.04166667e-01, -2.08333333e-02]])




```python
pinvX.shape
```




    (8, 2)




```python
X.dot(pinvX)
```




    array([[ 1.00000000e+00, -2.49800181e-16],
           [ 0.00000000e+00,  1.00000000e+00]])


