import shlex
import subprocess
from pathlib import Path



class RofiShell:

    class Mode():
        drun = "drun"
        run = "run"
        window = "window"
        filebrowser = "filebrowser"
        ssh = "ssh"

    MarkActive = "\x00active\x1ftrue"
    MarkUrgent = "\x00urgent\x1ftrue"

    @classmethod
    def Run(cls, cmd: str) -> str:
        output = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if (output.returncode == 0): return output.stdout.strip()
        return output.stderr.strip()
    

    def __init__(self, themepath: str) -> None:
        self.rasi = Path(themepath)


    def updateTheme(self, themepath: str) -> None:
        self.rasi = Path(themepath)
    

    def displayMode(self, mode: str):
        cmd = f"rofi -show {mode} -theme {self.rasi}"
        self.Run(cmd)


    def display(self, prompt: str, mesg: str, options: list[str], *, password: bool = False) -> str:
        proc = subprocess.Popen(
            [
                "rofi",
                "-dmenu",
                "-password" if password else "",
                "-p", prompt,
                "-mesg", mesg,
                "-theme", self.rasi,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        if proc.stdin:
            proc.stdin.write("\n".join(options))
            proc.stdin.close()

        proc.wait()

        if proc.stdout:
            selection = proc.stdout.read()
            return selection.strip()
        else:
            return ""
            

    def displayNoBlock(self, prompt: str, mesg: str, options: list[str]) -> subprocess.Popen:
        proc = subprocess.Popen(
            [
                "rofi",
                "-dmenu",
                "-p", prompt,
                "-mesg", mesg,
                "-theme", self.rasi,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        if proc.stdin:
            proc.stdin.write("\n".join(options))
            proc.stdin.close()

        return proc
