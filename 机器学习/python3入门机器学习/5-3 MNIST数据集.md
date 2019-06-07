

```python
import numpy as np
from sklearn.datasets import fetch_mldata
```


```python
mnist = fetch_mldata("MNIST original",data_home="/Users/shirukai/Desktop/MachineLearn/datasets/")
```


```python
mnist
```




    {'COL_NAMES': ['label', 'data'],
     'DESCR': 'mldata.org dataset: mnist-original',
     'data': array([[0, 0, 0, ..., 0, 0, 0],
            [0, 0, 0, ..., 0, 0, 0],
            [0, 0, 0, ..., 0, 0, 0],
            ...,
            [0, 0, 0, ..., 0, 0, 0],
            [0, 0, 0, ..., 0, 0, 0],
            [0, 0, 0, ..., 0, 0, 0]], dtype=uint8),
     'target': array([0., 0., 0., ..., 9., 9., 9.])}




```python
X,y = mnist['data'],mnist['target']
```


```python
X_train = np.array(X[:60000],dtype=float)
y_train = np.array(y[:60000],dtype=float)
X_test = np.array(X[60000:],dtype=float)
y_test = np.array(y[60000:],dtype=float)
```


```python
X_train.shape
```




    (60000, 784)




```python
y_train.shape
```




    (60000,)




```python
X_test.shape
```




    (10000, 784)




```python
y_test.shape
```




    (10000,)



## 使用kNN


```python
from sklearn.neighbors import KNeighborsClassifier
knn_clf = KNeighborsClassifier()
%time knn_clf.fit(X_train,y_train)
```

    CPU times: user 33 s, sys: 617 ms, total: 33.6 s
    Wall time: 34.9 s





    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=5, p=2,
               weights='uniform')




```python
%time knn_clf.score(X_test,y_test)
```

    CPU times: user 14min 54s, sys: 9.82 s, total: 15min 4s
    Wall time: 15min 21s





    0.9688



## 使用PCA进行降维


```python
from sklearn.decomposition import PCA
pca = PCA(0.9)
pca.fit(X_train)
X_train_reduction = pca.transform(X_train)
```


```python
X_train_reduction.shape
```




    (60000, 87)




```python
knn_clf = KNeighborsClassifier()
%time knn_clf.fit(X_train_reduction,y_train)
```

    CPU times: user 407 ms, sys: 8.76 ms, total: 415 ms
    Wall time: 419 ms





    KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=5, p=2,
               weights='uniform')




```python
X_test_reduction = pca.transform(X_test)
```


```python
%time knn_clf.score(X_test_reduction,y_test)
```

    CPU times: user 1min 20s, sys: 817 ms, total: 1min 20s
    Wall time: 1min 21s





    0.9728


