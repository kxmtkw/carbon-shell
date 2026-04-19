from typing import Callable, Literal

from carbon.utils import logger

class _Notify():
    "eafew"
    def __init__(self):
        self._function = None

    def setNotificationFunction(self, func: Callable):
        if self._function is not None:
            logger.log(
                "utils",
                f"Notify()'s function was set again by someone! Ignored.",
                logger.Level.warning
            )
            return
        self._function = func


    def __call__(
		self,
		summary: str, 
		body: str, 
		*,
		timeout: int = 5000,
		urgency: Literal["low", "normal", "critical"] = "normal"
		) -> int:
        if self._function is None:
            logger.log(
                "utils",
                f"Notify()'s function isn't set!",
                logger.Level.warning
            )
            return
        
        self._function(summary, body, timeout=timeout, urgency=urgency)


Notify = _Notify()