from carbon.managers.base import BaseManager

from carbon.managers.autostart import AutostartManager
from carbon.managers.theme import ThemeManager
from carbon.managers.controller import ControllerManager
from carbon.managers.notifications import NotificationManager
from carbon.managers.nightlight import NightLightManager
from carbon.managers.idle import IdleManager
from carbon.managers.power import PowerManager
from carbon.managers.panel import PanelManager
from carbon.managers.lock import LockScreenManager
from carbon.managers.backlight import BacklightManager


MANAGERS: list[type[BaseManager]] = [
	AutostartManager,
	ThemeManager,
	ControllerManager,
	NotificationManager,
	NightLightManager,
	IdleManager,
	PowerManager,
	PanelManager,
	LockScreenManager,
	BacklightManager
]