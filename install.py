from pathlib import Path
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

def run(cmd, wait: bool = True, *, hide_output: bool = True) -> bool | None:
    if wait:
        output = subprocess.run(cmd, shell=True, capture_output=hide_output, text=True)
        return output.returncode == 0
    else:
        subprocess.Popen(cmd, shell=True)
        return None

def prompt(msg: str, options: list[str]) -> str:

    print(f"{msg} {tuple(options)}")
   

    while True:
        chosen = input(">> ").lower()

        if chosen not in options:
            Color.Print("Invalid option!", Color.red)
            continue

        return chosen 
    

# Installation

def main():

    Color.Print(" >>> Starting Installation", Color.magenta)

    print("If you are on arch, this script will install dependancies for you. If not, install your distribution's version of packages.")

    chosen = prompt("Are you on arch?", ["y", "n"])

    if chosen == "y":

        Color.Print(" >>> Installing Core Packages", Color.magenta)

        print("Permission required. Packages will be installed from ./installation/core_packages.sh (for arch)")

        Color.Print(":: Proceeding with installation...", Color.blue)
        run("sh ./installation/core_packages.sh", hide_output=False)
        Color.Print(":: Installation finished.", Color.green)


        Color.Print(" >>> Installing App Packages", Color.magenta)

        print("These include KDE apps and other apps like network manager.")
        print("Permission required. Packages will be installed from ./installation/app_packages.sh (for arch)")

        chosen = prompt("proceed?", ["y", "n"])

        if chosen == "y":
            Color.Print(":: Proceeding with installation...", Color.blue)
            run("sh ./installation/app_packages.sh", hide_output=False)
            Color.Print(":: Installation finished.", Color.green)
        else:
            Color.Print(":: Installation canceled...", Color.yellow)

    else:
        Color.Print(":: Skipping package installation", Color.yellow)
        Color.Print(":: Make sure to install the required packages before proceeding. See the github repo or requirements.md", Color.yellow)
        prompt("Press enter to continue...", [""])

    Color.Print(" >>> Installing Carbon", Color.magenta)

    Color.Print(":: Installing python package...", Color.blue)

    run("python3 -m venv .venv")
    run("source ./.venv/bin/activate && pip install -e . ", hide_output=False)

    Color.Print(":: Linking hyprland...", Color.blue)

    if Path("~/.config/hypr").expanduser().exists():
        chosen = prompt("Hyprland config already exists. [S]ave to ~/.config/old_hypr or [O]verwrite? ", ["s", "o"])

        if chosen == "o":
            run("rm -rf ~/.config/hypr")
        else:
            run("mv ~/.config/hypr ~/.config/old_hypr")

    run("ln -s ~/.carbon/hypr ~/.config")

    run("touch ~/.carbon/hypr/hyprviz.conf")
    run("touch ~/.carbon/hypr/override.conf")
    run("mkdir ~/.carbon/hypr/user")


    Color.Print(":: Finalizing setup...", Color.blue)

    run("mkdir cache")
    run("mkdir user")

    run("mkdir -p /home/haseeb/.local/share/color-schemes")

    Color.Print(":: Starting shell...", Color.blue)

    run("pidof Hyprland && echo 'Hyprland already running!' || start-hyprland")
    run("carbon.shell daemon start", hide_output=False)
    run("hyprctl reload > /dev/null")
    run("carbon.shell daemon save-state", hide_output=True)

    Color.Print(" :: Carbon shell installed!", Color.green)


if __name__ == "__main__":
    try:
        main()
    
    except Exception as e:
        Color.Print(f":: Encountered Error: {e.__class__.__name__} [{str(e)}]", Color.red)