## Configuration

The shell is configured using toml. The configuration file is located at `~/.carbon/config.toml`.

Here are different sections in the configuration file.

### Defaults

``` toml
[defaults]
# default terminal
terminal = "alacritty" 

# Source Directory for wallpapers
# Can be a single path or a list of paths
wallpaperSource = [
    "~/Pictures", "~/Images"
]
```

### Theming

```toml
[theme]

# Profile Picture. 
face = "~/.carbon/assets/default_face.jpg"

# Theme color source
# Valid values: wallpaper, hex
source = "wallpaper" 

# Applied wallpaper. ~ supported.
wallpaper = "~/.carbon/assets/default_wallpaper.jpg"

# Color for when source is "hex"
hex = "#397cc4"

# Theme mode. 
# Valid values: dark, light
mode = "light"

# Theme variants. 
# Valid values: ash, coal, graphite, diamond
variant = "graphite"

# Theme contrast
contrast = 0.5

# Font
font = "Iosevka"
```

### Colorfiles

``` toml
[colorfiles]

hypr      = "~/.carbon/hypr/color.conf"
kitty     = "~/.config/kitty/color.conf"
alacritty = "~/.config/alacritty/color.toml"
```