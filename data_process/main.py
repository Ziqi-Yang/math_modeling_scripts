from collections.abc import Iterable
from compileall import compile_file
from distutils.command.config import config
import pandas as pd
import pickle
import sys
import os
from pyparsing import Combine
from rich.console import Console
from rich.prompt import Prompt,Confirm

console = Console()

rootPath = sys.path[0]
dataFolder = os.path.join(rootPath,"datas")
resultFolder = os.path.join(rootPath,"res")
dataFilesNames = os.listdir(dataFolder)
dataFiles = list(map(lambda x: os.path.join(dataFolder,x),dataFilesNames))
# dataFileTypeFunc ={"Expand":}

console.print(f"Here are data files in the 'datas' folder:\n{dataFilesNames} ")
console.print("Please set suitable attribution for each data file:")

dataFilesAttrs = {dataFileName: dict() for dataFileName in dataFilesNames}
attrsChoice = {"dataFileType":["time-expand","time-in-column"],"timeColumn": None,} # single stands for no limit, but default is the word

for dataFileName in dataFilesNames:
    console.rule(f"[bold magenta]{dataFileName}[/]")
    for attr in list(attrsChoice.keys()):
        dataFilesAttrs[dataFileName][attr] = Prompt.ask(f"{attr}",default=attrsChoice[attr][0] if isinstance(attrsChoice[attr],Iterable) else attrsChoice[attr],choices=attrsChoice[attr] if isinstance(attrsChoice[attr],list) else None)
console.clear()
console.rule(f"[bold red]Attribution Viewer[/]")
console.print(dataFilesAttrs)

hasProb = Confirm.ask("Has [bold red]problems[/] in the Attributions?")