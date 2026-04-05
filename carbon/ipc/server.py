import socket, threading, os, select, json
from queue import Queue, Empty
from dataclasses import asdict

from carbon.utils import CarbonError

from .payloads import CommandRequest, CommandOutput

class Server:

	address = "/tmp/carbon.portal"
	
	def __init__(self, timeout: float = 0.5):
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		self.clients: dict[int, socket.socket] = {}

		try:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind(Server.address)
		except Exception as e:
			CarbonError(f"Could not start carbon server. Reason: {e.__class__.__name__}::{str(e)}").halt()

		self.socket.settimeout(timeout)
		self.socket.listen()
		

	def close(self):
		self.socket.shutdown(socket.SHUT_WR)
		self.socket.close()
		os.remove(Server.address)

	
	def listen(self) -> tuple[int, CommandRequest]:
	
		while True:

			try:
				conn, _ = self.socket.accept()
			except TimeoutError, OSError:
				return (None, None)
			
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
		
		
	def send(self, client_id: int, output: CommandOutput):

		conn = self.clients.get(client_id)
		
		if not conn:
			print(f"Error: No active connection for Client ID {client_id}")
			return

		try:
			payload = output.serialize().encode('utf-8')
			conn.sendall(payload)
			
		except (BrokenPipeError, ConnectionResetError):
			print(f"Client {client_id} disconnected before response could be sent.")
		except Exception as e:
			print(f"Failed to send to Client {client_id}: {e}")
		finally:
			self.cleanup_client(client_id)


	def cleanup_client(self, client_id: int):
		conn = self.clients.pop(client_id, None)
		if conn:
			try:
				conn.close()
			except:
				pass
			


