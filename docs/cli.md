# carbon.shell CLI

Utility to control and communicate with the shell daemon.

```
carbon.shell COMMAND ...
```



## Commands

### `daemon`

Manage the Carbon daemon.

```
carbon.shell daemon ACTION
```

| Action | Description |
|--------|-------------|
| `start` | Start daemon |
| `restart` | Restart daemon |
| `end` | Ask daemon to shut down |
| `save-state` | Persist current state to disk |
| `load-state` | Load state from disk |
| `get-dispatch-map` | Print internal dispatch map |

---

### `theme`

Control theming.

```
carbon.shell theme ACTION [OPTIONS]
```

#### `update`

Generate and apply a new theme.

```
carbon.shell theme update (--img PATH | --hex COLOR) [--mode MODE] [--variant VARIANT] [--contrast AMOUNT]
```

| Option | Values | Description |
|--------|--------|-------------|
| `--img PATH` | e.g. `~/Pictures/wall.png` | Derive palette from image |
| `--hex COLOR` | e.g. `#a0c4ff` | Derive palette from hex color |
| `--mode` | `dark`, `light` | Color mode |
| `--variant` | `ash`, `coal`, `graphite`, `diamond` | Palette variant |
| `--contrast` | float | Contrast adjustment |

`--img` and `--hex` are mutually exclusive; one is required.

#### `update-variant`

```
carbon.shell theme update-variant VARIANT
```

`VARIANT`: `ash` | `coal` | `graphite` | `diamond`

#### `switch-mode`

```
carbon.shell theme switch-mode MODE
```

`MODE`: `dark` | `light`

#### `toggle-mode`

```
carbon.shell theme toggle-mode
```

Toggle between dark and light.

#### `set-wallpaper`

```
carbon.shell theme set-wallpaper PATH
```

Set wallpaper. Regenerates theme if theme source is wallpaper.

#### `set-face`

```
carbon.shell theme set-face PATH
```

Set user face image.

#### `set-font`

```
carbon.shell theme set-font NAME
```

Set UI font.

#### `set-wallpaper-animation`

```
carbon.shell theme set-wallpaper-animation STYLE
```

`STYLE`: wipe | left | right | top | bottom | outer | center | any | fade | random

---

### `nightlight`

Control night light / color temperature.

```
carbon.shell nightlight ACTION
```

| Action | Description |
|--------|-------------|
| `on` | Enable nightlight |
| `off` | Disable nightlight |
| `toggle` | Toggle nightlight |
| `set-temperature KELVIN` | Set color temperature (int, Kelvin) |
| `set-gamma GAMMA` | Set gamma value (int) |

---

### `notifications`

Control notifications.

#### `dnd`
Control "Do Not Disturb" mode.
```
carbon.shell notifications dnd STATE
```

`STATE`: on | off | toggle

---

### `controller`

Open or close shell menus.

```
carbon.shell controller ACTION
```

| Action | Description |
|--------|-------------|
| `run NAME` | Open named menu/controller |
| `close` | Close active controller |

`Supported Controllers (NAME)`: power | launcher | networker | runner | theme | clipboard | screenshot

---

### Examples

```sh
# Start daemon
carbon.shell daemon start

# Apply theme from wallpaper, dark mode, graphite variant
carbon.shell theme update --img ~/walls/forest.jpg --mode dark --variant graphite

# Apply theme from hex
carbon.shell theme update --hex "#a0c4ff"

# Toggle dark/light
carbon.shell theme toggle-mode

# Enable nightlight at 3500K
carbon.shell nightlight on
carbon.shell nightlight set-temperature 3500

# Enable DND
carbon.shell notifications dnd on

# Open app launcher
carbon.shell controller run launcher
```