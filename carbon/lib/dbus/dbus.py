import asyncio
import threading
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType

from carbon.utils import logger

from .notifications import NotificationServer
from .upower import UPower


class DBus:

	def __init__(self):
		self.notification_server: NotificationServer = NotificationServer()
		self.upower: UPower = UPower()


	def start(self):
		self._daemon_thread = threading.Thread(target=self._start, daemon=True)
		self._daemon_thread.start()


	def _start(self):

		async def _asyncio_start():
			sys_bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
			user_bus = await MessageBus().connect()

			logger.log(
				"dbus",
				"DBus objects are being intialized",
				logger.Level.debug
			)

			self.notification_server = await self.notification_server.init(user_bus)
			self.upower = await self.upower.init(sys_bus)

			logger.log(
				"dbus",
				"DBus objects initialized!",
				logger.Level.info
			)

			await asyncio.gather(
				sys_bus.wait_for_disconnect(),
				user_bus.wait_for_disconnect()
			)
		
		try:
			asyncio.run(_asyncio_start())
		except Exception as e:
			logger.log(
				"dbus",
                f"Dbus failure. {e.__class__.__name__} :: {str(e)}",
                logger.Level.critical
            )