
from typing import Any

from carbon.managers.base import BaseManager
from carbon.utils import shellrun, logger

from carbon.state.defaults import Defaults


class NightLightManager(BaseManager):


    def __init__(self):
        super().__init__()
        self.current_temperature = Defaults.nightlight_temperature
        self.current_gamma = Defaults.nightlight_gamma
    

    def handlers(self):
        return {
            "set-temperature": self.setTemperature,
            "set-gamma": self.setGamma
        }
    

    def saveState(self) -> dict[str, Any]:
        return {
            "temperature": self.current_temperature,
            "gamma": self.current_gamma,
        }
    

    def loadState(self, state):
        self.current_temperature = state.get("temperature", Defaults.nightlight_temperature)
        self.current_gamma = state.get("gamma", Defaults.nightlight_gamma)

        try:
            self.setTemperature(int(self.current_temperature))
            self.setGamma(int(self.current_gamma))
        except TypeError:
            logger.log(
                "nightlight", 
                "Invalid non-int values passed. Resorting to defaults.",
                logger.Level.warning
            )
            self.setTemperature(Defaults.nightlight_temperature)
            self.setGamma(Defaults.nightlight_gamma)


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
        self.current_temperature = value
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
        self.current_gamma = value
        return "Updated."
    

