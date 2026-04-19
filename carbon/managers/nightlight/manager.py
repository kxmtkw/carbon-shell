
from dataclasses import dataclass, replace
from typing import Any
import time

from carbon.managers.base import BaseManager
from carbon.utils import shellrun, logger, CarbonError, ProcessManager



class NightLightManager(BaseManager):

    @dataclass(init=True, kw_only=True)
    class State(BaseManager.State):
        toggled: bool
        temperature: int
        gamma: int


    def __init__(self):
        super().__init__()
        self.default_temperature = 6000
        self.default_gamma = 100

        self.state = NightLightManager.State(
            temperature=self.default_temperature,
            gamma=self.default_gamma,
            toggled=True
        )

        self.hyprsunset = ProcessManager("hyprsunset", only_one=True)
        self.hyprsunset.start("-g", self.state.gamma, "-t", self.state.temperature)


    def handlers(self):
        return {
            "on": lambda: self.toggleNightlight(True),
            "off": lambda: self.toggleNightlight(False),
            "toggle": lambda: self.toggleNightlight(not self.state.toggled),
            "set-temperature": self.setTemperature,
            "set-gamma": self.setGamma
        }
    

    def getState(self) -> State:
        return replace(self.state)
    

    def setState(self, state: State):
        self.toggleNightlight(state.toggled)
        self.setTemperature(state.temperature)
        self.setGamma(state.gamma)


    def toggleNightlight(self, on: bool):

        self.state.toggled = on
            
        if self.state.toggled:
            if not self.hyprsunset.poll(0.1):
                self.hyprsunset.start("-g", self.state.gamma, "-t", self.state.temperature)
            return "Nightlight turned on"
        else:
            self.hyprsunset.kill()
            return "Nightlight turned off"


    def setTemperature(self, value: int) -> str:

        if value < 1000 or value > 20000:
            raise CarbonError("Invalid temperature value. Valid range: 1000-20000.")
        
        if not self.state.toggled:
            return "Updated, but nightlight is off."
        
        success, output = shellrun(f"hyprctl hyprsunset temperature {value}")

        if not success:
            raise CarbonError(f"Failed. Reason: {output}")
        
        logger.log(
            "nightlight",
            f"Updated temperature to {value}",
            logger.Level.info
        )
        self.state.temperature = value
        return "Updated temperature."


    def setGamma(self, value: int) -> str:

        if value < 10 or value > 200:
            raise CarbonError("Invalid gamma value. Valid range: 10-200.")
        
        if not self.state.toggled:
            return "Updated, but nightlight is off."
        
        success, output = shellrun(f"hyprctl hyprsunset gamma {value}")

        if not success:
            raise CarbonError(f"Failed in setGamma. Reason: {output}")
        
        logger.log(
            "nightlight",
            f"Updated gamma to {value}",
            logger.Level.info
        )
        self.state.gamma = value
        return "Updated gamma."

