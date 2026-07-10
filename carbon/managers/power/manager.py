from dataclasses import dataclass, replace
from typing import Any, Callable
import time

from carbon.managers.base import BaseManager

from carbon.lib.dbus import UPower, getUpowerClient

from carbon.utils import logger, CarbonError, Notify, shellrun, clamp



class PowerManager(BaseManager):


	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		full_threshold: float
		warning_threshold: float
		critical_threshold: float
		force_hibernate_threshold: float


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], State]):
		super().__init__(internalDispatch, getManagerState)
		self.state: PowerManager.State = self.State(
			full_threshold=95,
			warning_threshold=20,
			critical_threshold=10,
			force_hibernate_threshold=5
		)

		self.previous_info: UPower.Info = UPower.Info(
			True,
			50,
			UPower.Status.unknown
		)

		self.was_full_triggered = False
		self.was_warning_triggered = False
		self.was_critical_triggered = False
		self.was_hibernate_triggered = False

		self.upower_client = getUpowerClient()
		self.upower_client.setCallback(self.UPowerCallback)


	def start(self):
		pass


	def end(self):
		pass


	def name(self):
		return "power"
	

	def handlers(self):
		return {
			"lock": lambda: self.runPowerOption("lock"),
			"shutdown": lambda: self.runPowerOption("shutdown"),
			"reboot": lambda: self.runPowerOption("reboot"),
			"suspend": lambda: self.runPowerOption("suspend"),
			"hibernate": lambda: self.runPowerOption("hibernate"),
			"logout": lambda: self.runPowerOption("logout"),
			"bios": lambda: self.runPowerOption("bios")
		}
	

	def getHelp(self):
		return _help


	def setState(self, state: PowerManager.State):
		self.state.full_threshold = clamp(state.full_threshold, 0, 100)
		self.state.warning_threshold = clamp(state.warning_threshold, 0, 100)
		self.state.critical_threshold = clamp(state.critical_threshold, 0, 100)
		self.state.force_hibernate_threshold = clamp(state.force_hibernate_threshold, 0, 100)


	def getState(self):
		return replace(self.state)
	
	# handler
	def runPowerOption(self, option: str) -> str:

		self.internalDispatch("controller", "close", {})
		self.internalDispatch("daemon", "save-state", {})

		match option:

			case "lock":
				shellrun("pidof hyprlock || hyprlock", wait=False)
				return "Locking your so precious computer."
			
			case "shutdown":
				shellrun("systemctl poweroff", wait=False)
				return "Bye Bye!"

			case "reboot":
				shellrun("systemctl reboot", wait=False)
				return "Be right back."

			case "suspend":
				shellrun("pidof hyprlock || hyprlock", wait=False)
				time.sleep(1)
				shellrun("systemctl suspend", wait=False)
				return "Good dreams..."

			case "hibernate":
				shellrun("pidof hyprlock || hyprlock", wait=False)
				time.sleep(1)
				shellrun("systemctl hibernate", wait=False)
				return "Winter here already?"

			case "logout":
				shellrun("rm /tmp/carbon.portal; hyprctl dispatch exit", wait=False)
				return "Logging out. Over."

			case "bios":
				shellrun("systemctl reboot --firmware-setup", wait=False)
				return "Damn, be careful vro."

			case _:
				logger.warn("power", f"Unknown power option: {option}")
				return "If you somehow see this message, something wrong."


	def UPowerCallback(self, info: UPower.Info | None):

		if info is None: return
		
		if not info.on_ac_only:
			self.notifyCharging(info)
			self.notifyPercentage(info)
		
		self.previous_info = info


	def notifyCharging(self, info: UPower.Info):
		if info.status == UPower.Status.charging and self.previous_info.status != UPower.Status.charging:
			Notify("Charger Connected", f"Device now charging ({int(info.percentage)}%)")
			self.was_hibernate_triggered = False
			self.was_critical_triggered = False
			self.was_warning_triggered = False
			self.was_full_triggered = False 


	def notifyPercentage(self, info: UPower.Info):
		perc = info.percentage
		if info.status != UPower.Status.charging:
			self.was_full_triggered = False
			if perc <= self.state.force_hibernate_threshold and not self.was_hibernate_triggered:
				self.triggerForceHibernate()
			elif perc <= self.state.critical_threshold and not self.was_critical_triggered:
				self.triggerCritical(info)
			elif perc <= self.state.warning_threshold and not self.was_warning_triggered:
				self.triggerWarning(info)
		else:
			if perc >= self.state.full_threshold and not self.was_full_triggered:
				self.triggerFull()


	def triggerCharging(self, info: UPower.Info):
		Notify("Charger Connected", f"Charging at {int(info.percentage)}%")


	def triggerFull(self):
		Notify("Battery Full", "Unplug charger to preserve battery health")
		self.was_full_triggered = True


	def triggerWarning(self, info: UPower.Info):
		perc = int(info.percentage)
		Notify("Low Battery", f"{perc}% remaining — plug in soon")
		self.was_warning_triggered = True


	def triggerCritical(self, info: UPower.Info):
		perc = int(info.percentage)
		Notify("Critical Battery", f"Plug in immediately! Only {perc}% remaining!", urgency="critical")
		self.was_warning_triggered = True
		self.was_critical_triggered = True

	def triggerForceHibernate(self):
		Notify("Extreme Battery", "Hibernating in 5 seconds to prevent data loss!", timeout=-1, urgency="critical")
		time.sleep(5)
		self.runPowerOption("hibernate")
		self.was_warning_triggered = True
		self.was_critical_triggered = True 
		self.was_hibernate_triggered = True


_help = """
==> power
Power manager, informs about battery updates.

handlers:

	> lock
		Lock session.
	
	> shutdown
		Poweroff the computer.

	> reboot
		Restart the system.

	> suspend
		Causes the system to sleep/suspend.

	> hibernate
		Causes the system to hibernate.

	> logout
		Logout user.

	> bios
		Restart and enter bios.
"""
