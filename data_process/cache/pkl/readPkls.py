# Read Pkls

import pandas as pd
import pickle

with open(r"C:\Users\Zarkli\Desktop\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_HH.pkl","rb") as f:
	df_0 = pickle.load(f)
with open(r"C:\Users\Zarkli\Desktop\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_OTHPRIVENT.pkl","rb") as f:
	df_1 = pickle.load(f)
with open(r"C:\Users\Zarkli\Desktop\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_PUB.pkl","rb") as f:
	df_2 = pickle.load(f)
with open(r"C:\Users\Zarkli\Desktop\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_PRIV.pkl","rb") as f:
	df_3 = pickle.load(f)
