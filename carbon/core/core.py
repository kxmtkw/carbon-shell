import json
import threading, dataclasses
from concurrent.futures import ThreadPoolExecutor

from carbon.ipc.server import Server
from carbon.ipc.payloads import CommandRequest, CommandOutput

from carbon.utils import CarbonError, logger, Notify, shellrun, locked

from carbon.state import StateManager
from carbon.lib.quickshell import Quickshell
from carbon.lib.dbus import DBus

from carbon.managers import BaseManager, MANAGERS

class CarbonCore:

	coreLock = threading.Lock()

	def __init__(self):

		logger.log("core", "Hello World!", logger.Level.info)

		self.server = Server(1)
		self.dbus = DBus()
		self.state = StateManager("~/.carbon/user/state.toml")

		self.lock = threading.Lock()
		self.thread_pool = ThreadPoolExecutor(10)
		self.is_running = True


	def init(self):
		
		# Starting quiskshell

		self.quickshell = Quickshell()
		try:
			self.quickshell.start()
		except Quickshell.Error as e:
			logger.log("core", f"Quickshell could not be started. Reason: {e.msg}", logger.Level.warning)


		# starting up managers

		self.managers: dict[str, BaseManager] = {}

		for mgr_class in MANAGERS:
			manager = mgr_class()
			self.managers[manager.name()] = manager

		self.dispatch_map = {
			"daemon": {
				"shutdown":         self.shutdown,
				"load-state":       self.loadState,
				"save-state":       self.saveState,
				"dump-state":       self.dumpState,
				"get-dispatch-map": self.getDispatchMap,
				"help-all":         self.getAllHelp
			}
		}

		for name, manager in self.managers.items():
			manager.start()
			self.dispatch_map[name] = manager.handlers()

		# wiring things up,
		# this needs to be done indpendently, might make each manager do this own its own instead of depending on the core.

		Notify.setNotificationFunction(self.dbus.notification_server.sendNotification)

		self.managers["controller"].setManagers(self.managers["theme"], self.managers["panel"])

		self.dbus.notification_server.setCallback(self.managers["notifications"].newNotification)
		self.dbus.upower.setCallback(self.managers["power"].UPowerCallback)
		self.dbus.start()


		Notify(
			"Hello World!",
			f"Logged in as: {shellrun("whoami")[1].strip()}",
			timeout=5000
		)
		
		try:
			self.loadState()
		except CarbonError as e:
			Notify(
				"State not loaded.",
				e.msg,
				urgency="critical"
			)


	def run(self):

		while self.is_running:
			payload = self.server.listen()
			if payload is None: continue
			self.dispatch(*payload)


	@locked(coreLock)
	def shutdown(self) -> str:

		if not self.is_running: 
			return "This call shouldn't have been possible."

		self.saveState()

		logger.log(
			"core",
			"Killing quickshell.",
			logger.Level.debug
		)
		self.quickshell.kill()

		self.is_running = False
		self.thread_pool.shutdown(False, cancel_futures=True)

		for manager in self.managers.values():
			manager.end()

		self.server.close()

		logger.log("core", "Shutting down.", logger.Level.info)

		return "Shutting down."
	

	def loadState(self) -> str:

		errors = ""
		
		if not self.state.load():
			msg = f"Corrupted state file. Invalid Json: {self.state.file}."

			logger.log(
				"core",
				msg,
				logger.Level.warning
			)  
			errors += msg
				

		for name, manager in self.managers.items():
			state = self.state.get(name)

			logger.log(
				"core",
				f"Loading state for manager {manager.__class__.__name__}",
				logger.Level.debug
			)

			if state is None: 
				logger.log(
					"core",
					f"Loading default state for manager {manager.__class__.__name__}",
					logger.Level.debug
				)
				manager.setState(manager.state) # default state
				continue

			try:
				manager.setState(manager.State(**state))
			except TypeError as e:
				msg = f"Corrupted state loaded for manager {name}: Does not match state structure. {str(e)}"
				logger.log(
					"core",
					msg,
					logger.Level.warning
				)
				errors += msg + "\n"
			except CarbonError as e:
				msg = f"Corrupted state loaded for manager {name}: {e.msg}"
				logger.log(
					"core",
					msg,
					logger.Level.warning
				)
				errors += msg + "\n"
				continue


		logger.log("core", "Loaded state.", logger.Level.info)
		
		if errors:
			raise CarbonError(errors.strip())
		
		return "State loaded successfully."


	def saveState(self):
		
		for name, manager in self.managers.items():
			self.state.update(
				name,
				dataclasses.asdict(manager.getState())
			)

		self.state.save()
		logger.log("core", "Saved state.", logger.Level.info)

		return "State saved."
	

	def dumpState(self) -> str:
		
		for name, manager in self.managers.items():
			self.state.update(
				name,
				dataclasses.asdict(manager.getState())
			)

		return self.state.dump()
	
	
	def getDispatchMap(self):

		dispatch_map = {}

		for key, value in self.dispatch_map.items():
			dispatch_map[key] = list(value.keys())

		string = json.dumps(dispatch_map, indent=4)

		return string
		

	def getHelp(self):
		return _help
	

	def getAllHelp(self):
		all_help = " -- Carbon Shell --"
		all_help += self.getHelp()

		for manager in self.managers.values():
			all_help += manager.getHelp()

		return all_help


	def dispatch(self, id: int, command: CommandRequest):
		
		logger.log("core", f"Received dispatch request from id:{id}.", logger.Level.info)

		try:
			manager_map = self.dispatch_map[command.manager]
		except KeyError:
			logger.log("core", f"Unknown manager requested by client(id:{id}): {command.manager}", logger.Level.warning)
			with self.lock:
				self.server.send(id, CommandOutput(1,f"Unknown manager: {command.manager}"))
				return
			
		if command.handler == "help":
			if command.manager == "daemon":
				handler = self.getHelp
			else:
				handler = self.managers[command.manager].getHelp

		elif command.handler not in manager_map:
			logger.log("core", f"Unknown handler '{command.handler}' for manager '{command.manager}' client(id:{id})", logger.Level.warning)
			with self.lock:
				self.server.send(id, CommandOutput(1, f"Unknown handler for {command.manager}: {command.handler}"))
			return
		
		else:
			handler = manager_map[command.handler]

		logger.log("core", f"Executing {command.manager}::{command.handler} with arguments: {command.args}", logger.Level.debug)
		self.thread_pool.submit(self.worker, id, command.manager, command.handler, handler, command.args, save_state=True if command.manager != "daemon" else False)


	def worker(self, id: int, manager: str, handler: str, func, args, *, save_state=True):

		try:
			response = func(**args)
			code = 0
		except CarbonError as e:
			response = e.msg
			code = 1
			logger.log(
				"core", 
				f"Carbon Error while executing {manager}::{handler} with arguments {args}: {str(e)}", 
				logger.Level.debug
			)
		except TypeError as e:
			response = f"{manager}::{handler} {" ".join(str(e).split(" ")[1:])}"
			code = 1
			logger.log(
				"core", 
				f"Type Error while executing {func.__name__} with arguments {args}: {str(e)}", 
				logger.Level.debug
			)
		except Exception as e:
			response = f"{e.__class__.__name__}: {str(e)}"
			code = 1
			logger.log(
				"core", 
				f"Unexpected Error while executing {func.__name__} with arguments {args}: ({e.__class__.__name__}) {str(e)}", 
				logger.Level.warning
			)

		output = CommandOutput(code, response)

		with self.lock:
			self.server.send(id, output)
			if save_state:
				self.saveState()


_help = """
==> daemon
Used to control the shell daemon and do special tasks.

handlers:

	> shutdown
		Shut the daemon down. Use carbon.daemon --end.
	> load-state
		Load state from state file.
	> save-state
		Manually save the state.
	> dump-state
		Print the state to the terminal.
	> get-dispatch-map
		Print dispatch map.
"""