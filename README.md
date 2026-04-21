


# Carbon Shell 

A desktop UI shell designed for `Hyrpland` to be pretty and functional.

+ Window Manager: `Hyprland`
+ Panel & Notifications: `Quickshell`
+ Controllers/Menus: `Rofi`

https://github.com/user-attachments/assets/11d270ad-722d-4eb4-9711-97d661c764bc

### Installation

`For installation, see:` [installation](docs/installation.md)

### Features

`For features, see:` [features](docs/features.md)


### Bindings

`For keybinds, see:`  [bindings](docs/bindings.md)


### Utilities

Along with that some other utilies include:

```bash
carbon.shell       # For starting and controlling the shell daemon
carbon.brightness  # For controlling brightness
carbon.audio       # For controlling audio
carbon.power       # For shutting down, rebooting etc...
```


### Configuration

The shell is supposed to be configured using the cli tool `carbon.shell`
.
The main utility is `carbon.shell`. It is used to start up the shell daemon and send commands to it.
```bash
carbon.shell COMMAND ...
```
`For a guide on how to use the tool, see:` [cli](docs/cli.md)

#### Examples

Here is an example script that allows you to focus on your work (or something like that).
```bash
carbon.shell theme switch-mode dark
carbon.shell nightlight on
carbon.shell nightlight set-temperature 5400
carbon.shell notifications dnd on
carbon.shell idle off
```

Another script to change wallpaper and theme depending upon the time of the day.
```bash
while true; do
    hour=$(date +%H)

    if (( hour >= 6 && hour < 18 )); then
        carbon.shell theme switch-mode light
        carbon.shell theme set-wallpaper ~/Pictures/light.png
        carbon.shell theme set-contrast 2
        carbon.shell nightlight off
    else
        carbon.shell theme switch-mode dark
        carbon.shell theme set-wallpaper ~/Pictures/dark.png
        carbon.shell theme set-contrast 0.1
        carbon.shell nightlight on
    fi

    sleep 60
done
```

#### File Method

If you prefer to use files as configuration, you can edit the json file in `~/.carbon/user/state.json`.

After editing the file, run:
```bash
carbon.shell daemon load-state
```

Here is an example config:

```json
{
    "theme": {
        "mode": "dark",
        "source": "wallpaper",
        "wallpaper": "~/.carbon/assets/default_wallpaper.jpg",
        "hex": "#82a0c0",
        "variant": "graphite",
        "contrast": 0.5,
        "font": "Iosevka",
        "face": "~/.carbon/assets/default_face.jpg",
        "wallpaperAnimation": "center"
    },
    "controller": {},
    "nightlight": {
        "toggled": true,
        "temperature": 6000,
        "gamma": 100
    },
    "notification": {
        "do_not_disturb": false
    },
    "idle": {
        "toggled": true
    }
}
```

