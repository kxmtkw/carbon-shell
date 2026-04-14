
# Carbon Shell

Carbon shell is designed to be a simple and functional desktop shell.
The shell is currently designed for `Hyprland` only.

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

Material color theming engine is used. The theme can be derived from the `current wallpaper` or `custom color` (in hex)

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

### Profile Picture

The profile picture or 'face' can be set using the CLI tool or the theme controller. You can also move your file to `~/.carbon/user/face` manually.

## Controllers

Controllers are menus with specific functionality.

### `Launcher`
App launcher to launch apps...duh
<img width="1920" height="1080" alt="2026-04-13-214435_hyprshot" src="https://github.com/user-attachments/assets/b5aa004f-2a32-4e5f-94ea-7f97324de6f6" />

### `Networker`
Controller to manage wifi and devices. 
<img width="1920" height="1080" alt="2026-04-13-214509_hyprshot" src="https://github.com/user-attachments/assets/b93cd102-d5e1-46b7-9647-cdb0850f900d" />

### `Runner`
Controller to run and launch processes.
<img width="1920" height="1080" alt="2026-04-13-214545_hyprshot" src="https://github.com/user-attachments/assets/41fdd07d-ef36-4807-a569-ca6b74560d0c" />

### `Power`
Power menu for functions like shutdown, reboot, lock etc.
<img width="1920" height="1080" alt="2026-04-13-214520_hyprshot" src="https://github.com/user-attachments/assets/33ddca50-4875-4c8e-a4e6-f2005a7293b5" />

### `Theme`
Controller that provides a GUI to theme the shell.
<img width="1920" height="1080" alt="2026-04-13-214552_hyprshot" src="https://github.com/user-attachments/assets/1ddf247d-8983-45e1-bdef-b44476e84e04" />

### `Screenshot`
For taking a screenshot.
<img width="1920" height="1080" alt="2026-04-13-214533_hyprshot" src="https://github.com/user-attachments/assets/49424c74-e000-45c3-9f99-c41503e443e5" />

### `Clipboard`
Stores a history of the last copied items (textual only).
<img width="1920" height="1080" alt="2026-04-13-214526_hyprshot" src="https://github.com/user-attachments/assets/27383135-64c8-4ada-a443-7ece15dd232f" />

### `Window Overview`
To view all open windows.
<img width="1920" height="1080" alt="2026-04-14-103024_hyprshot" src="https://github.com/user-attachments/assets/a30d12ef-0f1c-4594-b9b3-22ca4021d1fd" />



