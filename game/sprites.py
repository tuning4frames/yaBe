import pygame

from game import gui, paths

ROOT = paths.resources() / "assets" / "SGQ_ui"

KEYS = {
    "D": (77, 127), "F": (97, 127), "J": (157, 127), "K": (177, 127),
    "A": (37, 127),
    "Q": (32, 106), "R": (92, 106), "N": (142, 148), "[": (232, 106), "]": (252, 106),
    "1": (24, 85), "5": (104, 85), "2": (44, 85), "3": (64, 85),
    "UP": (62, 198), "LEFT": (40, 218), "DOWN": (62, 218), "RIGHT": (84, 218),
    "BLANK": (6, 200),
}
WIDE_KEYS = {"SPACE": (73, 169, 117, 18), "ENTER": (257, 127, 35, 18)}
KEY_FACE = 13
KEY_TRAVEL = 3

NINE = {
    "note": ("ui_elements", (3, 165, 18, 16), (3, 3, 3, 5)),
    "note_hit": ("ui_elements", (3, 189, 18, 14), (3, 3, 3, 3)),
    "panel": ("ui_elements", (5, 261, 14, 14), (3, 3, 3, 3)),
    "select": ("ui_elements", (67, 165, 18, 16), (3, 3, 3, 5)),
    "dark": ("ui_elements", (67, 213, 18, 16), (3, 3, 3, 5)),
}
BAR = (5, 37, 38, 8)
BAR_FILL = (8, 56, 32, 2)
ICONS = {"note": (0, 0), "play": (16, 16), "pause": (32, 16)}

_sheets = {}
_cache = {}

def sheet(name):
    if name not in _sheets:
        sub = "inputs" if name in ("keyboard", "gamepad") else "game_ui"
        img = pygame.image.load(str(ROOT / sub / f"{name}.png")).convert_alpha()
        px = pygame.PixelArray(img)
        px.replace(gui.SHEET_BROWN, gui.BROWN)
        px.replace(gui.SHEET_CREAM, gui.CREAM)
        px.replace(gui.SHEET_SAGE, gui.SAGE)
        px.replace(gui.SHEET_DEEP, gui.DEEP)
        del px
        _sheets[name] = img
    return _sheets[name]

def _cut(name, rect):
    return sheet(name).subsurface(pygame.Rect(rect)).copy()

def _scaled(surf, k):
    return pygame.transform.scale(surf, (surf.get_width() * k, surf.get_height() * k))

def key(name, pressed=False, k=4):
    ck = ("key", name, pressed, k)
    if ck not in _cache:
        if name in WIDE_KEYS:
            src = _cut("keyboard", WIDE_KEYS[name])
        else:
            x, y = KEYS.get(name, KEYS["BLANK"])
            src = _cut("keyboard", (x, y, 19, 18))
        if pressed:
            w, h = src.get_size()
            out = pygame.Surface((w, h), pygame.SRCALPHA)
            out.blit(src, (0, h - 2), (0, h - 2, w, 2))
            out.blit(src, (0, KEY_TRAVEL), (0, 0, w, KEY_FACE))
            src = out
        _cache[ck] = _scaled(src, k)
    return _cache[ck]

def nine(kind, size, k=2):
    w, h = int(size[0]), int(size[1])
    ck = ("nine", kind, w, h, k)
    if ck in _cache:
        return _cache[ck]
    name, rect, (bl, bt, br, bb) = NINE[kind]
    src = _cut(name, rect)
    sw, sh = src.get_size()
    iw, ih = max(bl + br + 1, w // k), max(bt + bb + 1, h // k)
    out = pygame.Surface((iw, ih), pygame.SRCALPHA)
    cols = [(0, bl, 0, bl), (bl, sw - bl - br, bl, iw - bl - br), (sw - br, br, iw - br, br)]
    rows = [(0, bt, 0, bt), (bt, sh - bt - bb, bt, ih - bt - bb), (sh - bb, bb, ih - bb, bb)]
    for sx, sw_, dx, dw in cols:
        for sy, sh_, dy, dh in rows:
            part = src.subsurface((sx, sy, sw_, sh_))
            if (dw, dh) != (sw_, sh_):
                part = pygame.transform.scale(part, (dw, dh))
            out.blit(part, (dx, dy))
    _cache[ck] = _scaled(out, k)
    return _cache[ck]

def bar(width, frac, k=2):
    iw = max(8, int(width) // k)
    ck = ("bar", iw, k)
    if ck not in _cache:
        src = _cut("hud", BAR)
        sw, sh = src.get_size()
        frame = pygame.Surface((iw, sh), pygame.SRCALPHA)
        frame.blit(src, (0, 0), (0, 0, 3, sh))
        frame.blit(pygame.transform.scale(src.subsurface((3, 0, 1, sh)), (iw - 6, sh)), (3, 0))
        frame.blit(src, (iw - 3, 0), (sw - 3, 0, 3, sh))
        fill = pygame.Surface((iw - 6, 2), pygame.SRCALPHA)
        strip = _cut("hud", BAR_FILL)
        for x in range(0, iw, strip.get_width()):
            fill.blit(strip, (x, 0))
        _cache[ck] = (frame, fill)
    frame, fill = _cache[ck]
    out = frame.copy()
    n = int((iw - 6) * max(0.0, min(1.0, frac)))
    out.blit(fill, (3, 3), (0, 0, n, 2))
    return _scaled(out, k)

def icon(name, k=2):
    ck = ("icon", name, k)
    if ck not in _cache:
        x, y = ICONS[name]
        _cache[ck] = _scaled(_cut("icons_16x16", (x, y, 16, 16)), k)
    return _cache[ck]
