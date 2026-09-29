# THANK YOU FOR CHECKING OUT MY GAME <3
import sys

import pygame
from game import audio, chart, gui, hit, levels, progress, sprites
from game import input as keys

LANES = 4
TRAVEL = 2.1
FIELD = (440, 96, 400, 576)
NOTE_INSET = 0
NOTE_H = 40
COMBO_X = 1030
HOLD_X = 232
STATS_X = 920
MISS_DRAIN = 0.04
HIT_HEAL = {"PERFECT": 0.03, "GREAT": 0.02, "GOOD": 0.01}

pygame.init()
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except (ImportError, AttributeError, OSError):
    pass

SIZE = (1280, 720)
CX = SIZE[0] // 2
window = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
fullscreen = False
screen = pygame.Surface(SIZE)
pygame.display.set_caption("yabe beat")
clock = pygame.time.Clock()
gui.init(screen)

def tint_titlebar():
    try:
        import ctypes
        if sys.platform != "win32":
            return
        hwnd = pygame.display.get_wm_info().get("window")
        if not hwnd:
            return
        for attr, col in ((35, gui.BROWN), (36, gui.CREAM)):
            ref = ctypes.c_uint((col[2] << 16) | (col[1] << 8) | col[0])
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attr, ctypes.byref(ref), ctypes.sizeof(ref))
    except (ImportError, AttributeError, OSError):
        pass

tint_titlebar()
huge = pygame.font.Font(gui.FONT, 96)

audio.ensure_mixer()
tick = audio.tick()
tick.set_volume(0.5)

li = 0
lv = levels.level(0)
NOTES = []
TOTAL = 0
TOTAL_JUDGE = 0
HOLD_BONUS = 300
TAIL_FORGIVE = 0.12
TICK_SCORE = 50
TICK_INTERVAL = 0.3  # reset per level in load_level to beat/2
SPAM_DRAIN = 0.02
SPAM_DEBOUNCE = 0.08
last_spam = [0.0] * LANES
by_lane = [[] for _ in range(LANES)]
cursor = [0] * LANES
WINDOWS = hit.windows(chart.timing(lv)[0])
MISS = hit.miss_window(WINDOWS)
offset_ms = progress.offset()

mode = "select"
score = 0
combo = 0
best_combo = 0
weights = []
counts = {"PERFECT": 0, "GREAT": 0, "GOOD": 0, "MISS": 0}
flashes = []
glow = [0.0] * LANES
health = 1.0
new_best = False
failed = False
popup = None
paused = False
paused_at = 0.0

def load_level(i):
    global lv, NOTES, TOTAL, TOTAL_JUDGE, by_lane, WINDOWS, MISS
    lv = levels.level(i)
    NOTES = []
    for n in chart.chart(lv):
        NOTES.append({
            "t": n["t"], "lane": n["lane"], "dur": n.get("dur", 0.0),
            "judged": False, "name": None,
            "holding": False, "tail_judged": False, "tail_name": None,
        })
    TOTAL = len(NOTES)
    TOTAL_JUDGE = TOTAL + sum(1 for n in NOTES if n["dur"] > 0.001)
    by_lane = [[j for j, n in enumerate(NOTES) if n["lane"] == lane] for lane in range(LANES)]
    WINDOWS = hit.windows(chart.timing(lv)[0])
    MISS = hit.miss_window(WINDOWS)
    pygame.mixer.music.load(str(audio.render(lv)))
    return lv

def nearest(lane, song_t):
    idx = by_lane[lane]
    while cursor[lane] < len(idx) and NOTES[idx[cursor[lane]]]["judged"]:
        cursor[lane] += 1
    best = None
    best_d = MISS
    for j in idx[cursor[lane]:cursor[lane] + 3]:
        d = abs(NOTES[j]["t"] - song_t)
        if d <= best_d:
            best, best_d = j, d
    return best

def song_time():
    if paused:
        return paused_at
    p = pygame.mixer.music.get_pos()
    return max(0.0, p / 1000.0) - offset_ms / 1000.0

def toggle_pause():
    global paused, paused_at
    if paused:
        paused = False
        pygame.mixer.music.unpause()
    else:
        paused_at = song_time()
        paused = True
        pygame.mixer.music.pause()

def to_select():
    global mode
    pygame.mixer.music.stop()
    pygame.mixer.music.unpause()
    reset()
    mode = "select"

def is_hold(n):
    return n.get("dur", 0.0) > 0.001


def lane_held(lane):
    held = pygame.key.get_pressed()
    return any(held[kc] for kc in keys.KEYS[lane])


def miss(n):
    global combo, health, popup
    n["judged"] = True
    n["name"] = "MISS"
    n["holding"] = False
    counts["MISS"] += 1
    weights.append(0.0)
    if is_hold(n):
        # head missed: tail auto-misses so holds count head+tail
        n["tail_judged"] = True
        n["tail_name"] = "MISS"
        counts["MISS"] += 1
        weights.append(0.0)
    combo = 0
    health = max(0.0, health - MISS_DRAIN)
    popup = ["MISS", "HOLD" if is_hold(n) else "", 1.0]


def tail_success(n):
    global score, combo, best_combo, health, popup
    n["holding"] = False
    n["tail_judged"] = True
    n["tail_name"] = "PERFECT"
    counts["PERFECT"] += 1
    weights.append(1.0)
    combo += 1
    best_combo = max(best_combo, combo)
    score += HOLD_BONUS + min(combo, 50) * 4
    health = min(1.0, health + HIT_HEAL["PERFECT"])
    popup = ["HOLD", "OK", 1.0]
    flashes.append([n["lane"], "PERFECT", 1.0])
    tick.play()


def tail_fail(n, label="DROP"):
    global combo, health, popup
    n["holding"] = False
    n["tail_judged"] = True
    n["tail_name"] = "MISS"
    counts["MISS"] += 1
    weights.append(0.0)
    combo = 0
    health = max(0.0, health - MISS_DRAIN)
    popup = ["HOLD", label, 1.0]


def update_holds(song_t):
    if paused:
        return
    for n in NOTES:
        if not is_hold(n) or not n["judged"] or n["tail_judged"] or not n["holding"]:
            continue
        if n["name"] == "MISS":
            continue
        tail_t = n["t"] + n["dur"]
        held = lane_held(n["lane"])
        if held:
            if song_t >= tail_t:
                tail_success(n)
        else:
            # forgiving: release within TAIL_FORGIVE of the end still clears
            if song_t < tail_t - TAIL_FORGIVE:
                tail_fail(n, "DROP")
            elif song_t >= tail_t:
                tail_success(n)


def press(lane, song_t):
    global score, combo, best_combo, health, popup
    j = nearest(lane, song_t)
    if j is None:
        if song_t - last_spam[lane] < SPAM_DEBOUNCE:
            return
        last_spam[lane] = song_t
        combo = 0
        health = max(0.0, health - SPAM_DRAIN)
        popup = ["EMPTY", "", 0.6]
        return
    n = NOTES[j]
    dt = n["t"] - song_t
    res = hit.judge(dt, WINDOWS)
    if res is None:
        return
    name, wt = res
    n["judged"] = True
    n["name"] = name
    counts[name] += 1
    weights.append(wt)
    combo += 1
    best_combo = max(best_combo, combo)
    score += hit.SCORE[name] + min(combo, 50) * 4
    health = min(1.0, health + HIT_HEAL[name])
    side = "" if name == "PERFECT" else ("EARLY" if dt > 0 else "LATE")
    if is_hold(n):
        n["holding"] = True
        n["tail_judged"] = False
        popup = [name, ("HOLD " + side).strip(), 1.0]
    else:
        popup = [name, side, 1.0]
    flashes.append([lane, name, 1.0])
    tick.play()

def reset():
    global score, combo, best_combo, health, weights, counts, flashes, failed, popup, paused
    for i in range(LANES):
        last_spam[i] = 0.0
    for n in NOTES:
        n["judged"] = False
        n["name"] = None
        n["holding"] = False
        n["tail_judged"] = False
        n["tail_name"] = None
    for i in range(LANES):
        cursor[i] = 0
        glow[i] = 0.0
    score = combo = best_combo = 0
    weights = []
    counts = {"PERFECT": 0, "GREAT": 0, "GOOD": 0, "MISS": 0}
    flashes = []
    health = 1.0
    failed = False
    popup = None
    paused = False

def start():
    global mode
    if not progress.unlocked(li):
        return
    load_level(li)
    reset()
    mode = "play"
    pygame.mixer.music.play(start=0.0)

def hint(items, cy, k=2):
    parts = []
    for names, label in items:
        for n in names:
            parts.append(("key", sprites.key(n, k=k)))
        parts.append(("text", gui.small.render(label, False, gui.MID)))
    width = sum(s.get_width() + (24 if kind == "text" else 4) for kind, s in parts) - 24
    x = CX - width // 2
    for kind, s in parts:
        screen.blit(s, (x, cy - s.get_height() // 2))
        x += s.get_width() + (24 if kind == "text" else 4)

def draw_select():
    screen.blit(sprites.icon("note", 3), (CX - 220, 20))
    gui.text("YABE BEAT", (CX, 44), gui.FG, gui.big, center=True)
    gui.text("no mouse. no tab. just keys.", (CX, 86), gui.MID, gui.small, center=True)

    y = 116
    for i, l in enumerate(levels.LEVELS):
        sel = i == li
        x = 290
        lock = not progress.unlocked(i)
        screen.blit(sprites.nine("select" if sel and not lock else "panel", (700, 80)), (x, y))
        fg = gui.BG if sel and not lock else gui.FG
        sub = gui.BG if sel and not lock else gui.MID
        gui.text(f"{i + 1}  {l['name']}", (x + 28, y + 12), fg, gui.font)
        hold_tag = "  HOLDS" if l.get("holds") else ""
        lock_tag = "  LOCKED" if lock else ""
        gui.text(levels.star_string(l["stars"]) + hold_tag + lock_tag, (x + 30, y + 48), sub, gui.small)
        gui.text(f"{l['bpm']} bpm   {levels.bars(l)} bars   goal {l['target']}",
                 (x + 200, y + 48), sub, gui.small)
        if lock:
            prev = levels.level(i - 1)
            gui.text(f"clear {prev['name']} {prev['target']}", (x + 500, y + 28), sub, gui.small)
        else:
            b = progress.best(l["id"])
            if b:
                gui.text(f"{b['grade']}  {b['score']}", (x + 500, y + 12), fg, gui.font)
                gui.text(f"{b['acc']}%", (x + 502, y + 48), sub, gui.small)
            else:
                gui.text("not played", (x + 500, y + 28), sub, gui.small)
        y += 88

    hint([(["UP", "DOWN"], "choose"), (["SPACE"], "play"), (["Q"], "quit")], 596)
    hint([(["D", "F", "J", "K"], "are your lanes")], 644)
    hint([(["[", "]"], f"audio offset {offset_ms:+d} ms, if notes feel off-beat")], 692)

def draw_pause():
    gui.dither((0, 0) + SIZE, (0, 0, 0), 3, cell=1)
    screen.blit(sprites.nine("panel", (640, 190)), (CX - 320, 256))
    gui.text("PAUSED", (CX, 300), gui.FG, gui.big, center=True)
    gui.text(f"{lv['name']}   {lv['bpm']} bpm", (CX, 344), gui.MID, gui.small, center=True)
    hint([(["SPACE"], "resume"), (["R"], "restart"), (["Q"], "levels")], 396)

def draw_play(song_t):
    lane_w = gui.field(FIELD, LANES)
    hit_y = FIELD[1] + FIELD[3]
    pps = FIELD[3] / TRAVEL
    note_w = int(lane_w - NOTE_INSET * 2)
    top_y = hit_y - NOTE_H
    held = pygame.key.get_pressed()

    screen.set_clip(pygame.Rect(FIELD))

    beat = chart.timing(lv)[0]
    k = int(song_t / beat)
    while (k * beat - song_t) <= TRAVEL:
        y = gui.snap(hit_y - (k * beat - song_t) * pps - NOTE_H / 2)
        if y < top_y:
            if k % 4 == 0:
                pygame.draw.rect(screen, gui.LOW, (FIELD[0], y, FIELD[2], gui.PX))
            else:
                for x in range(FIELD[0], FIELD[0] + FIELD[2], gui.PX * 4):
                    pygame.draw.rect(screen, gui.LOW, (x, y, gui.PX * 2, gui.PX))
        k += 1

    pygame.draw.rect(screen, gui.MID, (FIELD[0], hit_y - gui.PX, FIELD[2], gui.PX))

    for i in range(LANES):
        bands = -int(-glow[i] * 3 // 1)
        x = int(FIELD[0] + i * lane_w)
        for b in range(bands):
            gui.dither((x, hit_y - 48 * (b + 1), int(lane_w), 48), gui.LOW, 3 - b)

    for j in range(1, TOTAL):
        a, b = NOTES[j - 1], NOTES[j]
        dt = b["t"] - song_t
        if abs(a["t"] - b["t"]) > 1e-6 or dt > TRAVEL or dt < 0 or a["judged"] and b["judged"]:
            continue
        lo, hi = sorted((a["lane"], b["lane"]))
        y = gui.snap(hit_y - dt * pps - NOTE_H / 2)
        pygame.draw.rect(screen, gui.FG, (FIELD[0] + (lo + 0.5) * lane_w, y - gui.PX,
                                          (hi - lo) * lane_w, gui.PX * 2))

    for i in range(LANES):
        down = glow[i] > 0.6 or any(held[kc] for kc in keys.KEYS[i])
        base = pygame.Rect(int(FIELD[0] + i * lane_w), top_y, int(lane_w), NOTE_H)
        pygame.draw.rect(screen, gui.FG if down else gui.BG, base)
        pygame.draw.rect(screen, gui.FG if down else gui.MID, base, gui.PX)
        gui.text(keys.LABELS[i], base.center, gui.BG if down else gui.FG, gui.font,
                 center=True)

    note = sprites.nine("note", (note_w, NOTE_H))
    # hold bodies (under heads)
    for n in NOTES:
        dur = n.get("dur", 0.0)
        if dur <= 0.001:
            continue
        if n.get("name") == "MISS" and n.get("tail_judged"):
            continue
        head_dt = n["t"] - song_t
        tail_dt = n["t"] + dur - song_t
        if tail_dt < -0.25 or head_dt > TRAVEL:
            continue
        # skip fully-done holds that are long past
        if n.get("tail_judged") and tail_dt < -0.05:
            continue
        lane = n["lane"]
        x = int(FIELD[0] + lane * lane_w + NOTE_INSET)
        bw = int(lane_w - NOTE_INSET * 2)
        y_head = gui.snap(hit_y - head_dt * pps - NOTE_H)
        y_tail = gui.snap(hit_y - tail_dt * pps - NOTE_H)
        top = max(FIELD[1], min(y_head, y_tail))
        bottom = min(hit_y, max(y_head, y_tail) + NOTE_H)
        if bottom <= top:
            continue
        body_col = gui.FG if n.get("holding") else gui.MID
        # body
        pygame.draw.rect(screen, body_col, (x + bw // 4, top, bw // 2, bottom - top))
        pygame.draw.rect(screen, gui.FG, (x + bw // 4, top, bw // 2, bottom - top), gui.PX)
        # tail cap
        if tail_dt > -0.25 and tail_dt < TRAVEL:
            screen.blit(note, (x, y_tail))
    for n in NOTES:
        dt = n["t"] - song_t
        if dt > TRAVEL or dt < -0.25 or n["judged"]:
            # hold heads in active-hold state hide the head (already hit)
            continue
        lane = n["lane"]
        x = int(FIELD[0] + lane * lane_w + NOTE_INSET)
        y = gui.snap(hit_y - dt * pps - NOTE_H)
        screen.blit(note, (x, y))
        gui.text(keys.LABELS[lane], (x + note_w / 2, y + NOTE_H / 2 - 2), gui.BG, gui.small,
                 center=True)

    for f in flashes:
        x = int(FIELD[0] + f[0] * lane_w)
        gui.dither((x, top_y, int(lane_w), NOTE_H), gui.JUDGE_COLOR[f[1]], int(f[2] * 3) + 1)
    screen.set_clip(None)

    if NOTES:
        left = (NOTES[0]["t"] - song_t) / beat
        if left > 0:
            label = str(int(left) + 1) if left < 4 else "GET READY"
            gui.text(label, (FIELD[0] + FIELD[2] / 2, FIELD[1] + 180), gui.FG,
                     gui.big, center=True, outline=gui.BG)
            tip = "hold H notes till the tail, don't let go"
            if any(n.get("dur", 0.0) > 0.001 for n in NOTES):
                gui.text(tip, (FIELD[0] + FIELD[2] / 2,
                         FIELD[1] + 230), gui.MID, gui.small, center=True)
            else:
                gui.text("hit each note as it lands on its key", (FIELD[0] + FIELD[2] / 2,
                         FIELD[1] + 230), gui.MID, gui.small, center=True)

    if popup:
        cx = FIELD[0] + FIELD[2] / 2
        gui.text(popup[0], (cx, hit_y - 150), gui.JUDGE_COLOR.get(popup[0], gui.FG), gui.big, center=True,
                 outline=gui.BG)
        if popup[1]:
            gui.text(popup[1], (cx, hit_y - 116), gui.MID, gui.small, center=True, outline=gui.BG)

    judged = sum(counts.values())
    live = sum(weights) / judged * 100 if judged else 100.0
    gui.text(f"{score}", (60, 26), gui.FG, gui.big)
    gui.text(f"{live:.1f}%", (CX, 24), gui.FG, gui.font, center=True)
    gui.text(f"{lv['name']}  {levels.star_string(lv['stars'])}", (CX, 50),
             gui.MID, gui.small, center=True)
    frac = min(1.0, song_time() / chart.length(lv))
    screen.blit(sprites.bar(FIELD[2], frac), (FIELD[0], FIELD[1] - 34))

    gui.text(f"x{combo}", (COMBO_X, 150), gui.FG, gui.big, center=True)
    if combo >= 10:
        gui.text("COMBO", (COMBO_X, 190), gui.MID, gui.small, center=True)

    life = pygame.transform.rotate(sprites.bar(420, health, k=3), 90)
    gui.text("LIFE", (HOLD_X + life.get_width() // 2, 128), gui.MID, gui.small, center=True)
    screen.blit(life, (HOLD_X, 146))

    for i, name in enumerate(("PERFECT", "GREAT", "GOOD", "MISS")):
        gui.text(f"{name} {counts[name]}", (STATS_X, 420 + i * 24), gui.JUDGE_COLOR[name],
                 gui.small)

    gui.text("ESC pause   F11 fullscreen", (60, 690), gui.MID, gui.small)
    if paused:
        draw_pause()

def draw_result():
    acc = hit.accuracy(weights, TOTAL_JUDGE if TOTAL_JUDGE else TOTAL)
    g = hit.grade(acc)
    gui.text("FAILED" if failed else "CLEAR", (CX, 56), gui.MID if failed else gui.FG,
             gui.big, center=True)
    gui.text(f"{lv['name']}  {levels.star_string(lv['stars'])}", (CX, 96),
             gui.MID, gui.small, center=True)
    if new_best:
        gui.text("NEW BEST", (CX, 126), gui.FG, gui.font, center=True)
    gui.text(g, (CX, 196), gui.FG, huge, center=True)
    gui.text(f"{acc * 100:.2f}%", (CX, 276), gui.FG, gui.big, center=True)

    rows = [
        ("score", f"{score}"),
        ("max combo", f"{best_combo}"),
        ("perfect", f"{counts['PERFECT']}"),
        ("great", f"{counts['GREAT']}"),
        ("good", f"{counts['GOOD']}"),
        ("miss", f"{counts['MISS']}"),
    ]
    y = 324
    for label, val in rows:
        gui.text(label, (CX - 220, y), gui.MID, gui.font)
        gui.text(val, (CX + 120, y), gui.FG, gui.font)
        y += 34
    target = lv["target"]
    met = not failed and progress.ORDER.get(g, 0) >= progress.ORDER.get(target, 0)
    gui.text(f"goal {target}  {'cleared' if met else 'not cleared'}",
             (CX, 574), gui.FG if met else gui.MID, gui.font, center=True)
    items = [(["SPACE"], "retry")]
    if met and li + 1 < levels.count():
        items.append((["N"], "next level"))
    items.append((["Q"], "quit"))
    hint(items, 630)
    gui.text("ESC back to levels", (CX, 686), gui.MID, gui.small, center=True)

running = True
while running:
    dt = clock.tick(120) / 1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.VIDEORESIZE and not fullscreen:
            window = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            tint_titlebar()
        elif e.type != pygame.KEYDOWN:
            continue
        elif e.key == pygame.K_F11:
            fullscreen = not fullscreen
            window = pygame.display.set_mode((0, 0) if fullscreen else SIZE,
                                             pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE)
            tint_titlebar()
        elif mode == "play":
            if paused:
                if e.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                    toggle_pause()
                elif e.key == pygame.K_r:
                    toggle_pause()
                    start()
                elif e.key == pygame.K_q:
                    to_select()
                continue
            if e.key == pygame.K_ESCAPE:
                toggle_pause()
                continue
            lane = keys.key_to_lane(e.key)
            if lane is not None:
                glow[lane] = 1.0
                press(lane, song_time())
        elif e.key == pygame.K_q:
            running = False
        elif mode == "select":
            if e.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                if progress.unlocked(li):
                    start()
            elif pygame.K_1 <= e.key <= pygame.K_9 and e.key - pygame.K_1 < levels.count():
                li = e.key - pygame.K_1
            elif e.key in (pygame.K_UP, pygame.K_w):
                li = max(0, li - 1)
            elif e.key in (pygame.K_DOWN, pygame.K_s):
                li = min(levels.count() - 1, li + 1)
            elif e.key in (pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET):
                offset_ms += 10 if e.key == pygame.K_RIGHTBRACKET else -10
                progress.set_offset(offset_ms)
        elif mode == "result":
            if e.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                start()
            elif e.key == pygame.K_n and li + 1 < levels.count():
                li += 1
                start()
            elif e.key == pygame.K_ESCAPE:
                reset()
                mode = "select"

    gui.backdrop()
    if mode == "select":
        draw_select()
    elif mode == "play":
        st = song_time()
        for n in NOTES:
            if not n["judged"] and st - n["t"] > MISS:
                miss(n)
        update_holds(st)
        for f in flashes:
            f[2] -= dt * 3.5
        flashes = [f for f in flashes if f[2] > 0]
        if popup:
            popup[2] -= dt * 1.8
            if popup[2] <= 0:
                popup = None
        for i in range(LANES):
            if glow[i] > 0:
                glow[i] = max(0.0, glow[i] - dt * 3.0)
        draw_play(st)
        if st > chart.length(lv) + 0.6 or health <= 0.0:
            # settle any hold tails still pending so accuracy stays head+tail
            for n in NOTES:
                if n.get("dur", 0.0) > 0.001 and n["judged"] and not n["tail_judged"]:
                    if n["name"] == "MISS":
                        continue
                    tail_t = n["t"] + n["dur"]
                    if st >= tail_t and lane_held(n["lane"]):
                        tail_success(n)
                    else:
                        # don't double-popup on mass fail; keep first popup
                        was_popup = popup
                        tail_fail(n, "DROP")
                        if was_popup is not None and n != NOTES[-1]:
                            pass
            pygame.mixer.music.stop()
            failed = health <= 0.0
            mode = "result"
            acc = hit.accuracy(weights, TOTAL_JUDGE if TOTAL_JUDGE else TOTAL)
            new_best = not failed and progress.record(lv, score, hit.grade(acc), acc)
    else:
        draw_result()
    ww, wh = window.get_size()
    k = min(ww / SIZE[0], wh / SIZE[1])
    if k >= 1:
        k = int(k)
        out = pygame.transform.scale(screen, (SIZE[0] * k, SIZE[1] * k))
    else:
        out = pygame.transform.smoothscale(screen, (int(SIZE[0] * k), int(SIZE[1] * k)))
    window.fill(gui.BG)
    window.blit(out, out.get_rect(center=(ww // 2, wh // 2)))
    pygame.display.flip()

pygame.quit()