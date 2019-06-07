
## 岭回归
![](https://shirukai.gitee.io/images/860bd06f124bdab731e6109844e30712.jpg)
## LASSO Regression
![](https://shirukai.gitee.io/images/f90f7b158eb22cb2edf3d17523ea2682.jpg)
Least Absolute Shrinkage and Selection Operator Regression


```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
x = np.random.uniform(-3.0,3.0,size=100)
X = x.reshape(-1,1)
y = 0.5 * x + 3 + np.random.normal(0,1,size=100)

plt.scatter(x, y)
plt.show()
```


![](https://shirukai.gitee.io/images/387fc0a17126a3d1df5e22184bc35c41.jpg)



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


![](https://shirukai.gitee.io/images/9dce2320f1650f4b1e7be566a767e7df.jpg)


## LASSO


```python
from sklearn.linear_model import Lasso
```


```python
def LassoRegression(degree,alpha):
    return Pipeline([
        ("poly",PolynomialFeatures(degree=degree)),
        ("std_scaler",StandardScaler()),
        ("lasso_reg",Lasso(alpha=alpha))
    ])
```


```python
lasso1_reg = LassoRegression(20,0.01)
```


```python
lasso1_reg.fit(X_train,y_train)
```




    Pipeline(memory=None,
         steps=[('poly', PolynomialFeatures(degree=20, include_bias=True, interaction_only=False)), ('std_scaler', StandardScaler(copy=True, with_mean=True, with_std=True)), ('lasso_reg', Lasso(alpha=0.01, copy_X=True, fit_intercept=True, max_iter=1000,
       normalize=False, positive=False, precompute=False, random_state=None,
       selection='cyclic', tol=0.0001, warm_start=False))])




```python
y1_predict = lasso1_reg.predict(X_test)
```


```python
mean_squared_error(y_test,y1_predict)
```




    1.1496080843259966




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
plot_model(lasso1_reg)
```


![](https://shirukai.gitee.io/images/d3180efb0abdf563600c0233d90ec5d3.jpg)



```python
lasso2_reg = LassoRegression(20,0.1)
lasso2_reg.fit(X_train,y_train)
y2_predict = lasso2_reg.predict(X_test)
mean_squared_error(y_test,y2_predict)
```


    1.1213911351818648


```python
plot_model(lasso2_reg)
```


![](https://shirukai.gitee.io/images/a83f2b9919162fae575c20cf4e92002c.jpg)



```python
lasso3_reg = LassoRegression(20,1)
lasso3_reg.fit(X_train,y_train)
y3_predict = lasso3_reg.predict(X_test)
mean_squared_error(y_test,y3_predict)
```


    1.8408939659515595


```python
plot_model(lasso3_reg)
```


![](https://shirukai.gitee.io/images/ed8a1f3869b9c51f9b0812e43441ab50.jpg)


![](https://shirukai.gitee.io/images/1d87139c3f93d9165ca33c295ca41e22.jpg)

![](https://shirukai.gitee.io/images/0873bea64f44328eff9790f8fff35a26.jpg)
![](https://shirukai.gitee.io/images/9a97f2927ac379dca4800404fcd7e855.jpg)
![](https://shirukai.gitee.io/images/11676506ee8eb2be0aa43c097fa8aa03.jpg)
