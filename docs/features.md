
# Carbon Shell

Carbon Shell is a UI shell for linux designed to be highly functional and pretty. 

## Shell

The shell includes the following UI components:

+ Panel
+ Lock Screen
+ Launcher
+ Power Menu
+ Wifi/Networks Menu
+ Windows Overview
+ Run Prompt
+ Screenshot Utility
+ Clipboard
+ Theme Utility
+ Notifications


## Theming

The shell can by dynamically themed using the theme utility or the `carbon.theme` CLI.
Plus, two target apps are also supported which include:

+ kitty
+ alacritty

These apps can be chosen as targets in the config file so that the shell can theme them as well.


## Utilities

The shells comes with several utilities:

+ carbon.shell
+ carbon.theme
+ carbon.controller
+ carbon.power
+ carbon.brightness
+ carbon.audio


## Essential Apps

The shell also handles the installation and theming of essential desktop apps.

- `Terminal` alacritty
- `Archive Manager` ark
- `Calendar` calindori
- `File Manager` dolphin
- `Disk Usage Analyzer` filelight
- `Image Viewer` gwenview
- `Media Player` haruna
- `Hyprland Settings` hyprviz
- `ISO Image Writer` isoimagewriter
- `Camera` kamoso
- `Calculator` kcalc
- `Clock` kclock
- `Torrent Client` ktorrent
- `Network Manager GUI` nm-connection-editor
- `GTK Appearance Settings` nwg-look
- `Document Viewer` okular
- `Partition Manager` partitionmanager
- `System Monitor` plasma-systemmonitor


## Hyprland

The shell comes with a complete `Hyprland Config` that is automatically linked upon installation.
The config includes:
+ Hyprland WM config
+ Hyprlock config
+ Hyprsunset config
+ Hypridle config
+ Sources for hyprviz

### Modifications

It is recomended to not touch the files that come with the shell as it can later cause issues during updates.
If you want to make changes, you have two methods.

+ `Create override.conf`: Create a file with this name under ~/.config/hypr and it will be automatically included, you can make all your changes and overrides here.

+ `Use Hyprviz`: Hyprviz, which is a GUI for hyprland config, can also be used to override the main config without touching it.
