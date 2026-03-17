from .updater import ConfigUpdater
from .getter import CarbonConfig

def main():
    updater = ConfigUpdater(CarbonConfig)
    updater.update()

if __name__ == "__main__":
    main()