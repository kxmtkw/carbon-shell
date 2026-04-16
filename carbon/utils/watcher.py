from typing import Callable

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from pathlib import Path

from .logs import logger

class FileWatcher:

    def __init__(self, file: str, callback: Callable[[],]):
        self._path = Path(file).expanduser()
        self._callback = callback
        self._observer = Observer()

        path = Path(self._path)
        if not path.expanduser().exists():
            path.parent.mkdir(511, True, True)
            path.touch()
        
        self._thread = threading.Thread(target=self._start, daemon=True)
        self._thread.start()
            
    def _start(self):
        
        handler = _Handler(self._callback)
        self._observer.schedule(handler, self._path, recursive=True)
        self._observer.start()

        logger.log(
            "filewatcher",
            f"Watching over file: {self._path}",
            logger.Level.debug
        )


class _Handler(FileSystemEventHandler):

    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        logger.log(
            "filewatcher",
            f"Calling callback: {self.callback}",
            logger.Level.debug
        )
        self.callback()