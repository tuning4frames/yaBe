from pathlib import Path

import pygame
from game import hit

FONT = str(Path(__file__).resolve().parent.parent / "fonts" / "BoldPixels.ttf")

SHEET_BROWN = (88, 68, 34)
BROWN = (30, 22, 10)
DEEP = (94, 133, 73)
SAGE = (120, 164, 106)
CREAM = (212, 210, 155)

BG = BROWN
FG = CREAM
MID = SAGE
LOW = DEEP

INK = FG
DARK = MID
LIGHT = LOW
PAPER = BG
LANE_BG = BG
LANE_LINE = LOW
WHITE = FG
GREY = MID
DIM = LOW
GOLD = FG
GREEN = FG
PINK = MID
CYAN = FG

LANE_COLORS = (SAGE, SAGE, SAGE, SAGE)
JUDGE_COLOR = {
    "PERFECT": CREAM, "GREAT": SAGE, "GOOD": DEEP, "MISS": DEEP,
}

PX = 2

scr = None
font = None
small = None
big = None
_tiles = {}
_backdrop = None

def init(screen):
    global scr, font, small, big
    scr = screen
    font = pygame.font.Font(FONT, 32)
    small = pygame.font.Font(FONT, 16)
    big = pygame.font.Font(FONT, 48)

def snap(v):
    return int(v) // PX * PX

def text(t, pos, col=WHITE, f=None, center=False, outline=None):
    f = f or font
    img = f.render(t, False, col)
    r = img.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    if outline:
        edge = f.render(t, False, outline)
        for dx, dy in ((-PX, 0), (PX, 0), (0, -PX), (0, PX), (-PX, -PX), (PX, PX), (-PX, PX), (PX, -PX)):
            scr.blit(edge, r.move(dx, dy))
    scr.blit(img, r)

def _tile(col, level, cell):
    key = (col, level, cell)
    if key not in _tiles:
        s = pygame.Surface((8 * PX, 8 * PX))
        s.fill((255, 0, 255))
        s.set_colorkey((255, 0, 255))
        n = (8 * PX) // cell
        for gy in range(n):
            for gx in range(n):
                on = {
                    1: gx % 2 == 0 and gy % 2 == 0,
                    2: (gx + gy) % 2 == 0,
                    3: not (gx % 2 == 1 and gy % 2 == 1),
                }[level]
                if on:
                    s.fill(col, (gx * cell, gy * cell, cell, cell))
        _tiles[key] = s
    return _tiles[key]

def dither(rect, col, level, dst=None, cell=PX):
    dst = dst or scr
    if level >= 4:
        dst.fill(col, rect)
        return
    if level <= 0:
        return
    rect = pygame.Rect(rect)
    tile = _tile(col, level, cell)
    tw, th = tile.get_size()
    old = dst.get_clip()
    dst.set_clip(rect.clip(old))
    for y in range(rect.top - rect.top % th, rect.bottom, th):
        for x in range(rect.left - rect.left % tw, rect.right, tw):
            dst.blit(tile, (x, y))
    dst.set_clip(old)

def backdrop():
    global _backdrop
    if _backdrop is None:
        _backdrop = pygame.Surface(scr.get_size())
        _backdrop.fill(BG)
    scr.blit(_backdrop, (0, 0))

def field(rect, lanes=4):
    from game import sprites
    x0, y0, fw, fh = rect
    pad = 3 * PX
    scr.blit(sprites.nine("panel", (fw + pad * 2, fh + pad * 2)), (x0 - pad, y0 - pad))
    w = fw / lanes
    for i in range(1, lanes):
        pygame.draw.rect(scr, LOW, (x0 + i * w - PX // 2, y0, PX, fh))
    return w

def arrow(lane, cx, cy, size, col):
    h = size
    w = size * 1.15
    if lane == 0:
        pts = [(cx - w / 2, cy), (cx, cy - h / 2), (cx, cy + h / 2)]
    elif lane == 1:
        pts = [(cx, cy + h / 2), (cx - w / 2, cy), (cx + w / 2, cy)]
    elif lane == 2:
        pts = [(cx, cy - h / 2), (cx - w / 2, cy), (cx + w / 2, cy)]
    else:
        pts = [(cx + w / 2, cy), (cx, cy - h / 2), (cx, cy + h / 2)]
    pygame.draw.polygon(scr, col, pts)
