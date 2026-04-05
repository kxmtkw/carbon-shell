import subprocess
from pathlib import Path
from enum import Enum

class RofiShell:

    class Mode(Enum):
        drun = "drun"
        run = "run"
        window = "window"
        filebrowser = "filebrowser"
        ssh = "ssh"
        dmenu = "dmenu"

    class Error(Exception):
        def __init__(self, *args):
            super().__init__(*args)


    def __init__(self, themepath: str):
        self._proc: subprocess.Popen | None = None
        self.rasi: Path | None = None

        self.updateTheme(themepath)


    def updateTheme(self, themepath: str) -> None:
        self.rasi = Path(themepath).expanduser()
        
        if not self.rasi.exists():
            raise FileNotFoundError(self.rasi)
        

    def display(
        self, 
        *,
        mode: RofiShell.Mode, 
        prompt: str = "", 
        mesg: str = "", 
        options: list[str] = [], 
        password: bool = False
        ) -> None:
        """
        Display rofi with the given arguments.

        Options argument is ignored unless mode is 'dmenu'
        """

        if self._proc:
            self.close()
        
        if mode == RofiShell.Mode.dmenu:

            proc = subprocess.Popen(
                [
                    "rofi",
                    "-dmenu",
                    "-markup-rows",
                    "-password" if password else "",
                    "-p", prompt,
                    "-mesg", mesg,
                    "-theme", self.rasi,
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True
            )

            if proc.stdin:
                proc.stdin.write("\n".join(options))
                proc.stdin.close()

        else:

            proc = subprocess.Popen(
                [
                    "rofi",
                    "-show", mode.value,
                    "-password" if password else "",
                    "-p", prompt,
                    "-mesg", mesg,
                    "-theme", self.rasi,
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True
            )

        self._proc = proc

        
    def wait(self, timeout: float | None = None) -> str | None:
        "Wait for rofi to close. Useful for dmenu"

        if not self._proc:
            raise RofiShell.Error("No Rofi running.")
        
        try:
            self._proc.wait(timeout)
        except subprocess.TimeoutExpired:
            return None

        if self._proc.stdout:
            selection = self._proc.stdout.read()
            self._proc = None
            return selection.strip()
        else:
            self._proc = None
            return ""
        
    
    def close(self):
        "Forcefully close rofi"

        if not self._proc:
            raise RofiShell.Error("No Rofi running.")
        
        self._proc.kill()
        self._proc.wait()
        self._proc = None


    @classmethod
    def markActive(cls, option: str) -> str:
        active = "\x00active\x1ftrue"
        return f"{option}{active}"
    
    @classmethod
    def markUrgent(cls, option: str) -> str:
        urgent = "\x00urgent\x1ftrue"
        return f"{option}{urgent}"
    
    @classmethod
    def markWithIcon(cls, option: str, icon: str) -> str:
        icon_option = f"{option}\x00icon\x1f{icon}"
        return icon_option

