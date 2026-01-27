import argparse

def buildParser() -> argparse.ArgumentParser:
	
	parser = argparse.ArgumentParser(
		prog="carbon",
		description="Carbon Shell — because theming your system is apparently a personality trait.",
		formatter_class=argparse.RawTextHelpFormatter
	)

	subparsers = parser.add_subparsers(dest="command", required=True)

	# install / uninstall
	subparsers.add_parser("install", help="Install Carbon")
	subparsers.add_parser("uninstall", help="Uninstall Carbon")

	# colorify
	colorify = subparsers.add_parser("colorify", help="Set color theme")
	colorify.add_argument("theme", choices=["dark", "light"], help="Theme mode")
	source_group = colorify.add_mutually_exclusive_group(required=True)
	source_group.add_argument("--img", dest="image", help="Source image")
	source_group.add_argument("--hex", dest="hex", help="Source hex color")
	colorify.add_argument(
		"variant",
		choices=["ash", "coal", "graphite", "diamond"],
		help="Theme variant"
	)

	# switch
	theme =subparsers.add_parser("switch", help="Switch between light and dark mode")
	theme.add_argument("theme", choices=["light", "dark"])

	# wall
	wall = subparsers.add_parser(
		"wall",
		help="Set wallpaper (via swww) and change the color theme"
	)
	wall.add_argument("image", help="Path to Image.")
	wall.add_argument("theme", choices=["dark", "light"], help="Theme mode")
	wall.add_argument(
		"variant",
		choices=["ash", "coal", "graphite", "diamond"],
		help="Theme variant"
	)
	wall.add_argument("--cache", action="store_true")


	# controllers
	launch = subparsers.add_parser(
		"launch",
		help="Launch a controller"
	)
	launch.add_argument("controller", help="controller name")

	return parser


def parseArgs():
	parser = buildParser()
	args = parser.parse_args()
	return args

