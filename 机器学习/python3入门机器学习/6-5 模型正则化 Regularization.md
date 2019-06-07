# 模型正则化 Regularization

模型正则化：限制参数的大小
![](https://shirukai.gitee.io/images/3af7ce8e2f159117bb1cebf2f0e62974.jpg)

## 岭回归


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
np.random.seed(42)
x = np.random.uniform(-3.0,3.0,size=100)
X = x.reshape(-1,1)
y = 0.5 * x + 3 + np.random.normal(0,1,size=100)
```


```python
plt.scatter(x, y)
plt.show()
```


![](https://shirukai.gitee.io/images/1bea820fd1fdcf7430802b48740770b5.jpg)



```python
# 使用多项式回归

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
```


```python
def PolynomiaRegression(degree):
    return Pipeline([
        ("poly",PolynomialFeatures(degree=degree)),
        ("std_scaler",StandardScaler()),
        ("line_reg",LinearRegression())
    ])
```


```python
from sklearn.model_selection import train_test_split
np.random.seed(666)
X_train,X_test,y_train,y_test = train_test_split(X,y)
```


```python
from sklearn.metrics import mean_squared_error
poly_reg = PolynomiaRegression(degree=20)
poly_reg.fit(X_train,y_train) 
y_poly_predict = poly_reg.predict(X_test)
mean_squared_error(y_test,y_poly_predict)
```


    167.9401086729357


```python
X_plot = np.linspace(-3,3,100).reshape(100,1)
y_plot = poly_reg.predict(X_plot)
plt.scatter(x,y)
plt.plot(X_plot[:,0],y_plot,color='r')
plt.axis([-3,3,0,6])
plt.show()
```


![](https://shirukai.gitee.io/images/f7b0f5276758025b684c40f217113450.jpg)

```python
def plot_model(model):
    X_plot = np.linspace(-3,3,100).reshape(100,1)
    y_plot = model.predict(X_plot)
    
    plt.scatter(x,y)
    plt.plot(X_plot[:,0],y_plot,color='r')
    plt.axis([-3,3,0,6])
    plt.show()
```


```python
plot_model(poly_reg)
```


![](https://shirukai.gitee.io/images/e83794746d54a762f7e751c3ea93964e.jpg)


### 使用岭回归


```python
from sklearn.linear_model import Ridge

```


```python
def RidgeRegression(degree,alpha):
    return Pipeline([
        ("poly",PolynomialFeatures(degree=degree)),
        ("std_scaler",StandardScaler()),
        ("line_reg",Ridge(alpha=alpha))
    ])
```


```python
ridge1_reg = RidgeRegression(20,0.0001)
```


```python
ridge1_reg.fit(X_train,y_train)
y1_predict = ridge1_reg.predict(X_test)
```


```python
mean_squared_error(y_test,y1_predict)
```


    1.323349275406402


```python
plot_model(ridge1_reg)
```


![](https://shirukai.gitee.io/images/d80ab9bc9f179329461ff5cb37f6fbda.jpg)



```python
ridge2_reg = RidgeRegression(20,1)
ridge2_reg.fit(X_train,y_train)
y2_predict = ridge2_reg.predict(X_test)
mean_squared_error(y_test,y2_predict)
```


    1.1888759304218448


```python
plot_model(ridge2_reg)
```


![](https://shirukai.gitee.io/images/e8ef5dfbbd2542fc31fa94c3ce70b774.jpg)



```python
ridge3_reg = RidgeRegression(20,100)
ridge3_reg.fit(X_train,y_train)
y3_predict = ridge3_reg.predict(X_test)
mean_squared_error(y_test,y3_predict)
```


    1.3196456113086197


```python
plot_model(ridge3_reg)
```


![](https://shirukai.gitee.io/images/1c3855e34a5a7071461f0ba1eccb2bc9.jpg)

