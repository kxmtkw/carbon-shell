from .color_print import Color

class CarbonError():

    def __init__(self, msg: str) -> None:
        self.msg = msg 
        Color.Print("[Error]", Color.red)
        print(msg)
        
    def halt(self):
        exit(1)