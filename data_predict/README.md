# 注意

此预测方法采用的是`多项式拟合`,本预测还设置了之后每年都可以在原来年份增长基础上加上增加百分之几的作用。具体设置在程序文件`predict.ipynb`中。  
如果要使用`时间序列分析`算法(如`ARIMA`)，请移至`modeling_algorithm`


## Tips:

- 一般选用`拟合算法`。
- `灰色预测`我还没学。
- 预测人口可以使用`Leslie`(莱斯利人口模型)。
- 有季节性变化(类周期性)的话可以使用`SARIMA`模型。
