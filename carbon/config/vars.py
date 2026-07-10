from pathlib import Path
from dataclasses import dataclass

@dataclass(init=True, frozen=True)
class _ConfigVar:
	dir: Path
	statefile: Path
	datadir: Path

