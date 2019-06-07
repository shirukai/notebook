# 使用PCA进行降噪

```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
X = np.empty((100,2))
```


```python
X[:,0] = np.random.uniform(0.,100.,size=100)
```


```python
X[:,1] = 0.75 * X[:,0] + 3. + np.random.normal(0,5,size=100)
```


```python
plt.scatter(X[:,0],X[:,1])
plt.show()
```


![](https://shirukai.gitee.io/images/9236be6efe3d4eaa947fb5075e2f1c82.jpg)



```python
from sklearn.decomposition import PCA
pca = PCA(n_components=1)
pca.fit(X)
X_reduction = pca.transform(X)
X_restore = pca.inverse_transform(X_reduction)
```


```python
plt.scatter(X_restore[:,0],X_restore[:,1])
plt.show()
```


![](https://shirukai.gitee.io/images/3bcd7be7089323092fd7bae7ff9e98e6.jpg)


## 手写识别的例子


```python
from sklearn import datasets
digits = datasets.load_digits()
X = digits.data
y = digits.target
```


```python
noisy_digits = X + np.random.normal(0,4,size=X.shape)
```


```python
example_digits = noisy_digits[y==0,:][:10]
for num in range(1,10):
    X_num = noisy_digits[y==num,:][:10]
    example_digits = np.vstack([example_digits,X_num])
```


```python
example_digits.shape
```


    (100, 64)


```python
def plot_digits(data):
    fig, axes = plt.subplots(10,10,figsize=(10,10),subplot_kw={'xticks':[],'yticks':[]},
    gridspec_kw = dict(hspace=0.1,wspace=0.1))
    for i,ax in enumerate(axes.flat):
        ax.imshow(data[i].reshape(8,8),
                 cmap='binary',interpolation='nearest',clim=(0,16))
    plt.show()
```


```python
plot_digits(example_digits)
```


![](https://shirukai.gitee.io/images/05c4bf9d3360fee0eba34d363f910ffc.jpg)

```python
pca = PCA(0.5)
```


```python
pca.fit(example_digits)
```




    PCA(copy=True, iterated_power='auto', n_components=0.5, random_state=None,
      svd_solver='auto', tol=0.0, whiten=False)




```python
pca.n_components_
```


    8


```python
components = pca.transform(example_digits)
filtered_digits = pca.inverse_transform(components)
```


```python
plot_digits(filtered_digits)
```


![](https://shirukai.gitee.io/images/16aa308c2491c481254974149070e078.jpg)

```python
from sklearn.datasets import fetch_lfw_people
```


```python
faces = fetch_lfw_people()

faces.keys()
```

    dict_keys(['data', 'images', 'target', 'target_names', 'DESCR'])


```python
faces.data.shape
```


    (13233, 2914)


