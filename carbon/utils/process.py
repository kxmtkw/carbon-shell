import subprocess, time

class ProcessManager:
    "Class to manage basic processes."

    def __init__(self, cmd: str, *, only_one: bool = False):
        self._cmd = cmd
        self._proc = None
        self._only_one = only_one


    def start(self, *args):

        if self._proc and self._proc.poll() is None:
            self.kill()

        if self._only_one:
            subprocess.run(f"killall {self._cmd}", shell=True, capture_output=True)

        self._proc = subprocess.Popen(
            [self._cmd, *[str(a) for a in args]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


    def poll(self, timeout: float = 1.0) -> bool:
        if not self._proc:
            return False
        start = time.time()
        while time.time() - start < timeout:
            if self._proc.poll() is None:
                return True
            time.sleep(0.1)
        return False


    def kill(self):
        if self._proc:
            self._proc.terminate()
            self._proc = None