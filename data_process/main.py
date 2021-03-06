from calendar import c
from collections.abc import Iterable
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
import pickle
import sys
import os
import shutil
from rich.console import Console
from rich.prompt import Prompt, Confirm
from processFunc import time_expand,time_in_column

import logging
from rich.logging import RichHandler
logging.basicConfig(
    level="ERROR",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")

console = Console()

rootPath = sys.path[0]
dataFolder = os.path.join(rootPath, "datas")
resultFolder = os.path.join(rootPath, "result")
cacheFolder = os.path.join(rootPath,"cache")
cacheExpandFolder = os.path.join(cacheFolder,"expand")
pklFolder = os.path.join(cacheFolder,"pkl") 
if not os.path.exists(dataFolder):
    os.mkdir(dataFolder)

if not os.path.exists(cacheFolder):
    os.mkdir(cacheFolder)
else:
    shutil.rmtree(cacheFolder)
    os.mkdir(cacheFolder)
os.mkdir(cacheExpandFolder)
os.mkdir(pklFolder)

if not os.path.exists(resultFolder):
    os.mkdir(resultFolder)
else:
    shutil.rmtree(resultFolder)
    os.mkdir(resultFolder)



dataFilesNames = os.listdir(dataFolder)
dataFilesPath = list(map(lambda x: os.path.join(dataFolder, x), dataFilesNames))
dataFilesPath = [dataFilePath for dataFilePath in dataFilesPath if os.path.isfile(dataFilePath)] # shouldn't include folder
dataFilesNames = [os.path.basename(filename) for filename in dataFilesPath]

DATAS = dict()

console.clear()
console.print(f"Here are data files in the 'datas' folder:\n{dataFilesNames} ")

# load files
if Confirm.ask("[bold red]Important[/] Have you already pre-process (like [bold cyan]delete unneeded rows or columns[/]) those files in [yellow]Excel[/]?"):
    console.rule()
    unrecognizedFiles = []
    with console.status("Reading data files..."):
        index = 0
        while index < len(dataFilesPath):
            dataFilePath = dataFilesPath[index]
            fileName = os.path.basename(dataFilePath)
            if dataFilePath.endswith("csv"):
                try:
                    DATAS[fileName] = pd.read_csv(dataFilePath)
                except:
                    log.exception(f"Reading file '{fileName}' failed.")
                    exit(1)
                console.print(f"Reading [yellow]{fileName}[/] done.")
            elif dataFilePath.endswith("excel"):
                try:
                    DATAS[fileName] = pd.read_excel(dataFilePath)
                except:
                    log.exception(f"Reading file '{fileName}' failed.")
                    exit(1)
                console.print(f"Reading [yellow]{fileName}[/] done.")
            else:
                unrecognizedFiles.append(fileName)
                console.print(f"[bold red]Warning[/] can't recognize file [yellow]{fileName}[/]. Please reexamine its file format.")
            index += 1
    console.rule()
    console.print("Unrecognized(ignored) Files:")
    console.print(unrecognizedFiles)
    if not Confirm.ask("Whether to continute the program?"):
        exit(0)
else:
    exit(0)




# set attribution for each files, respectfully
console.clear()
console.print("Please set suitable attribution for each data file:")

dataFilesAttrs = {dataFileName: dict() for dataFileName in DATAS.keys()}
attrsChoice = {
    "dataFileType": ["time-expand", "time-in-column","complex"],
    "countryColumnName": None,
    "subjectColumnName": None,
    "timeColumnName": None,
    "valueColumnName": None,
    "theme": None
}  # single stands for no limit, but default is the word

index = 0
dataFilesNames = list(dataFilesAttrs.keys())
while index < len(dataFilesNames):
    dataFileName = dataFilesNames[index]
    console.rule(f"[bold red]{dataFileName}[/]",align="left")

    attrIndex = 0
    attrs = list(attrsChoice.keys())
    # for attr in list(attrsChoice.keys()):
    while attrIndex < len(attrs):
        attr = attrs[attrIndex]
        prompt = ""
        if attr == "countryColumnName":
            prompt = " (Leave [grey]empty[/] if first column)"
        elif attr == "valueColumnName":
            prompt = " (Leave [grey]empty[/] if last column)"
        elif attr == "theme":
            theme = dataFileName.split(".")[0]
            prompt = f" (used as a column name in composed data sheet, default [yellow]{theme}[/])"

        if attr == "timeColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] == "time-expand": # auto set value to None, and skip question
            dataFilesAttrs[dataFileName][attr] = None
        elif attr == "subjectColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] != "complex": # auto set value to None, and skip question
            dataFilesAttrs[dataFileName][attr] = None
        elif attr == "valueColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] == "time-expand": # auto set value to None, and skip question
            dataFilesAttrs[dataFileName][attr] = None
        else:
            default = attrsChoice[attr][0] if isinstance(attrsChoice[attr], Iterable) else attrsChoice[attr]
            if attr == "dataFileType":
                if len(DATAS[dataFileName].columns) == 3:
                    default = "time-in-column"
                elif len(DATAS[dataFileName].columns) == 4:
                    default = "complex"

            dataFilesAttrs[dataFileName][attr] = Prompt.ask(
                f"{attr}{prompt}",
                default=default,
                choices=attrsChoice[attr] if isinstance(attrsChoice[attr], list) else None,
            )

        dataFileType = dataFilesAttrs[dataFileName]["dataFileType"]
        attrValue = dataFilesAttrs[dataFileName][attr]

        # auto set values if file is in compliance with requirements
        if attrIndex == 0: # after set dataFileType
            if attrValue == "time-in-column":
                columns = DATAS[dataFileName].columns
                if list(columns.map(lambda x: x.lower())) == ["country","time","value"]:
                    if Confirm.ask(f"Detect your file is in compliance with [cyan]{attrValue}[/] requirement, do you want to [yellow]auto[/] set most of the attributions?"):
                        dataFilesAttrs[dataFileName]["countryColumnName"] = columns[0]
                        dataFilesAttrs[dataFileName]["subjectColumnName"] = None
                        dataFilesAttrs[dataFileName]["timeColumnName"] = columns[1]
                        dataFilesAttrs[dataFileName]["valueColumnName"] = columns[2]
                        console.print("[yellow]Current Attributions[/]:")
                        console.print(dataFilesAttrs[dataFileName])
                        attrIndex += 4 # in the later within this loop, attrIndex will also plus 1
                    
            elif attrValue == "complex":
                columns = DATAS[dataFileName].columns
                if list(columns.map(lambda x: x.lower())) == ["country","subject","time","value"]:
                    if Confirm.ask(f"Detect your file is in compliance with [cyan]{attrValue}[/] requirement, do you want to [yellow]auto[/] set most of the attributions?"):
                        dataFilesAttrs[dataFileName]["countryColumnName"] = columns[0]
                        dataFilesAttrs[dataFileName]["subjectColumnName"] = columns[1]
                        dataFilesAttrs[dataFileName]["timeColumnName"] = columns[2]
                        dataFilesAttrs[dataFileName]["valueColumnName"] = columns[3]
                        console.print("[yellow]Current Attributions[/]:")
                        console.print(dataFilesAttrs[dataFileName])
                        attrIndex += 4


        # exmaine attribution value
        if attr == "countryColumnName" and attrValue == None:
            dataFilesAttrs[dataFileName][attr] = DATAS[dataFileName].columns[0]
        elif attr == "valueColumnName" and attrValue == None and dataFileType != "time-expand":
            dataFilesAttrs[dataFileName][attr] = DATAS[dataFileName].columns[-1]
        elif attr == "theme" and attrValue == None:
            dataFilesAttrs[dataFileName][attr] = dataFileName.split(".")[0]
        
        # update attrValue
        attrValue = dataFilesAttrs[dataFileName][attr]

        # exmaine attribution value
        if attr == "countryColumnName" or (dataFileType == "complex" and attr in ["subjectColumnName","timeColumnName","valueColumnName"]) or (dataFileType == "time-in-column" and attr in ["timeColumnName","valueColumnName"]):
            if attrValue not in DATAS[dataFileName].columns:
                console.print(f"[bold red]Warning[/] file '{dataFileName}' doesn't contain column named '{attrValue}'. Please reset the attribution. [ENTER]",end="")
                input()
                attrIndex -= 1


        attrIndex += 1

    index += 1

hasProb = True
while hasProb:
    console.clear()
    console.rule(f"[bold red]Attribution Viewer[/]")
    console.print(dataFilesAttrs)
    hasProb = Confirm.ask("Have [bold red]problems[/] in the Attributions?")
    if not hasProb:
        break
    tmpConfigPath = os.path.join(rootPath,"tmpConfig.yaml")
    with open(tmpConfigPath,"w",encoding="utf-8") as f:
        yaml.dump(dataFilesAttrs,f,allow_unicode=True)
    console.print(f"Please edit the config file '[yellow]{os.path.basename(tmpConfigPath)}[/]' which is in the same folder with the program.[ENTER]",end="")
    input()
    console.print("Reading attributions...")
    with open(tmpConfigPath,encoding="utf-8") as f:
        dataFilesAttrs = yaml.load(f,Loader=yaml.FullLoader)


# data processing

# load ISO 3661 country code dict
console.print("Loading country_code_dict...")
country_code_dict_pkl_path = os.path.join(rootPath,"core/country_code_dict.pkl")
if os.path.exists(country_code_dict_pkl_path):
    with open(country_code_dict_pkl_path,"rb") as f:
        country_code_dict = pickle.load(f)
else:
    try:
        df_country_code_dict = pd.read_csv("core/ISO3661-modified.csv")
    except:
        log.exception("reading file [yellow]core/ISO3661-modified.csv/] error")        
        exit(1)

    fullname = df_country_code_dict["name"]
    alpha2 = df_country_code_dict["alpha-2"]
    alpha3 = df_country_code_dict["alpha-3"]

    country_code_dict = dict(list(zip(fullname,alpha3)) + list(zip(alpha2,alpha3)) + list(zip(alpha3,alpha3)))

    with open(country_code_dict_pkl_path,"wb") as f:
        pickle.dump(country_code_dict,f)



# map Country Name to ISO 3661 and process datas
allMissingCountries = []
index = 0
cachePkls = dict() # store process data objects

while index < len(dataFilesNames):
    console.clear()
    dataFileName = dataFilesNames[index]
    console.rule(f"Processing [yellow]{dataFileName}[/]")

    df = DATAS[dataFileName]
    dfAttrs = dataFilesAttrs[dataFileName]
    df.rename(columns={dfAttrs["countryColumnName"]: "Country"},inplace=True)

    allCoutries = df["Country"].unique()
    console.print(f"[yellow]All entries[/]: {len(df.Country)} ; [yellow]All Countries Number[/]:{len(allCoutries)}")
    console.print(f"[yellow]All Countries[/]:")
    console.print(f"{allCoutries}")  # for dense view

    missingCountries = df[df["Country"].isin(country_code_dict.keys()) == False]["Country"].unique()
    df.loc[:,"Country"] = df["Country"].map(country_code_dict)
    missingEntriesNum = df["Country"].isna().sum()
    df = df[df["Country"].isna() == False]

    console.print("[*] Mapping ISO-3661 Country Code done.")

    console.print(f"[yellow]Missing entries[/]: {missingEntriesNum} ; [yellow]Missing Countries Number[/]: {len(missingCountries)}")
    console.print("[yellow]Missing Countries[/]:")
    console.print(f"{missingCountries}") # for dense view

    console.print()

    if dfAttrs["dataFileType"] == "time-expand":
        process = Prompt.ask("Process to apply",choices=["min","max","sum","mean","median","std","var","count"],default="mean")

        df,lossCountries = time_expand(df,process,dataFileName)
        console.print("[yellow]Data overview[/] (non-empty):")
        console.print(df)
        console.print(f"[yellow]Empty Data Countries[/] (dropped) [bold magenta]({len(lossCountries)})[/] (possibily originally empty):")
        console.print(lossCountries)

    elif dfAttrs["dataFileType"] == "time-in-column":
        process = Prompt.ask("Process to apply",choices=["min","max","sum","mean","median","std","var","count"],default="mean")

        dupErr,redicious =  time_in_column(df,dfAttrs,process,dataFileName)
        if dupErr == False:
            df,lossCountries = redicious # type(redicious) == tuple
            console.print("[yellow]Data overview[/] (non-empty):")
            console.print(df)
            console.print(f"[yellow]Empty Data Countries[/] (dropped) [bold magenta]({len(lossCountries)})[/] (possibily originally empty):")
            console.print(lossCountries)
        else:
            df_dup = redicious
            console.print("[red]The Files contain duplicated Lines.[/] [yellow]Overview:[/]")
            console.print(df_dup)
            console.print("[*] Drop duplicated lines.")
            df = df.drop_duplicates(keep="first").reset_index(drop=True)
            console.print("[*] Reprocessing the file...")

            try:
                dupErr,(df,lossCountries) =  time_in_column(df,dfAttrs,process,dataFileName)
            except:
                log.exception("[bold red] Please reexamine your data. Your data may contains contradictory lines (like functions whose x have multiple corresponding y)[/]")
                exit(1)
            if dupErr == False:
                console.print("[yellow]Data overview[/] (non-empty):")
                console.print(df)
                console.print(f"[yellow]Empty Data Countries[/] (dropped) [bold magenta]({len(lossCountries)})[/] (possibily originally empty):")
                console.print(lossCountries)

    elif dfAttrs["dataFileType"] == "complex":
        for subject in df[dfAttrs["subjectColumnName"]].unique():
            df_sub = df[df[dfAttrs["subjectColumnName"]] == subject]
            df_sub = df_sub.drop(columns=["SUBJECT"]).reset_index(drop=True)

            console.rule(f"[bold red]-[/] processing subject [yellow]{subject}[/]",align="left")
            # directly copy the copy for time-in-column, hh
            process = Prompt.ask("Process to apply for the subject",choices=["min","max","sum","mean","median","std","var","count"],default="mean")

            dupErr,redicious =  time_in_column(df_sub,dfAttrs,process,dataFileName.split(".")[0] + f"-{subject}.csv")
            if dupErr == False:
                df_sub,lossCountries = redicious # type(redicious) == tuple
                console.print("[yellow]Data overview[/] (non-empty):")
                console.print(df_sub)
                console.print(f"[yellow]Empty Data Countries[/] (dropped) [bold magenta]({len(lossCountries)})[/] (possibily originally empty):")
                console.print(lossCountries)
            else:
                df_dup = redicious
                console.print("[red]The Files contain duplicated Lines.[/] [yellow]Overview:[/]")
                console.print(df_dup)
                console.print("[*] Drop duplicated lines.")
                df = df.drop_duplicates(keep="first").reset_index(drop=True)
                console.print("[*] Reprocessing the file...")

                try:
                    dupErr,(df_sub,lossCountries) =  time_in_column(df_sub,dfAttrs,process,dataFileName.split(".")[0] + f"-{subject}.csv")
                except:
                    log.exception("[bold red] Please reexamine your data. Your data may contains contradictory lines (like functions whose x have multiple corresponding y)[/]")
                    exit(1)
                if dupErr == False:
                    console.print("[yellow]Data overview[/] (non-empty):")
                    console.print(df_sub)
                    console.print(f"[yellow]Empty Data Countries[/] (dropped) [bold magenta]({len(lossCountries)})[/] (possibily originally empty):")
                    console.print(lossCountries)

            cachePkls[dfAttrs["theme"] + f"_{subject}"] = df_sub.copy()
            cachePath = os.path.join(cacheFolder,dataFileName.split(".")[0] + f"_{subject}.csv")
            df_sub.to_csv(cachePath)
    
    if dfAttrs["dataFileType"] != "complex":
        cachePath = os.path.join(cacheFolder,dataFileName)
        cachePkls[dfAttrs["theme"]] = df.copy()
        df.to_csv(cachePath)

    console.print()
    input("[ENTER]")

    index += 1

# compose dataframes
console.clear()
console.rule("[bold red]Composing Data[/]")

datas = list(cachePkls.values()).copy()
sharedKeys = [key for key in datas[0].index if all(map(lambda x: key in list(x.index),datas))]
console.print(f"Here are [yellow]shared countries[/] [red]({len(sharedKeys)})[/] though all the data sheets:")
console.print(f"{sharedKeys}") # for dense view
input("[ENTER]")
console.print("[*] concating datas")
for i in range(len(datas)):
    data = datas[i]
    datas[i] = data[data.index.isin(sharedKeys)] # couldn't simply use data = data[...]
    
df_final = pd.concat(datas,axis=1)
df_final.columns = list(cachePkls.keys())
# df_final.reset_index(inplace=True)
console.print("[yellow]composed sheet[/]:")
console.print(df_final)

console.print()
input("[ENTER]")

cachePkls["COMPOSED"] = df_final.copy() # uppercase to avoid name contradictory
df_final.to_csv(os.path.join(cacheFolder,"COMPOSED.csv"))
df_final.to_csv(os.path.join(resultFolder,"COMPOSED.csv"))

# draw charts
console.clear()

chartFolder = os.path.join(resultFolder,"chart") 
if not os.path.exists(chartFolder):
    os.mkdir(chartFolder)
if Confirm.ask("Do you want to get the [red]heatmap[/] of the [yellow]correlation[/] between each variable(column)?"):
    console.print("[*] Using [yellow]pearson[/] correlation coefficient.")
    console.print("[*] Creating pairplot...")
    sns.pairplot(df_final,kind="reg")
    plt.savefig(os.path.join(chartFolder,"pairplot.png"),dpi=300)

    console.print("[*] Creating heatmap...")
    cmap_0 = "RdYlGn"
    cmap_1 = sns.diverging_palette(230, 20, as_cmap=True)
    cmap_2 = "YlGnBu"
    cmaps = [cmap_0,cmap_1,cmap_2]

    index = 0
    for cmap in cmaps:
        plt.figure(figsize=(16,10))
        relation = df_final.corr()
        sns.heatmap(relation,xticklabels=relation.columns,yticklabels=relation.columns,annot=True,cmap=cmap,center=0,annot_kws={"fontweight":"demibold"})
        plt.savefig(os.path.join(chartFolder,f"correlation_{index}.png"),dpi=300)
        index += 1

    console.print()
    input("[ENTER]")





# save cachePkl to cache/pkl folder
console.clear()
console.print("[*] Saving datas using pickcle...")

with console.status("[red]Saving datas using pickle[/]"):
    for key in cachePkls.keys():
        path = os.path.join(pklFolder,key + ".pkl")
        with open(path,"wb") as f:
            pickle.dump(cachePkls[key],f)
            console.print(f"save [yellow]{key}[/] done.")

# generate read pkl file
console.print()
pklFiles = [file for file in os.listdir(pklFolder) if file.endswith("pkl")]
with open(os.path.join(pklFolder,"readPkls.py"),"w",encoding='utf-8') as f:
    readPkls_code = """# Read Pkls
import pandas as pd
import pickle\n\n"""

    index = 0
    for key in pklFiles:
        readPkls_code += f"# df_{index}: {key}\n"
        index += 1

    index = 0
    for key in pklFiles:
        path = os.path.join(pklFolder,key)
        readPkls_code += f"""with open(r"{path}","rb") as f:
\tdf_{index} = pickle.load(f) #{key}\n\n"""
        index += 1
    f.write(readPkls_code)

console.print()
console.rule("[bold yellow]Afterword[/]")
console.print("[cyan]composed data file[/] is in the [yellow]result[/] folder.")
console.print("[cyan]charts[/] are in the [yellow]result/chart[/] folder.")
console.print("[cyan]processed data files[/] are in the [yellow]cache[/] folder.")
console.print("[cyan]expanded (according to time) data files[/] are in the [yellow]cache/expand[/] folder.")
console.print("[cyan]pkl files[/] are in the [yellow]cache/pkl[/] folder.")
