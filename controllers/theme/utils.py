from pathlib import Path
import subprocess

from carbon.config import CarbonConfig
from carbon.config.defaults import ConfigDefaults
from carbon.helpers import CarbonError
from carbon.rofi import RofiShell



def get_wallpapers():

    wallpapers: list[str] = []

    # Getting Wallpaper Source dirs
    wallpaper_paths: list[Path] = []

    wallpaper_dirs = CarbonConfig.get("defaults.wallpaperSource", ConfigDefaults.wallpaperSource, valid_types=(str, list))

    # Adding paths
    if isinstance(wallpaper_dirs, str):
        wallpaper_paths.append(Path(wallpaper_dirs).expanduser())
    else:
        for item in wallpaper_dirs:
            if not isinstance(item, str): continue
            wallpaper_paths.append(Path(item).expanduser())

    # Checking paths
    for item in wallpaper_paths:
        if not item.exists():
            CarbonError(f"Wallpaper source directory does not exist: '{item.absolute}' ")
            continue

        if not item.is_dir():
            CarbonError(f"Wallpaper source is not a directory: '{item.absolute}' ")

        images = get_images(item)

        wallpapers.extend(images)

    wallpapers.sort()


    return wallpapers


def get_images(directory: Path) -> list[str]:

    images = []
    
    for item in directory.iterdir():
        if item.is_file():
            absolute = item.absolute()
            option = RofiShell.markWithIcon(absolute, absolute)
            images.append(option)

    return images


valid_chars = set("0123456789abcdefABCDEF")

def is_valid_hex(hex_string: str) -> bool:
    
    hex_string = hex_string.strip()

    if not hex_string.startswith("#"):
        return False
    
    h = hex_string.lstrip("#")

    return len(h) in (3, 6) and all(c in valid_chars for c in h)


def is_valid_number(num_string: str) -> bool:

    try:
        float(num_string)
        return True
    except ValueError:
        return False
    

# todo: add cache system
def get_fonts() -> list[str]:

    output = subprocess.run("fc-list --format='%{family[0]}\n' | sort | uniq", shell=True, capture_output=True, text=True)

    fonts = []
    if output.returncode != 0: return fonts

    for item in output.stdout.splitlines():
        font_entry = f"<span font='{item}'>{item}</span>"
        fonts.append(font_entry)

    return fonts


def extract_font_from_rofi(selected: str) -> str:

    part = selected.split(">")[1].split("<")[0]

    return part.title()
