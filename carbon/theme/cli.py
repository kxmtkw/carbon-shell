import argparse
import sys
from typing import Literal

from carbon.config import CarbonConfig
from carbon.config.defaults import ConfigDefaults
from carbon.theme import Theme


TC: dict = {}


def load_theme_config():
    global TC
    TC = {
        "source":    CarbonConfig.get("theme.source",    ConfigDefaults.source,    valid_types=(str,), valid_values=["wallpaper", "hex"]),
        "wallpaper": CarbonConfig.get("theme.wallpaper", ConfigDefaults.wallpaper, valid_types=(str,)),
        "hex":       CarbonConfig.get("theme.hex",       ConfigDefaults.hex,       valid_types=(str,)),
        "mode":      CarbonConfig.get("theme.mode",      ConfigDefaults.mode,      valid_types=(str,), valid_values=["light", "dark"]),
        "variant":   CarbonConfig.get("theme.variant",   ConfigDefaults.variant,   valid_types=(str,), valid_values=["ash", "coal", "graphite", "diamond"]),
        "contrast":  CarbonConfig.get("theme.contrast",  ConfigDefaults.contrast,  valid_types=(float, int)),
    }


def set_config(key: str, value):
    CarbonConfig.set(f"theme.{key}", value)
    TC[key] = value


def cmd_update(args):
    mode     = args.mode     or TC["mode"]
    variant  = args.variant  or TC["variant"]
    contrast = args.contrast or TC["contrast"]

    if args.image:
        Theme.change_color_theme(mode, variant, img=args.image, contrast=contrast)
        set_config("wallpaper", args.image)
        set_config("source",    "wallpaper")
    else:
        Theme.change_color_theme(mode, variant, hex=args.hex, contrast=contrast)
        set_config("hex",    args.hex)
        set_config("source", "hex")

    set_config("mode",     mode)
    set_config("variant",  variant)
    set_config("contrast", contrast)


def cmd_update_variant(args):
    if TC["source"] == "wallpaper":
        Theme.change_color_theme(TC["mode"], args.variant, img=TC["wallpaper"], contrast=TC["contrast"])
    else:
        Theme.change_color_theme(TC["mode"], args.variant, hex=TC["hex"], contrast=TC["contrast"])
    set_config("variant", args.variant)


def cmd_update_mode(args):
    Theme.switch_theme_mode(args.mode)
    set_config("mode", args.mode)


def cmd_toggle_mode(args):
    new_mode: Literal["light", "dark"] = "dark" if TC["mode"] == "light" else "light"
    Theme.switch_theme_mode(new_mode)
    set_config("mode", new_mode)


def cmd_set_contrast(args):
    if TC["source"] == "wallpaper":
        Theme.change_color_theme(TC["mode"], TC["variant"], img=TC["wallpaper"], contrast=args.contrast)
    else:
        Theme.change_color_theme(TC["mode"], TC["variant"], hex=TC["hex"], contrast=args.contrast)
    set_config("contrast", args.contrast)


def cmd_wallpaper(args):
    if args.update_theme:
        Theme.change_color_theme(TC["mode"], TC["variant"], img=args.image, contrast=TC["contrast"])
        set_config("source", "wallpaper")

    Theme.set_wallpaper(args.image)
    set_config("wallpaper", args.image)


def cmd_set_font(args):
    Theme.set_font(args.font)
    set_config("font", args.font)


def main():
    parser = argparse.ArgumentParser(prog="carbon.theme")
    sub = parser.add_subparsers(dest="command")

    p_update = sub.add_parser("update")
    src = p_update.add_mutually_exclusive_group(required=True)
    src.add_argument("--image", metavar="IMG")
    src.add_argument("--hex",   metavar="HEX")
    p_update.add_argument("--variant",    choices=["ash", "coal", "graphite", "diamond"])
    p_update.add_argument("--mode",     choices=["light", "dark"])
    p_update.add_argument("--contrast", type=float)

    p_variant = sub.add_parser("update-variant")
    p_variant.add_argument("variant", choices=["ash", "coal", "graphite", "diamond"])

    p_mode = sub.add_parser("update-mode")
    p_mode.add_argument("mode", choices=["light", "dark"])

    sub.add_parser("toggle-mode")

    p_contrast = sub.add_parser("set-contrast")
    p_contrast.add_argument("contrast", type=float)

    p_wallpaper = sub.add_parser("wallpaper")
    p_wallpaper.add_argument("image", metavar="IMG")
    p_wallpaper.add_argument("--update-theme", action="store_true")

    p_font = sub.add_parser("set-font")
    p_font.add_argument("font", metavar="NAME")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    load_theme_config()

    if args.command == "update":
        cmd_update(args)
    elif args.command == "update-variant":
        cmd_update_variant(args)
    elif args.command == "update-mode":
        cmd_update_mode(args)
    elif args.command == "toggle-mode":
        cmd_toggle_mode(args)
    elif args.command == "set-contrast":
        cmd_set_contrast(args)
    elif args.command == "wallpaper":
        cmd_wallpaper(args)
    elif args.command == "set-font":
        cmd_set_font(args)


if __name__ == "__main__":
    main()