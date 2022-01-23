# Pandas Notes


## 公共键

```python
# 注意list
sharedKeys = [key for key in df["Country"] if key in list(df["Country"])]
```

## 查找重复行

### 仅返回index
```python
df = df[df.duplicated(keep=False)]

df = df.groupby(df.columns.tolist()).apply(lambda x: tuple(x.index)).tolist()
print (df)
# [(1, 6), (2, 4), (3, 5)]
```

### 看到重复行的值

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