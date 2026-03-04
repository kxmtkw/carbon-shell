import subprocess
from pathlib import Path

from carbon.helpers.settings import SettingsLoader

from . import configs

settings = SettingsLoader("~/.carbon/settings/colors.toml")
carbon_path = Path("~/.carbon").expanduser()


def write_theme(filepath: str, theme: str) -> None:
    abspath = carbon_path.joinpath(filepath)
    with open(abspath, "w") as file:
        file.write(theme)


def update_colors(colors: dict[str, str]) -> None:
    for type, filepath in settings.get("colorfiles").items():

        filepath = Path(filepath).expanduser()

        match type:
            case "hypr":
                string = configs.update_hypr(colors)
                write_theme(filepath, string)
            case "json":
                string = configs.update_json(colors)
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
            case _:
                print(f"Error :: {type}")
                continue

        print(f"Updated :: {filepath}")

    for cmd in settings.get("commands"):
        print(f"Running cmd: {cmd}")
        subprocess.run(cmd, shell=True, capture_output=True)
