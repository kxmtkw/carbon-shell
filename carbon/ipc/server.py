import socket, threading, os, select, json
from queue import Queue, Empty
from dataclasses import asdict

from carbon.utils import CarbonError, logger

from .payloads import CommandRequest, CommandOutput

class Server:

	address = "/tmp/carbon.portal"
	
	def __init__(self, timeout: float = 0.5):

		logger.log("server", f"Starting server at {self.address}", logger.Level.info)

		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		self.clients: dict[int, socket.socket] = {}

		try:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind(Server.address)
		except Exception as e:
			logger.log("server", f"Could not start carbon server. Reason: {e.__class__.__name__}::{str(e)}", logger.Level.critical)
			exit(1)

		self.socket.settimeout(timeout)
		self.socket.listen()
		logger.log(
			"server",
			"Server is listening.",
			logger.Level.info
		)
		

	def close(self):
		self.socket.shutdown(socket.SHUT_WR)
		self.socket.close()
		os.remove(Server.address)
		logger.log(
			"server",
			"Successfully closed server socket.",
			logger.Level.info
		)

	
	def listen(self) -> tuple[int, CommandRequest] | None:
		

		while True:

			try:
				conn, _ = self.socket.accept()
			except TimeoutError, OSError:
				return None
			
			id = len(self.clients)
			self.clients[id] = conn

			logger.log("server", f"Got request! Associated id:{id} with client.", logger.Level.debug)

			buffer = b""
			while True:
				chunk = conn.recv(2048)
				buffer += chunk
				
				if not chunk or b'\n' in chunk: break

			buffer = buffer.decode()

			if "\n" not in buffer: 
				logger.log("server", f"Incomplete payload from client with id:{id}", logger.Level.warning)
				continue

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
			logger.log("server", f"Connection not found for client id:{client_id}. Maybe they disconnected.", logger.Level.warning)
			return

		try:
			payload = output.serialize().encode('utf-8')
			conn.sendall(payload)
		except (BrokenPipeError, ConnectionResetError):
			logger.log("server", f"Connection broken with client id:{client_id}. Maybe they disconnected.", logger.Level.warning)
		except Exception as e:
			logger.log("server", f"Unexpected error occured: {e.__class__.__name__}({str(e)})", logger.Level.warning)
		finally:
			self.cleanup_client(client_id)


	def cleanup_client(self, client_id: int):
		logger.log("server", f"Cleaning up client with id:{client_id}.", logger.Level.debug)
		conn = self.clients.pop(client_id, None)
		if conn:
			try:
				conn.close()
			except:
				pass
			


