from carbon.rofi import RofiShell

class Launcher():
	
	def __init__(self):
		self.rofi = RofiShell("Config/rofi/launcher.rasi")
		
	def launchApps(self):
		self.rofi.displayMode(RofiShell.Mode.drun)

	def launchRun(self):
		self.rofi.displayMode(RofiShell.Mode.run)