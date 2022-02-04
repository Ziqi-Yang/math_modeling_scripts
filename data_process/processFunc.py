import pandas as pd
import sys
import os
import pickle

rootPath = sys.path[0]
cacheFolder = os.path.join(rootPath, "cache")
cacheExpandFolder = os.path.join(cacheFolder,"expand")
pklFolder = os.path.join(cacheFolder,"pkl") 


def time_expand(df:pd.DataFrame,process: str, filename:str,saveData=True):
    df.set_index("Country",inplace=True)

    if saveData:
        filename = filename.split(".")[0] + "-expand.csv"
        df.to_csv(os.path.join(cacheExpandFolder,filename))
        filename = filename.split(".")[0] + ".pkl"
        with open(os.path.join(pklFolder,filename), "wb") as f:
            pickle.dump(df,f)

    df = pd.DataFrame(df.apply(process,axis=1))
    df.columns = [process]
    df.apply(process,axis=1)
    lossCountries = list(df[df[process].isna()].index)
    df = df[df[process].isna() == False]
    return df,lossCountries

def time_in_column(df:pd.DataFrame , dfAttrs: dict, process:str,filename:str):
    dupErr = False
    try:
        df = df.pivot("Country",dfAttrs["timeColumnName"],dfAttrs["valueColumnName"]).rename_axis(columns=None).reset_index()
        return dupErr,time_expand(df,process,filename)
    except ValueError: # Index contains duplicate entries, cannot reshape
        dupErr = True
        df_dup = df[df.duplicated(keep=False)]
        df_dup = (df_dup.groupby(df_dup.columns.tolist())
            .apply(lambda x: tuple(x.index))
            .reset_index(name='Index'))
        return dupErr,df_dup



if __name__ == "__main__":
    pass