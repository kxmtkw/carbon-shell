from carbon.args import parseArgs

from carbon.installer import installCarbon
from carbon.colors import colorify, set_wallpaper, switch_theme
from carbon.controllers import launch_controller

def main():

    args = parseArgs()

    match args.command:

        case "install":
            installCarbon()

        case "uninstall":
            print("Uninstall unsupported")

        case "colorify":
            colorify(args.theme, args.variant, args.image, args.hex)

        case "switch":
            switch_theme(args.theme)

        case "wall":
            set_wallpaper(args.theme, args.variant, args.image)

        case "launch":
            launch_controller(args.controller)
