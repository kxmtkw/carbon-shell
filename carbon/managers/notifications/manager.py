import asyncio
from threading import Lock, Thread
from typing import Any, Callable, Dict
from dbus_next.service import ServiceInterface, method, signal
from dbus_next.aio import MessageBus
from dbus_next import Variant

from carbon.managers.base import BaseManager
from carbon.utils import locked, logger

from carbon.lib.quickshell import Quickshell

from .server import NotificationServer, Notification

notificationLock = Lock()

class NotificationManager(BaseManager):
    

    def __init__(self):
        super().__init__()
        self.server: NotificationServer
        self.daemon_thread = Thread(target=self.startServer, daemon=True)
        self.daemon_thread.start()
        self.quickshell = Quickshell()
        

    def handlers(self) -> Dict[str, Callable]:
        return {}
    

    def saveState(self) -> dict[str, Any]:
        return
    

    def loadState(self, state: dict[str, Any]):
        return
    

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
        
        self.quickshell.sendNotification(
            notif.id,
            notif.replaces_id,
            notif.app_name,
            notif.app_icon,
            notif.summary,
            notif.body,
            notif.urgency,
            notif.image,
            notif.expire_timeout
        )

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
