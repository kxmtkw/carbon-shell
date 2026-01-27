from carbon.args import parseArgs

from carbon.installer import installCarbon
from carbon.colors import colorifyCarbon, switchTheme

def main():

    args = parseArgs()

    match args.command:

        case "install":
            installCarbon()

        case "uninstall":
            print("Uninstall unsupported")

        case "colorify":
            colorifyCarbon(args.theme, args.variant, args.image, args.hex)

        case "switch":
            switchTheme(args.theme)

        case "wall":
            print()
