import asyncio
import threading
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType

from carbon.utils import logger, CarbonError

from .notifications import NotificationServer
from .upower import UPower

_notification_server: NotificationServer = NotificationServer()
_upower: UPower = UPower()


def _start():

	async def _asyncio_start():
		sys_bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
		user_bus = await MessageBus().connect()

		logger.log(
			"dbus",
			"DBus objects are being intialized",
			logger.Level.debug
		)

		global _notification_server, _upower

		_notification_server = await _notification_server.init(user_bus)
		_upower = await _upower.init(sys_bus)

		logger.log(
			"dbus",
			"DBus objects initialized!",
			logger.Level.info
		)

		await asyncio.gather(
			sys_bus.wait_for_disconnect(),
			user_bus.wait_for_disconnect()
		)

		_dbus_started = True
	
	try:
		asyncio.run(_asyncio_start())
	except Exception as e:
		logger.log(
			"dbus",
			f"Dbus failure. {e.__class__.__name__} :: {str(e)}",
			logger.Level.critical
		)
		

_daemon_thread = threading.Thread(target=_start, daemon=True)



def startDbusClient():
	_daemon_thread.start()

def getNotificationServer() -> NotificationServer:
	return _notification_server

def getUpowerClient():
	return _upower

