import argparse


def parseArgs():

    parser = argparse.ArgumentParser(
        description="Carbon Shell - Minimal yet Functional"
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--install",
        action="store_true",
        help="Install Carbon Shell"
    )

    group.add_argument(
        "--colorify",
        action="store_true",
        help="Update the color theme of the shell. Can take a hex color value or path to an image."
    )

    group.add_argument(
        "--run",
        metavar="TARGET",
        help="Run a controller."
    )

    group.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall Carbon Shell"
    )

    
    args = parser.parse_args()
    
    return args


