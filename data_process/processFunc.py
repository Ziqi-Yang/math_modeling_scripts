import pandas as pd


def time_expand(df:pd.DataFrame,process: str):
    df.set_index("Country",inplace=True)
    df = pd.DataFrame(df.apply(process,axis=1))
    df.columns = [process]
    df.apply(process,axis=1)
    lossCountries = list(df[df[process].isna()].index)
    df = df[df[process].isna() == False]
    return df,lossCountries

def time_in_column(df:pd.DataFrame , dfAttrs: dict, process):
    dupErr = False
    try:
        df = df.pivot("Country",dfAttrs["timeColumnName"],dfAttrs["valueColumnName"]).rename_axis(columns=None).reset_index()
        return dupErr,time_expand(df,process)
    except ValueError: # Index contains duplicate entries, cannot reshape
        dupErr = True
        df_dup = df[df.duplicated(keep=False)]
        df_dup = (df_dup.groupby(df_dup.columns.tolist())
            .apply(lambda x: tuple(x.index))
            .reset_index(name='Index'))
        return dupErr,df_dup
        

def complex_data(df:pd.DataFrame , dfAttrs: dict): # to aviod name crash with buildin function complex
    pass




if __name__ == "__main__":
    pass