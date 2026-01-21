import subprocess
from pathlib import Path
import json
import shutil

from .misc import Color, CarbonError, prompt

mShellError = CarbonError

CONFIG = Path("info/config.json")


def loadConfig() -> list[dict[str, str]]:

    if not CONFIG.exists():
        mShellError().throw(f"Config file '{CONFIG}' does not exist!").halt()

    with open(CONFIG) as file:
        config = json.load(file)

    return config["config"]


def link(src: Path, dest: Path):

    Color.Print(f"Moving :: {src.name}", Color.white)

    dest = dest.expanduser()

    if not src.exists():
        mShellError().throw(f"Config Src '{src}' does not exist!").halt()
        
    if dest.is_symlink():
        dest.unlink()
        
    elif dest.exists():

        choice = prompt(
            f"{dest} already exists! Do you want to remove it?",
            ["y", "n"]
        )

        if choice == "y":

            Color.Print(f"Removing {dest}", Color.yellow)
            if dest.is_file():
                dest.unlink()
            elif dest.is_dir():
                shutil.rmtree(dest)

        else:
            Color.Print(f"Skipped {dest}", Color.yellow)
            return
        
    dest.symlink_to(src.absolute(), src.is_dir())

    Color.Print(f"Symlinked :: {dest} -> {src}", Color.green)


def installCarbon():

    config_files = loadConfig()

    Color.Print("Installing carbon shell...", Color.blue)

    for file in config_files:
        link(Path(file["src"]), Path(file["dest"]))

        if Path(file["src"]).name == "hypr":
            subprocess.run("hyprctl reload", shell=True, capture_output=True)

    
    Color.Print("Installation complete!", Color.blue)


    
def uninstallCarbon():
    pass