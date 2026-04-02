import socket, threading, os, select, json
from queue import Queue, Empty
from dataclasses import asdict

from utils import CarbonError

from .payloads import CommandRequest, CommandOutput

class Server:

	address = "/tmp/carbon.portal"
	
	def __init__(self):
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		self.clients: dict[int, socket.socket] = {}

		try:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind(Server.address)
		except Exception as e:
			CarbonError(f"Could not start carbon server. Reason: {e.__class__.__name__}::{str(e)}").halt()

		self.socket.listen()
		

	def close(self):
		self.socket.shutdown(socket.SHUT_WR)
		self.socket.close()
		os.remove(Server.address)

	
	def listen(self) -> tuple[int, CommandRequest]:
	
		while True:
			conn, _ = self.socket.accept()
			
			id = len(self.clients)
			self.clients[id] = conn

			buffer = b""
			while True:
				chunk = conn.recv(2048)
				buffer += chunk
				
				if not chunk or b'\n' in chunk: break

			buffer = buffer.decode()

			if "\n" not in buffer: 
				continue # log here

			part = buffer.splitlines()[0]

			try:
				command = CommandRequest.deserialize(part)
			except CarbonError as e:
				print(e)
				continue

			return (id, command)
			


