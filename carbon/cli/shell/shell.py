from carbon.ipc.clients import Client
from carbon.ipc.payloads import CommandRequest
from carbon.utils import CarbonError, Color

import sys


def help():
	return """ -- Carbon Shell Utility --
Usage:
	carbon.shell [manager] [handler] {{--key value}}

For help on any particular manager, use:
	carbon.shell [manager] help

For complete help:
	carbon.shell daemon help-all

For a list of managers:
	carbon.shell daemon list-managers"""


def parseArgs(argv):
	if argv is None:
		argv = sys.argv[1:]

	result = {
		"manager": None,
		"handler": None,
		"flags": {}
	}

	argv = [str(a) for a in argv]

	i = 0

	# manager
	if i < len(argv) and not argv[i].startswith("--"):
		val = argv[i].strip()
		if not val:
			return result
		result["manager"] = val
		i += 1

	# handler
	if i < len(argv) and not argv[i].startswith("--"):
		val = argv[i].strip()
		if not val:
			return result
		result["handler"] = val
		i += 1

	# flags
	while i < len(argv):
		token = argv[i]

		if not token.startswith("--"):
			raise ValueError(
				f"Unexpected positional {token!r} argument."
			)

		key = token[2:].strip()
		
		if not key:
			raise ValueError(f"Empty flag name at index {i} (bare '--' not allowed)")

		if key in result["flags"]:
			raise ValueError(f"Duplicate flag --{key}")

		values = []
		i += 1

		while i < len(argv) and not argv[i].startswith("--"):
			v = argv[i]
			if not v.strip():
				raise ValueError(f"Empty value at index {i} for flag --{key}")
			values.append(v)
			i += 1

		if len(values) == 0:
			raise ValueError(f"No value provided to key '{key}'")
		elif len(values) == 1:
			result["flags"][key] = values[0]
		else:
			result["flags"][key] = " ".join(values)


	return result


def main():
	
	try:
		result =  parseArgs(sys.argv[1:])

		if result["manager"] is None:
			print(help())
			exit(2)

		if result["manager"] == "help":
			print(help())
			exit(2)
	
		if result["handler"] is None:
			result["handler"] = "help"
		
	except ValueError as e:
		Color.Print("[Error] ", Color.red, end="")
		print(str(e))
		exit(1)
			
	request = CommandRequest(
		result["manager"],
		result["handler"],
		result["flags"]
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