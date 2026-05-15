from .args import getParser
from .handlers import (
	handle_daemon,
	handle_theme,
	handle_nightlight,
	handle_idle,
	handle_notifications,
	handle_controller,
	handle_panel,
	handle_lock
)


def main():
	parser = getParser()
	args = parser.parse_args()

	match args.command:
		case "daemon":
			handle_daemon(args)
		case "theme":
			handle_theme(args)
		case "nightlight":
			handle_nightlight(args)
		case "idle":
			handle_idle(args)
		case "notifications":
			handle_notifications(args)
		case "controller":
			handle_controller(args)
		case "panel":
			handle_panel(args)
		case "lockscreen":
			handle_lock(args)
		case _:
			parser.print_help()


if __name__ == "__main__":
	main()
