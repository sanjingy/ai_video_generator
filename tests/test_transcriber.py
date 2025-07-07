import json
from pathlib import Path
print(json.loads(Path("D:\download\config.json").read_text(encoding="utf-8")))
