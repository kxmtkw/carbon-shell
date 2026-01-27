import venv, os
from pathlib import Path
import subprocess

carbon_path = Path("~/.carbon").expanduser()

wd = Path(__file__).parent

if wd != carbon_path:
    print("Cannot install Carbon Shell. 'install.py' is not within ~/.carbon")
    exit(1)


print("Creating venv...")

try:
    venv.create(carbon_path.joinpath(".venv"))
except Exception as e:
    print(f"Something went wrong during venv creation.")
    raise e 

print("Created venv!")

print("Setting up...")

subprocess.run(f"{carbon_path.joinpath(".venv/bin/activate")}", shell=True)

subprocess.run(f"pip install .", shell=True)

print("Setup complete! Activate venv and run 'carbon'!")