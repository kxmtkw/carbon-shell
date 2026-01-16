from pathlib import Path
import shutil

import subprocess

exclude = ["alacritty", "quickshell"]

def main():

	print("Starting install...")


	user = Path("~/.config").expanduser()
	config = Path("Config")

	for item in config.iterdir():

		if item.name in exclude:
			print(f"Excluded: {item.name}")
			continue

		print(f"Transferring: {item.name}")

		dest = user.joinpath(item.name) 

		if dest.exists():
			print(f"Removed previous: {dest.absolute()}")
			shutil.rmtree(dest)

		shutil.copytree(item.absolute(), dest)
		print(f"Created: {dest.absolute()}")


	print("Reloading hyprland...")

	subprocess.run("hyprctl reload", shell=True, capture_output=True)

main()
