
# 逻辑回归

解决分类问题

* 回归问题怎么解决分类问题？
将样本的特征和样本发生的概率联系起来，概率是一个数

![](https://shirukai.gitee.io/images/bad1d717ed47371720e8c22cc579ce16.jpg)


![](https://shirukai.gitee.io/images/539d4e19f8a70f5f92fff9ca911ad2c5.jpg)
![](https://shirukai.gitee.io/images/b7aa72129f76a389b66f0706e2ecc105.jpg)

## Sigmoid 函数


```python
import numpy as np
import matplotlib.pyplot as plt
```


```python
def sigmoid(t):
    return 1 / (1 + np.exp(-t))
```


```python
x = np.linspace(-10,10,500)
y = sigmoid(x)

plt.plot(x,y)
plt.show()
```


![](https://shirukai.gitee.io/images/ca0099f1ffcd8830afab355938ba386c.jpg)


![](https://shirukai.gitee.io/images/208881e80ec1eeb0e633e6e58cc5fcff.jpg)
![](https://shirukai.gitee.io/images/12c9518ea11fcbe9c19fb822a9de770d.jpg)
### 问题：
对于给定的样本数据集X,y，我们如何找到参数theta，使得用这样的方式，可以最大程度获取样本数据集X对应的分类输出y？

