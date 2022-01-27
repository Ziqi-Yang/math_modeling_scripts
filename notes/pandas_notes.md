# Pandas Notes

- [Pandas Notes](#pandas-notes)
  - [公共键](#公共键)
  - [重复行处理](#重复行处理)
  - [行转列](#行转列)
  - [一行生成多行](#一行生成多行)
  - [字典拆分成多列](#字典拆分成多列)
  - [列转行](#列转行)
  - [列转行(键值列)](#列转行键值列)

## 公共键

```python
# 本例的目的就是为了说 x in df[..] 是不对的
# 要用 x in list(df[...])
# datas = [df_0,df_1,df_2]
sharedKeys = [key for key in datas[0].index if all(map(lambda x: key in list(x.index),datas))]
```

## 重复行处理

- 检测重复行

```python
dframe.duplicated()
```

- 删除重复行

```python
#删除重复行，该函数返回的是删除重复行后的DataFrame对象
dframe.drop_duplicates()
```

- 仅返回index
```python
df = df[df.duplicated(keep=False)]

df = df.groupby(df.columns.tolist()).apply(lambda x: tuple(x.index)).tolist()
print (df)
# [(1, 6), (2, 4), (3, 5)]
```

- 看到重复行的值 + index

```python
df1 = (df.groupby(df.columns.tolist())
       .apply(lambda x: tuple(x.index))
       .reset_index(name='idx'))
print (df1)

#    param_a  param_b  param_c     idx
# 0        0        0        0  (1, 6)
# 1        0        2        1  (2, 4)
# 2        2        1        1  (3, 5)
```


## 行转列

原始数据
```python
df.head(5)
# 	Country TIME	Value
# 0	AUS	2017	51.989063
# 1	AUS	2018	51.393173
# 2	AUS	2019	52.478458
# 3	AUS	2020	54.614105
# 4	AUT	2017	40.324657
```
要转化成的数据
```python

# Country 2017	       2018	       2019	       2020
# ARG	18.388876	39.957542	NaN	       NaN
# AUS	51.989063	51.393173	52.478458	54.614105
# AUT	40.324657	40.458271	41.610401	41.419125
# BEL	45.725086	47.397144	47.282982	48.508053
# BRA	19.613668	21.314569	21.602325	23.531902
```

- 法一 `pivot`方法
```python
df.pivot("LOCATION","TIME","Value").rename_axis(columns=None)
```

- 法二 具有多index的array的`unstack`方法
```python
df.set_index(["Country","TIME"])["Value"].unstack()
```

## 一行生成多行

原始数据
```python
	声优	生日	       作品
0	关智一	1972-09-08	吉尔伽美什,罗布·路奇,桥田至
1	松冈祯丞	1986-09-17	贝尔·克朗尼,桐人,神田空太,安艺伦也
2	雨宫天	1993-08-28	赤瞳,雾嶋董香,米娅,阿克娅
```
要转化成的数据
```python
	声优	生日	       配音角色
0	关智一	1972-09-08	吉尔伽美什
1	关智一	1972-09-08	罗布·路奇
2	关智一	1972-09-08	桥田至
3	松冈祯丞	1986-09-17	贝尔·克朗尼
4	松冈祯丞	1986-09-17	桐人
5	松冈祯丞	1986-09-17	神田空太
6	松冈祯丞	1986-09-17	安艺伦也
7	雨宫天	1993-08-28	赤瞳
8	雨宫天	1993-08-28	雾嶋董香
9	雨宫天	1993-08-28	米娅
10	雨宫天	1993-08-28	阿克娅
```

- 法一 具有多index的array的`stack`方法
(第二步的`stack`其实有点`列转行`的意味)

```python
df = df.set_index(["声优","生日"])["作品"].str.split(",",expand=True)
df.stack().reset_index(drop=True,level=-1).reset_index().rename(columns={0: "配音角色"})
```


- 法二 `explode` 方法
```python
df["作品"] = df["作品"].str.split(",")
# df["作品"] = df["作品"].map(lambda x: x.split(","))
df.explode("作品")
```

## 字典拆分成多列

原始数据  
注意，这种数据在保存时最好用`pickle`，如果用`csv`和`excel`在加载数据后都要进行类型转化，可以考虑`df["info"] = df["info"].apply(eval)`方法(若是其他语言提供的api，里面的数据表达方式可能不同，如`true`和`True`，这时候可以用`json`库或者字符串替换)

```python
       id                                                      info  
0       0           {'声优': '关智一', '生日': '1972-09-08', '作品': '吉尔伽美什,罗布·路奇,桥田至'}  
1       1 {'声优': '松冈祯丞', '生日': '1986-09-17', '作品': '贝尔·克朗尼,桐人,神田空太,安艺伦也','外号':'后宫王'}  
2       2           {'声优': '雨宫天', '生日': '1993-08-28', '作品': '赤瞳,雾嶋董香,米娅,阿克娅'}
```
要转化成的数据

```python
    id   声优	生日	        作品	                        外号
0   0    关智一	1972-09-08	吉尔伽美什,罗布·路奇,桥田至	NaN
1   1    松冈祯丞 1986-09-17	贝尔·克朗尼,桐人,神田空太,安艺伦也	后宫王
2   2    雨宫天	1993-08-28	赤瞳,雾嶋董香,米娅,阿克娅	        NaN
```

方法 `pd.Series`

```python
tmp = df["info"].apply(pd.Series)
# 因为我们这里的值是一个字典, 而Series接收一个字典的话, 那么字典的key就是索引, value就是值
# 在扩展成DataFrame的时候同样会考虑到字典中所有的key, 有多少个不重复的key就会生成多少个列
# 如果该行没有对应的值则使用NaN填充
df[tmp.columns] = tmp # 将tmp添加到df中
df = df.drop(columns="info")
df
```

## 列转行

原始数据

```python
	姓名	水果	星期一	星期二	星期三
0	古明地觉	草莓	70斤	72斤	60斤
1	雾雨魔理沙 樱桃	61斤	60斤	81斤
2	琪露诺	西瓜	103斤	116斤	153斤
```

要转换成的数据

```python
	姓名	水果	星期几?	销量
0	古明地觉	草莓	星期一	70斤
1	雾雨魔理沙 樱桃	星期一	61斤
2	琪露诺	西瓜	星期一	103斤
3	古明地觉	草莓	星期二	72斤
4	雾雨魔理沙	樱桃	星期二	60斤
5	琪露诺	西瓜	星期二	116斤
6	古明地觉	草莓	星期三	60斤
7	雾雨魔理沙 樱桃	星期三	81斤
8	琪露诺	西瓜	星期三	153斤
```

方法一 内置`melt`函数
```python
pd.melt(df,id_vars=["姓名","水果"],value_vars=["星期一","星期二","星期三"],var_name="星期几?",value_name="销量")
# pd.melt(df,id_vars=["姓名","水果"],var_name="星期几?",value_name="销量") # 只指定id_vars,var_name就默认为所有其他列
```

方法二 用`stack`函数来实现`melt`函数

```python
def my_melt(frame: pd.DataFrame,
            id_vars: list,
            value_vars: list,
            var_name: str,
            value_name: str):
    # 先将id_vars和value_vars指定的字段筛选出来
    frame = frame[id_vars + value_vars]

    # 将id_vars指定的字段设置为索引
    frame = frame.set_index(id_vars)
    print(">>>筛选字段、设置索引之后对应的DataFrame:\n", frame)

    # 调用frame的stack方法, 会得到一个具有多级索引的Series
    # frame的列就是生成的Series的最后一级索引
    s = frame.stack()
    print(">>>得到的具有多级索引的Series:\n", s)

    # 直接对该Series进行reset_index即可, 会得到DataFrame, 将索引变成列
    frame = s.reset_index()
    print(">>>具有多级索引的Series执行reset_index:\n", frame)

    # 重命名
    frame.columns = id_vars + [var_name, value_name]
    print(">>>最终返回的DataFrame:")
    return frame
```

## 列转行(键值列)

原始数据

| 姓名   | 年龄 | 技能1  | 活动地点1 | 技能2  | 活动地点2 | 技能3  | 活动地点3 |
|------|----|------|-------|------|-------|------|-------|
| 麦克雷  | 37 | 闪光弹  | 66号公路 | 战术翻滚 | 多拉多   | 神射手  | 漓江塔   |
| 源氏   | 35 | 闪    | 尼泊尔   | 影    | 花村    | 斩    | 直布罗陀  |
| 士兵76 | 55 | 螺旋飞弹 | 多拉多   | 生物立场 | 伊里奥斯  | 战术目镜 | 努巴尼   |

要转化成的数据:

|   | 姓名   | 年龄 | 技能   | 活动地点  |
|---|------|----|------|-------|
| 0 | 麦克雷  | 37 | 闪光弹  | 66号公路 |
| 0 | 麦克雷  | 37 | 战术翻滚 | 多拉多   |
| 0 | 麦克雷  | 37 | 神射手  | 漓江塔   |
| 1 | 源氏   | 35 | 闪    | 尼泊尔   |
| 1 | 源氏   | 35 | 影    | 花村    |
| 1 | 源氏   | 35 | 斩    | 直布罗陀  |
| 2 | 士兵76 | 55 | 螺旋飞弹 | 多拉多   |
| 2 | 士兵76 | 55 | 生物立场 | 伊里奥斯  |
| 2 | 士兵76 | 55 | 战术目镜 | 努巴尼   |


方法一 `综合`

```python
df["技能"] = df[["技能1","技能2","技能3"]].agg(tuple,axis=1)
df["活动地点"] = df[["活动地点1","活动地点2","活动地点3"]].agg(tuple,axis=1)
df = df.filter(regex=r"(?<!\d)$") # 筛选出不存在数字的列
df["技能-活动地点"] = df["技能"].combine(df["活动地点"],func=lambda x,y:list(zip(x,y)))
df = df.drop(columns=["技能","活动地点"])
df = df.explode("技能-活动地点")
df[["技能","活动地点"]] = df["技能-活动地点"].apply(pd.Series)
df = df.drop(columns=["技能-活动地点"])
df
```

方法二 `pd.lreshape`

```python
df = pd.lreshape(df,{"技能":["技能1","技能2","技能3"],"活动地点":["活动地点1","活动地点2","活动地点3"]}) 
# 注意不能有空值，否则会被舍弃.要保留空值要用dropna=False
```