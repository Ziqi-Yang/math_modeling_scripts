from calendar import c
from collections.abc import Iterable
from concurrent.futures import process
import pandas as pd
import yaml
import pickle
import sys
import os
from rich.console import Console
from rich.prompt import Prompt, Confirm
from processFunc import time_expand,time_in_column,complex_data

import logging
from rich.logging import RichHandler
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")

console = Console()

rootPath = sys.path[0]
dataFolder = os.path.join(rootPath, "datas")
resultFolder = os.path.join(rootPath, "res")
cacheFolder = os.path.join(rootPath,"cache")
dataFilesNames = os.listdir(dataFolder)
dataFilesPath = list(map(lambda x: os.path.join(dataFolder, x), dataFilesNames))
dataFilesPath = [dataFilePath for dataFilePath in dataFilesPath if os.path.isfile(dataFilePath)] # shouldn't include folder
dataFilesNames = [os.path.basename(filename) for filename in dataFilesPath]

DATAS = dict()

console.clear()
console.print(f"Here are data files in the 'datas' folder:\n{dataFilesNames} ")

# load files
if Confirm.ask("[bold red]Important[/] Have you already pre-process (like [bold magenta]delete unneeded rows or columns[/]) those files in [bold cyan]Excel[/]?"):
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
    "theme": None
}  # single stands for no limit, but default is the word

index = 0
dataFilesNames = list(dataFilesAttrs.keys())
while index < len(dataFilesNames):
    dataFileName = dataFilesNames[index]
    console.rule(f"[bold magenta]{dataFileName}[/]")

    attrIndex = 0
    attrs = list(attrsChoice.keys())
    # for attr in list(attrsChoice.keys()):
    while attrIndex < len(attrs):
        attr = attrs[attrIndex]
        prompt = ""
        if attr == "countryColumnName":
            prompt = " (Leave [grey]empty[/] if first column)"
        elif attr == "theme":
            theme = dataFileName.split(".")[0]
            prompt = f" (used as a column name in composed data sheet, default [yellow]{theme}[/])"

        if attr == "timeColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] == "time-expand": # auto set value to None
            dataFilesAttrs[dataFileName][attr] = None
        elif attr == "subjectColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] != "complex": # auto set value to None
            dataFilesAttrs[dataFileName][attr] = None
        else:
            dataFilesAttrs[dataFileName][attr] = Prompt.ask(
                f"{attr}{prompt}",
                default=attrsChoice[attr][0]
                if isinstance(attrsChoice[attr], Iterable)
                else attrsChoice[attr],
                choices=attrsChoice[attr] if isinstance(attrsChoice[attr], list) else None,
            )

        dataFileType = dataFilesAttrs[dataFileName]["dataFileType"]
        if attr == "timeColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] in ["time-in-column","complex"] and dataFilesAttrs[dataFileName][attr] == None:
            console.print(
                f"[bold red]Warning[/] [yellow]{attr}[/] must be non-null value when [yellow]dataFileType[/] is set to [bold magenta]{dataFileType}[/]"
            )
            input("Please reset the attribution. [ENTER]")
            attrIndex -= 1
        elif attr == "subjectColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] in ["complex"] and dataFilesAttrs[dataFileName][attr] == None:
            console.print(
                f"[bold red]Warning[/] [yellow]{attr}[/] must be non-null value when [yellow]dataFileType[/] is set to [bold magenta]{dataFileType}[/]"
            )
            input("Please reset the attribution. [ENTER]")
            attrIndex -= 1
        elif attr == "countryColumnName" and dataFilesAttrs[dataFileName][attr] == None:
            dataFilesAttrs[dataFileName][attr] = DATAS[dataFileName].columns[0]
        elif attr == "theme" and dataFilesAttrs[dataFileName][attr] == None:
            dataFilesAttrs[dataFileName][attr] = dataFileName.split(".")[0]

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

    country_code_dict = dict(list(zip(fullname,alpha3)) + list(zip(alpha2,alpha3)))

    with open(country_code_dict_pkl_path,"wb") as f:
        pickle.dump(country_code_dict,f)

with open("country_code_dict.pkl","wb") as f:
    pickle.dump(country_code_dict,f)



# map Country Name to ISO 3661 and process datas
allMissingCountries = []
console.clear()
index = 0
cachePkls = [] # store process data objects

while index < len(dataFilesNames):
    dataFileName = dataFilesNames[index]
    console.rule(f"Processing [yellow]{dataFileName}[/]")

    df = DATAS[dataFileName]
    dfAttrs = dataFilesAttrs[dataFileName]
    df.rename(columns={dfAttrs["countryColumnName"]: "Country"},inplace=True)

    allCoutries = df["Country"].unique()
    console.print(f"[yellow]All entries[/]: {len(df.Country)} ; [yellow]All Countries Number[/]:{len(allCoutries)}")
    console.print(f"[yellow]All Countries[/]:")
    console.print(allCoutries)

    if all(map(lambda x: len(x) == 3,df["Country"])): # ISO 3661 alpha-3
        missingCountries = [] 
        missingEntriesNum = 0
    else:
        missingCountries = df[df["Country"].isin(country_code_dict.keys()) == False]["Country"].unique()
        df.loc[:,"Country"] = df["Country"].map(country_code_dict)
        missingEntriesNum = df["Country"].isna().sum()
        df = df[df["Country"].isna() == False]
    console.print("[*] Mapping ISO-3661 Country Code done.")

    console.print(f"[yellow]Missing entries[/]: {missingEntriesNum} ; [yellow]Missing Countries Number[/]: {len(missingCountries)}")
    console.print("[yellow]Missing Countries[/]:")
    console.print(missingCountries)

    console.print()
    cachePath = os.path.join(cacheFolder,dataFileName)
    # NOTICE process not defined
    if dfAttrs["dataFileType"] == "time-expand":
        process = Prompt.ask("Process to apply",choices=["min","max","sum","mean","median","std","var","count"],default="mean")
        df,lossCountries = time_expand(df,dfAttrs,process)
        console.print("[yellow]Data overview[/] (non-empty):")
        console.print(df)
        console.print(f"[yellow]Empty Data Countries[/] (dropped) [bold magenta]({len(lossCountries)})[/] (possibily originally empty):")
        console.print(lossCountries)
    elif dfAttrs["dataFileType"] == "time-in-column":
        time_in_column(df,dfAttrs,process)
    elif dfAttrs["dataFileType"] == "complex":
        complex_data(df,dfAttrs,process)

    cachePkls.append(df.copy())
    df.to_csv(cachePath)



    console.print()
    input("[ENTER]")


    index += 1
