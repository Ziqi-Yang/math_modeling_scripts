import pandas as pd


def time_expand(df:pd.DataFrame , dfAttrs: dict,process: str) -> pd.DataFrame:
    df.set_index("Country",inplace=True)
    df = pd.DataFrame(df.apply(process,axis=1))
    df.columns = [process]
    df.apply(process,axis=1)
    lossCountries = list(df[df[process].isna()].index)
    df = df[df[process].isna() == False]
    return df,lossCountries

def time_in_column(df:pd.DataFrame , dfAttrs: dict):
    pass

def complex_data(df:pd.DataFrame , dfAttrs: dict): # to aviod name crash with buildin function complex
    pass




if __name__ == "__main__":
    pass