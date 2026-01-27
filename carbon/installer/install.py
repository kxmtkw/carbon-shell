import subprocess
from pathlib import Path
import json
import shutil

from carbon.helpers import Color, CarbonError, prompt

from carbon.colors import colorify

CONFIG = Path("info/config.json")


def loadConfig() -> list[dict[str, str]]:

    if not CONFIG.exists():
        CarbonError(f"Config file '{CONFIG}' does not exist!").halt()

    with open(CONFIG) as file:
        config = json.load(file)

    return config["config"]


def link(src: Path, dest: Path):

    Color.Print(f"Moving :: {src.name}", Color.white)

    dest = dest.expanduser()

    if not src.exists():
        CarbonError(f"Config Src '{src}' does not exist!").halt()
        
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

    cache = Path("~/.carbon/cache").expanduser()
    cache.mkdir(exist_ok=True)
    Color.Print(f"Created cache :: {cache}", Color.green)

    for file in config_files:
        link(Path(file["src"]), Path(file["dest"]))

        if Path(file["src"]).name == "hypr":
            subprocess.run("hyprctl reload", shell=True, capture_output=True)

    # default theme
    colorify("dark", "graphite", None, "#4169e1")
    
    Color.Print("Installation complete!", Color.blue)
