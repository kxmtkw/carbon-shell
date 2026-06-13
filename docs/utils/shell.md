# Carbon Shell Documentation

This document outlines the available commands and handlers for the **Carbon Shell** system.


## daemon

Used to control the shell daemon and perform special system tasks.

| Handler | Description |
| --- | --- |
| `shutdown` | Shut the daemon down. Use `carbon.daemon --end`. |
| `load-state` | Load state from state file. |
| `save-state` | Manually save the state. |
| `dump-state` | Print the state to the terminal. |
| `get-dispatch-map` | Print dispatch map. |
| `list-managers` | List all managers. |


## autostart

Starts up specified commands on startup of the shell.

| Handler | Description |
| --- | --- |
| `restart-user` | Restart all user-listed commands. Useful when updating the autostart's state. |
| `list` | List all commands executed by the autostart. |


## theme

Change and update the shell theme.

| Handler | Arguments | Description |
| --- | --- | --- |
| `update-theme` | `--mode`, `--variant`, `--contrast`, `--source`, `--hex`, `--img` | Generate a theme from a source. Missing arguments use previous values. |
| `set-shell-style` | `--style [material/modern]` | Set the style of the shell. |
| `switch-mode` | `--mode [dark/light]` | Switch between light and dark mode. |
| `toggle-mode` | - | Toggle light or dark mode. |
| `change-font` | `--font [name]` | Change the shell font. |
| `set-face` | `--img [path]` | Update the profile picture for the shell. |
| `set-wallpaper` | `--img [path]` | Set wallpaper. |
| `set-wallpaper-animation` | `--style [style]` | Set wallpaper animation style. Valid styles: *wipe, left, right, top, bottom, outer, center, any, random, fade.* |

> **Note on `update-theme` variants:**
> * `ash`: Desaturated scheme
> * `coal`: Monotone scheme
> * `graphite`: True-to-source scheme
> * `diamond`: True material scheme


## controller

Open and close controllers (menus).

| Handler | Arguments | Description |
| --- | --- | --- |
| `run` | `--name [name]` | Open/Close the named controller. |
| `close` | - | Close any active controller. |
| `list` | - | List all available controllers. |


## notifications

Send notifications and control their behavior.

| Handler | Arguments | Description |
| --- | --- | --- |
| `notify` | `--summary`, `--body`, `--app`, `--timeout`, `--urgency` | Send a notification. Only `--summary` is required. |
| `dnd` | `--state [on/off/toggle]` | Set 'Do Not Disturb' state. |


## nightlight

Control the nightlight features.

| Handler | Arguments | Description |
| --- | --- | --- |
| `on` | - | Turn on nightlight. |
| `off` | - | Turn off nightlight. |
| `toggle` | - | Toggle nightlight. |
| `set-temperature` | `--value [1000-20000]` | Set temperature (lower = warmer). |
| `set-gamma` | `--value [10-200]` | Set gamma (perceived brightness). |


## idle

Control the idle manager, which triggers actions based on user inactivity.

| Handler | Description |
| --- | --- |
| `on` | Turn on the idle manager. |
| `off` | Turn off the idle manager. |
| `toggle` | Toggle the idle manager. |


## power

Power manager; informs about battery and system state.

| Handler | Description |
| --- | --- |
| `lock` | Lock session. |
| `shutdown` | Poweroff the computer. |
| `reboot` | Restart the system. |
| `suspend` | System sleep/suspend. |
| `hibernate` | System hibernate. |
| `logout` | Logout user. |
| `bios` | Restart and enter BIOS. |


## panel

Configure the shell panel.

| Handler | Arguments | Description |
| --- | --- | --- |
| `set-mode` | `--mode [show/hide/bypass]` | Set panel mode. |
| `toggle-bypass` | `--state [on/off]` | Switch between bypass and last active mode. |
| `set-position` | `--position [top/bottom]` | Set panel position. |


## lockscreen

Set lockscreen styles.

| Handler | Arguments | Description |
| --- | --- | --- |
| `lock` | - | Trigger the lockscreen. |
| `set-style` | `--style [screenshot/image/wallpaper]`, `--img [path]` | Set style. `--img` is only needed if style is `image`. |


## backlight

Control screen brightness.

| Handler | Arguments | Description |
| --- | --- | --- |
| `get` | - | Get current brightness value. |
| `set` | `--value [number]` | Set brightness (clamped to min/max). |
| `increase` | `--value [number]` | Increase brightness by percentage. |
| `decrease` | `--value [number]` | Decrease brightness by percentage. |
| `save` | - | Save current brightness. |
| `restore` | - | Restore last saved brightness. |


## audio

Control audio

| Handler | Arguments | Description |
| --- | --- | --- |
| `get` | - | Get current volume value. |
| `set` | `--value [number]` | Set volume (clamped to min/max). |
| `increase` | `--value [number]` | Increase volume by percentage. |
| `decrease` | `--value [number]` | Decrease volume by percentage. |
| `mute/unmute/toggle-mute` | - | Update volume mute status. |
| `mute-mic/unmute-mic/toggle-mic` | - | Update mic mute status. |