import subprocess
from typing import Literal
from pathlib import Path
import json

from carbon.helpers import Color, CarbonError
from carbon.settings import SettingsLoader
from .material import MaterialColors
from . import configs  

settings = SettingsLoader("~/.carbon/settings/colors.toml")

def write_theme(filepath: str, theme: str):
    with open(filepath, "w") as file:
        file.write(theme)


def write_dunst_theme(dunstrc: str, theme: str):
    with open(dunstrc, "r") as file:
        contents = file.read()

    breakpoint = "CARBON_BREAK_POINT"

    parts = contents.split(breakpoint)

    updated = f"{parts[0]}{breakpoint}\n{theme}"

    with open(dunstrc, "w") as file:
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
        subprocess.run(cmd, shell=True, capture_output=True)


def colorify(
    theme: Literal["dark", "light"],
    variant: str,
    img: str | None = None,
    hex: str | None = None,
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
    
    if img:
        colors.generate_from_image(img, contrast, theme_variant)

        if theme == "light":
            update_colors(colors.lightMapping)
        elif theme == "dark":
            update_colors(colors.darkMapping)
        else:
            CarbonError().throw("Invalid theme!").halt()

    elif hex:
        colors.generate_from_color(hex, contrast, theme_variant)

        if theme == "light":
            update_colors(colors.lightMapping)
        else:
            update_colors(colors.darkMapping)

    cache = Path("~/.carbon/cache").expanduser()
    if not cache.exists():
        CarbonError(f"Cache dir not found :: {cache}.\nSomething is really really wrong.")

    with open(cache.joinpath("darktheme.json"), "w") as file:
        json.dump(colors.darkMapping, file, indent=4)

    with open(cache.joinpath("lighttheme.json"), "w") as file:
        json.dump(colors.lightMapping, file, indent=4)


def switch_theme(color: Literal["dark", "light"]):

    cache = Path("~/.carbon/cache").expanduser()

    if not cache.exists():
        CarbonError(f"Cache dir not found :: {cache}.\nSomething is really really wrong. Cannot switch without cached themes.").halt()


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

        
def set_wallpaper(
    theme: Literal["dark", "light"],
    variant: str,
    img: str,
    contrast: float | None
    ):

    img_path = Path(img).expanduser()

    if not img_path.exists():
        CarbonError(f"File not found :: {img_path}").halt()

    output = subprocess.run(f"swww img {img_path}", shell=True, capture_output=True, text=True)
    
    if output.returncode != 0:
        CarbonError(f"Failed to change wallpaper :: {output.stderr}").halt()

    colorify(theme, variant, img, None, contrast)