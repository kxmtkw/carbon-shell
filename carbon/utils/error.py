from .color_print import Color

class CarbonError(Exception):

	def __init__(self, msg: str) -> None:
		self.msg = msg 
		super().__init__(msg)
		
	def print(self):
		Color.Print("[Error] ", Color.red, end="")
		print(self.msg)

	def halt(self):
		self.print()
		exit(1)