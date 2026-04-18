import json
import threading, dataclasses
from concurrent.futures import ThreadPoolExecutor

from carbon.ipc.server import Server
from carbon.ipc.payloads import CommandRequest, CommandOutput

from carbon.utils import CarbonError, logger, notify, shellrun, locked

from carbon.state import StateManager
from carbon.lib.quickshell import Quickshell

from carbon.managers.base import BaseManager
from carbon.managers.theme import ThemeManager
from carbon.managers.controller import ControllerManager
from carbon.managers.notifications import NotificationManager
from carbon.managers.nightlight import NightLightManager


class CarbonCore:

    def __init__(self):

        logger.log("core", "Hello World!", logger.Level.info)

        self.server = Server(1)
        self.state = StateManager("~/.carbon/user/state.json")

        self.lock = threading.Lock()
        self.thread_pool = ThreadPoolExecutor(5)
        self.is_running = True


    def init(self):

        self.theme_manager = ThemeManager()
        self.notification_manager = NotificationManager()
        self.nightlight_manager = NightLightManager()
        self.controller_manager = ControllerManager(self.theme_manager)

        self.all_managers: list[BaseManager] = [
            self.theme_manager,
            self.controller_manager,
            self.nightlight_manager,
            self.notification_manager
        ]

        self.dispatch_map = {
            "daemon": {
                "end": self.shutdown,
                "load-state": self.loadState,
                "save-state": self.saveState,
                "get-dispatch-map": self.getDispatchMap
            },
            "theme": self.theme_manager.handlers(),
            "controller": self.controller_manager.handlers(),
            "nightlight": self.nightlight_manager.handlers(),
            "notifications": self.notification_manager.handlers()
        }

        self.quickshell = Quickshell()
        try:
            self.quickshell.start()
        except Quickshell.Error as e:
            logger.log("core", f"Quickshell could not be started. Reason: {e.msg}", logger.Level.warning)

        self.loadState()


    def run(self):

        notify(
            "Hello World!",
            f"Logged in as: {shellrun("whoami")[1]}",
            timeout=8000
        )

        while self.is_running:
            payload = self.server.listen()
            if payload is None: continue
            self.dispatch(*payload)


    def shutdown(self) -> str:

        if not self.is_running: 
            return "This call shouldn't have been possible."

        logger.log(
			"core",
			"Killing quickshell.",
			logger.Level.debug
		)
        self.quickshell.kill()

        self.server.close()
        self.saveState()
        self.is_running = False
        self.thread_pool.shutdown(False, cancel_futures=True)

        logger.log("core", "Shutting down.", logger.Level.info)

        return "Shutting down."
    
    def loadState(self) -> str:
        
        if not self.state.load():
            raise CarbonError(f"Corrupted state file. Invalid Json: {self.state.file}")

        errors = ""

        for manager in self.all_managers:
            state = self.state.get(manager.__class__.__name__)

            if state is None: 
                manager.setState(manager.state) # default state

            try:
                manager.setState(manager.State(**state))
            except TypeError:
                logger.log(
                    "core",
                    f"Corrupted state loaded for manager {manager.__class__.__name__}",
                    logger.Level.warning
                )
                continue
            except CarbonError as e:
                logger.log(
                    "core",
                    f"Corrupted state loaded for manager {manager.__class__.__name__}: {e.msg}",
                    logger.Level.warning
                )
                errors += e.msg + "\n"
                continue

            logger.log(
                "core",
                f"Loaded for manager {manager.__class__.__name__}",
                logger.Level.debug
            )

        logger.log("core", "Loaded state.", logger.Level.info)
        
        if errors:
            raise CarbonError(errors.strip())
        
        return "State loaded successfully."


    def saveState(self):
        
        for manager in self.all_managers:
            self.state.update(
                manager.__class__.__name__,
                dataclasses.asdict(manager.getState())
            )

        self.state.save()
        logger.log("core", "Saved state.", logger.Level.info)

        return "State saved."
    
    
    def getDispatchMap(self):

        dispatch_map = {}

        for key, value in self.dispatch_map.items():
            dispatch_map[key] = list(value.keys())

        string = json.dumps(dispatch_map, indent=4)

        return string


    def dispatch(self, id: int, command: CommandRequest):
        
        logger.log("core", f"Received dispatch request from id:{id}.", logger.Level.info)

        try:
            manager_map = self.dispatch_map[command.manager]
        except KeyError:
            logger.log("core", f"Unknown manager requested by client(id:{id}): {command.manager}", logger.Level.warning)
            with self.lock:
                self.server.send(id, CommandOutput(1,f"Unknown manager: {command.manager}"))
                return
            
        try:
            handler = manager_map[command.handler]
        except KeyError:
            logger.log("core", f"Unknown handler for manager '{command.manager}' requested by client(id:{id}): {command.handler}", logger.Level.warning)
            with self.lock:
                self.server.send(id, CommandOutput(1, f"Unknown handler for manager '{command.manager}': {command.handler}"))
                return

        logger.log("core", f"Executing {command.manager}::{command.handler} with arguments: {command.args}", logger.Level.debug)
        self.thread_pool.submit(self.worker, id, handler, command.args)


    def worker(self, id: int, func, args):

        try:
            response = func(**args)
            code = 0
        except CarbonError as e:
            response = e.msg
            code = 1
            logger.log(
                "core", 
                f"Carbon Error while executing {func.__name__} with arguments {args}: {str(e)} ", 
                logger.Level.debug
            )
        except Exception as e:
            response = f"{e.__class__.__name__}: {str(e)}"
            code = 1
            logger.log(
                "core", 
                f"Unexpected Error while executing {func.__name__} with arguments {args}: ({e.__class__.__name__}) {str(e)} ", 
                logger.Level.warning
            )

        output = CommandOutput(code, response)

        with self.lock:
            self.server.send(id, output)
            self.saveState()