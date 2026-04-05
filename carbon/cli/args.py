import argparse

# used AI :p

def get_parser():

    parser = argparse.ArgumentParser(
        prog="carbon.shell", 
        description="CLI for Carbon Shell"
    )
    subparsers = parser.add_subparsers(dest="category", required=True)

    # ==========================================
    # DAEMON COMMANDS
    # Usage: daemon [start|restart|kill]
    # ==========================================
    daemon_parser = subparsers.add_parser("daemon")
    daemon_parser.add_argument("action", choices=["start", "restart", "end"], help="Action to perform on the daemon")

    # ==========================================
    # THEME COMMANDS
    # ==========================================
    theme_parser = subparsers.add_parser("theme")
    theme_sub = theme_parser.add_subparsers(dest="action", required=True)

    # theme update --image/--hex [--theme] [--mode] [--contrast]
    update_parser = theme_sub.add_parser("update")
    source_group = update_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--image", metavar="IMG")
    source_group.add_argument("--hex", metavar="HEX")
    
    update_parser.add_argument("--variant", choices=["ash", "coal", "graphite", "diamond"])
    update_parser.add_argument("--mode", choices=["light", "dark"])
    update_parser.add_argument("--contrast", type=float)

    # theme update-variant [ash|coal|graphite|diamond]
    variant_parser = theme_sub.add_parser("update-variant")
    variant_parser.add_argument("variant", choices=["ash", "coal", "graphite", "diamond"])

    # theme update-mode [light|dark]
    mode_parser = theme_sub.add_parser("switch-mode")
    mode_parser.add_argument("mode", choices=["light", "dark"])

    # theme toggle-mode / theme set-contrast
    theme_sub.add_parser("toggle-mode")
    
    contrast_parser = theme_sub.add_parser("set-contrast")
    contrast_parser.add_argument("value", type=float)

    # theme wallpaper img [--update-theme]
    wall_parser = theme_sub.add_parser("wallpaper")
    wall_parser.add_argument("image", help="Path to wallpaper image")
    wall_parser.add_argument("--update-theme", action="store_true")

    # theme set-font name
    font_parser = theme_sub.add_parser("set-font")
    font_parser.add_argument("font", help="Font family name")

    # ==========================================
    # CONTROLLER COMMANDS
    # Usage: controller [run <name> | close-all]
    # ==========================================
    controller_parser = subparsers.add_parser("controller")
    ctrl_sub = controller_parser.add_subparsers(dest="action", required=True)
    
    run_parser = ctrl_sub.add_parser("run")
    run_parser.add_argument("name", help="Name of the controller")
    
    ctrl_sub.add_parser("close-all")

    return parser
