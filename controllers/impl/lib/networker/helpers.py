import subprocess
from dataclasses import dataclass

@dataclass(init=True)
class ShellOutput:
    success: bool
    stdout: str

def shellRun(cmd: str) -> ShellOutput:
    output = subprocess.run(cmd, text=True, capture_output=True, shell=True)

    if output.returncode == 0:
        return ShellOutput(True, output.stdout.strip())
    else:
        return ShellOutput(False, (output.stdout + output.stderr).strip())
    
def processRun(cmd: list[str]) -> ShellOutput:
    output = subprocess.run(cmd, text=True, capture_output=True)

    if output.returncode == 0:
        return ShellOutput(True, output.stdout.strip())
    else:
        return ShellOutput(False, (output.stdout + output.stderr).strip())