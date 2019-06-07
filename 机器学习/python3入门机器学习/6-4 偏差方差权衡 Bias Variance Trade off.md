
## 偏差和方差
![](https://shirukai.gitee.io/images/48ae6a58b1071eea8c1da486202ac13c.jpg)


## 模型误差
模型误差 = 偏差（Bias）+ 方差（Variance）+ 不可避免的误差
## 偏差（Bias）
![](https://shirukai.gitee.io/images/fa531befa54190f14b7797c8ba1b2e64.jpg)
## 方差（Variance）
![](https://shirukai.gitee.io/images/b6dda8eba923ca8b5c4f8a8859babeab.jpg)
## 偏差和方差
![](https://shirukai.gitee.io/images/a8430de9690e1c5be5905c8e37256db0.jpg)
偏差和方差通常是矛盾的：降低偏差，会提高方差，降低方差会提高偏差

机器学习的主要挑战，来自于方差
### 解决高方差的通常手段
1. 降低模型复杂度
2. 减少数据维度；降噪
3. 增加样本数
4. 使用验证集
5. 模型正则化
