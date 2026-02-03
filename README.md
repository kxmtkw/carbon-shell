
# Carbon Shell

Carbon Shell is a UI shell for linux designed to be highly functional and efficient. It uses quickshell and rofi to achieve this.

## Installation

First install dependancies.

```bash
hyprland \
hyprsunset \
hyprshot \
swww \ 
quickshell \
rofi
```

Other than these, the shell also expects `NetworkManager` and it's associated tools like `nmcli` for the wifi controller to work.

Clone the repo at `~/.carbon` and it MUST be cloned exactly at this path for the shell to work.

```
git clone git@github.com:kxmtkw/carbon-shell.git ~/.carbon
cd ~/.carbon
chmod +x install.sh
./install.sh
```

What this script would do:
+ Setup a python venv at `~/.carbon/.venv`
+ Install all python dependancies
+ Finally run `carbon install` to install the shell.

> The shell is still barebones, Soon a better and quicker way to install will be implemented.


