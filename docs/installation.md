# Installation

A guide on how to install Carbon Shell.

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
