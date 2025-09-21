# utils/helpers.py
import json
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).parent.parent

def load_projects() -> List[Dict]:
    path = ROOT / "projects.json"
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
