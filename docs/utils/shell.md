# Carbon Shell Utility

A reference sheet for the `carbon.shell` cli tool.

## `daemon`

### shutdown
Shut the daemon down.
```sh
carbon.shell daemon shutdown
# or the better approach is to use this command:
carbon.daemon --end 
```

### load-state
Load state from state file.
```sh
carbon.shell daemon load-state
```

### save-state
Manually save the state.
```sh
carbon.shell daemon save-state
```

### dump-state
Print the state to the terminal.
```sh
carbon.shell daemon dump-state
```

### get-dispatch-map
Print dispatch map.
```sh
carbon.shell daemon get-dispatch-map
```


## `theme`

### update-theme
Update the shell theme. Missing flags fall back to previous values.

| Flag | Values |
|---|---|
| `--mode` | `dark` \| `light` |
| `--variant` | `ash` \| `coal` \| `graphite` \| `diamond` |
| `--contrast` | decimal |
| `--source` | `wallpaper` \| `hex` |
| `--hex` | hex color code |
| `--img` | path |

> When `--source wallpaper`, `--img` defaults to current wallpaper. Passing a custom `--img` updates for the session only — does not persist.

```sh
carbon.shell theme update-theme --mode dark --variant coal --source wallpaper
carbon.shell theme update-theme --source hex --hex ff6a00
carbon.shell theme update-theme --source wallpaper --img /path/to/image.png
```

### switch-mode
Switch between light and dark mode.
```sh
carbon.shell theme switch-mode --mode dark
carbon.shell theme switch-mode --mode light
```

### toggle-mode
Toggle light/dark mode.
```sh
carbon.shell theme toggle-mode
```

### change-font
Change the shell font.
```sh
carbon.shell theme change-font --font "Iosevka"
```

### set-face
Update the shell profile picture.
```sh
carbon.shell theme set-face --img /path/to/avatar.png
```

### set-wallpaper
Set wallpaper.
```sh
carbon.shell theme set-wallpaper --img /path/to/wallpaper.jpg
```

### set-wallpaper-animation
Set wallpaper transition animation style.

Valid styles: `wipe` `left` `right` `top` `bottom` `outer` `center` `any` `random` `fade`

```sh
carbon.shell theme set-wallpaper-animation --style wipe
carbon.shell theme set-wallpaper-animation --style random
```


## `controller`

### run
Open or close a named controller.
```sh
carbon.shell controller run --name launcher
carbon.shell controller run --name power
```

### close
Close any active controller.
```sh
carbon.shell controller close
```

---

## `notifications`

### notify
Send a notification directly through the daemon. Only `--summary` is required.

| Flag | Values | Required |
|---|---|---|
| `--summary` | string | **Yes** |
| `--body` | string |
| `--app` | string |
| `--timeout` | int (ms) |
| `--urgency` | `low` \| `normal` \| `critical` |

```sh
carbon.shell notifications notify --summary "Build done"
carbon.shell notifications notify --summary "Low battery" --body "Plug in soon." --urgency critical
carbon.shell notifications notify --summary "Update" --app Carbon --timeout 3000
```

### dnd
Set Do Not Disturb state.
```sh
carbon.shell notifications dnd --state on
carbon.shell notifications dnd --state off
carbon.shell notifications dnd --state toggle
```


## `nightlight`

### on
Turn on nightlight.
```sh
carbon.shell nightlight on
```

### off
Turn off nightlight.
```sh
carbon.shell nightlight off
```

### toggle
Toggle nightlight.
```sh
carbon.shell nightlight toggle
```

### set-temperature
Set color temperature. Range: `1000–20000`.
```sh
carbon.shell nightlight set-temperature --value 4500
```

### set-gamma
Set gamma. Range: `10–200`.
```sh
carbon.shell nightlight set-gamma --value 100
```


## `idle`

### on
Turn on idle manager.
```sh
carbon.shell idle on
```

### off
Turn off idle manager.
```sh
carbon.shell idle off
```

### toggle
Toggle idle manager.
```sh
carbon.shell idle toggle
```


## `power`

> This manager has no handlers.


## `panel`

### set-mode
Set panel visibility mode.

Valid modes: `show`, `hide`, `bypass`
```sh
carbon.shell panel set-mode --mode hide
```

### set-position
Set panel position.

Valid positions: `top`, `bottom`
```sh
carbon.shell panel set-position --position top
```


## `lockscreen`

### lock
Trigger the lockscreen.
```sh
carbon.shell lockscreen lock
```

### set-style
Set lockscreen background style. `--img` only required when `--style image`.
```sh
carbon.shell lockscreen set-style --style screenshot
carbon.shell lockscreen set-style --style wallpaper
carbon.shell lockscreen set-style --style image --img /path/to/image.png
```