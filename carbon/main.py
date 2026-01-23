import os
from pathlib import Path

from .args import parseArgs
from .install import installCarbon, uninstallCarbon
from .misc import CarbonError

def main():

    carbon_path = Path("~/code/carbon-shell").expanduser()

    if not carbon_path.exists():
        CarbonError().throw(f"Carbon path '{carbon_path}' not found!").halt()

    os.chdir(carbon_path)

    args = parseArgs()

    if args.install:
        installCarbon()

    elif args.uninstall:
        uninstallCarbon()

    elif args.colorify:
        pass 





    


