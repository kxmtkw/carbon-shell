import subprocess
from pathlib import Path



class RofiShell:

    class Mode():
        drun = "drun"
        run = "run"
        window = "window"
        filebrowser = "filebrowser"
        ssh = "ssh"

    @classmethod
    def Run(cls, cmd: str) -> str:
        output = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if (output.returncode == 0): return output.stdout
        return output.stderr


    def __init__(self, rasi: str) -> None:
        self.rasi = Path(rasi)


    def displayMode(self, mode: str):
        cmd = f"rofi -show {mode} -theme {self.rasi}"
        self.Run(cmd)


    def display(self, prompt: str, mesg: str, options: list[str]) -> str:
        cmd = f"echo -e '{"\n".join(options)}' | rofi -dmenu -p '{prompt}' -mesg '{mesg}' -theme {self.rasi}"
        return self.Run(cmd)
    

