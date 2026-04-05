import json
from typing import Any

from carbon.utils import CarbonError



class CommandRequest:


    def __init__(self, manager: str, handler: str,args: dict[str, Any]):
        self.manager = manager
        self.handler = handler
        self.args = args

    def serialize(self) -> str:
        try:
            data = {
                "manager": self.manager,
                "handler": self.handler,
                "args": self.args
            }
            return json.dumps(data) + "\n"
        except (TypeError, ValueError) as e:
            raise CarbonError(f"Failed to serialize request: {e}")


    @classmethod
    def deserialize(cls, raw_data: str) -> "CommandRequest":
        try:
            data = json.loads(raw_data.strip())
            return cls(
                manager=data["manager"],
                handler=data["handler"],
                args=data.get("args", {})
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise CarbonError(f"Failed to deserialize request: {e}")



class CommandOutput:


    def __init__(self, code: int, output: str):
        self.code = code
        self.output = output


    def serialize(self) -> str:
        try:
            data = {
                "code": self.code,
                "output": self.output
            }
            return json.dumps(data) + "\n"
        except (TypeError, ValueError) as e:
            raise CarbonError(f"Failed to serialize output: {e}")


    @classmethod
    def deserialize(cls, raw_data: str) -> "CommandOutput":
        try:
            data = json.loads(raw_data.strip())
            return cls(
                code=data["code"],
                output=data["output"]
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise CarbonError(f"Failed to deserialize output: {e}")