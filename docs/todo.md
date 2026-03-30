
## Todo


#### Better Runner

Runner needs more modes:

- Default: Executes binaries from $PATH
- Shell($): Executes shell commands using default shell
- Calculate(=): Calculates a string
- Sudo(#): Run a command with sudo -A
- File(/): Search the file system
- Search(?): Search the web
- Custom(@): Built-in runner commands (these should also be with $PATH entries)
- History(%): Last executed commands (thes should also be with $PATH entries)

#### Better Theme Manager (DONE)

Theme manager for stuff like wallpapers, profile pics

#### Wifi Manager (DONE)

The current wifi manager "Just Works", I need it to make it more functional and maybe make it a proper wrapper around nmcli

#### Bluetooth Manager

Same as the wifi manager but for bluetooth devices, probably build it using bluetoothctl and have an option to open blueman.

#### Responsive Bar (In Progress)

I need to make the bar feel more responsive.

+ Better and smoother animations for the OSDs.
+ More applets like bluetooth, clipboard and even a way to hide and show them like a drawer.
+ A system tray, highly needed.
+ Music Indicator which only appears when media is being played and clicking it opens player controller
+ Date on the bar too, currently only time is shown. Maybe clicking the clock could "expand" it and reveal the date for some short while. Maybe open the calendar on double click?
+ CPU and RAM and stuff? Could be done but we need to be vary of the space.
+ Wifi and Bluetooth applet displaying their connected SSIDs?

#### System Tray

System Tray

#### Battery Manager
 
The controller that opens after clicking the battery info. Display basic battery info and different power options and a way to open TLP.

#### Better Notifs

The current notifs in quickshell look ugly. Make them more material and modern.

#### Basic Pacman System

A basic pacman wrapper for:

+ Taking a look at all installed packages and general info about them.
+ Updating pacman
+ Deleting useless packages
+ Installing new packages
+ And other general stuff...

Since pacman is a SYSTEM pacakage manager, we can't just subprocess the pacman command without sudo. So for this:

+ Either we build a sudo askpass
+ Or we make it so that a terminal is opened with the command the user wants execute and the user can run the command from there.

#### Mount Manager

A controller to manage mounted devices.

#### Better Media Player

The current media player works fine but we need to display the album art which would be sick.

#### Carbon State (DONE - implemented using Carbon Config)

A better way to track state of the carbon shell. The current implementation relies on a free json file where any key can be added AND it resides in cache/ which makes it more unserious

#### Carbon Config (DONE)

A way to configure the shell!

+ Profile Pic
+ Wallpaper (ehh...? we need to make it so that wallpaper will be loaded from the config instead of the state)
+ Theme (so basically, move the carbon state to the config which fixes the "unserious" issue as well)
+ Bar position (top/bottom)
+ Applet positions (too complex perhaps)
+ Default terminal


#### Design (In Progress)

I tried implementing material design and it works for the most part. But some improvements can be here and their especially with rofi.

#### GTK Theming

I added theming for KDE/QT apps but GTK apps still need some love. This will be trivial to implement... I hope.


#### Daemon (CANCELLED)

Implement a daemon that will:

+ Manage controllers so we don't have to use the file hack we currently use.
+ Hot reload config
+ Manage state
+ Cache themes
+ Do Not Disturb state
+ Screen temp state

#### Better hyprland theming

The current method causes env = PATH to be reloaded again and again causing a long PATH var. The fix is to re send the contents of color.conf using hyprctl instead of using file based theming.

#### Better controller configuration

Adding options like position and even multiple variants.
