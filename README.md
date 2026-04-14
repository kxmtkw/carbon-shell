


# Carbon Shell 

A desktop UI shell designed for `Hyrpland` to be pretty and functional.

+ Window Manager: `Hyprland`
+ Panel & Notifications: `Quickshell`
+ Controllers/Menus: `Rofi`

https://github.com/user-attachments/assets/11d270ad-722d-4eb4-9711-97d661c764bc

### Features

`For features, see:` [features](docs/features.md)


### Bindings

`For keybinds, see:`  [bindings](docs/bindings.md)


### Utilities

The shell also comes with multiple CLI tools.




The main utility is `carbon.shell`. It is used to start up the shell daemon and send commands to it.
```sh
carbon.shell COMMAND ...
```
`For a guide on how to use the tool, see:` [cli](docs/cli.md)

Along with that some other utilies include:

```sh
carbon.brightness # For controlling brightness
carbon.audio      # For controlling audio
carbon.power      # For shutting down, rebooting etc...
```


## Installation

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

> [!WARNING]
> Sourcing unknown sh files is always dangerous, you should take a look inside the env file for reassurance

### Restart

Then just restart hyprland and everything should work.
