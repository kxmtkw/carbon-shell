from typing import Self


class CarbonError():

    def throw(self, msg: str) -> Self:
        Color.Print("[Error]", Color.red)
        print(msg)
        return self

    def halt(self):
        exit()


class Color:

    reset = "\033[0m"

    black   = "\033[30m"
    red     = "\033[31m"
    green   = "\033[32m"
    yellow  = "\033[33m"
    blue    = "\033[34m"
    magenta = "\033[35m"
    cyan    = "\033[36m"
    white   = "\033[37m"

    bright_black   = "\033[90m"
    bright_red     = "\033[91m"
    bright_green   = "\033[92m"
    bright_yellow  = "\033[93m"
    bright_blue    = "\033[94m"
    bright_magenta = "\033[95m"
    bright_cyan    = "\033[96m"
    bright_white   = "\033[97m"

    @classmethod
    def Print(cls, msg: str, color: str):
        print(f"{color}{msg}{Color.reset}")


def prompt(msg: str, options: list[str]) -> str:

    print(msg)
    print(f"Choose from: {tuple(options)}")
   

    for i in range(3):
        chosen = input(">> ").lower()

        if chosen not in options:
            print("Invalid option!")
            continue

        return chosen 
    
    CarbonError().throw("Too many retries").halt()