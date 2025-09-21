# utils/helpers.py
import json
from pathlib import Path
import os
import requests

ROOT = Path(__file__).parent.parent

def load_settings():
    """
    Load settings từ local settings.json hoặc remote (nếu có biến env SETTINGS_URL).
    """
    remote = os.environ.get("SETTINGS_URL")
    if remote:
        try:
            resp = requests.get(remote, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict):
                return data
        except Exception as e:
            print("Warning: failed to fetch remote settings:", e)

    local_path = ROOT / "settings.json"
    if local_path.exists():
        try:
            return json.loads(local_path.read_text(encoding="utf-8"))
        except Exception as e:
            print("Warning: failed to parse local settings.json:", e)
    return {}

def load_projects():
    """
    Load projects từ file projects.json ở root project.
    """
    path = ROOT / "projects.json"
    if not path.exists():
        print("⚠️ Không tìm thấy projects.json")
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print("⚠️ Lỗi đọc projects.json:", e)
        return []
