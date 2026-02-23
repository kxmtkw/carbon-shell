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
	themeupdater.add_argument("image", help="Source image")
	themeupdater.add_argument("theme", choices=["dark", "light"], help="Theme mode")
	themeupdater.add_argument(
		"variant",
		choices=["ash", "coal", "graphite", "diamond"],
		help="Theme variant"
	)
	themeupdater.add_argument("--contrast", dest="contrast", help="Theme contrast", type=float)


	# switch
	mode =subparsers.add_parser("switch-mode", help="Switch between light and dark mode")
	mode.add_argument("mode", choices=["light", "dark"])

	# wall no colors
	wall = subparsers.add_parser(
		"update-wallpaper",
		help="Set wallpaper (via swww)"
	)
	wall.add_argument("image", help="Path to Image.")


	return parser


def parseArgs():
	parser = buildParser()
	args = parser.parse_args()
	return args

