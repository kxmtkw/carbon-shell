import subprocess
from pathlib import Path
from .error import CarbonError


def shellrun(cmd: str, wait: bool = True) -> tuple[bool, str]:
    "Run a shell command."

    if wait:
        output = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
    else:
        output = subprocess.run(
            cmd, 
            shell=True, 
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    if output is None: return (True, "")

    if output.returncode == 0:
        return (True, output.stdout)
    else: 
        return (False, output.stdout or output.stderr)
    

def procrun(cmd: list[str], wait: bool = True) -> tuple[bool, str]:
    "Run a process"

    if wait:
        output = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True
        )
    else:
        output = subprocess.run(
            cmd, 
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    if output is None: return (True, "")

    if output.returncode == 0:
        return (True, output.stdout)
    else: 
        return (False, output.stdout or output.stderr)
    
    
valid_chars = set("0123456789abcdefABCDEF")
def isValidHex(hex_string: str) -> bool:
    "Validated hex formats: #abc #aabbcc"
    if not hex_string.startswith("#"):
        return False
    
    h = hex_string.lstrip("#")

    return len(h) in (3, 6) and all(c in valid_chars for c in h)


def isValidNumber(num_string: str) -> bool:
    "Checks whether the provided string is valid integar or float"
    try:
        float(num_string)
        return True
    except ValueError:
        return False
    

def writefile(filepath: str, content: str) -> None:
    "Writes to a file, creates any missing parents."
    abspath = Path(filepath).expanduser()

    if not abspath.parent.exists():
        abspath.parent.mkdir(511, True, True)

    with open(abspath, "w") as file:
        file.write(content)


def prompt(msg: str, options: list[str]) -> str:

    print(msg)
    print(f"Choose from: {tuple(options)}")
   

    for i in range(3):
        chosen = input(">> ").lower()

        if chosen not in options:
            print("Invalid option!")
            continue

        return chosen 
    
    CarbonError("Too many retries").halt()


def notify(summary, body="", *, urgency="normal", icon="", timeout=-1, app_name="CarbonShell"):
    cmd = ["notify-send", "--app-name", app_name, "--urgency", urgency]
    if icon:
        cmd += ["--icon", icon]
    if timeout >= 0:
        cmd += ["--expire-time", str(timeout)]
    cmd += [summary]
    if body:
        cmd += [body]
    subprocess.run(cmd)