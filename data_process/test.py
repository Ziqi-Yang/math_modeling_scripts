from numpy import full
import pandas  as pd
import pickle

df_country_code_dict = pd.read_csv("data_process/core/ISO3661-modified.csv")

fullname = df_country_code_dict["name"]
alpha2 = df_country_code_dict["alpha-2"]
alpha3 = df_country_code_dict["alpha-3"]

country_code_dict = dict(list(zip(alpha3,fullname)) + list(zip(alpha2,fullname)) + list(zip(fullname,fullname)))

with open("code_country_dict.pkl","wb") as f:
    pickle.dump(country_code_dict,f)
