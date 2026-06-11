import time
from typing import Dict, Callable, Any
from dataclasses import dataclass, replace
from threading import Lock

from carbon.managers.base import BaseManager
from carbon.utils import CarbonError, shellrun, clamp, procrun, logger, locked


class BacklightManager(BaseManager):

	backlightLock = Lock()

	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		value: float
		update_delay: float
		minimum: float
		maximum: float


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], State]):
		super().__init__(internalDispatch, getManagerState)

		self.state = self.State(
			value=100,
			update_delay=0.05,
			minimum=10,
			maximum=100
		)

		self.max_brightness: int = 0

		self.max_steps = 60
		self.min_steps = 10

		self.saved_brightness = 100

		self.is_busy = False

	
	def start(self):
		success, out = procrun(["brightnessctl", "m"])
		if not success:
			raise CarbonError(f"brightnessctl failure: {out}")
		self.max_brightness = int(out) 


	def end(self):
		pass
	

	def name(self) -> str:
		return "backlight"
	

	def handlers(self) -> Dict[str, Callable]:
		return {
			"get": self.getBrightness,
			"set": self.setBrightness,
			"increase": self.increaseBrightness,
			"decrease": self.decreaseBrightness,
			"save": self.saveBrightness,
			"restore": self.restoreBrightness
		}
	

	def getState(self) -> State:
		return replace(self.state)
	

	def setState(self, state: State):
		self.setBrightness(value=state.value)

		try:
			self.state.update_delay = float(state.update_delay)
			self.state.minimum = float(state.minimum)
			self.state.maximum = float(state.maximum)
		except ValueError:
			raise CarbonError("Non-number types used in numeral values of backlight manager.")


	def getHelp(self) -> str:
		return _help
	

	def updateCurrentBrightness(self):
		success, out = procrun(["brightnessctl", "g"])
		if not success:
			raise CarbonError(f"brightnessctl failure: {out}")
	
		current_brightness = int(out)

		self.state.value = (current_brightness / self.max_brightness) * 100

		logger.debug("backlight", "Brightness updated.")
	 
	
	@locked(backlightLock)
	def transitionBrightness(self, target: float):

		current = self.state.value
		target = clamp(target, self.state.minimum, self.state.maximum)

		if current == target:
			logger.debug("backlight", "Target was equal to current so no need to perform transition.")
			return

		diff = target - current

		step_count = int(clamp(abs(diff), self.min_steps, self.max_steps))
		step_size = diff / step_count
				
		for i in range(step_count):
			current = current + step_size
			procrun(["brightnessctl", "--device", "*backlight*", "set", f"{current}%"])
			time.sleep(self.state.update_delay)

		procrun(["brightnessctl", "--device", "*backlight*", "set", f"{target}%"])
		self.state.value = target
				

	def getBrightness(self):
		self.updateCurrentBrightness()
		return self.state.value


	def setBrightness(self, *, value: float):

		self.updateCurrentBrightness()

		try:
			value = float(value)
		except ValueError:
			raise CarbonError(f"Value must be an integar.")
		
		if value < 0 or value > 100:
			raise CarbonError("Value must be within 0-100.")
		
		self.transitionBrightness(value)
		
		msg = f"Brightness set to {self.state.value}%."

		logger.info("backlight", msg)
		return msg

	
	def increaseBrightness(self, *, value: float):
		
		self.updateCurrentBrightness()

		try:
			value = float(value)
		except ValueError:
			raise CarbonError(f"Value must be an number.")
		
		if value < 0 or value > 100:
			raise CarbonError("Value must be within 0-100.")

		self.transitionBrightness(self.state.value + value)
		
		msg = f"Brightness increased by {value}%. Is now {self.state.value}%."

		logger.info("backlight", msg)
		return msg


	def decreaseBrightness(self, *, value: float):
		
		self.updateCurrentBrightness()

		try:
			value = float(value)
		except ValueError:
			raise CarbonError(f"Value must be an number.")
		
		if value < 0 or value > 100:
			raise CarbonError("Value must be within 0-100.")

		self.transitionBrightness(self.state.value - value)

		msg = f"Brightness decreased by {value}%. Is now {self.state.value}%."

		logger.info("backlight", msg)
		return msg


	def saveBrightness(self):
		self.saved_brightness = self.state.value
		msg = f"Brightness saved with value {self.saved_brightness}%."
		logger.info("backlight", msg)
		return msg


	def restoreBrightness(self):
		self.setBrightness(value=self.saved_brightness)
		msg = f"Brightness restored to {self.saved_brightness}%."
		logger.info("backlight", msg)
		return msg
	

	
_help = """
==> backlight
Control and set the screen brightness.

handlers:

	> get
		Get the current brightness value.

	> set --value [number]
		Set the current value to this percentage.
		Note that number is clamped between the min and max values.

	> increase --value [number]
		Increase the brightness by some percentage.

	> decrease --value [number]
		Decrease the brightness by some percentage.

	> save
		Save the current brightness.

	> restore
		Restore the last saved brightness level.
"""