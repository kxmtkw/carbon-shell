
## Todo

#### Better Runner

Runner needs more modes. Some example modes could be:

- Default: Executes binaries from $PATH
- Shell($): Executes shell commands using default shell
- Calculate(=): Calculates a string
- Sudo(#): Run a command with sudo -A
- File(/): Search the file system
- Search(?): Search the web
- Custom(@): Built-in runner commands (these should also be with $PATH entries)
- History(%): Last executed commands (thes should also be with $PATH entries)


#### Bluetooth Manager

Same as the wifi manager but for bluetooth devices, probably build it using bluetoothctl and have an option to open blueman.


#### System Tray

Add a system tray to the bar.


#### Battery Manager
 
The controller that opens after clicking the battery info. Display basic battery info and different power options and a way to open TLP.


#### Better Notifs (DONE)

Make notifications actually work in quickshell.


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


#### GTK Theming

I added theming for KDE/QT apps but GTK apps still need some love.


#### Better hyprland theming

The current method causes env = PATH to be reloaded again and again causing a long PATH var. The fix is to re send the contents of color.conf using hyprctl instead of using file based theming.


#### Better controller configuration

Adding options like position and even multiple variants.


#### Custom Launcher (CANCELLED)

Build the shell's own launcher instead of relying on rofi's drun. For some reason, the application rofi -drun launchs lives under the daemon process. That means when daemon ends, all programs that were launched by the rofi launcher also end up closing.

> No need now since i figured out what was wrong. Tho if i want to be able to not show certain apps, then this could be implemented. Also with our daemon, we could lauch the rofi menu even faster since we can cache the applications in memory.