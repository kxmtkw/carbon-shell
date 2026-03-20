
# Carbon Shell

Carbon Shell is a UI shell for linux designed to be highly functional and pretty. The shell is specifically built for the `Hyprland` WM.

The shell has a `Material You` inspired design and uses its theming scheme.

## Previews

![](/assets/launcher.png)


![](/assets/lightmode.png)


![](/assets/wallpaper.png)


![](/assets/lockscreen.png)


## Features

Some notable features of the shell:

+ `Dynamic Theming`: The shell dynamically themes itself and all supported apps when you change your wallpaper.
+ `Controllers`: Functional menus for controlling things like wifi, launching apps, power, theming and much more.
+ `KDE App Support`: Theming of KDE apps is fully supported.
+ `Configurable`: The shell can configured via a very simple config file.

The shell includes:

+ Lock Screen
+ Panel
+ Power Menu
+ Launcher
+ Screenshot Util
+ Wifi Menu
+ Theming Menu
+ Media Player Controller
+ Clipboard Util
+ Essential Desktop Apps (from KDE) (Optional)


## Installation

The shell can be installed by using this one-line:

```bash
curl -fsSL https://raw.githubusercontent.com/kxmtkw/carbon-shell/main/install.sh | bash
```

What this script would do:
+ Install core packages
+ Install packages for essential apps (optional)
+ Install the shell

Then just start up hyprland and everything should work.


### Manual

Clone the repo at `~/.carbon` and it MUST be cloned exactly at this path for the shell to work.

``` bash
git clone https://github.com/kxmtkw/carbon-shell.git ~/.carbon
cd ~/.carbon
python3 install.py
```


## TODO
Here is a list of planned features/improvements: [todo](/docs/todo.md)
