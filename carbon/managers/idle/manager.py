from dataclasses import dataclass, replace

from carbon.managers.base import BaseManager
from carbon.utils import ProcessManager, Notify, logger


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

            if not self.hypridle.poll(0.1):
                self.hypridle.start()
                msg = "Idle manager turned on."
                changed = True
            else:
                msg = "Idle manager already on."
                changed = False

        else:

            if self.hypridle.poll(0.1):
                self.hypridle.kill()
                msg = "Idle manager turned off."
                changed = True
            else:
                msg = "Idle manager already off."
                changed = False

        if changed:
            Notify("Idle toggled", msg)

        logger.log("idle", msg, logger.Level.info if changed else logger.Level.debug)
        return msg