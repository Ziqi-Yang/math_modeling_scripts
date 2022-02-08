import pandas as pd
import os
import sys

# 默认都是极大型指标

os.chdir(sys.path[0])
df = pd.read_csv("./COMPOSED.csv")

# 采用min-max标准化方法
df.set_index("Country",inplace=True)
# 数据标准化，为了计算final_score
df = df.apply(lambda col: list(map(lambda x: (x- col.min())/(col.max()-col.min()),col)), axis=0)
df.reset_index(inplace=True)

# print(df)
df.to_csv("./COMPOSED_norm.csv")