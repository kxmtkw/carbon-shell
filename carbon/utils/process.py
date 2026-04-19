import subprocess

class ProcessManager:
    "Class to manage basic processes."

    def __init__(self, cmd: str):
        self._cmd = cmd
        self._proc = None


    def start(self, *args):

        if self._proc and self._proc.poll() is None:
            self.kill()

        self._proc = subprocess.Popen(
            [self._cmd, *[str(a) for a in args]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


    def kill(self):
        if self._proc:
            self._proc.terminate()
            self._proc = None