


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

### Configuration

The shell is supposed to be configured using the cli `carbon.shell`. But if you prefer normal configuration methods, the shell can be be configured using `~/.carbon/user/state.json`.

```json
{
    "ThemeManager": {
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
    "ControllerManager": {},
    "NightLightManager": {
        "toggled": true,
        "temperature": 5800,
        "gamma": 100
    },
    "NotificationManager": {
        "do_not_disturb": false
    }
}
```

After configuration using `carbon.shell`, run:
```bash
carbon.shell daemon save-state
```
to regenerate this file.