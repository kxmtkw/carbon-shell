import asyncio
from dataclasses import dataclass, replace
from threading import Lock, Thread
from typing import Any, Callable, Dict, Literal
from dbus_next.service import ServiceInterface, method, signal
from dbus_next.aio import MessageBus
from dbus_next import Variant

from carbon.managers.base import BaseManager
from carbon.utils import locked, logger, CarbonError

from carbon.lib.quickshell import Quickshell

from .server import NotificationServer, Notification




notificationLock = Lock()

class NotificationManager(BaseManager):
    

    @dataclass(init=True, kw_only=True)
    class State(BaseManager.State):
        do_not_disturb: bool


    def __init__(self):
        super().__init__()
        self.server: NotificationServer
        self.notifications: list[Notification] = []

        self.daemon_thread = Thread(target=self.startServer, daemon=True)
        self.daemon_thread.start()

        self.quickshell = Quickshell()

        self.state = NotificationManager.State(
            do_not_disturb=False
        )
        

    def handlers(self) -> Dict[str, Callable]:
        return {
            "dnd": self.setDND
        }
    

    def getState(self) -> dict[str, Any]:
        return replace(self.state)
    

    def setState(self, state: State):
        self.setDND(state.do_not_disturb)
    

    def startServer(self):

        # so sorry lol, could'nt find any dbus lib that didnt involve GObject.
        # just a hack, probably won't fix it.
        async def _server():

            bus = await MessageBus().connect()

            self.server = NotificationServer(self.newNotification)

            bus.export('/org/freedesktop/Notifications', self.server)
        
            await bus.request_name('org.freedesktop.Notifications')
        
            logger.log(
                "notification",
                "DBUS notification server is now active.",
                logger.Level.info
            )

            await bus.wait_for_disconnect()
        
        asyncio.run(_server())


    @locked(notificationLock)
    def newNotification(self, notif: Notification):
        
        self.notifications.append(notif)

        logger.log(
            "notifications",
            f"Received notification #{notif.id} from {notif.app_name}",
            logger.Level.info
        )

        logger.log(
            "notifications",
            f"Notification info for #{notif.id}: ({notif.app_name}) ({notif.app_icon}) ({notif.summary}) ({notif.body if len(notif.body) > 20 else f'{notif.body[:17]}...'}) ({notif.image}) ({notif.urgency})",
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
        

    @locked(notificationLock)
    def setDND(self, *, state: Literal["on", "off", "toggled"]):

        if state == "on":
            self.state.do_not_disturb = True
        elif state == "off":
            self.state.do_not_disturb = False
        elif state == "toggle":
            self.state.do_not_disturb = not self.state.do_not_disturb
        else:
            raise CarbonError(f"Invalid state: {state}. Valid values are: on, off, toggle.")
        
        if self.state.do_not_disturb:
            msg = "DND now on. Notifications will be hidden until it is turned on."
        else:
            msg = "DND now off. Queued Notifications will now be shown."

        logger.log(
            "notifications",
            msg,
            logger.Level.info
        )

        return msg
