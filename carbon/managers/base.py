from typing import Dict, Callable, Any

class BaseManager:

    def __init__(self):
        pass

    def handlers(self) -> Dict[str, Callable]:
        raise NotImplementedError()
    
    def saveState(self) -> dict[str, Any]:
        raise NotImplementedError()
    
    def loadState(self, state: dict[str, Any]):
        raise NotImplementedError()
