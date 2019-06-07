#  OvR 与 OvO解决多分类



![](https://shirukai.gitee.io/images/3a3edaba1cdb382aa06019fd7e8e0ce4.jpg)
![](https://shirukai.gitee.io/images/af0c7ba97530ce83762fa9fcfc21d7d4.jpg)
![](https://shirukai.gitee.io/images/c54541865e379c096cc9301aa4f713d7.jpg)
![](https://shirukai.gitee.io/images/cab2ab5d89a392568e6eece7c8863349.jpg)

## OvR 和 OvO


```python
import numpy as np 
import matplotlib.pyplot as plt
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data[:,:2]
y = iris.target
```

    /Users/shirukai/anaconda3/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility. Expected 96, got 88
      return f(*args, **kwds)



```python
from sklearn.model_selection import train_test_split
X_train,X_test,y_tran,y_test = train_test_split(X,y,random_state=666)
```


```python
from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression()
log_reg.fit(X_train,y_tran)
```




    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False)




```python
log_reg.score(X_test,y_test)
```




    0.6578947368421053




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
plot_decision_boundary(log_reg,axis=[4,8.5,1.5,4.5])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.scatter(X[y==2,0],X[y==2,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)



![](https://shirukai.gitee.io/images/9fb3f5b89afc2101a71c3551d003db63.jpg)

```python
# ovo
log_reg2 = LogisticRegression(multi_class="multinomial",solver="newton-cg")
```


```python
log_reg2.fit(X_train,y_tran)
```


    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='multinomial',
              n_jobs=1, penalty='l2', random_state=None, solver='newton-cg',
              tol=0.0001, verbose=0, warm_start=False)




```python
log_reg2.score(X_test,y_test)
```




    0.7894736842105263




```python
plot_decision_boundary(log_reg2,axis=[4,8.5,1.5,4.5])
plt.scatter(X[y==0,0],X[y==0,1])
plt.scatter(X[y==1,0],X[y==1,1])
plt.scatter(X[y==2,0],X[y==2,1])
plt.show()
```

    /Users/shirukai/anaconda3/lib/python3.6/site-packages/matplotlib/contour.py:967: UserWarning: The following kwargs were not used by contour: 'linewidth'
      s)



![](https://shirukai.gitee.io/images/20d41353eb0b76f6b06229d187474a97.jpg)


## 使用所有数据


```python
X = iris.data
y = iris.target
```


```python
X_train,x_test,y_train,y_test = train_test_split(X,y,random_state=666)
```


```python
# 默认ovr
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)
```


    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False)


```python
log_reg.score(x_test,y_test)
```


    0.9473684210526315


```python
# 使用ovo
log_reg2 = LogisticRegression(multi_class="multinomial",solver="newton-cg")
log_reg2.fit(X_train,y_train)
```


    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='multinomial',
              n_jobs=1, penalty='l2', random_state=None, solver='newton-cg',
              tol=0.0001, verbose=0, warm_start=False)


```python
log_reg2.score(x_test,y_test)
```


    1.0

## OvO and OvR


```python
from sklearn.multiclass import OneVsRestClassifier
```


```python
ovr = OneVsRestClassifier(log_reg)
```


```python
ovr.fit(X_train,y_train)
ovr.score(x_test,y_test)
```


    0.9473684210526315


```python
from sklearn.multiclass import OneVsOneClassifier
```


```python
ovo = OneVsOneClassifier(log_reg)
```


```python
ovo.fit(X_train,y_train)
ovo.score(x_test,y_test)
```


    1.0


