import json

from game import levels, paths

PATH = paths.user_data() / "progress.json"
ORDER = {"D": 0, "C": 1, "B": 2, "A": 3, "S": 4}

def load():
    if PATH.exists():
        try:
            data = json.loads(PATH.read_text())
        except json.JSONDecodeError:
            return {}
        # id rename: equinox -> leafy. Carry any existing best over.
        if "equinox" in data and "leafy" not in data:
            data["leafy"] = data.pop("equinox")
            try:
                save(data)
            except OSError:
                pass
        return data
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

def world_seen(w):
    # w is the 0-based world index. World 0 needs no celebration.
    if w <= 0:
        return True
    data = load()
    if f"_world{w}_seen" in data:
        return bool(data[f"_world{w}_seen"])
    # legacy flag from when only world 2 existed.
    if w == 1:
        return bool(data.get("_world2_seen", False))
    return False

def mark_world_seen(w):
    data = load()
    data[f"_world{w}_seen"] = True
    save(data)

def replay_world(w):
    data = load()
    data[f"_world{w}_seen"] = False
    if w == 1:
        data["_world2_seen"] = False
    save(data)
