from carbon.ipc.clients import Client
from carbon.ipc.payloads import CommandRequest
from carbon.utils import CarbonError, Color
import subprocess, sys, time

def help():
	return """ -- Carbon Daemon Utility --
Usage:
	--start      Start the daemon.
	--restart    Restart the daemon.
	--end        Kill the daemon.
	--help       Print this message."""


def parseFlag(argv: list[str]) -> str | None:
    for token in argv:
        if token.startswith("--"):
            return token[2:]
    return None


def sendRequest(request: CommandRequest):
	client = Client()
	try:
		return client.send(request)
	except CarbonError as e:
		e.halt()
	finally:
		client.close()


def start():
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


def restart():
	request = CommandRequest(
		"daemon", "end",
		{				
		}
	)
	output = sendRequest(request)

	if output.code != 0:
		print(output.output)
		exit(output.code)

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


def end():
	request = CommandRequest(
		"daemon", "end",
		{				
		}
	)
	output = sendRequest(request)
	print(output.output)
	exit(output.code)


def main():
    
	flag = None
	if len(sys.argv) > 1:
		flag = parseFlag(sys.argv)

	if flag is None:
		print(f"No flag provided!")
		print(help())
		exit(2)
		
	match flag:
		case "start":
			start()
		case "restart":
			restart()
		case "end":
			end()
		case "help":
			print(help())
			exit(2)
		case _:
			print(f"Unknown flag: {flag}")
			print(help())
			exit(2)
            
	