

```python
import numpy as np
from sklearn import datasets
```


```python
digits = datasets.load_digits()
```


```python
X = digits.data
```


```python
y = digits.target
```


```python
from sklearn.model_selection import train_test_split
```


```python
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=666)
```


```python
from sklearn.neighbors import KNeighborsClassifier
knn_clf = KNeighborsClassifier(n_neighbors=3)
knn_clf.fit(X_train,y_train)
knn_clf.score(X_test,y_test)
```




    0.9888888888888889



## 超参数和模型参数

* 超参数：在算法运行前需要决定的参数
* 模型参数： 算法过程中学习的参数

KNN算法没有模型参数、kNN算法中的k是典型的超参数

## 寻找好的超参数
* 领域知识
* 经验数值
* 实验搜索

### 寻找最好的K


```python
best_score = 0.0
besk_k = -1
for k in range(1,11):
    knn_clf = KNeighborsClassifier(n_neighbors=k)
    knn_clf.fit(X_train,y_train)
    score = knn_clf.score(X_test,y_test)
    if score > best_score:
        besk_k = k
        best_score = score
print("best_k=",besk_k)
print("best_score=",best_score)
```

    best_k= 4
    best_score= 0.9916666666666667


### 考虑距离？不考虑距离？


```python
best_method= ""
best_score = 0.0
besk_k = -1
for method in ["uniform","distance"]:
    for k in range(1,11):
        knn_clf = KNeighborsClassifier(n_neighbors=k,weights=method)
        knn_clf.fit(X_train,y_train)
        score = knn_clf.score(X_test,y_test)
        if score > best_score:
            besk_k = k
            best_score = score
            best_method = method
print("best_k=",besk_k)
print("best_score=",best_score)
print("bset_method=",best_method)
```

    best_k= 4
    best_score= 0.9916666666666667
    bset_method= uniform


### 搜索明科夫斯基距离相应的p


```python
%%time
best_p = -1
best_score = 0.0
besk_k = -1
for k in range(1,11):
    for p in range(1,11):
        knn_clf = KNeighborsClassifier(n_neighbors=k,weights="distance",p=p)
        knn_clf.fit(X_train,y_train)
        score = knn_clf.score(X_test,y_test)
        if score > best_score:
            besk_k = k
            best_score = score
            best_p = p
print("best_k=",besk_k)
print("best_score=",best_score)
print("bset_p=",best_p)
```

    best_k= 3
    best_score= 0.9888888888888889
    bset_p= 2
    CPU times: user 44.4 s, sys: 556 ms, total: 45 s
    Wall time: 45.8 s


### 网格搜索


```python
param_grid = [
    {
        'weights':['uniform'],
        'n_neighbors':[i for i in range(1,11)]
    },
    {
        'weights':['distance'],
        'n_neighbors':[i for i in range(1,11)],
        'p':[i for i in range(1,6)]
    }
]
```


```python
knn_clf = KNeighborsClassifier()
```


```python
from sklearn.model_selection import GridSearchCV
```


```python
grid_search = GridSearchCV(knn_clf,param_grid)
```


```python
%%time
grid_search.fit(X_train,y_train)
```

    CPU times: user 2min 27s, sys: 2.01 s, total: 2min 29s
    Wall time: 2min 33s





    GridSearchCV(cv=None, error_score='raise',
           estimator=KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=5, p=2,
               weights='uniform'),
           fit_params=None, iid=True, n_jobs=1,
           param_grid=[{'weights': ['uniform'], 'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}, {'weights': ['distance'], 'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'p': [1, 2, 3, 4, 5]}],
           pre_dispatch='2*n_jobs', refit=True, return_train_score='warn',
           scoring=None, verbose=0)




```python
grid_search.best_estimator_
```




    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=3, p=3,
               weights='distance')




```python
grid_search.best_score_
```




    0.9853862212943633




```python
grid_search.best_params_
```




    {'n_neighbors': 3, 'p': 3, 'weights': 'distance'}




```python
knn_clf = grid_search.best_estimator_
```


```python
knn_clf.predict(X_test)
```




    array([8, 1, 3, 4, 4, 0, 7, 0, 8, 0, 4, 6, 1, 1, 2, 0, 1, 6, 7, 3, 3, 6,
           5, 2, 9, 4, 0, 2, 0, 3, 0, 8, 7, 2, 3, 5, 1, 3, 1, 5, 8, 6, 2, 6,
           3, 1, 3, 0, 0, 4, 9, 9, 2, 8, 7, 0, 5, 4, 0, 9, 5, 5, 8, 7, 4, 2,
           8, 8, 7, 5, 4, 3, 0, 2, 7, 2, 1, 2, 4, 0, 9, 0, 6, 6, 2, 0, 0, 5,
           4, 4, 3, 1, 3, 8, 6, 4, 4, 7, 5, 6, 8, 4, 8, 4, 6, 9, 7, 7, 0, 8,
           8, 3, 9, 7, 1, 8, 4, 2, 7, 0, 0, 4, 9, 6, 7, 3, 4, 6, 4, 8, 4, 7,
           2, 6, 9, 5, 8, 7, 2, 5, 5, 9, 7, 9, 3, 1, 9, 4, 4, 1, 5, 1, 6, 4,
           4, 8, 1, 6, 2, 5, 2, 1, 4, 4, 3, 9, 4, 0, 6, 0, 8, 3, 8, 7, 3, 0,
           3, 0, 5, 9, 2, 7, 1, 8, 1, 4, 3, 3, 7, 8, 2, 7, 2, 2, 8, 0, 5, 7,
           6, 7, 3, 4, 7, 1, 7, 0, 9, 2, 8, 9, 3, 8, 9, 1, 1, 1, 9, 8, 8, 0,
           3, 7, 3, 3, 4, 8, 2, 1, 8, 6, 0, 1, 7, 7, 5, 8, 3, 8, 7, 6, 8, 4,
           2, 6, 2, 3, 7, 4, 9, 3, 5, 0, 6, 3, 8, 3, 3, 1, 4, 5, 3, 2, 5, 6,
           9, 6, 9, 5, 5, 3, 6, 5, 9, 3, 7, 7, 0, 2, 4, 9, 9, 9, 2, 5, 6, 1,
           9, 6, 9, 7, 7, 4, 5, 0, 0, 5, 3, 8, 4, 4, 3, 2, 5, 3, 2, 2, 3, 0,
           9, 8, 2, 1, 4, 0, 6, 2, 8, 0, 6, 4, 9, 9, 8, 3, 9, 8, 6, 3, 2, 7,
           9, 4, 2, 7, 5, 1, 1, 6, 1, 0, 4, 9, 2, 9, 0, 3, 3, 0, 7, 4, 8, 5,
           9, 5, 9, 5, 0, 7, 9, 8])




```python
knn_clf.score(X_test,y_test)
```




    0.9833333333333333




```python
%%time
# n_jobs 运行核数，-1代表全部使用
# verbose日志输入
grid_search = GridSearchCV(knn_clf,param_grid,n_jobs=-1,verbose=2)
grid_search.fit(X_train,y_train)
```

    Fitting 3 folds for each of 60 candidates, totalling 180 fits
    [CV] n_neighbors=1, weights=uniform ..................................
    [CV] n_neighbors=1, weights=uniform ..................................
    [CV] n_neighbors=1, weights=uniform ..................................
    [CV] n_neighbors=2, weights=uniform ..................................
    [CV] ................... n_neighbors=1, weights=uniform, total=   0.8s
    [CV] n_neighbors=2, weights=uniform ..................................
    [CV] ................... n_neighbors=1, weights=uniform, total=   0.9s
    [CV] n_neighbors=2, weights=uniform ..................................
    [CV] ................... n_neighbors=1, weights=uniform, total=   1.0s
    [CV] n_neighbors=3, weights=uniform ..................................
    [CV] ................... n_neighbors=2, weights=uniform, total=   1.0s
    [CV] n_neighbors=3, weights=uniform ..................................
    [CV] ................... n_neighbors=2, weights=uniform, total=   0.9s
    [CV] n_neighbors=3, weights=uniform ..................................
    [CV] ................... n_neighbors=2, weights=uniform, total=   1.0s
    [CV] n_neighbors=4, weights=uniform ..................................
    [CV] ................... n_neighbors=3, weights=uniform, total=   1.1s
    [CV] n_neighbors=4, weights=uniform ..................................
    [CV] ................... n_neighbors=3, weights=uniform, total=   1.0s
    [CV] n_neighbors=4, weights=uniform ..................................
    [CV] ................... n_neighbors=3, weights=uniform, total=   0.9s
    [CV] n_neighbors=5, weights=uniform ..................................
    [CV] ................... n_neighbors=4, weights=uniform, total=   1.0s
    [CV] n_neighbors=5, weights=uniform ..................................
    [CV] ................... n_neighbors=4, weights=uniform, total=   1.0s
    [CV] n_neighbors=5, weights=uniform ..................................
    [CV] ................... n_neighbors=4, weights=uniform, total=   1.0s
    [CV] n_neighbors=6, weights=uniform ..................................
    [CV] ................... n_neighbors=5, weights=uniform, total=   1.2s
    [CV] n_neighbors=6, weights=uniform ..................................
    [CV] ................... n_neighbors=5, weights=uniform, total=   1.1s
    [CV] n_neighbors=6, weights=uniform ..................................
    [CV] ................... n_neighbors=5, weights=uniform, total=   1.1s
    [CV] n_neighbors=7, weights=uniform ..................................
    [CV] ................... n_neighbors=6, weights=uniform, total=   1.0s
    [CV] n_neighbors=7, weights=uniform ..................................
    [CV] ................... n_neighbors=6, weights=uniform, total=   1.1s
    [CV] n_neighbors=7, weights=uniform ..................................
    [CV] ................... n_neighbors=6, weights=uniform, total=   1.1s
    [CV] n_neighbors=8, weights=uniform ..................................
    [CV] ................... n_neighbors=7, weights=uniform, total=   1.1s
    [CV] n_neighbors=8, weights=uniform ..................................
    [CV] ................... n_neighbors=7, weights=uniform, total=   1.3s
    [CV] n_neighbors=8, weights=uniform ..................................
    [CV] ................... n_neighbors=7, weights=uniform, total=   1.2s
    [CV] n_neighbors=9, weights=uniform ..................................
    [CV] ................... n_neighbors=8, weights=uniform, total=   1.1s
    [CV] n_neighbors=9, weights=uniform ..................................
    [CV] ................... n_neighbors=8, weights=uniform, total=   1.0s
    [CV] n_neighbors=9, weights=uniform ..................................
    [CV] ................... n_neighbors=8, weights=uniform, total=   1.2s
    [CV] n_neighbors=10, weights=uniform .................................
    [CV] ................... n_neighbors=9, weights=uniform, total=   1.2s
    [CV] n_neighbors=10, weights=uniform .................................
    [CV] ................... n_neighbors=9, weights=uniform, total=   1.1s
    [CV] n_neighbors=10, weights=uniform .................................
    [CV] ................... n_neighbors=9, weights=uniform, total=   1.0s
    [CV] n_neighbors=1, p=1, weights=distance ............................
    [CV] ............. n_neighbors=1, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=1, p=1, weights=distance ............................
    [CV] ............. n_neighbors=1, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=1, p=1, weights=distance ............................
    [CV] ............. n_neighbors=1, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=1, p=2, weights=distance ............................
    [CV] ............. n_neighbors=1, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=1, p=2, weights=distance ............................
    [CV] ............. n_neighbors=1, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=1, p=2, weights=distance ............................
    [CV] ............. n_neighbors=1, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=1, p=3, weights=distance ............................


    [Parallel(n_jobs=-1)]: Done  33 tasks      | elapsed:   21.3s


    [CV] .................. n_neighbors=10, weights=uniform, total=   1.2s
    [CV] n_neighbors=1, p=3, weights=distance ............................
    [CV] ............. n_neighbors=1, p=3, weights=distance, total=   0.9s
    [CV] n_neighbors=1, p=3, weights=distance ............................
    [CV] .................. n_neighbors=10, weights=uniform, total=   1.1s
    [CV] n_neighbors=1, p=4, weights=distance ............................
    [CV] .................. n_neighbors=10, weights=uniform, total=   1.0s
    [CV] n_neighbors=1, p=4, weights=distance ............................
    [CV] ............. n_neighbors=1, p=3, weights=distance, total=   0.9s
    [CV] n_neighbors=1, p=4, weights=distance ............................
    [CV] ............. n_neighbors=1, p=3, weights=distance, total=   0.7s
    [CV] n_neighbors=1, p=5, weights=distance ............................
    [CV] ............. n_neighbors=1, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=1, p=5, weights=distance ............................
    [CV] ............. n_neighbors=1, p=4, weights=distance, total=   0.6s
    [CV] n_neighbors=1, p=5, weights=distance ............................
    [CV] ............. n_neighbors=1, p=4, weights=distance, total=   0.8s
    [CV] n_neighbors=2, p=1, weights=distance ............................
    [CV] ............. n_neighbors=2, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=2, p=1, weights=distance ............................
    [CV] ............. n_neighbors=1, p=5, weights=distance, total=   0.8s
    [CV] n_neighbors=2, p=1, weights=distance ............................
    [CV] ............. n_neighbors=2, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=2, p=2, weights=distance ............................
    [CV] ............. n_neighbors=2, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=2, p=2, weights=distance ............................
    [CV] ............. n_neighbors=2, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=2, p=2, weights=distance ............................
    [CV] ............. n_neighbors=1, p=5, weights=distance, total=   0.8s
    [CV] n_neighbors=2, p=3, weights=distance ............................
    [CV] ............. n_neighbors=2, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=2, p=3, weights=distance ............................
    [CV] ............. n_neighbors=1, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=2, p=3, weights=distance ............................
    [CV] ............. n_neighbors=2, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=2, p=4, weights=distance ............................
    [CV] ............. n_neighbors=2, p=3, weights=distance, total=   0.9s
    [CV] n_neighbors=2, p=4, weights=distance ............................
    [CV] ............. n_neighbors=2, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=2, p=4, weights=distance ............................
    [CV] ............. n_neighbors=2, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=2, p=5, weights=distance ............................
    [CV] ............. n_neighbors=2, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=2, p=5, weights=distance ............................
    [CV] ............. n_neighbors=2, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=2, p=5, weights=distance ............................
    [CV] ............. n_neighbors=2, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=3, p=1, weights=distance ............................
    [CV] ............. n_neighbors=2, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=3, p=1, weights=distance ............................
    [CV] ............. n_neighbors=3, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=3, p=1, weights=distance ............................
    [CV] ............. n_neighbors=2, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=3, p=2, weights=distance ............................
    [CV] ............. n_neighbors=3, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=3, p=2, weights=distance ............................
    [CV] ............. n_neighbors=3, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=3, p=2, weights=distance ............................
    [CV] ............. n_neighbors=3, p=1, weights=distance, total=   0.2s
    [CV] n_neighbors=3, p=3, weights=distance ............................
    [CV] ............. n_neighbors=3, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=3, p=3, weights=distance ............................
    [CV] ............. n_neighbors=3, p=2, weights=distance, total=   0.2s
    [CV] n_neighbors=3, p=3, weights=distance ............................
    [CV] ............. n_neighbors=2, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=3, p=4, weights=distance ............................
    [CV] ............. n_neighbors=3, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=3, p=4, weights=distance ............................
    [CV] ............. n_neighbors=3, p=3, weights=distance, total=   1.2s
    [CV] n_neighbors=3, p=4, weights=distance ............................
    [CV] ............. n_neighbors=3, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=3, p=5, weights=distance ............................
    [CV] ............. n_neighbors=3, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=3, p=5, weights=distance ............................
    [CV] ............. n_neighbors=3, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=3, p=5, weights=distance ............................
    [CV] ............. n_neighbors=3, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=4, p=1, weights=distance ............................
    [CV] ............. n_neighbors=3, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=4, p=1, weights=distance ............................
    [CV] ............. n_neighbors=4, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=4, p=1, weights=distance ............................
    [CV] ............. n_neighbors=4, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=4, p=2, weights=distance ............................
    [CV] ............. n_neighbors=4, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=4, p=2, weights=distance ............................
    [CV] ............. n_neighbors=4, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=4, p=2, weights=distance ............................
    [CV] ............. n_neighbors=4, p=2, weights=distance, total=   0.2s
    [CV] n_neighbors=4, p=3, weights=distance ............................
    [CV] ............. n_neighbors=4, p=2, weights=distance, total=   0.2s
    [CV] n_neighbors=4, p=3, weights=distance ............................
    [CV] ............. n_neighbors=3, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=4, p=3, weights=distance ............................
    [CV] ............. n_neighbors=3, p=5, weights=distance, total=   1.2s
    [CV] n_neighbors=4, p=4, weights=distance ............................
    [CV] ............. n_neighbors=4, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=4, p=4, weights=distance ............................
    [CV] ............. n_neighbors=4, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=4, p=4, weights=distance ............................
    [CV] ............. n_neighbors=4, p=3, weights=distance, total=   0.9s
    [CV] n_neighbors=4, p=5, weights=distance ............................
    [CV] ............. n_neighbors=4, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=4, p=5, weights=distance ............................
    [CV] ............. n_neighbors=4, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=4, p=5, weights=distance ............................
    [CV] ............. n_neighbors=4, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=5, p=1, weights=distance ............................
    [CV] ............. n_neighbors=5, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=5, p=1, weights=distance ............................
    [CV] ............. n_neighbors=5, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=5, p=1, weights=distance ............................
    [CV] ............. n_neighbors=4, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=5, p=2, weights=distance ............................
    [CV] ............. n_neighbors=5, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=5, p=2, weights=distance ............................
    [CV] ............. n_neighbors=5, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=5, p=2, weights=distance ............................
    [CV] ............. n_neighbors=5, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=5, p=3, weights=distance ............................
    [CV] ............. n_neighbors=4, p=5, weights=distance, total=   0.8s
    [CV] n_neighbors=5, p=3, weights=distance ............................
    [CV] ............. n_neighbors=5, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=5, p=3, weights=distance ............................
    [CV] ............. n_neighbors=4, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=5, p=4, weights=distance ............................
    [CV] ............. n_neighbors=5, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=5, p=4, weights=distance ............................
    [CV] ............. n_neighbors=5, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=5, p=4, weights=distance ............................
    [CV] ............. n_neighbors=5, p=3, weights=distance, total=   0.9s
    [CV] n_neighbors=5, p=5, weights=distance ............................
    [CV] ............. n_neighbors=5, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=5, p=5, weights=distance ............................
    [CV] ............. n_neighbors=5, p=4, weights=distance, total=   0.9s
    [CV] n_neighbors=5, p=5, weights=distance ............................
    [CV] ............. n_neighbors=5, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=6, p=1, weights=distance ............................
    [CV] ............. n_neighbors=5, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=6, p=1, weights=distance ............................
    [CV] ............. n_neighbors=6, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=6, p=1, weights=distance ............................
    [CV] ............. n_neighbors=6, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=6, p=2, weights=distance ............................
    [CV] ............. n_neighbors=6, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=6, p=2, weights=distance ............................
    [CV] ............. n_neighbors=6, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=6, p=2, weights=distance ............................
    [CV] ............. n_neighbors=6, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=6, p=3, weights=distance ............................
    [CV] ............. n_neighbors=6, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=6, p=3, weights=distance ............................
    [CV] ............. n_neighbors=5, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=6, p=3, weights=distance ............................
    [CV] ............. n_neighbors=5, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=6, p=4, weights=distance ............................
    [CV] ............. n_neighbors=6, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=6, p=4, weights=distance ............................
    [CV] ............. n_neighbors=6, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=6, p=4, weights=distance ............................
    [CV] ............. n_neighbors=6, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=6, p=5, weights=distance ............................
    [CV] ............. n_neighbors=6, p=4, weights=distance, total=   1.1s
    [CV] n_neighbors=6, p=5, weights=distance ............................
    [CV] ............. n_neighbors=6, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=6, p=5, weights=distance ............................
    [CV] ............. n_neighbors=6, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=1, weights=distance ............................
    [CV] ............. n_neighbors=6, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=1, weights=distance ............................
    [CV] ............. n_neighbors=7, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=7, p=1, weights=distance ............................
    [CV] ............. n_neighbors=7, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=7, p=2, weights=distance ............................
    [CV] ............. n_neighbors=7, p=1, weights=distance, total=   0.2s
    [CV] n_neighbors=7, p=2, weights=distance ............................
    [CV] ............. n_neighbors=7, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=7, p=2, weights=distance ............................
    [CV] ............. n_neighbors=7, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=7, p=3, weights=distance ............................
    [CV] ............. n_neighbors=7, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=7, p=3, weights=distance ............................
    [CV] ............. n_neighbors=6, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=3, weights=distance ............................
    [CV] ............. n_neighbors=6, p=5, weights=distance, total=   1.1s
    [CV] n_neighbors=7, p=4, weights=distance ............................
    [CV] ............. n_neighbors=7, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=4, weights=distance ............................
    [CV] ............. n_neighbors=7, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=4, weights=distance ............................
    [CV] ............. n_neighbors=7, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=5, weights=distance ............................
    [CV] ............. n_neighbors=7, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=5, weights=distance ............................
    [CV] ............. n_neighbors=7, p=4, weights=distance, total=   1.0s
    [CV] ............. n_neighbors=7, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=7, p=5, weights=distance ............................
    [CV] n_neighbors=8, p=1, weights=distance ............................
    [CV] ............. n_neighbors=8, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=8, p=1, weights=distance ............................
    [CV] ............. n_neighbors=8, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=8, p=1, weights=distance ............................
    [CV] ............. n_neighbors=7, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=8, p=2, weights=distance ............................
    [CV] ............. n_neighbors=8, p=1, weights=distance, total=   0.1s
    [CV] ............. n_neighbors=8, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=8, p=2, weights=distance ............................
    [CV] n_neighbors=8, p=2, weights=distance ............................
    [CV] ............. n_neighbors=8, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=8, p=3, weights=distance ............................
    [CV] ............. n_neighbors=8, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=8, p=3, weights=distance ............................
    [CV] ............. n_neighbors=7, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=8, p=3, weights=distance ............................
    [CV] ............. n_neighbors=7, p=5, weights=distance, total=   0.9s
    [CV] n_neighbors=8, p=4, weights=distance ............................
    [CV] ............. n_neighbors=8, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=8, p=4, weights=distance ............................
    [CV] ............. n_neighbors=8, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=8, p=4, weights=distance ............................
    [CV] ............. n_neighbors=8, p=3, weights=distance, total=   0.9s
    [CV] n_neighbors=8, p=5, weights=distance ............................
    [CV] ............. n_neighbors=8, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=8, p=5, weights=distance ............................
    [CV] ............. n_neighbors=8, p=4, weights=distance, total=   1.1s
    [CV] ............. n_neighbors=8, p=4, weights=distance, total=   1.2s
    [CV] n_neighbors=8, p=5, weights=distance ............................
    [CV] n_neighbors=9, p=1, weights=distance ............................
    [CV] ............. n_neighbors=9, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=9, p=1, weights=distance ............................
    [CV] ............. n_neighbors=8, p=5, weights=distance, total=   1.1s
    [CV] n_neighbors=9, p=1, weights=distance ............................
    [CV] ............. n_neighbors=9, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=9, p=2, weights=distance ............................
    [CV] ............. n_neighbors=9, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=9, p=2, weights=distance ............................
    [CV] ............. n_neighbors=9, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=9, p=2, weights=distance ............................
    [CV] ............. n_neighbors=9, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=9, p=3, weights=distance ............................
    [CV] ............. n_neighbors=9, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=9, p=3, weights=distance ............................


    [Parallel(n_jobs=-1)]: Done 154 tasks      | elapsed:  1.2min


    [CV] ............. n_neighbors=8, p=5, weights=distance, total=   1.1s
    [CV] n_neighbors=9, p=3, weights=distance ............................
    [CV] ............. n_neighbors=8, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=9, p=4, weights=distance ............................
    [CV] ............. n_neighbors=9, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=9, p=4, weights=distance ............................
    [CV] ............. n_neighbors=9, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=9, p=4, weights=distance ............................
    [CV] ............. n_neighbors=9, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=9, p=5, weights=distance ............................
    [CV] ............. n_neighbors=9, p=4, weights=distance, total=   1.0s
    [CV] n_neighbors=9, p=5, weights=distance ............................
    [CV] ............. n_neighbors=9, p=4, weights=distance, total=   1.1s
    [CV] n_neighbors=9, p=5, weights=distance ............................
    [CV] ............. n_neighbors=9, p=4, weights=distance, total=   1.1s
    [CV] n_neighbors=10, p=1, weights=distance ...........................
    [CV] ............. n_neighbors=9, p=5, weights=distance, total=   1.0s
    [CV] n_neighbors=10, p=1, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=10, p=1, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=1, weights=distance, total=   0.1s
    [CV] n_neighbors=10, p=2, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=1, weights=distance, total=   0.2s
    [CV] n_neighbors=10, p=2, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=10, p=2, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=2, weights=distance, total=   0.1s
    [CV] n_neighbors=10, p=3, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=2, weights=distance, total=   0.2s
    [CV] n_neighbors=10, p=3, weights=distance ...........................
    [CV] ............. n_neighbors=9, p=5, weights=distance, total=   1.2s
    [CV] n_neighbors=10, p=3, weights=distance ...........................
    [CV] ............. n_neighbors=9, p=5, weights=distance, total=   1.3s
    [CV] n_neighbors=10, p=4, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=10, p=4, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=3, weights=distance, total=   1.1s
    [CV] n_neighbors=10, p=4, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=3, weights=distance, total=   1.0s
    [CV] n_neighbors=10, p=5, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=4, weights=distance, total=   1.4s
    [CV] n_neighbors=10, p=5, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=4, weights=distance, total=   1.2s
    [CV] n_neighbors=10, p=5, weights=distance ...........................
    [CV] ............ n_neighbors=10, p=4, weights=distance, total=   1.1s
    [CV] ............ n_neighbors=10, p=5, weights=distance, total=   1.2s
    [CV] ............ n_neighbors=10, p=5, weights=distance, total=   1.0s
    [CV] ............ n_neighbors=10, p=5, weights=distance, total=   0.7s
    CPU times: user 619 ms, sys: 271 ms, total: 890 ms
    Wall time: 1min 31s


    [Parallel(n_jobs=-1)]: Done 180 out of 180 | elapsed:  1.5min finished


![](https://shirukai.gitee.io/images/aa787f1550afb8ab1b77583fcbf2a0dd.jpg)
