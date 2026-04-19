import argparse
from carbon.ipc.payloads import CommandRequest
from .request import sendRequest
import subprocess, sys, time

def handle_daemon(args: argparse.Namespace):
	manager = "daemon"

	match args.daemon_cmd:

		case "start":
			process = subprocess.Popen(
				[sys.executable, "-m", "carbon.core"],
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,  
				stdin=subprocess.DEVNULL,
				start_new_session=True
			)
			time.sleep(1)

			if process.poll() is None:
				print("Daemon successfully started.")
				return
			
			from carbon.utils import logger, Color

			print("Could not start daemon.")
			print(logger.extractStartupError(), end='')

		case "restart":

			request = CommandRequest(
				manager, "end",
				{				
				}
			)
			output = sendRequest(request)

			process = subprocess.Popen(
				[sys.executable, "-m", "carbon.core"],
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL,  
				stdin=subprocess.DEVNULL,
				start_new_session=True
			)
			time.sleep(1)

			if process.poll() is None:
				print("Daemon successfully restarted.")
				return
			
			from carbon.utils import logger, Color

			print("Could not restart daemon.")
			print(logger.extractStartupError())		

		case "end":
			request = CommandRequest(
				manager, "end",
				{				
				}
			)
			output = sendRequest(request)

		case "save-state":
			request = CommandRequest(
				manager, "save-state",
				{				
				}
			)
			output = sendRequest(request)
			print(output.output)
			exit(output.code)
			
		case "load-state":
			request = CommandRequest(
				manager, "load-state",
				{				
				}
			)
			output = sendRequest(request)
			print(output.output)
			exit(output.code)

		case "get-dispatch-map":
			request = CommandRequest(
				manager, "get-dispatch-map",
				{				
				}
			)
			output = sendRequest(request)
			print(output.output)
			exit(output.code)




def handle_theme(args: argparse.Namespace):
	manager = "theme"
	
	match args.theme_cmd:

		case "update":
			# args.img or args.hex (mutually exclusive, one guaranteed)
			# args.mode, args.variant, args.contrast (all optional)
			request = CommandRequest(
				manager, "update-theme",
				{
					"mode": args.mode,
					"variant": args.variant,
					"contrast": args.contrast,
					"hex": args.hex,
					"img": args.img,
					"source": "wallpaper" if args.img else "hex"					
				}
			)
			output = sendRequest(request)

		case "update-variant":
			# args.variant
			request = CommandRequest(
				manager, "update-theme",
				{
					"variant": args.variant					
				}
			)
			output = sendRequest(request)

		case "switch-mode":
			request = CommandRequest(
				manager, "switch-mode",
				{
					"mode": args.mode
				}
			)
			output = sendRequest(request)

		case "toggle-mode":
			request = CommandRequest(
				manager, "toggle-mode",
				{
				}
			)
			output = sendRequest(request)

		case "set-wallpaper":
			request = CommandRequest(
				manager, "set-wallpaper",
				{
					"img": args.img
				}
			)
			output = sendRequest(request)

		case "set-face":
			request = CommandRequest(
				manager, "set-face",
				{
					"img": args.img
				}
			)
			output = sendRequest(request)

		case "change-font":
			request = CommandRequest(
				manager, "change-font",
				{
					"font": args.font
				}
			)
			output = sendRequest(request)

		case "set-wallpaper-animation":
			request = CommandRequest(
				manager, "set-wallpaper-animation",
				{
					"style": args.style
				}
			)
			output = sendRequest(request)

	print(output.output)
	exit(output.code)


def handle_nightlight(args: argparse.Namespace):
	manager = "nightlight"
	match args.nightlight_cmd:

		case "on":
			request = CommandRequest(
				manager, "on",
				{
				}
			)
			output = sendRequest(request)

		case "off":
			request = CommandRequest(
				manager, "off",
				{
				}
			)
			output = sendRequest(request)
		
		case "toggle":
			request = CommandRequest(
				manager, "toggle",
				{
				}
			)
			output = sendRequest(request)

		case "set-temperature":
			request = CommandRequest(
				manager, "set-temperature",
				{
					"value": args.value					
				}
			)
			output = sendRequest(request)
			
			
		case "set-gamma":
			request = CommandRequest(
				manager, "set-gamma",
				{
					"value": args.value					
				}
			)
			output = sendRequest(request)

	print(output.output)
	exit(output.code)


def handle_notifications(args: argparse.Namespace):
	manager = "notifications"
	match args.notif_cmd:
		case "dnd":
			request = CommandRequest(
				manager, "dnd",
				{
					"state": args.state					
				}
			)
			output = sendRequest(request)

	print(output.output)
	exit(output.code)


def handle_controller(args: argparse.Namespace):
	manager = "controller"

	match args.ctrl_cmd:

		case "run":
			request = CommandRequest(
				manager, "run",
				{
					"name": args.name					
				}
			)
			output = sendRequest(request)

		case "close":
			request = CommandRequest(
				manager, "close",
				{
				}
			)
			output = sendRequest(request)

	print(output.output)
	exit(output.code)