from .error import CarbonError

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