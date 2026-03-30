
# Carbon Shell

A desktop UI shell designed for `Hyprland` to be functional and pretty!


## Features

Some notable features of the shell:

+ `Dynamic Theming`: The shell dynamically themes itself and all supported apps when you change your wallpaper.
+ `Controllers`: Functional menus for controlling things like wifi, launching apps, power, theming and much more.
+ `Hyprland Config`: Hyprland and its essential tools come preconfigured.
+ `KDE App Support`: Theming of KDE apps is fully supported.
+ `Configurable`: The shell can configured via a very simple config file. See [configuration](docs/configuration.md).

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

For more features: [features](docs/features.md)

For keybinds see: [bindings](docs/bindings.md)


## Installation

### Dependancies

If on `Arch Linux`, the installation script will handle all the packages. 

If you're on some other distribution or want to manually install packages, see [requirements](docs/requirements.md).

### Cloning

The shell can be installed by using this command:

``` bash
git clone https://github.com/kxmtkw/carbon-shell.git ~/.carbon
cd ~/.carbon
python3 install.py
```

> [!IMPORTANT]
> The shell must be cloned at '~/.carbon' for it to work.

What this script would do:
+ Install core packages
+ Install packages for essential apps (optional)
+ Install the shell

### Environment

Finally, add this line in your shell config. The file should be sourced by all shell instances.
``` bash
source ~/.carbon/env
```

The recomended shell config files are:

+ `~/.zshenv` for zsh
+ `~/.bashrc` for bash
+ `~/.config/fish/config.fish` for fish


### Restart

Then just restart hyprland and everything should work.
You can edit the shell config present at `~/.carbon/config.toml`.


## Previews

![](/assets/launcher.png)


![](/assets/lightmode.png)


![](/assets/wallpaper.png)


![](/assets/lockscreen.png)


## TODO
Here is a list of planned features/improvements: [todo](/docs/todo.md)
