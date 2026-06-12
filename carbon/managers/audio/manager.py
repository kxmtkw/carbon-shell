import time
from typing import Dict, Callable, Any
from dataclasses import dataclass, replace
from threading import Lock

from carbon.managers.base import BaseManager
from carbon.utils import CarbonError, shellrun, clamp, procrun, logger, locked


class AudioManager(BaseManager):

	audioLock = Lock()

	@dataclass(init=True, kw_only=True)
	class State(BaseManager.State):
		volume: float
		muted: bool
		mic_muted: bool
		minimum: float
		maximum: float


	def __init__(self, internalDispatch: Callable[[str, str, dict[str, Any]], None], getManagerState: Callable[[str], State]):
		super().__init__(internalDispatch, getManagerState)

		self.state: AudioManager.State = self.State(
			volume=100,
			muted=False,
			mic_muted=False,
			minimum=0,
			maximum=100
		)

		self.saved_volume = 100
		self.saved_mic_volume = 100

	def start(self):
		pass


	def end(self):
		pass
	

	def name(self) -> str:
		return "audio"
	

	def handlers(self) -> Dict[str, Callable]:
		return {
			"get": self.getVolume,
			"set": self.setVolume,
			"increase": self.increaseVolume,
			"decrease": self.decreaseVolume,
			"mute": lambda: self.muteVolume(muted=True),
			"unmute": lambda: self.muteVolume(muted=False),
			"toggle-mute": lambda: self.muteVolume(muted=not self.state.muted),
			"mute-mic": lambda: self.muteMic(muted=True),
			"unmute-mic": lambda: self.muteMic(muted=False),
			"toggle-mic": lambda: self.muteMic(muted=not self.state.mic_muted)
		}
	

	def getState(self) -> State:
		return replace(self.state)
	

	def setState(self, state: State):
		self.setVolume(value=state.volume)
		self.muteMic(muted=state.mic_muted)
		self.muteVolume(muted=state.muted)

		try:
			self.state.minimum = float(state.minimum)
			self.state.maximum = float(state.maximum)
		except ValueError:
			raise CarbonError("Non-number types used in numeral values of audio manager.")


	def getHelp(self) -> str:
		return _help
	

	def updateCurrentVolume(self):
		# Update sink volume
		success, out = procrun(["pactl", "get-sink-volume", "@DEFAULT_SINK@"])
		if not success:
			raise CarbonError(f"pactl failure: {out}")
		
		import re
		match = re.search(r"(\d+)%", out)
		if not match:
			raise CarbonError(f"Could not parse sink volume from pactl output: {out}")
		self.state.volume = float(match.group(1))

		success, out = procrun(["pactl", "get-sink-mute", "@DEFAULT_SINK@"])
		if not success:
			raise CarbonError(f"pactl failure: {out}")
		self.state.muted = "yes" in out.lower()


	def setVolume(self, *, value: float):

		try:
			value = float(value)
		except ValueError:
			raise CarbonError("Value must be a number.")
		
		value = clamp(value, self.state.minimum, self.state.maximum)
		procrun(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{value}%"])
		self.state.volume = value

		msg = f"Volume set to {self.state.volume}%"
		logger.info("audio", msg)
		return msg
	

	def muteVolume(self, *, muted: bool):

		procrun(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1" if muted else "0"])
		self.state.muted = muted

		msg = "Volume muted." if muted else "Volume unmuted."
		logger.info("audio", msg)
		return msg


	def increaseVolume(self, *, value: float):

		self.updateCurrentVolume()

		try:
			value = float(value)
		except ValueError:
			raise CarbonError("Value must be a number.")
		
		new_volume = self.state.volume + value
		self.setVolume(value=new_volume)
		
		msg = f"Volume increased by {value}%. Is now {self.state.volume}%."
		logger.info("audio", msg)
		return msg
	

	def decreaseVolume(self, *, value: float):

		self.updateCurrentVolume()

		try:
			value = float(value)
		except ValueError:
			raise CarbonError("Value must be a number.")
		
		new_volume = self.state.volume - value
		self.setVolume(value=new_volume)
		
		msg = f"Volume decreased by {value}%. Is now {self.state.volume}%."
		logger.info("audio", msg)
		return msg


	def getVolume(self):
		self.updateCurrentVolume()
		return self.state.volume


	def muteMic(self, *, muted: bool):
		procrun(["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "1" if muted else "0"])
		self.state.mic_muted = muted
		msg = "Microphone muted." if muted else "Microphone unmuted."
		logger.info("audio", msg)
		return msg



_help = """
==> audio
Control and set the system audio levels.

handlers:

	> get
		Get the current volume and mic status.

	> set --value [number]
		Set the volume to this percentage.

	> increase --value [number]
		Increase the volume by some percentage.

	> decrease --value [number]
		Decrease the volume by some percentage.

	> mute
		Mute the audio output.

	> unmute
		Unmute the audio output.

	> toggle-mute
		Toggle audio output mute status.

	> mute-mic
		Mute the microphone.

	> unmute-mic
		Unmute the microphone.

	> toggle-mic
		Toggle the microphone mute status.
"""
