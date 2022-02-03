# Read Pkls
import pandas as pd
import pickle

# df_0: complex-HH-expand.pkl
# df_1: complex-OTHPRIVENT-expand.pkl
# df_2: complex-PRIV-expand.pkl
# df_3: complex-PUB-expand.pkl
# df_4: complex_HH.pkl
# df_5: complex_OTHPRIVENT.pkl
# df_6: complex_PRIV.pkl
# df_7: complex_PUB.pkl
# df_8: COMPOSED.pkl
# df_9: time-expand-expand.pkl
# df_10: time-expand.pkl
# df_11: time-in-column_1-expand.pkl
# df_12: time-in-column_1.pkl
with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex-HH-expand.pkl","rb") as f:
	df_0 = pickle.load(f) #complex-HH-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex-OTHPRIVENT-expand.pkl","rb") as f:
	df_1 = pickle.load(f) #complex-OTHPRIVENT-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex-PRIV-expand.pkl","rb") as f:
	df_2 = pickle.load(f) #complex-PRIV-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex-PUB-expand.pkl","rb") as f:
	df_3 = pickle.load(f) #complex-PUB-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_HH.pkl","rb") as f:
	df_4 = pickle.load(f) #complex_HH.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_OTHPRIVENT.pkl","rb") as f:
	df_5 = pickle.load(f) #complex_OTHPRIVENT.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_PRIV.pkl","rb") as f:
	df_6 = pickle.load(f) #complex_PRIV.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\complex_PUB.pkl","rb") as f:
	df_7 = pickle.load(f) #complex_PUB.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\COMPOSED.pkl","rb") as f:
	df_8 = pickle.load(f) #COMPOSED.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\time-expand-expand.pkl","rb") as f:
	df_9 = pickle.load(f) #time-expand-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\time-expand.pkl","rb") as f:
	df_10 = pickle.load(f) #time-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\time-in-column_1-expand.pkl","rb") as f:
	df_11 = pickle.load(f) #time-in-column_1-expand.pkl

with open(r"D:\Document\math_modeling\math_modeling_scripts\data_process\cache\pkl\time-in-column_1.pkl","rb") as f:
	df_12 = pickle.load(f) #time-in-column_1.pkl

