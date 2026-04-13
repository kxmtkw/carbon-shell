
# Carbon Shell

Carbon shell is designed to be a simple and functional desktop shell.
Though the shell is currently designed for `Hyprland` only and includes a config, It is possible to use this shell with other compositors through some hacks.

### Overview

If the features were to be summarized, they would include:

- `Panel`
- `Lockscreen`
- `Power Menu`
- `Launcher`
- `Screenshot Util`
- `Wifi Menu`
- `Theming Menu`
- `Clipboard Util`
- `Essential Desktop Apps from KDE` (Optional)
- `Hypr configuration`
- `Complete desktop theming`
- `Notifications`
- `Nightlight`

## Hyprland

The shell comes with hyprland and its utilities. This includes:

+ `Main Config`
+ `Hyprlock Config`
+ `Hyprsunset Config`
+ `Hypridle Config`


### Overriding

These files are locked and they shouldn't be modified. If you want to `make changes` to hyprland then:

+ `Use hyprviz` This is a GUI tool for hyprland config. It works with the shell.
+ `Create override.conf in ~/.config/hypr` and make your changes there.


## Theming

The shell puts theming first. The shell can theme:

+ `Main shell UI`
+ `All KDE apps`
+ `alacritty`
+ `kitty`

Many more will be supported later.

### Themes

Material color theming engine is used. The theme can be derived from the `current wallpaper` or `custom color (in hex)`

Along with dark/light version of themes, a total of 4 variants exist:

+ `Ash` A desaturated color scheme
+ `Coal` Mono color scheme
+ `Graphite` Closest color scheme to the theme source
+ `Diamond` True material color scheme

### Wallpaper

The wallpaper daemon used is `swww`.
These animations can be used for swww:
wipe, left, right, top, bottom, outer, center, any, fade, random

### Font

Fonts can also be set but currently only default fonts are supported (i.e. non-bold and non-italic) and the icons are a bit weird. It is recommended to use `Iosevka` and `Iosevka Nerd Font`. Fonts are only updated for the shell UI.


## Controllers

Controllers are menus with specific functionality.

### `Launcher`
App launcher to launch apps...duh

### `Networker`
Controller to manage wifi and devices. 

### `Runner`
Controller to run and launch processes.

### `Power`
Power menu for functions like shutdown, reboot, lock etc.

### `Theme`
Controller that provides a GUI to theme the shell.

### `Screenshot`
For taking a screenshot.

### `Clipboard`
Stores a history of the last copied items (textual only).

### `Window Overview`
To view all open windows.


