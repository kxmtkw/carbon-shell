from carbon.args import parseArgs

from carbon.installer import installCarbon
from carbon.theme import Theme

def main():

    args = parseArgs()

    match args.command:

        case "install":
            installCarbon()

        case "uninstall":
            print("Uninstall unsupported")

        case "update-theme":
            Theme.change_color_theme(args.theme, args.variant, img=args.image, hex=args.hex, contrast=args.contrast)

        case "switch-mode":
            Theme.switch_theme_mode(args.mode)

        case "update-wallpaper":
            Theme.set_wallpaper(args.image)

        case "update-wallpaper-theme":
            Theme.set_wallpaper(args.image)
            Theme.change_color_theme(args.theme, args.variant, img=args.image, contrast=args.contrast)
