
from dataclasses import dataclass, replace
from typing import Any

from carbon.managers.base import BaseManager
from carbon.utils import shellrun, logger

from carbon.state.defaults import Defaults


class NightLightManager(BaseManager):

    @dataclass(init=True, kw_only=True)
    class State(BaseManager.State):
        temperature: int
        gamma: int


    def __init__(self):
        super().__init__()
        self.state = NightLightManager.State(
            temperature= Defaults.nightlight_temperature,
            gamma= Defaults.nightlight_gamma
        )

    
    def handlers(self):
        return {
            "set-temperature": self.setTemperature,
            "set-gamma": self.setGamma
        }
    

    def getState(self) -> State:
        return replace(self.state)
    

    def setState(self, state: State):
        self.setTemperature(state.temperature)
        self.setGamma(state.gamma)


    def setTemperature(self, value: int) -> str:

        if value < 1000 or value > 20000:
            return "Invalid temperature value. Valid range: 1000-20000."
        
        success, output = shellrun(f"hyprctl hyprsunset temperature {value}")

        if not success:
            return f"Failed. Reason: {output}"
        
        logger.log(
            "nightlight",
            f"Updated temperature to {value}",
            logger.Level.info
        )
        self.state.temperature = value
        return "Updated."


    def setGamma(self, value: int) -> str:

        if value < 10 or value > 200:
            return "Invalid gamma value. Valid range: 10-200."
        
        success, output = shellrun(f"hyprctl hyprsunset gamma {value}")

        if not success:
            return f"Failed. Reason: {output}"
        
        logger.log(
            "nightlight",
            f"Updated gamma to {value}",
            logger.Level.info
        )
        self.state.gamma = value
        return "Updated."
    

