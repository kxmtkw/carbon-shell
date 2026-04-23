from dataclasses import dataclass
from enum import Enum
from typing import Callable
from dbus_next.aio import MessageBus
from dbus_next.errors import DBusError

from carbon.utils import logger

class UPower:


	class Status(Enum):
		unknown = 0
		empty = 1
		discharging = 2
		charging = 3
		full = 4
		

	@dataclass(init=True, frozen=True)
	class Info:
		percentage: float
		status: UPower.Status


	def __init__(self):
		self._callback: Callable[[UPower.Info], None] | None = None

		self._state_map = {
			0: UPower.Status.unknown,
			1: UPower.Status.charging,
			2: UPower.Status.discharging,
			3: UPower.Status.empty,
			4: UPower.Status.full,
			5: UPower.Status.charging,
			6: UPower.Status.discharging,
		}
		
		self._initialized = False


	async def init(self, bus: MessageBus):

		if self._initialized: return

		intro = await bus.introspect("org.freedesktop.UPower", "/org/freedesktop/UPower")
		obj = bus.get_proxy_object("org.freedesktop.UPower", "/org/freedesktop/UPower", intro)
		iface = obj.get_interface("org.freedesktop.UPower")

		display_path = await iface.call_get_display_device()
		
		self._intro = await bus.introspect("org.freedesktop.UPower", display_path)
		self._obj = bus.get_proxy_object("org.freedesktop.UPower", display_path, self._intro)
		self._props = self._obj.get_interface("org.freedesktop.DBus.Properties")
		self._props.on_properties_changed(self._wrapper)
		
		is_present = await self._props.call_get("org.freedesktop.UPower.Device", "IsPresent")

		if not is_present.value:
			self._ac_system_detected = True
			if self._callback:
				self._callback(None)
			return self
		else:
			self._ac_system_detected = False
			logger.log(
				"dbus-upower",
				"System with batteries detected!",
				logger.Level.info
			)

		pct = await self._props.call_get("org.freedesktop.UPower.Device", "Percentage")
		state = await self._props.call_get("org.freedesktop.UPower.Device", "State")
		self.info = UPower.Info(
			percentage=pct.value,
			status=self._state_map.get(state.value, UPower.Status.unknown)
		)
		if self._callback:
			self._callback(self.info)

		self._initialized = False

		return self


	def _wrapper(self, iface, changed, invalidated):

		pct = changed["Percentage"].value if "Percentage" in changed else self.info.percentage
		state = changed["State"].value if "State" in changed else None
		status = self._state_map.get(state, self.info.status) if state is not None else self.info.status

		self.info = UPower.Info(percentage=pct, status=status)

		if self._callback:
			self._callback(self.info)


	def setCallback(self, func: Callable[[UPower.Info | None], None]):
		if self._callback is not None: return

		logger.log(
			"dbus",
			f"UPower callback has been set. Is {func}",
			logger.Level.debug
		)
		self._callback = func