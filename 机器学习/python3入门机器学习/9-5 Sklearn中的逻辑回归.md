
## 逻辑回归中使用正则化

![](https://shirukai.gitee.io/images/57e7ac7799a8022219a8cfde71af1989.jpg)
## scikit-learn中的逻辑回归


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
np.random.seed(666)
```


```python
X = np.random.normal(0,1,size=(200,2))
y = np.array(X[:,0]**2 + X[:,1] < 1.5,dtype='int')
for _ in range(20):
    y[np.random.randint(200)] = 1
```


```python
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.show()
```


![](https://shirukai.gitee.io/images/d084395beabee730624bb8ecbe25b16d.jpg)



```python
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=666)
```


```python
# 使用逻辑回归
from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)
```




    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False)




```python
log_reg.score(X_train,y_train)
```




    0.7933333333333333




```python
log_reg.score(X_test,y_test)
```




    0.86




```python
def plot_decision_boundary(model, axis): 
    x0, x1 = np.meshgrid( 
        np.linspace(axis[0], axis[1], int((axis[1]-axis[0])*100)).reshape(-1, 1),
        np.linspace(axis[2], axis[3], int((axis[3]-axis[2])*100)).reshape(-1, 1), ) 
    X_new = np.c_[x0.ravel(), x1.ravel()] 
    y_predict = model.predict(X_new) 
    zz = y_predict.reshape(x0.shape) 
    from matplotlib.colors import ListedColormap 
    custom_cmap = ListedColormap(['#EF9A9A','#FFF59D','#90CAF9']) 
    plt.contourf(x0, x1, zz, linewidth=5, cmap=custom_cmap)
```


```python
plot_decision_boundary(log_reg,axis=[-4,4,-4,4])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)



![](https://shirukai.gitee.io/images/2cde531475487820e3a079803db477f2.jpg)

```python
# 使用多项式逻辑回归
```


```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
def PolynomialLogisticRegression(degree):
    return Pipeline([
        ('poly',PolynomialFeatures(degree)),
        ('std_scaler',StandardScaler()),
        ('log_reg',LogisticRegression())
    ])
```


```python
ploy_log_reg = PolynomialLogisticRegression(degree=2)
ploy_log_reg.fit(X_train,y_train)
```


    Pipeline(memory=None,
         steps=[('poly', PolynomialFeatures(degree=2, include_bias=True, interaction_only=False)), ('std_scaler', StandardScaler(copy=True, with_mean=True, with_std=True)), ('log_reg', LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False))])




```python
ploy_log_reg.score(X_train,y_train)
```




    0.9133333333333333




```python
plot_decision_boundary(ploy_log_reg,axis=[-4,4,-4,4])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)

![](https://shirukai.gitee.io/images/aee243e3c542c35c80893d04eac4617e.jpg)



```python
ploy_log_reg2 = PolynomialLogisticRegression(degree=20)
ploy_log_reg2.fit(X_train,y_train)
```


    Pipeline(memory=None,
         steps=[('poly', PolynomialFeatures(degree=20, include_bias=True, interaction_only=False)), ('std_scaler', StandardScaler(copy=True, with_mean=True, with_std=True)), ('log_reg', LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False))])


```python
plot_decision_boundary(ploy_log_reg2,axis=[-4,4,-4,4])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)



![](https://shirukai.gitee.io/images/b388663e7603abf68d596efee909786b.jpg)



```python
def PolynomialLogisticRegression(degree,C):
    return Pipeline([
        ('poly',PolynomialFeatures(degree)),
        ('std_scaler',StandardScaler()),
        ('log_reg',LogisticRegression(C=C))
    ])
```


```python
ploy_log_reg3 = PolynomialLogisticRegression(degree=20,C=0.1)
ploy_log_reg3.fit(X_train,y_train)
```




    Pipeline(memory=None,
         steps=[('poly', PolynomialFeatures(degree=20, include_bias=True, interaction_only=False)), ('std_scaler', StandardScaler(copy=True, with_mean=True, with_std=True)), ('log_reg', LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False))])




```python
ploy_log_reg3.score(X_train,y_train)
```




    0.8533333333333334




```python
ploy_log_reg3.score(X_test,y_test)
```




    0.92




```python
plot_decision_boundary(ploy_log_reg3,axis=[-4,4,-4,4])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)



![](https://shirukai.gitee.io/images/b59916744f56d4719b9f40d9c22f6a39.jpg)



```python
def PolynomialLogisticRegression(degree,C,penalty='l2'):
    return Pipeline([
        ('poly',PolynomialFeatures(degree)),
        ('std_scaler',StandardScaler()),
        ('log_reg',LogisticRegression(C=C,penalty=penalty))
    ])
```


```python
ploy_log_reg4 = PolynomialLogisticRegression(degree=20,C=0.1,penalty="l1")
ploy_log_reg4.fit(X_train,y_train)
```




    Pipeline(memory=None,
         steps=[('poly', PolynomialFeatures(degree=20, include_bias=True, interaction_only=False)), ('std_scaler', StandardScaler(copy=True, with_mean=True, with_std=True)), ('log_reg', LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l1', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False))])


```python
ploy_log_reg4.score(X_train,y_train)
```


    0.8266666666666667


```python
ploy_log_reg4.score(X_test,y_test)
```


    0.9


```python
plot_decision_boundary(ploy_log_reg4,axis=[-4,4,-4,4])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)

![](https://shirukai.gitee.io/images/d748ea447d0d885025fdd35671ed9c2a.jpg)

