import json
import subprocess
from pathlib import Path
from typing import Literal

from carbon.helpers import CarbonError
from carbon.config import CarbonConfig

from .material import MaterialColors
from .update import update_colors


class Theme:

    ## update the wallpaper state in carbon.state

    #output = subprocess.run("swww query | grep -oP '(?<=image: ).*'", shell=True, capture_output=True, text=True)
    #CarbonConfig.set("theme_wallpaper", output.stdout.strip())

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
        
        colors.generate_from_image(Path(img).expanduser(), contrast, theme_variant)

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
      


    @classmethod
    def switch_theme_mode(cls, color: Literal["dark", "light"]):
        
        cache = Path("~/.carbon/cache").expanduser()

        if not cache.exists():
            CarbonError(f"Cache dir not found :: {cache}.\nSomething is really really wrong. Cannot switch without cached themes.").halt()


        if CarbonConfig.get("theme.mode", str) == color:
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




    @classmethod
    def set_wallpaper(cls, img: str):

        img_path = Path(img).expanduser()

        if not img_path.exists():
            CarbonError(f"File not found :: {img_path}").halt()

        output = subprocess.run(["swww", "img", "--transition-type", "outer", img_path],capture_output=True, text=True)
        
        if output.returncode != 0:
            CarbonError(f"Failed to change wallpaper :: {output.stderr}").halt()
