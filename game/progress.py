import json
from pathlib import Path

from game import levels

def _save_path():
    import os
    import sys
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("APPDATA", str(Path.home()))) / "yaBe"
        base.mkdir(parents=True, exist_ok=True)
        return base / "progress.json"
    return Path(__file__).resolve().parent.parent / "progress.json"


PATH = _save_path()
ORDER = {"D": 0, "C": 1, "B": 2, "A": 3, "S": 4}

def load():
    if PATH.exists():
        try:
            return json.loads(PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {}

def save(data):
    PATH.write_text(json.dumps(data, indent=2, sort_keys=True))

def record(lv, score, grade, acc):
    data = load()
    key = lv["id"]
    prev = data.get(key)
    better = (
        prev is None
        or ORDER.get(grade, 0) > ORDER.get(prev.get("grade", "D"), 0)
        or (grade == prev.get("grade") and score > prev.get("score", 0))
    )
    if better:
        data[key] = {"name": lv["name"], "score": score, "grade": grade,
                     "acc": round(acc * 100, 2)}
        save(data)
        return True
    return False

def best(level_id):
    return load().get(level_id)


def goal_met(i):
    lv = levels.level(i)
    b = best(lv["id"])
    if not b:
        return False
    return ORDER.get(b.get("grade", "D"), 0) >= ORDER.get(lv.get("target", "C"), 0)


def unlocked(i):
    if i <= 0:
        return True
    return goal_met(i - 1)

def offset():
    return load().get("_offset_ms", 0)

def set_offset(ms):
    data = load()
    data["_offset_ms"] = ms
    save(data)
