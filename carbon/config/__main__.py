from .updater import ConfigUpdater
from .getter import CarbonConfig

import sys

def main():
    updater = ConfigUpdater(CarbonConfig)
    updater.update()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--silent":
        return
    
    updater.notify()

if __name__ == "__main__":
    main()