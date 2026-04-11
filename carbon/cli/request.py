from carbon.ipc.clients import Client
from carbon.ipc.payloads import CommandRequest
from carbon.utils import CarbonError

def sendRequest(request: CommandRequest):
	client = Client()
	try:
		return client.send(request)
	except CarbonError as e:
		e.halt()
	finally:
		client.close()