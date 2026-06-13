
## Todo

#### Better Runner `(DONE)`o

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


#### Mount Manager

A controller to manage mounted devices.


#### Media Player

A media player needs to be implemented. Ideally the implementation can be done using the dbus, we already have the dbus class for it. The easier solution would be using playerctl.


#### GTK Theming

I added theming for KDE/QT apps but GTK apps still need some love.


#### Better controller configuration `(DONE)`

Adding options like position and even multiple variants.


#### Custom Launcher `(CANCELLED)`

Build the shell's own launcher instead of relying on rofi's drun. For some reason, the application rofi -drun launchs lives under the daemon process. That means when daemon ends, all programs that were launched by the rofi launcher also end up closing.

> No need now since i figured out what was wrong. Tho if i want to be able to not show certain apps, then this could be implemented. Also with our daemon, we could lauch the rofi menu even faster since we can cache the applications in memory.

#### Install scripts for other distributions

Currently the installer only resolves arch dependancies. More distributions need to be supported.