import argparse


def getParser() -> argparse.ArgumentParser:

	parser = argparse.ArgumentParser(
		prog="carbon.shell",
		description="Carbon Shell — daemon and shell control utility",
	)

	parser.add_argument("--version", "-v", action="store_true", help="Show version")
	
	sub = parser.add_subparsers(dest="command", metavar="COMMAND")
	sub.required = True
	
	# ── help ────────────────────────────────────────────────────────────────
	sub.add_parser("help", help="Show this help message")

	# ── daemon ────────────────────────────────────────────────────────────────
	daemon = sub.add_parser("daemon", help="Manage the Carbon daemon")
	daemon_sub = daemon.add_subparsers(dest="daemon_cmd", metavar="ACTION")
	daemon_sub.required = True

	daemon_sub.add_parser("start",      help="Start the daemon")
	daemon_sub.add_parser("restart",    help="Restart the daemon")
	daemon_sub.add_parser("end",        help="Ask daemon to shut down")
	daemon_sub.add_parser("save-state", help="Persist current state to disk")
	daemon_sub.add_parser("load-state", help="Load state from disk")
	daemon_sub.add_parser("get-dispatch-map", help="Get internal dispatch map")

	# ── theme ─────────────────────────────────────────────────────────────────
	theme = sub.add_parser("theme", help="Control theming")
	theme_sub = theme.add_subparsers(dest="theme_cmd", metavar="ACTION")
	theme_sub.required = True

	# update
	update = theme_sub.add_parser("update", help="Generate and apply a new theme")
	src = update.add_mutually_exclusive_group(required=True)
	src.add_argument("--img",  metavar="PATH",  help="Wallpaper image to derive palette from")
	src.add_argument("--hex",  metavar="COLOR", help="Hex color to derive palette from (e.g. #a0c4ff)")
	update.add_argument("--mode",    choices=["dark", "light"],                         default=None, metavar="MODE")
	update.add_argument("--variant", choices=["ash", "coal", "graphite", "diamond"],    default=None, metavar="VARIANT")
	update.add_argument("--contrast",type=float,                                        default=None, metavar="AMOUNT")

	# update-variant
	uv = theme_sub.add_parser("update-variant", help="Change palette variant")
	uv.add_argument("variant", choices=["ash", "coal", "graphite", "diamond"])

	# switch-mode
	sm = theme_sub.add_parser("switch-mode", help="Switch to a specific mode")
	sm.add_argument("mode", choices=["dark", "light"])

	theme_sub.add_parser("toggle-mode", help="Toggle between dark and light")

	# set-wallpaper
	sw = theme_sub.add_parser("set-wallpaper", help="Set wallpaper without regenerating theme")
	sw.add_argument("img", metavar="PATH")

	# set-face
	sf = theme_sub.add_parser("set-face", help="Set user face image")
	sf.add_argument("img", metavar="PATH")

	# set-font
	sfont = theme_sub.add_parser("set-font", help="Set UI font")
	sfont.add_argument("font", metavar="NAME")

	# ── nightlight ────────────────────────────────────────────────────────────
	nightlight = sub.add_parser("nightlight", help="Control night light / color temperature")
	nl_sub = nightlight.add_subparsers(dest="nightlight_cmd", metavar="ACTION")
	nl_sub.required = True

	nl_sub.add_parser("on",     help="Enable nightlight")
	nl_sub.add_parser("off",    help="Disable nightlight")
	nl_sub.add_parser("toggle", help="Toggle nightlight")

	st = nl_sub.add_parser("set-temperature", help="Set color temperature (Kelvin)")
	st.add_argument("value", type=int, metavar="KELVIN")

	sg = nl_sub.add_parser("set-gamma", help="Set gamma value")
	sg.add_argument("value", type=float, metavar="GAMMA")

	# ── notifications ─────────────────────────────────────────────────────────
	notif = sub.add_parser("notifications", help="Control notifications")
	notif_sub = notif.add_subparsers(dest="notif_cmd", metavar="ACTION")
	notif_sub.required = True

	dnd = notif_sub.add_parser("dnd", help="Do Not Disturb")
	dnd.add_argument("state", choices=["on", "off", "toggle"])

	# ── controller ────────────────────────────────────────────────────────────
	ctrl = sub.add_parser("controller", help="Open/close shell menus")
	ctrl_sub = ctrl.add_subparsers(dest="ctrl_cmd", metavar="ACTION")
	ctrl_sub.required = True

	run = ctrl_sub.add_parser("run", help="Open a named menu/controller")
	run.add_argument("name", metavar="NAME")

	ctrl_sub.add_parser("close", help="Close the active controller")

	return parser