BANDS = [
    (0.20, 0.100, "PERFECT", 1.0),
    (0.34, 0.170, "GREAT", 0.85),
    (0.50, 0.250, "GOOD", 0.6),
]

SCORE = {"PERFECT": 300, "GREAT": 200, "GOOD": 100, "MISS": 0}

def windows(beat):
    return [(min(cap, beat * frac), name, w) for frac, cap, name, w in BANDS]

def judge(dt, w):
    d = abs(dt)
    for window, name, weight in w:
        if d <= window:
            return name, weight
    return None

def miss_window(w):
    return w[-1][0]

def accuracy(hits, total):
    if not total:
        return 0.0
    return sum(hits) / total

def grade(acc):
    if acc >= 0.95:
        return "S"
    if acc >= 0.87:
        return "A"
    if acc >= 0.75:
        return "B"
    if acc >= 0.60:
        return "C"
    return "D"
