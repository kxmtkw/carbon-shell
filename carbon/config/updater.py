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

    def update_theme(self):
        
        wallpaper = self.config.get("theme.wallpaper", ConfigDefaults.wallpaper, valid_types=(str,))
        mode = self.config.get("theme.mode", ConfigDefaults.mode, valid_types=(str,), valid_values=("dark", "light"))
        variant = self.config.get("theme.variant", ConfigDefaults.variant, valid_types=(str,), valid_values=("ash", "graphite", "diamond", "coal"))
        contrast = self.config.get("theme.contrast", ConfigDefaults.contrast, valid_types=(float, int))

        Theme.set_wallpaper(wallpaper)
        Theme.change_color_theme(mode, variant, wallpaper, contrast=contrast)

        face = self.config.get("theme.face", ConfigDefaults.wallpaper, valid_types=(str,))

        if Path(face).expanduser().exists():
            run(f"cp {face} ~/.carbon/user/face")
        else:
            CarbonError(f"Face file does not exist: {face}").halt()
            

        
