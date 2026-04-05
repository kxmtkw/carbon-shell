import subprocess
from pathlib import Path
from .error import CarbonError


def shellrun(cmd: str) -> tuple[bool, str]:
    "Run a shell command."
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if output.returncode == 0:
        return (True, output.stdout)
    else: 
        return (False, output.stderr or output.stdout)
    

def procrun(cmd: list[str]) -> tuple[bool, str]:
    "Start a process"
    output = subprocess.run(cmd, capture_output=True, text=True)

    if output.returncode == 0:
        return (True, output.stdout)
    else: 
        return (False, output.stderr or output.stdout)
    
    
valid_chars = set("0123456789abcdefABCDEF")
def is_valid_hex(hex_string: str) -> bool:
    "Validated hex formats: #abc #aabbcc"
    if not hex_string.startswith("#"):
        return False
    
    h = hex_string.lstrip("#")

    return len(h) in (3, 6) and all(c in valid_chars for c in h)


def is_valid_number(num_string: str) -> bool:
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