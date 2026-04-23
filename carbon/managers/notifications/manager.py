import asyncio
from dataclasses import dataclass, replace
from threading import Lock, Thread
from typing import Any, Callable, Dict, Literal

from carbon.lib.dbus import NotificationServer

from carbon.lib.quickshell import Quickshell
from carbon.managers.base import BaseManager

from carbon.utils import locked, logger, CarbonError, Notify


notificationLock = Lock()

class NotificationManager(BaseManager):
	

	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		do_not_disturb: bool


	def __init__(self):
		super().__init__()
		self.notifications: list[NotificationServer.Notification] = []

		self.quickshell = Quickshell()

		self.state = NotificationManager.State(
			do_not_disturb=False
		)		


	def handlers(self) -> Dict[str, Callable]:
		return {
			"dnd": self.setDND
		}


	def end(self):
		pass
	

	def getState(self) -> dict[str, Any]:
		return replace(self.state)
	

	def setState(self, state: State):
		self.setDND(state= "on" if state.do_not_disturb else "off")
	

	@locked(notificationLock)
	def newNotification(self, notif: NotificationServer.Notification):
		"Set as callback to carbon.lib.dbus.notification's Notification Server"
		
		self.notifications.append(notif)

		logger.log(
			"notifications",
			f"Received notification #{notif.id} from {notif.app_name}",
			logger.Level.info
		)

		logger.log(
			"notifications",
			f"Notification info for #{notif.id}: ({notif.app_name}) ({notif.app_icon}) ({notif.summary}) ({notif.body if len(notif.body) < 20 else f'{notif.body[:17]}...'}) ({notif.image}) ({notif.urgency})",
			logger.Level.debug
		)

		if self.state.do_not_disturb:
			logger.log(
				"notifications",
				f"Not dispatching notification #{notif.id} due to DND",
				logger.Level.debug
			)
			return
		

		while len(self.notifications) > 0:
			n = self.notifications.pop()
			self.quickshell.sendNotification(
				n.id,
				n.replaces_id,
				n.app_name,
				n.app_icon,
				n.summary,
				n.body,
				n.urgency,
				n.image,
				n.expire_timeout
			)

			logger.log(
				"notifications",
				f"Dispatching notification #{n.id}.",
				logger.Level.debug
			)
		

	def setDND(self, *, state: Literal["on", "off", "toggle"]):

		match state:
			case "on":     dnd = True
			case "off":    dnd = False
			case "toggle": dnd = not self.state.do_not_disturb
			case _:        raise CarbonError(f"Invalid state: {state}. Valid: on, off, toggle.")

		if dnd == self.state.do_not_disturb:
			return

		msg     = "DND on. Notifications will now be hidden." if dnd else "DND off. Queued notifications will now be shown."
		summary = "DND on" if dnd else "DND off"

		logger.log("notifications", msg, logger.Level.info)

		if self.state.do_not_disturb:
			self.state.do_not_disturb = dnd
			self.sendNotification(summary, msg)
		else:
			self.sendNotification(summary, msg)
			self.state.do_not_disturb = dnd

		return msg
	
