from dataclasses import dataclass
from typing import Any, Callable, Literal
import queue

from dbus_next.service import ServiceInterface, method, signal
from dbus_next.aio import MessageBus
from dbus_next import Variant

from carbon.utils import logger

class NotificationServer(ServiceInterface):

	@dataclass(init=True)
	class Notification:
		id: int
		replaces_id: int
		app_name: str
		app_icon: str
		summary: str
		body: str
		actions: list[str]
		urgency: Literal[0, 1, 2]
		image: str
		expire_timeout: int


	def __init__(self):
		super().__init__('org.freedesktop.Notifications')
		self._queue = queue.Queue()
		self._current_id = 1
		self._callback: Callable[[NotificationServer.Notification],None] | None = None


	async def init(self, bus: MessageBus):
		bus.export('/org/freedesktop/Notifications', self)
		await bus.request_name('org.freedesktop.Notifications')
		return self


	def setCallback(self, func: Callable[[Notification],None]):

		if self._callback is not None: return

		logger.log(
			"dbus",
			f"Notification server callback has been set. Is {func}",
			logger.Level.debug
		)
		self._callback = func
		

	@method()
	def GetCapabilities(self) -> 'as':
		return ['body', 'actions', 'persistence', 'icon-static']


	@method()
	def GetServerInformation(self) -> 'ssss':
		return ["CarbonShell", "Haseeb", "1.0", "1.2"]


	@method()
	def Notify(
		self, 
		app_name: 's', 
		replaces_id: 'u', 
		app_icon: 's', 
		summary: 's', 
		body: 's', 
		actions: 'as', 
		hints: 'a{sv}', 
		expire_timeout: 'i'
		) -> 'u':
		
		if replaces_id == 0:
			notif_id = self._current_id
			self._current_id += 1
		else:
			notif_id = replaces_id

		notification = NotificationServer.Notification(
			notif_id,
			replaces_id,
			app_name,
			app_icon,
			summary,
			body,
			actions,
			hints.get("urgency").value if hints.get("urgency") is not None else 0,
			hints.get("image-path").value if hints.get("image-path") is not None else "",
			expire_timeout
		)
		
		if self._callback:
			self._callback(notification)
		
		return notification.id


	@method()
	def CloseNotification(self, id: 'u'):
		print(f"Closing notification {id}")
		self.NotificationClosed(id, 2) # 2 = dismissed by server


	@signal()
	def NotificationClosed(self, id: 'u', reason: 'u') -> 'uu':
		return [id, reason]


	@signal()
	def ActionInvoked(self, id: 'u', action_key: 's') -> 'us':
		return [id, action_key]
	

	def sendNotification(
		self,
		summary: str, 
		body: str, 
		*,
		timeout: int = 5000,
		urgency: Literal["low", "normal", "critical"] = "normal"
		) -> int:
		"To send notifications to the server from inside the daemon. This will be wired to carbon.utils.notification's Notify later."

		match urgency:
			case "low": urgency = 0
			case "normal": urgency = 1
			case "critical": urgency = 2
			case _: urgency = 1
			
		self.Notify(
			"CarbonShell",
			0,
			"",
			summary,
			body,
			[],
			{"urgency": Variant("y", urgency)},
			timeout
		)
