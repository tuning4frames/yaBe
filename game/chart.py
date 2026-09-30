import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import levels

def timing(lv):
    beat = 60.0 / lv["bpm"]
    return beat, beat * 4, beat / 4

def chord(bi, lv, song_bi=None):
    roots = levels.style_of(lv, song_bi)["roots"]
    base = roots[bi % len(roots)]
    return (base, base + 3, base + 7)

def lane_pitch(bi, lane, lv, song_bi=None):
    ch = chord(bi, lv, song_bi)
    return (ch[0], ch[1], ch[2], ch[0] + 12)[lane] + 12

def _holds_lookup(lv):
    # {(song_bar_idx, step, lane): len_steps}
    out = {}
    for h in lv.get("holds", []):
        try:
            b, s, lane, n = h
            out[(int(b), int(s), int(lane))] = int(n)
        except (ValueError, TypeError):
            continue
    return out


def _bar_events(bi, lv):
    ev = []
    main_from = levels.INTRO_BARS
    main_to = levels.INTRO_BARS + levels.main_bars(lv)
    in_main = main_from <= bi < main_to
    in_outro = bi >= main_to
    song_bi = bi - main_from if in_main else None
    st = levels.style_of(lv, song_bi)
    ch = chord(bi, lv, song_bi)
    beat, _, step_dur = timing(lv)
    pat = levels.pattern(lv, bi - main_from) if in_main else None
    rest = in_main and not pat.strip(".")

    if bi < levels.INTRO_BARS:
        if bi == levels.INTRO_BARS - 1:
            for s in st["kick"]:
                ev.append((s, "kick", None))
            for s in st["snare"]:
                ev.append((s, "snare", None))
    elif in_outro or rest:
        for s in st["kick"]:
            ev.append((s, "kick", None))
        if bi % 2 == 1:
            for s in st["snare"]:
                ev.append((s, "snare", None))
    else:
        for s in st["kick"]:
            ev.append((s, "kick", None))
        for s in st["snare"]:
            ev.append((s, "snare", None))

    for s in range(0, 16, st["hat_every"]):
        ev.append((s, "hat", s == 14 and bi % 4 == 3))

    for s in st["bass"]:
        ev.append((s, "bass", ch[0] - 12))

    if in_main:
        holds = _holds_lookup(lv)
        song_bi = bi - main_from
        emitted = set()
        for s, c in enumerate(pat):
            for lane in levels.lanes_of(c):
                nsteps = holds.get((song_bi, s, lane), 0)
                dur = max(0.0, nsteps * step_dur)
                ev.append((s, "lead", (lane_pitch(bi, lane, lv, song_bi), dur)))
                ev.append((s, "note", (lane, dur)))
                emitted.add((s, lane))
        # holds that have no matching tap still spawn a hold note
        for (b, s, lane), nsteps in holds.items():
            if b != song_bi or (s, lane) in emitted:
                continue
            dur = max(0.0, nsteps * step_dur)
            ev.append((s, "lead", (lane_pitch(bi, lane, lv, song_bi), dur)))
            ev.append((s, "note", (lane, dur)))
    return ev

def events(lv):
    _, bar, step = timing(lv)
    for bi in range(levels.bars(lv)):
        base = bi * bar
        for s, kind, payload in _bar_events(bi, lv):
            yield base + s * step, kind, payload

def length(lv):
    return levels.bars(lv) * timing(lv)[1]

def chart(lv):
    _, _, step_dur = timing(lv)
    out = []
    for t, kind, p in events(lv):
        if kind != "note":
            continue
        # backward compat: old payload was int lane
        if isinstance(p, (list, tuple)):
            lane, dur = p
        else:
            lane, dur = p, 0.0
        out.append({"t": t, "lane": int(lane), "dur": float(dur)})
    out.sort(key=lambda n: n["t"])
    # safety: truncate holds that would overlap the next head on same lane.
    # keep at least a half-step gap so heads stay readable.
    by_lane = {}
    for n in out:
        by_lane.setdefault(n["lane"], []).append(n)
    for lane_notes in by_lane.values():
        for a, b in zip(lane_notes, lane_notes[1:]):
            if a["dur"] <= 0:
                continue
            max_dur = b["t"] - a["t"] - step_dur * 0.5
            if max_dur < 0:
                max_dur = 0.0
            if a["dur"] > max_dur:
                a["dur"] = max_dur
    return out


def is_hold(n):
    return n.get("dur", 0.0) > 0.001


def hold_count(lv):
    return len(lv.get("holds", []))
