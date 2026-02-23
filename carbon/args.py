import argparse

def buildParser() -> argparse.ArgumentParser:
	
	parser = argparse.ArgumentParser(
		prog="carbon",
		formatter_class=argparse.RawTextHelpFormatter
	)

	subparsers = parser.add_subparsers(dest="command", required=True)

	# install / uninstall
	subparsers.add_parser("install", help="Install Carbon")
	subparsers.add_parser("uninstall", help="Uninstall Carbon")

	# themeupdater
	themeupdater = subparsers.add_parser("update-theme", help="Set color theme")
	themeupdater.add_argument("theme", choices=["dark", "light"], help="Theme mode")
	source_group = themeupdater.add_mutually_exclusive_group(required=True)
	source_group.add_argument("--img", dest="image", help="Source image")
	source_group.add_argument("--hex", dest="hex", help="Source hex color")
	themeupdater.add_argument("--contrast", dest="contrast", help="Theme contrast", type=float)
	themeupdater.add_argument(
		"variant",
		choices=["ash", "coal", "graphite", "diamond"],
		help="Theme variant"
	)

	# switch
	mode =subparsers.add_parser("switch-mode", help="Switch between light and dark mode")
	mode.add_argument("mode", choices=["light", "dark"])

	# wall no colors
	wallc = subparsers.add_parser(
		"update-wallpaper",
		help="Set wallpaper (via swww)"
	)
	wallc.add_argument("image", help="Path to Image.")

	# wall
	wall = subparsers.add_parser(
		"update-wallpaper-theme",
		help="Set wallpaper (via swww) and change the color theme"
	)
	wall.add_argument("image", help="Path to Image.")
	wall.add_argument("theme", choices=["dark", "light"], help="Theme mode")
	wall.add_argument("--contrast", dest="contrast", help="Theme contrast", type=float)
	wall.add_argument(
		"variant",
		choices=["ash", "coal", "graphite", "diamond"],
		help="Theme variant"
	)

	return parser


def parseArgs():
	parser = buildParser()
	args = parser.parse_args()
	return args

