from .color_print import Color

class CarbonError(Exception):

    def __init__(self, msg: str) -> None:
        self.msg = msg 
        Color.Print("[Error] ", Color.red, end="")
        print(msg)
        
    def halt(self):
        exit(1)