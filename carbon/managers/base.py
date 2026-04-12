from typing import Dict, Callable, Any
from dataclasses import dataclass

class BaseManager:

    class State:
        pass

    def __init__(self):
        pass
    
    def handlers(self) -> Dict[str, Callable]:
        raise NotImplementedError()
    
    def getState(self) -> State:
        raise NotImplementedError()
    
    def setState(self, state: State):
        raise NotImplementedError()
