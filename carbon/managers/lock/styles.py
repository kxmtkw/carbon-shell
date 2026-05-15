from carbon.utils import writefile

def writeLockStyle(file: str, path: str):
	string = f"""
background {{
    monitor =
    path = {path}
    blur_passes = 4
    blur_size = 5
    noise = 0.06
    brightness = 0.6
}}
"""
	writefile(file, string)


