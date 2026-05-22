from carbon.ipc.clients import Client
from carbon.ipc.payloads import CommandRequest
from carbon.utils import CarbonError, Color

import sys


def help():
	return """ -- Carbon Shell Utility --
Usage:
	carbon.shell [manager] [handler] {{--key value}}

For help on any particular manager, use:
	carbon.shell [manager] help"""


def parseArgs(argv: list[str]):
	
	if len(argv) < 2:
		print(help())
		exit(2)
	
	manager, handler, *rest = argv
	args = {}
	it = iter(rest)
	for token in it:
		if token.startswith("--"):
			args[token[2:]] = next(it, None)
			
	return manager, handler, args


def main():
	
	manager, handler, args =  parseArgs(sys.argv[1:])

	request = CommandRequest(
		manager,
		handler,
		args
	)

	client = Client()

	try:
		output = client.send(request)
	except CarbonError as e:
		e.halt()
	finally:
		client.close()

	if output.code != 0:
		Color.Print("[Error] ", Color.red, end="")
	print(output.output)
	exit(output.code)


if __name__ == "__main__":
	main()