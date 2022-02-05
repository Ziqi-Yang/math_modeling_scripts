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