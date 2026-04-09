from carbon.ipc.clients import Client
from carbon.ipc.payloads import CommandRequest

from .args import getParser

import subprocess, sys
from carbon.core.main import main as core_main
from carbon.utils import CarbonError

def sendRequest(request: CommandRequest):
	client = Client()
	try:
		return client.send(request)
	except CarbonError as e:
		e.halt()
	finally:
		client.close()


def handleDaemon(args):

	if args.action == "start":

		process = subprocess.Popen(
			[sys.executable, "-m", "carbon.core"],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,  
			stdin=subprocess.DEVNULL,
			start_new_session=True
		)

		print(f"Daemon started successfully. (pid = {process.pid})")
		exit(0)

	elif args.action == "restart":

		request = CommandRequest("daemon", "shutdown", {})
		out = sendRequest(request)

		if out.code != 0:
			print("Failed to shutdown daemon:", out.output)
			exit(1)

		process = subprocess.Popen(
			[sys.executable, "-m", "carbon.core"],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,  
			stdin=subprocess.DEVNULL,
			start_new_session=True
		)

		print(f"Daemon restarted successfully. (pid = {process.pid})")
		exit(0)

	elif args.action == "end":


		request = CommandRequest("daemon", "shutdown", {})
		out = sendRequest(request)
		if out.code != 0:
			print("Failed to shutdown daemon:", out.output)
			exit(1)

		print(out.output)
		exit(0)

	elif args.action == "load-state":

		request = CommandRequest("daemon", "load-state", {})
		out = sendRequest(request)
		print(out.output)

	elif args.action == "save-state":

		request = CommandRequest("daemon", "save-state", {})
		out = sendRequest(request)
		print(out.output)
	
	exit(out.code)


def handleTheme(args):

	action = args.action
	
	if action == "update":
		source = "wallpaper" if args.image else "hex"
		request = CommandRequest("theme", "update-theme", 
			{
				"mode" : args.mode if args.mode else None,
				"variant": args.variant if args.variant else None,
				"contrast": args.contrast if args.contrast else None,
				"source": source,
				"img": args.image if args.image else None,
				"hex": args.hex if args.hex else None
			}
		)
		output = sendRequest(request)
		print(output.output)
		

	elif action == "update-variant":
		request = CommandRequest("theme", "update-theme", 
			{
				"variant": args.variant
			}
		)
		output = sendRequest(request)
		print(output.output)


	elif action == "switch-mode":
		request = CommandRequest("theme", "switch-mode", 
			{
				"mode": args.mode
			}
		)
		output = sendRequest(request)
		print(output.output)
		

	elif action == "toggle-mode":
		request = CommandRequest("theme", "toggle-mode", {})
		output = sendRequest(request)
		print(output.output)
		

	elif action == "set-contrast":
		request = CommandRequest("theme", "update-theme", 
			{
				"contrast": args.contrast
			}
		)
		output = sendRequest(request)
		print(output.output)

		
	elif action == "wallpaper":

		if args.update_theme:

			request = CommandRequest("theme", "update-theme", 
				{
					"source": "wallpaper",
					"img": args.image
				}
			)
			output = sendRequest(request)
			print(output.output)

		else:

			request = CommandRequest("theme", "set-wallpaper", 
				{
					"img": args.image
				}
			)
			output = sendRequest(request)
			print(output.output)

		
	elif action == "set-font":
		request = CommandRequest("theme", "change-font", 
			{
				"font": args.font
			}
		)
		output = sendRequest(request)
		print(output.output)

	elif action == "set-face":
		request = CommandRequest("theme", "set-face", 
			{
				"img": args.img
			}
		)
		output = sendRequest(request)
		print(output.output)

	exit(output.code)

def handleController(args):

	action = args.action
	
	if action == "run":
		request = CommandRequest("controller", "run", 
			{
				"name": args.name
			}
		)
		output = sendRequest(request)
		print(output.output)

	elif action == "close-all":
		request = CommandRequest("controller", "close-all", {})
		output = sendRequest(request)
		print(output.output)

	exit(output.code)


def handleNightlight(args):

	action = args.action

	if action == "set-temperature":
		request = CommandRequest("nightlight", "set-temperature",
			{
				"value": args.value
			}			   
		)
		output = sendRequest(request)
		print(output.output)

	elif action == "set-gamma":
		request = CommandRequest("nightlight", "set-gamma",
			{
				"value": args.value
			}			   
		)
		output = sendRequest(request)
		print(output.output)

	exit(output.code)


def main():

	args = getParser().parse_args()

	if args.category == "daemon":
		handleDaemon(args)
		
	elif args.category == "theme":
		handleTheme(args)
		
	elif args.category == "controller":
		handleController(args)

	elif args.category == "nightlight":
		handleNightlight(args)


