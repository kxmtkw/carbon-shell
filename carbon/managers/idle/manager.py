from dataclasses import dataclass, replace

from carbon.managers.base import BaseManager
from carbon.utils import ProcessManager


class IdleManager(BaseManager):

    @dataclass(init=True, kw_only=True)
    class State(BaseManager.State):
        toggled: bool


    def __init__(self):
        super().__init__()

        self.state = IdleManager.State(
            toggled=True
        )

        self.hypridle = ProcessManager("hypridle", only_one=True)
        self.hypridle.start()


    def handlers(self):
        return {
            "on": lambda: self.toggleIdle(True),
            "off": lambda: self.toggleIdle(False),
            "toggle": lambda: self.toggleIdle(not self.state.toggled),
        }


    def getState(self) -> State:
        return replace(self.state)


    def setState(self, state: State):
        self.toggleIdle(state.toggled)


    def toggleIdle(self, on: bool):

        self.state.toggled = on

        if self.state.toggled:
            if self.hypridle.poll(0.1):
                self.hypridle.start()
            return "Idle manager turned on"
        else:
            self.hypridle.kill()
            return "Idle manager turned off"
