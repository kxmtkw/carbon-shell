


# Carbon Shell 

A desktop UI shell designed for `Hyrpland` to be pretty and functional.

+ Window Manager: `Hyprland`
+ Panel & Notifications: `Quickshell`
+ Controllers/Menus: `Rofi`

---

https://github.com/user-attachments/assets/7c049d7c-49b4-412b-a11a-a3797e1d9e94

---

### `Installation`

A guide on how to install Carbon Shell.

### 1) Dependancies

If on `Arch Linux`, the installation script will handle all the packages. 

If you're on some other distribution or want to manually install packages, see [requirements](docs/requirements.md).

### 2) Getting Shell

The shell can be installed by using this command:

``` bash
curl -fsSL https://raw.githubusercontent.com/kxmtkw/carbon-shell/main/install.sh -o /tmp/install.sh && bash /tmp/install.sh
```

What this script would do:
+ Install core packages
+ Install packages for essential apps (optional)
+ Install the shell

### 3) Restart

Then just restart hyprland and everything should work.

### `Bindings`

For keybinds, see:  [bindings](docs/bindings.md)

### `Utilities`

Along with that some other utilies include:

```bash
carbon-daemon # for starting/ending the shell daemon
carbon-shell  # for controlling the daemon
```

Reference sheet for each utility:

+ [carbon-daemon](docs/utils/daemon.md)
+ [carbon-shell](docs/utils/shell.md)


### `Configuration`

The shell is supposed to be configured using the cli tool `carbon-shell`
.
The main utility is `carbon-shell`. It is used to start up the shell daemon and send commands to it.
```bash
carbon-shell COMMAND ...
```
For a guide on how to use the tool, see: [carbon-shell](docs/utils/shell.md)

### Examples

Here is an example script that allows you to focus on your work (or something like that).
```bash
carbon-shell theme switch-mode --mode dark
carbon-shell nightlight on
carbon-shell nightlight set-temperature --value 5400
carbon-shell backlight set --value 60
carbon-shell notifications dnd --state on
carbon-shell idle off
```

Another script to change wallpaper and theme depending upon the time of the day.
```bash
while true; do
    hour=$(date +%H)

    if (( hour >= 6 && hour < 18 )); then
        carbon-shell theme switch-mode --mode light
        carbon-shell theme set-wallpaper --img ~/Pictures/light.png
        carbon-shell theme set-contrast --value 1
        carbon-shell nightlight off
    else
        carbon-shell theme switch-mode --mode dark
        carbon-shell theme set-wallpaper --img ~/Pictures/dark.png
		carbon-shell theme set-contrast --value 0.1
        carbon-shell nightlight on
    fi

    sleep 60
done
```

### File Method

If you prefer to use files as configuration, you can edit the json file in `~/.carbon/user/state.toml`.

After editing the file, run:
```bash
carbon-shell daemon load-state
```

Here is an example config:

```toml
[autostart]
commands = []

[theme]
mode = "dark"
source = "wallpaper"
style = "material"
wallpaper = "~/.carbon/assets/default_wallpaper.jpg"
hex = "#82a0c0"
variant = "graphite"
contrast = 0.5
font = "Iosevka"
face = "~/.carbon/assets/default_face.jpg"
wallpaper_animation = "center"

[controller]

[notifications]
do_not_disturb = false

[nightlight]
toggled = true
temperature = 6000.0
gamma = 100.0

[idle]
toggled = true

[power]
full_threshold = 95
warning_threshold = 15
critical_threshold = 5
force_hibernate_threshold = 2

[panel]
mode = "show"
position = "bottom"

[lockscreen]
style = "screenshot"
image = "~/.carbon/assets/default_wallpaper.jpg"
```

### `Project Structure`

The project has been divided into different folders (duh...)
```sh
carbon-shell/
	assets/
		# Contains the default profile and wallpaper
	bin/
		# Used to contain old scripts until I moved them to .venv via pip. 
	carbon/
		# The main python module
		cli/
			# The cli implementations
		core/
			# The core of the daemon
		ipc/
			# Classes for ipc between client and daemon
		lib/
			# Contains essential classes for the shell to function.
		managers/
			# Different managers, each with their own responsibility
		state/
			# State manager
		utils/
			# Some utilities
	docs/
		# Documentation for the shell
	hypr/
		# Configuration for Hyprland which manages windows.
	shell/
		# Configuration for the visible "shell"
		rofi/
			# Rofi configuration (the controllers/menus)
		quickshell/
			# Quickshell config (the panel & notifications)
	installation/
		# Scripts to install the shell
```

### `Todo`

A list of todos: [todo](docs/todo.md)