from dataclasses import dataclass
from typing import Any, Callable, Literal
import queue

from dbus_next.service import ServiceInterface, method, signal
from dbus_next.aio import MessageBus
from dbus_next import Variant


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


class NotificationServer(ServiceInterface):


    def __init__(self, callback: Callable[[Notification],None]):
        super().__init__('org.freedesktop.Notifications')
        self.queue = queue.Queue()
        self.current_id = 1
        self.callback = callback


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
            notif_id = self.current_id
            self.current_id += 1
        else:
            notif_id = replaces_id

        notification = Notification(
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
        
        self.callback(notification)
        
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
