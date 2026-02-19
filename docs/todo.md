
## Todo

#### Notification (DONE)

Either configure dunst or build your own notification daemon. The latter is only needed if i want actions in my notifs which are'nt supported by dunst.

> Dunst added for now, i think it would suffice

#### Power Management

No power daemon is present, no notifs sent obviously. Also need a critical reminder that forces the user to shutdown or something.

#### Terminal (DONE)

Switch terminal from kitty to alacritty maybe? the reason being that kitty does'nt support dynamic theming so the whole thing does'nt feel that satisfying but i'll think about it.

#### Wifi (DONE)

Need a proper UI to control wifi. Stuff like hotspot and airplane mode would be nice

#### Bluetooth

This would be a little more complicated to make than the wifi one since i need to support a lot of features for this one.

#### Settings for Carbon

I want a single config file for the whole of carbon. And moreover i want the shell to be configured from a settings menu (maybe a gui with qt even or just winging it with rofi). I should be ble to configure themes, bar position, defualt terminals, workspace count etc

#### Theming

Central menu for theming carbon

#### Lock screen (DONE)

Probably need something that can handle both. Nevermind, let the user themselves handle the login manager for now.

#### Fastfetch (ONGOING)

Maybe have a default fastfetch config or something

#### Screenshot util (DONE)

Improve that

#### Caching themes

Cache themes generated from wallpapers

#### OSDs

OSDs for brightness, sound and mic

#### Media Control (DONE)

Add a media controller, don't know how i will do it. Rofi stutters a bit but maybe i can find some hyprland way to fix it.

> Make it update dynamically? that could be cool (DONE)

#### KDE apps and coloring (DONE)

I found out how KDE apps are themed so maybe if i can connect it with my colorify, we can have material kde apps as well, this will take some work.

#### Rainbow colors (DONE)

Add the rainbow colors for terminals by shifting some base colors towards the primary or something. 

#### Calculator?

Maybe add a small rofi calculator?

#### Small Pacman rofi

A small pacman wrapper for basic tasks like: see all packages, all user packages, update everything, install a new package, uninstall a package and stuff like that.

#### A sudo runner?

no, build a askpass

#### Better Runner

Runner needs more modes:

- Default: Executes binaries from $PATH
- Shell($): Executes shell commands using default shell
- Calculate(=): Calculates a string
- Sudo(#): Run a command with sudo -A
- File(/): Search the file system
- Search(?): Search the web
- Custom(!): Built-in runner commands (these should also be with $PATH entries)
- History(%): Last executed commands (thes should also be with $PATH entries)

#### Utils

Add utils/ and add stuff like brightness.
- Install them to ~/.carbon/bin or ~/.carbon/.venv/bin