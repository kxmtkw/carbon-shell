from genericpath import isdir, isfile
from pathlib import Path
from pydoc import isdata
import shutil
import json

import subprocess

CONFIG = Path("Config")


def get_transfer_details() -> dict:

	json_path = CONFIG.joinpath("transfer.json")

	with open(json_path) as file:
		details = json.load(file)

	return details


def main():

	print("Starting install...")

	transfer_details: dict = get_transfer_details()

	for item in transfer_details["config"]:

		src = CONFIG.joinpath(item["name"])

		if not item["include"]:
			print(f"Skipped :: {item["name"]}")
			continue
		
		dest = Path(item["dest"]).expanduser()

		if src.is_file():
			shutil.copy(src, dest)

		if src.is_dir():

			if dest.exists():
				shutil.rmtree(dest)
				print(f"Removed :: {dest.absolute()}")

			shutil.copytree(src, dest)

		print(f"Transferred :: {src.name} -> {dest.absolute()}")

		
	print("Reloading hyprland...")

	subprocess.run("hyprctl reload", shell=True, capture_output=True)


main()
