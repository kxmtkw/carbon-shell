import socket
from .payloads import CommandRequest, CommandOutput
from carbon.utils import CarbonError

from .server import Server

class Client:

    address = Server.address

    def __init__(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.is_conntected = False


    def close(self):
        self.socket.close()


    def send(self, request: CommandRequest) -> CommandOutput:

        try:

            if not self.is_conntected:
                self.socket.connect(Client.address)
                self.is_conntected = True

            payload = request.serialize().encode('utf-8')
            self.socket.sendall(payload)

            buffer = b""
            while True:
                chunk = self.socket.recv(2048)

                if not chunk:
                    raise CarbonError("Server closed connection before responding.")
                
                buffer += chunk
                if b'\n' in chunk:
                    break

            response_line = buffer.decode('utf-8').splitlines()[0]
            return CommandOutput.deserialize(response_line)

        except FileNotFoundError:
            raise CarbonError(f"Carbon server is not running (socket not found at {self.address}).")
        except ConnectionRefusedError:
            raise CarbonError("Connection refused. Is the Carbon daemon dead?")
        except socket.timeout:
            raise CarbonError("Request timed out waiting for server response.")
        except Exception as e:
            raise CarbonError(f"Client communication error: {e.__class__.__name__}::{str(e)}")
