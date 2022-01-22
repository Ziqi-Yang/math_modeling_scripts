from collections.abc import Iterable
import pandas as pd
import yaml
import pickle
import sys
import os
from rich.console import Console
from rich.prompt import Prompt, Confirm

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
dataFilesNames = os.listdir(dataFolder)
dataFilesPath = list(map(lambda x: os.path.join(dataFolder, x), dataFilesNames))
DATAS = dict()

console.clear()
console.print(f"Here are data files in the 'datas' folder:\n{dataFilesNames} ")

# load files
if Confirm.ask("Have you already pre-process (like [yellow]delete rows or columns[/]) those files in [bold cyan]Excel[/]?"):
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
    console.print("Unrecognized Files:")
    console.print(unrecognizedFiles)
    if not Confirm.ask("Whether to continute the program?"):
        exit(0)




# set attribution for each files, respectfully
console.clear()
console.print("Please set suitable attribution for each data file:")

dataFilesAttrs = {dataFileName: dict() for dataFileName in DATAS.keys()}
attrsChoice = {
    "dataFileType": ["time-expand", "time-in-column"],
    "timeColumnName": None,
}  # single stands for no limit, but default is the word

index = 0
dataFilesNames = list(dataFilesAttrs.keys())
while index < len(dataFilesNames):
    dataFileName = dataFilesNames[index]
    console.rule(f"[bold magenta]{dataFileName}[/]")
    for attr in list(attrsChoice.keys()):
        if attr == "timeColumnName" and dataFilesAttrs[dataFileName]["dataFileType"] != "time-in-column":
            dataFilesAttrs[dataFileName][attr] = None
        else:
            dataFilesAttrs[dataFileName][attr] = Prompt.ask(
                f"{attr}",
                default=attrsChoice[attr][0]
                if isinstance(attrsChoice[attr], Iterable)
                else attrsChoice[attr],
                choices=attrsChoice[attr] if isinstance(attrsChoice[attr], list) else None,
            )

    if (
        dataFilesAttrs[dataFileName]["dataFileType"] == "time-in-column"
        and dataFilesAttrs[dataFileName]["timeColumnName"] == None
    ):
        console.print(
            "[bold red]Warning[/] [yellow]timeColumnName[/] must be non-value value when [yellow]dataFileType[/] is set to [magenta]time-in-column[/]"
        )
        input("Please reset the attribution of this file.")
        index -= 1

    index += 1

hasProb = True
while hasProb:
    console.clear()
    console.rule(f"[bold red]Attribution Viewer[/]")
    console.print(dataFilesAttrs)
    hasProb = Confirm.ask("Has [bold red]problems[/] in the Attributions?")
    if not hasProb:
        break
    tmpConfigPath = os.path.join(rootPath,"tmpConfig.yaml")
    with open(tmpConfigPath,"w",encoding="utf-8") as f:
        yaml.dump(dataFilesAttrs,f,allow_unicode=True)
    console.print(f"Please edit the config file '[yellow]{os.path.basename(tmpConfigPath)}[/]' which is in the same folder with the program.",end="")
    input()
    console.print("Reading attributions...")
    with open(tmpConfigPath,encoding="utf-8") as f:
        dataFilesAttrs = yaml.load(f,Loader=yaml.FullLoader)

