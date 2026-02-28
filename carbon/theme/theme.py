import subprocess
import time
from typing import Literal
from pathlib import Path
import json

from carbon.helpers import Color, CarbonError
from carbon.helpers.settings import SettingsLoader
from .material import MaterialColors
from . import configs  

from carbon.state import CarbonState

settings = SettingsLoader("~/.carbon/settings/colors.toml")
carbon_path = Path("~/.carbon").expanduser()

def write_theme(filepath: str, theme: str):
    abspath = carbon_path.joinpath(filepath)
    with open(abspath, "w") as file:
        file.write(theme)


def write_dunst_theme(dunstrc: str, theme: str):
    abspath = carbon_path.joinpath(dunstrc)
    with open(abspath, "r") as file:
        contents = file.read()

    breakpoint = "CARBON_BREAK_POINT"

    parts = contents.split(breakpoint)

    updated = f"{parts[0]}{breakpoint}\n{theme}"

    with open(abspath, "w") as file:
        file.write(updated)
    

def update_colors(colors: dict[str, str]):

    for type, filepath in settings.get("colorfiles").items():
        
        match type:
            case "hypr":
                string = configs.update_hypr(colors)
                write_theme(filepath, string)
            case "qml":
                string = configs.update_quickshell(colors)
                write_theme(filepath, string)
            case "kitty":
                string = configs.update_kitty(colors)
                write_theme(filepath, string)
            case "rofi":
                string = configs.update_rofi(colors)  
                write_theme(filepath, string)  
            case "alacritty":
                string = configs.update_alacritty(colors)
                write_theme(filepath, string)   
            case "kde":
                string = configs.update_kde(colors) 
                write_theme(filepath, string)
            case "dunst":
                string = configs.update_dunst(colors)
                write_dunst_theme(filepath, string)
            case _:
                print(f"Error :: {type}")
                continue
        
        print(f"Updated :: {type}")


    for cmd in settings.get("commands"):
        print(f"Running cmd: {cmd}")
        out = subprocess.run(cmd, shell=True, capture_output=True)



class Theme:

    ## update the wallpaper state in carbon.state

    output = subprocess.run("swww query | grep -oP '(?<=image: ).*'", shell=True, capture_output=True, text=True)
    CarbonState.set("theme_wallpaper", output.stdout.strip())

    @classmethod
    def change_color_theme(
        cls,
        theme: Literal["dark", "light"],
        variant: str,
        img: str,
        *,
        contrast: float | None = None,
        ):

        if contrast is None:
            contrast = 0.25

        match variant:
            case "ash":
                theme_variant = MaterialColors.Variant.ash
            case "coal":
                theme_variant = MaterialColors.Variant.coal
            case "graphite":
                theme_variant = MaterialColors.Variant.graphite
            case "diamond":
                theme_variant = MaterialColors.Variant.diamond
            case _:
                theme_variant = MaterialColors.Variant.graphite

        colors = MaterialColors()
        
        colors.generate_from_image(img, contrast, theme_variant)

        if theme == "light":
            update_colors(colors.lightMapping)
        elif theme == "dark":
            update_colors(colors.darkMapping)
        else:
            CarbonError().throw("Invalid theme!").halt()


        cache = Path("~/.carbon/cache").expanduser()

        if not cache.exists():
            CarbonError(f"Cache dir not found :: {cache}.\nSomething is really really wrong.")

        with open(cache.joinpath("darktheme.json"), "w") as file:
            json.dump(colors.darkMapping, file, indent=4)

        with open(cache.joinpath("lighttheme.json"), "w") as file:
            json.dump(colors.lightMapping, file, indent=4)


        CarbonState.set("theme_wallpaper", str(img))
        CarbonState.set("theme_contrast", contrast)
        CarbonState.set("theme_variant", variant)           


    @classmethod
    def switch_theme_mode(cls, color: Literal["dark", "light"]):
        
        cache = Path("~/.carbon/cache").expanduser()

        if not cache.exists():
            CarbonError(f"Cache dir not found :: {cache}.\nSomething is really really wrong. Cannot switch without cached themes.").halt()


        if CarbonState.get("theme_mode", str) == color:
            print("Mode already active.")
            exit()

        
        if color == "dark":
            dark_path = cache.joinpath("darktheme.json")
            
            if not dark_path.exists():
                CarbonError(f"Color file not found :: {dark_path}.\nSomething is really really wrong. Cannot switch without cached themes.").halt()

            with open(dark_path, "r") as file:
                mapping = json.load(file)

            update_colors(mapping)

        else:

            light_path = cache.joinpath("lighttheme.json")
            
            if not light_path.exists():
                CarbonError(f"Color file not found :: {light_path}.\nSomething is really really wrong. Cannot switch without cached themes.").halt()

            with open(light_path, "r") as file:
                mapping = json.load(file)

            update_colors(mapping)


        CarbonState.set("theme_mode", color)


    @classmethod
    def set_wallpaper(cls, img: str):

        img_path = Path(img).expanduser()

        if not img_path.exists():
            CarbonError(f"File not found :: {img_path}").halt()

        output = subprocess.run(f"swww img {img_path}", shell=True, capture_output=True, text=True)
        
        if output.returncode != 0:
            CarbonError(f"Failed to change wallpaper :: {output.stderr}").halt()
