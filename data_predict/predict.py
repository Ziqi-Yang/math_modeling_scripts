import pandas as pd
import matplotlib.pyplot as plt
from rich import console
import seaborn as sns
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

console.clear()
console.rule("[bold red]Initialization[/]")
console.print("This program can help you generate [yellow]pridicted datas and map[/] from data sheets.")
console.print("It also supports [yellow]multiple countries[/] comparison.")

