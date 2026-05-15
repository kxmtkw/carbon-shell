from dataclasses import dataclass, replace

from carbon.managers.base import BaseManager

from carbon.lib.dbus import UPower

from carbon.utils import logger, CarbonError, Notify, shellrun, clamp


class PowerManager(BaseManager):


	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		full_threshold: float
		warning_threshold: float
		critical_threshold: float
		force_hibernate_threshold: float


	def __init__(self):
		super().__init__()
		self.state = self.State(
			full_threshold=95,
			warning_threshold=15,
			critical_threshold=5,
			force_hibernate_threshold=2
		)

		self.previous_info: UPower.Info = UPower.Info(
			True,
			50,
			UPower.Status.unknown
		)

		self.was_full_triggered = False
		self.was_warning_triggered = False
		self.was_critical_triggered = False



	def setState(self, state: PowerManager.State):
		self.state.full_threshold = clamp(state.full_threshold, 0, 100)
		self.state.warning_threshold = clamp(state.warning_threshold, 0, 100)
		self.state.critical_threshold = clamp(state.critical_threshold, 0, 100)
		self.state.force_hibernate_threshold = clamp(state.force_hibernate_threshold, 0, 100)


	def getState(self):
		return replace(self.state)
	

	def end(self):
		pass


	def UPowerCallback(self, info: UPower.Info | None):

		if info is None: return
		
		if not info.on_ac_only:
			self.notifyCharging(info)
			self.notifyPercentage(info)
		
		self.previous_info = info


	def notifyCharging(self, info: UPower.Info):

		if info.status == UPower.Status.charging and self.previous_info.status != UPower.Status.charging:
			Notify("Charger Connected", f"Device now charging ({int(info.percentage)}%)")
			self.was_critical_triggered = False
			self.was_warning_triggered = False


	def notifyPercentage(self, info: UPower.Info):

		perc = info.percentage
		if not info.status == UPower.Status.charging:
			if perc <= self.state.force_hibernate_threshold and not self.was_critical_triggered:
				self.triggerForceHibernate()
			elif perc <= self.state.critical_threshold and not self.was_critical_triggered:
				self.triggerCritical(info)
			elif perc <= self.state.warning_threshold and not self.was_warning_triggered:
				self.triggerWarning(info)
		else:
			if perc >= self.state.full_threshold and not self.was_full_triggered:
				self.triggerFull()
			else:
				self.was_full_triggered = False


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
		Notify("Critical Battery", f"Plug in immediately! Only {perc}% remaining!")
		self.was_critical_triggered = True

	def triggerForceHibernate(self):
		Notify("Extreme Battery", "Hibernating in 30 seconds to prevent data loss!")
		shellrun("sleep 30 && carbon.power hibernate")