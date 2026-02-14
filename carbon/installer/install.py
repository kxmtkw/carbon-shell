import subprocess
from pathlib import Path
import json
import shutil

from carbon.helpers import Color, CarbonError, prompt
from carbon.settings import SettingsLoader

from carbon.colors import colorify

settings = SettingsLoader("~/.carbon/settings/configs.toml")



def link(src: Path, dest: Path):

    Color.Print(f"Moving :: {src.name}", Color.white)

    dest = dest.expanduser()

    if not src.exists():
        CarbonError(f"Config Src '{src}' does not exist!").halt()
        
    if dest.is_symlink():
        dest.unlink()
        
    elif dest.exists(follow_symlinks=True):

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
    else: 
        parent = dest.parent
        if not parent.exists(follow_symlinks=True):
            parent.mkdir(parents=True, exist_ok=True)

        
    dest.symlink_to(src.absolute(), src.is_dir())

    Color.Print(f"Symlinked :: {dest} -> {src}", Color.green)


def installCarbon():

    Color.Print("Installing carbon shell...", Color.blue)

    cache = Path("~/.carbon/cache").expanduser()
    cache.mkdir(exist_ok=True)
    Color.Print(f"Created cache :: {cache}", Color.green)

    colorify('dark', "graphite", None, "#84d0d9") # default theme, will move this later

    for name, details  in settings.get().items():

        item_settings = SettingsLoader(details)

        link(Path(item_settings.get("src")), Path(item_settings.get("dest")))

        if name == "hypr":
            subprocess.run("hyprctl reload", shell=True, capture_output=True)

   
    Color.Print("Installation complete!", Color.blue)
