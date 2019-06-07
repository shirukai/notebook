# 实现Simple Linear Regression

```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
x = np.array([1.,2.,3.,4.,5.])
y = np.array([1.,3.,2.,3.,5.])
```


```python
plt.scatter(x,y)
plt.axis([0,6,0,6])
plt.show()
```


![](https://shirukai.gitee.io/images/67742323850bc45c95548d86b1a6a259.jpg)

```python
# x的均值
x_mean = np.mean(x)
# y的均值
y_mean = np.mean(y)
```


```python
# 定义分子
num = 0.0
# 定义分母
d = 0.0

for x_i,y_i in zip(x,y):
    num += (x_i - x_mean) * (y_i - y_mean)
    d += (x_i -x_mean) ** 2 
```


```python
a = num/d
b = y_mean-a*x_mean
```


```python
a
```


    0.8


```python
b
```


    0.39999999999999947


```python
y_hat = a * x +b

plt.scatter(x,y)
plt.plot(x,y_hat,color="r")
plt.axis([0,6,0,6])
plt.show()
```


![](https://shirukai.gitee.io/images/555b5d041e471c3a9e3c9b4750b91331.jpg)



```python
x_predict = 6
y_predict = a * x_predict + b 
```


```python
y_predict
```


    5.2



### 使用我们自己的SimpleLinearRegression


```python
from script.SimpleLinearRegression import SimpleLinearRegression1

reg1 = SimpleLinearRegression1()
reg1.fit(x,y)
```


    SimpleLinearRegression1()


```python
reg1.predict(np.array([x_predict]))
```


    array([5.2])


```python
reg1.a_
```


    0.8


```python
reg1.b_
```


    0.39999999999999947


```python
y_hat1 = reg1.predict(x)
```


```python
plt.scatter(x,y)
plt.plot(x,y_hat1,color="r")
plt.axis([0,6,0,6])
plt.show()
```


![](https://shirukai.gitee.io/images/67955b2cdccdec5bf12ed2e66977c05e.jpg)


### 向量化实现SimpleLinearRegression


```python
from script.SimpleLinearRegression import SimpleLinearRegression2
```


```python
reg2 = SimpleLinearRegression2()
```


```python
reg2.fit(x,y)
```


    SimpleLinearRegression2()


```python
reg2.a_
```


    0.8


```python
reg2.b_
```


    0.39999999999999947




```python
y_hat2 = reg1.predict(x)
plt.scatter(x,y)
plt.plot(x,y_hat2,color="r")
plt.axis([0,6,0,6])
plt.show()
```


![](https://shirukai.gitee.io/images/e3ce36da023f07ed5842367bbe12a9e1.jpg)


### 向量化实现的性能测试


```python
m = 1000000
big_x = np.random.random(size=m)
big_y = big_x * 2.0 + 3.0 + np.random.normal(size=m)
```


```python
%timeit reg1.fit(big_x,big_y)
%timeit reg2.fit(big_x,big_y)
```

    910 ms ± 7.69 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    20.5 ms ± 1.04 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)

```python
reg1.a_
```


    1.9896828127473971


```python
reg1.b_
```


    3.0065742729200817


