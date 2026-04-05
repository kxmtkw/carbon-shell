from carbon.ipc.clients import Client
from carbon.ipc.payloads import CommandRequest

from .args import get_parser

import subprocess, sys
from carbon.core.main import main as core_main
from carbon.utils import CarbonError

def send_request(request: CommandRequest):
	client = Client()
	try:
		return client.send(request)
	except CarbonError as e:
		e.halt()
	finally:
		client.close()


def handle_daemon(args):

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
		out = send_request(request)

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
		out = send_request(request)
		if out.code != 0:
			print("Failed to shutdown daemon:", out.output)
			exit(1)

		print(out.output)
		exit(0)
 

def handle_theme(args):

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
		output = send_request(request)
		print(output.output)
		

	elif action == "update-variant":
		request = CommandRequest("theme", "update-theme", 
			{
				"variant": args.variant
			}
		)
		output = send_request(request)
		print(output.output)


	elif action == "switch-mode":
		request = CommandRequest("theme", "switch-mode", 
			{
				"mode": args.mode
			}
		)
		output = send_request(request)
		print(output.output)
		

	elif action == "toggle-mode":
		request = CommandRequest("theme", "toggle-mode", {})
		output = send_request(request)
		print(output.output)
		

	elif action == "set-contrast":
		request = CommandRequest("theme", "update-theme", 
			{
				"contrast": args.contrast
			}
		)
		output = send_request(request)
		print(output.output)

		
	elif action == "wallpaper":

		if args.update_theme:

			request = CommandRequest("theme", "update-theme", 
				{
					"source": "wallpaper",
					"img": args.image
				}
			)
			output = send_request(request)
			print(output.output)

		else:

			request = CommandRequest("theme", "set-wallpaper", 
				{
					"img": args.image
				}
			)
			output = send_request(request)
			print(output.output)

		
	elif action == "set-font":
		request = CommandRequest("theme", "change-font", 
			{
				"font": args.font
			}
		)
		output = send_request(request)
		print(output.output)


def handle_controller(args):

	action = args.action
	
	if action == "run":
		request = CommandRequest("controller", "run", 
			{
				"name": args.name
			}
		)
		output = send_request(request)
		print(output.output)

	elif action == "close-all":
		request = CommandRequest("controller", "close-all", {})
		output = send_request(request)
		print(output.output)


def main():

	args = get_parser().parse_args()

	if args.category == "daemon":
		handle_daemon(args)
		
	elif args.category == "theme":
		handle_theme(args)
		
	elif args.category == "controller":
		handle_controller(args)


