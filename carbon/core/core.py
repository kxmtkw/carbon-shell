import threading
from concurrent.futures import ThreadPoolExecutor

from carbon.ipc.server import Server
from carbon.ipc.payloads import CommandRequest, CommandOutput

from carbon.utils import CarbonError

from carbon.managers.theme import ThemeManager
from carbon.managers.controller import ControllerManager

from carbon.state import StateManager

from carbon.lib.quickshell import Quickshell

class CarbonCore:


    def __init__(self):
        self.server = Server(1)
        self.lock = threading.Lock()
        self.thread_pool = ThreadPoolExecutor(5)
        self.is_running = True

        self.state = StateManager()

        self.theme_manager = ThemeManager()
        self.controller_manager = ControllerManager(self.theme_manager)


        self.quickshell = Quickshell()

        try:
            self.quickshell.start()
        except Quickshell.Error as e:
            CarbonError(f"Quickshell could not be started. Reason: {e.msg}").print()


        self.dispatch_map = {
            "daemon": {
                "shutdown": self.shutdown
            },
            "theme": self.theme_manager.handlers(),
            "controller": self.controller_manager.handlers()
        }

        self.loadState()


    def run(self):

        while self.is_running:
            id, command = self.server.listen()
            if id is None: continue
            self.dispatch(id, command)

    
    def shutdown(self) -> str:
        if not self.is_running: 
            return "This call shouldn't have been possible."
        
        self.saveState()
        self.server.close()
        self.is_running = False
        self.thread_pool.shutdown(False, cancel_futures=True)
        return "Shutting down."
    

    def loadState(self):
        self.state.load()
        self.theme_manager.loadState(self.state.get("theme"))


    def saveState(self):
        self.state.update("theme", self.theme_manager.saveState())
        self.state.save()


    def dispatch(self, id: int, command: CommandRequest):

        try:
            manager_map = self.dispatch_map[command.manager]
        except KeyError:
            with self.lock:
                self.server.send(id, CommandOutput(1,f"Unknown manager: {command.manager}"))
                return
            
        try:
            handler = manager_map[command.handler]
        except KeyError:
            with self.lock:
                self.server.send(id, CommandOutput(1, f"Unknown handler for manager '{command.manager}': {command.handler}"))
                return

        self.thread_pool.submit(self.worker, id, handler, command.args)


    def worker(self, id: int, func, args):

        try:
            response = func(**args)
            code = 0
        except CarbonError as e:
            response = e.msg
            code = 1
        except Exception as e:
            response = f"{e.__class__.__name__}: {str(e)}"
            code = 1

        output = CommandOutput(code, response)

        with self.lock:
            self.server.send(id, output)
