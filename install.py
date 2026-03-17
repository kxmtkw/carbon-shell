import subprocess

class Color:

    reset = "\033[0m"

    black   = "\033[30m"
    red     = "\033[31m"
    green   = "\033[32m"
    yellow  = "\033[33m"
    blue    = "\033[34m"
    magenta = "\033[35m"
    cyan    = "\033[36m"
    white   = "\033[37m"

    bright_black   = "\033[90m"
    bright_red     = "\033[91m"
    bright_green   = "\033[92m"
    bright_yellow  = "\033[93m"
    bright_blue    = "\033[94m"
    bright_magenta = "\033[95m"
    bright_cyan    = "\033[96m"
    bright_white   = "\033[97m"

    @classmethod
    def Print(cls, msg: str, color: str):
        print(f"{color}{msg}{Color.reset}")

def run(cmd):
    subprocess.run(cmd, shell=True)

def prompt(msg: str, options: list[str]) -> str:

    print(f"{msg} {tuple(options)}")
   

    while True:
        chosen = input(">> ").lower()

        if chosen not in options:
            Color.Print("Invalid option!", Color.red)
            continue

        return chosen 
    

# Installation

Color.Print(" >>> Installing Core Packages", Color.blue)

print("Permission required. Packages will be installed from ./installation/core_packages.sh (for arch)")

chosen = prompt("proceed?", ["y", "n"])

if chosen == "y":
    Color.Print(":: Proceeding with installation...", Color.blue)
    run("sh ./installation/core_packages.sh")
    Color.Print(":: Core packages installed!", Color.green)
else:
    Color.Print(":: Installation canceled...", Color.yellow)


Color.Print(" >>> Installing App Packages", Color.blue)

print("These include KDE apps and a small part of KDE ecosystem for theming (does not include plasma itself)")
print("Permission required. Packages will be installed from ./installation/app_packages.sh (for arch)")

chosen = prompt("proceed?", ["y", "n"])

if chosen == "y":
    Color.Print(":: Proceeding with installation...", Color.blue)
    run("sh ./installation/core_packages.sh")
    Color.Print(":: App packages installed!", Color.green)
else:
    Color.Print(":: Installation canceled...", Color.yellow)


Color.Print(" >>> Installing Carbon", Color.blue)

Color.Print(":: Installing python package...", Color.blue)

run("python3 -m venv .venv")
run("source ./.venv/bin/activate && pip install . ")

Color.Print(":: Linking hyprland...", Color.blue)

run("ln -s -i ~/.carbon/hypr ~/.config/hypr")
run("touch ~/.carbon/hypr/hyprviz.conf")
run("touch ~/.carbon/hypr/override.conf")

Color.Print(":: Moving settings...", Color.blue)

run("mkdir user")
run("mkdir settings")
run("cp -i ~/.carbon/defaults/config.toml ~/.carbon/settings/config.toml")
run("cp -i ~/.carbon/defaults/colors.toml ~/.carbon/settings/colors.toml")


Color.Print(" :: Carbon shell installed!", Color.green)
