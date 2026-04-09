
def updateRofi(s: dict[str, str]) -> str:
    base = """
// NOTE: written by carbon shell
* {
"""
    for name, val in s.items():
        base += f"{name:<30}: {val};\n"
        
    base += "\n}"
    return base