from carbon.args import parseArgs

from carbon.installer import installCarbon

def main():

    args = parseArgs()
    
    match args.command:

        case "install":
            installCarbon()

        case "uninstall":
            print("Uninstall unsupported")

        case "colorify":
            print("Uninstall unsupported")

        case "switch":
            print("switch-theme")

        case "wall":
            print()
