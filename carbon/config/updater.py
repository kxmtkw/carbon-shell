from pathlib import Path

from .getter import CarbonConfig, ConfigGetter
from .defaults import ConfigDefaults

from carbon.theme import Theme
from carbon.helpers import run, CarbonError

class ConfigUpdater:

    def __init__(self, config: ConfigGetter):
        self.config = config

    def update(self):
        self.update_theme()
        self.update_hyprland_defaults()

    def update_theme(self):
        
        source = self.config.get("theme.source", ConfigDefaults.wallpaper, valid_types=(str,), valid_values=["wallpaper", "hex"])

        wallpaper = self.config.get("theme.wallpaper", ConfigDefaults.wallpaper, valid_types=(str,))
        hex = self.config.get("theme.hex", ConfigDefaults.hex, valid_types=(str,))

        mode = self.config.get("theme.mode", ConfigDefaults.mode, valid_types=(str,), valid_values=("dark", "light"))
        variant = self.config.get("theme.variant", ConfigDefaults.variant, valid_types=(str,), valid_values=("ash", "graphite", "diamond", "coal"))
        contrast = self.config.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))

        Theme.set_wallpaper(wallpaper)

        if source == "wallpaper":
            Theme.change_color_theme(mode, variant, img=wallpaper, contrast=contrast)
        else:
            Theme.change_color_theme(mode, variant, hex=hex, contrast=contrast)

        face = self.config.get("theme.face", ConfigDefaults.face, valid_types=(str,))

        if Path(face).expanduser().exists():
            run(f"cp {face} ~/.carbon/user/face")
        else:
            CarbonError(f"Face file does not exist: {face}").halt()


        font = self.config.get("theme.font", ConfigDefaults.font, valid_types=(str,))
        Theme.set_font(font)


    def update_hyprland_defaults(self):

        config_str = ""

        terminal = self.config.get("defaults.terminal", None, valid_types=(str,))

        if terminal:
            config_str += f"$default_terminal = '{terminal}'\n"

        user_dir = Path("~/.config/hypr/user").expanduser()

        if not user_dir.exists():
            run("mkdir ~/.config/hypr/user")

        with open(user_dir.joinpath("default.conf"), "w") as file:
            file.write(config_str)


    def notify(self):
        run("notify-send -a 'Carbon Shell' 'Config Reloaded'")

            

        
