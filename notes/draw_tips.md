# `python`画图`tips`

## 将`legend`移到外部

参考：[stackoverflow](https://stackoverflow.com/questions/30490740/move-legend-outside-figure-in-seaborn-tsplot)

```python
plt.legend(bbox_to_anchor=(1.05, 1),loc=2,borderaxespad=0.)
# 注意在保存的时候要设置bbox_inches
plt.savefig("save_path.png",dpi=300,bbox_inches='tight')
# bbox_inches='tight' 是为了保存legend, 否则legend可能会被裁剪
```

## 当`plt`里的函数不提供数字和数组设置`color`时，自定义`color`

可以看看`stem`函数，里面之提供了`markerfmt`和`linefmt`参数，都只能接受字符串，而设置颜色只能通过字符串`r`,`b`等，若要自定义设置可参考下这:

```python
markerline, stemlines, baseline = ax.stem(data=df,x="complex_HH",y="complex_PRIV",z=final_score)
plt.getp(stemlines,"color") # 得到参考格式
# [[0.7, 0.46666667, 0.70588235, 1.        ]]
# plt.setp(stemlines,"color",[[0.7, 0.46666667, 0.70588235, 1.        ]])
```

## 安装`matplotlib`的`basemap`

虽然`basemap`官方说将要被抛弃了，推荐使用[cartopy](https://scitools.org.uk/cartopy/docs/latest/getting_started/index.html)，但是网上有些代码还是用`basemap`，为了快而方便地调用别人的代码，还是写了这个  
`matplotlib`的`basemap`很坑，会遇到各种报错,总之这里给出通用安装方法
步骤:
    1. `conda`创建`python3.6`的环境，然后再`conda install basemap`
    2. 然后将`matplotlib`降级至`3.2`,命令`pip install -U matplotlib==3.2`