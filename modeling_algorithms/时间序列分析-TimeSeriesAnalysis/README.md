# 时间序列分析 Time Series Analysis

`python`实现教程(三种`指数平滑`,`SARIMA`,`regression`)可以至网站[mlcourse.ai](https://mlcourse.ai/book/topic09/topic9_part1_time_series_python.html#feature-extraction)查看，或者到`res`目录下查看`本地版`。

(备注: [pmdarima](http://alkaline-ml.com/pmdarima/quickstart.html) 里的`auto_arima`似乎是一个更方便的选择,安装`pmdarima`的时候直接用`pip`就好了,在按官网上说的`conda`三步曲导致环境检测一直有矛盾，还直接改你`conda`配置,导致安装其它库的时候也环境矛盾)

`pmdarima-year.ipynb`里有`缺失值补全`

## Tips

若分析得到的模型是 `ARIMA(p,0,q)`，也就是`ARMA`模型,我们可以画出时间序列样本的`ACF`和`PACF`图形分析; 如果得到的是`ARIMA（p，1，q）`模型，我们可以先对数据进行`1阶差分`后再用`ACF`和`PACF`图形分析；如果得到的结果与`季节性`(`SARIMA`)相关，那么我们可以考虑使用`时间序列分解`(就是多写一点，主要还是用`SARIMA`)。
