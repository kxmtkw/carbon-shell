import material_color_utilities as material
from PIL import Image
from pathlib import Path
import json

from misc import Color, CarbonError

import sys


class MaterialColors:


    class Variant:
        ash      = (0.1, material.Variant.VIBRANT)
        coal     = (0.2, material.Variant.MONOCHROME)
        graphite = (0.2, material.Variant.TONALSPOT)
        diamond  = (2, material.Variant.VIBRANT)


    def __init__(self):
        self.darkScheme: material.DynamicScheme 
        self.lightScheme: material.DynamicScheme

        self.darkMapping: dict[str, str]
        self.lightMapping: dict[str, str]

        self._contrast: float = 0
        self._variant = 0


    def generateFromImage(self, image: str, variant: tuple):

        if not Path(image).exists():
            CarbonError().throw(f"Image not found: {image}").halt()

        theme = material.theme_from_image(Image.open(image), variant[0], variant[1])

        self.darkScheme = theme.schemes.dark
        self.lightScheme = theme.schemes.light

        self.darkMapping = self.make_mapping(self.darkScheme)
        self.lightMapping = self.make_mapping(self.lightScheme)


    def generateFromColor(self, color: str, variant: tuple):

        theme = material.theme_from_color(color, variant[0], variant[1])

        self.darkScheme = theme.schemes.dark
        self.lightScheme = theme.schemes.light

        self.darkMapping = self.make_mapping(self.darkScheme)
        self.lightMapping = self.make_mapping(self.lightScheme)


    def make_mapping(self, s: material.DynamicScheme) -> dict[str, str]:
        scheme = {
            "background": s.background,
            "surface": s.surface,
            "surface_dim": s.surface_dim,
            "surface_bright": s.surface_bright,
            "surface_container_lowest": s.surface_container_lowest,
            "surface_container_low": s.surface_container_low,
            "surface_container": s.surface_container,
            "surface_container_high": s.surface_container_high,
            "surface_container_highest": s.surface_container_highest,
            "on_surface": s.on_surface,
            "surface_variant": s.surface_variant,
            "on_surface_variant": s.on_surface_variant,
            "inverse_surface": s.inverse_surface,
            "inverse_on_surface": s.inverse_on_surface,
            "outline": s.outline,
            "outline_variant": s.outline_variant,
            "shadow": s.shadow,
            "scrim": s.scrim,
            "surface_tint": s.surface_tint,

            "primary": s.primary,
            "on_primary": s.on_primary,
            "primary_container": s.primary_container,
            "on_primary_container": s.on_primary_container,
            "inverse_primary": s.inverse_primary,

            "secondary": s.secondary,
            "on_secondary": s.on_secondary,
            "secondary_container": s.secondary_container,
            "on_secondary_container": s.on_secondary_container,

            "tertiary": s.tertiary,
            "on_tertiary": s.on_tertiary,
            "tertiary_container": s.tertiary_container,
            "on_tertiary_container": s.on_tertiary_container,

            "error": s.error,
            "on_error": s.on_error,
            "error_container": s.error_container,
            "on_error_container": s.on_error_container,

            "primary_fixed": s.primary_fixed,
            "primary_fixed_dim": s.primary_fixed_dim,
            "on_primary_fixed": s.on_primary_fixed,
            "on_primary_fixed_variant": s.on_primary_fixed_variant,

            "secondary_fixed": s.secondary_fixed,
            "secondary_fixed_dim": s.secondary_fixed_dim,
            "on_secondary_fixed": s.on_secondary_fixed,
            "on_secondary_fixed_variant": s.on_secondary_fixed_variant,

            "tertiary_fixed": s.tertiary_fixed,
            "tertiary_fixed_dim": s.tertiary_fixed_dim,
            "on_tertiary_fixed": s.on_tertiary_fixed,
            "on_tertiary_fixed_variant": s.on_tertiary_fixed_variant,
        }

        return scheme
    


COLORS = Path("~/.carbon/info/colors.json").expanduser()


def loadColors() -> dict[str, str]:

    if not COLORS.exists():
        CarbonError().throw(f"Color file '{COLORS}' does not exist!").halt()

    with open(COLORS) as file:
        config = json.load(file)

    return config


def updateKitty(s: dict[str, str]):

    material.Hct

    base = (
        "// NOTE: written by carbon shell\n" 
        f"selection_foreground     {s["on_surface"]}\n"
        f"selection_background     {s["surface_container_highest"]}\n"
        f"active_border_color      {s["on_surface"]}\n"
        f"inactive_border_color    {s["on_surface"]}\n"
        f"active_tab_foreground    {s["on_surface"]}\n"
        f"active_tab_background    {s["surface_container"]}\n"
        f"inactive_tab_foreground  {s["on_surface"]}\n"
        f"inactive_tab_background  {s["background"]}\n"
        f"background               {s["background"]}\n"
        f"foreground               {s["on_surface"]}\n"
        f"color0                   #323234\n"
        f"color1                   #b3261e\n"
        f"color2                   #1b6b44\n"
        f"color3                   #7f5700\n"
        f"color4                   #005ac1\n"
        f"color5                   #7b1fa2\n"
        f"color6                   #006a6a\n"
        f"color7                   #e6e1e5\n"
        f"color8                   #49454f\n"
        f"color9                   #ff5449\n"
        f"color10                  #4fd8a0\n"
        f"color11                  #ffb74d\n"
        f"color12                  #6f9cff\n"
        f"color13                  #ce93d8\n"
        f"color14                  #4dd0e1\n"
        f"color15                  #ffffff\n"
        f"cursor                   {s["on_surface"]}\n"
        f"cursor_text_color        {s["on_surface"]}\n"
        f"url_color                {s["tertiary"]}\n"
    )

    return base


def updateHypr(s: dict[str, str]):
    outline = s["outline"][1:]

    base = (
        "# NOTE: written by carbon shell\n"
        f"$border_active = rgb({outline})\n"
        f"$border_inactive = rgba({outline}40)\n"
    )

    return base


def updateRofi(s: dict[str, str]):
    base = (
        "// NOTE: written by carbon shell\n"
        "* {\n"
        f"background:                     {s["background"]};\n"
        f"surfaceContainer:               {s["surface_container"]};\n"
        f"onSurface:                      {s["on_surface"]};\n"
        f"surfaceContainerHigh:           {s["surface_container_high"]};\n"
        f"surfaceContainerHighest:        {s["surface_container_highest"]};\n"
        f"outline:                        {s["outline"]};\n"
        f"primary:                        {s["primary"]};\n"
        f"onPrimary:                      {s["on_primary"]};\n"
        "}"
    )

    return base


def updateQuickshell(s: dict[str, str]) -> str:
    base = """
    // NOTE: written by carbon shell
    pragma Singleton

    import QtQuick
    import Quickshell

    Singleton 
    {
    property color invisible					 : "#00000000"\n
    """

    for name, val in s.items():
        base += f"property color {name:<30}: \"{val}\"\n"

    base += "\n}"

    return base

   

def updateColors(colors: dict[str, str]):
    color_files = loadColors()

    for type, filepath in color_files.items():
        
        match type:
            case "hypr":
                string = updateHypr(colors)
            case "qml":
                string = updateQuickshell(colors)
            case "kitty":
                string = updateKitty(colors)
            case "rofi":
                string = updateRofi(colors)    
            case _:
                print(f"Error :: {type}")
                continue
        
        with open(filepath, "w") as file:
            file.write(string)

        print(f"Updated :: {type}")



def main():
    
    if len(sys.argv) != 5:
        CarbonError().throw(
            "Insufficient arguments. Need: dark/light -i image / -c hexcolor variant[ash/coal/graphite/diamond]"
        ).halt()

    theme = sys.argv[1]
    option = sys.argv[2]
    source = sys.argv[3]
    variant = sys.argv[4]

    theme_variant: tuple[float, str]

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
            CarbonError().throw("Invalid variant[ash/coal/graphite/diamond]").halt()

    if option == "-i":
        colors = MaterialColors()
        colors.generateFromImage(source, theme_variant)

        if theme == "light":
            updateColors(colors.lightMapping)
        elif theme == "dark":
            updateColors(colors.darkMapping)
        else:
            CarbonError().throw("Invalid theme!").halt()

    elif option == "-c":
        colors = MaterialColors()
        colors.generateFromColor(source, theme_variant)

        if theme == "light":
            updateColors(colors.lightMapping)
        elif theme == "dark":
            updateColors(colors.darkMapping)
        else:
            CarbonError().throw("Invalid theme!").halt()

    info = f"Color Info :: theme:{theme} {'image' if option == "-i" else 'color'}:{source} variant:{variant}"
    print(info)

if __name__ == "__main__":
    main()