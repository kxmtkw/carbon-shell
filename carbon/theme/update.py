import subprocess
from pathlib import Path

from carbon.config.getter import CarbonConfig

from . import configs

carbon_path = Path("~/.carbon").expanduser()


def write_theme(filepath: str, theme: str) -> None:
    abspath = Path(filepath).expanduser()

    if not abspath.parent.exists():
        abspath.parent.mkdir(511, True, True)

    with open(abspath, "w") as file:
        file.write(theme)


def update_colors(colors: dict[str, str]) -> None:

    colorfiles = CarbonConfig.get("colorfiles", {}, valid_types=dict)

    shellfiles = {}
    shellfiles["rofi"] = "~/.carbon/shell/rofi/Config/color.rasi"
    shellfiles["json"] = "~/.carbon/shell/quickshell/Config/color.json"
    shellfiles["kde"]  = "~/.local/share/color-schemes/Carbon.colors"

    shellfiles.update(colorfiles)

    for type, filepath in shellfiles.items():

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

        print(f"Updated :: {type}")

    print(f":: Running post theme commands")

    commands = [
        "plasma-apply-colorscheme BreezeDark && plasma-apply-colorscheme Carbon",
        "hyprctl reload",
        "quickshell --config ~/.carbon/shell/quickshell ipc call theme update",
    ]

    for cmd in commands:
        subprocess.run(cmd, shell=True, capture_output=True)
