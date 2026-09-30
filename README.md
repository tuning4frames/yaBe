# yaBe

no mouse. no tab. just keys.

A 4-lane retro rhythm game built with pygame. Hit taps, hold long notes,
don't mash - and clear each level's goal grade to unlock the next.

**Repo: https://github.com/tuning4frames/yaBe**

Made for Hack Club. 🕹️

Latest changes: [RELEASE_NOTES.md](RELEASE_NOTES.md)

## Download & run the game

Grab a release from **https://github.com/tuning4frames/yaBe/releases**
(or clone the repo), then:

```sh
pip install pygame
python main.py
```

Synth audio builds itself into `.synth/` on first run.
Bests + audio offset save to `progress.json`.

## Controls

| Where  | Keys |
|--------|------|
| Select | `LEFT`/`RIGHT` change world · `UP`/`DOWN` choose · `SPACE` play · `1`–`5` jump · `[`/`]` audio offset ±10ms · `Q` quit |
| Play   | `D` `F` `J` `K` lanes · `ESC` pause · `F11` fullscreen |
| Result | `SPACE` retry · `N` next level (if goal met) · `ESC` back to levels |
| Endless| `E` from the level select · die to end the run |

## Worlds

| World | Look | Tracks |
|-------|------|--------|
| 1 | autumn (brown/green/cream) | ACORN · HARVEST · EMBER · COPPER · BONFIRE |
| 2 | winter (blue/white) | FROST · BLIZZARD · GLACIER · AURORA · WHITEOUT |
| 3 | ember (red/orange/gold) | MAPLE · PUMPKIN · CIDER · AMBER · LEAFY |

Each world has its own palette and music style, and unlocks the next one —
world 2 by clearing BONFIRE, world 3 by clearing WHITEOUT. Endless mode plays
the style of the world you're on.

## Levels

World 1:

| # | Name     | BPM | Goal | Notes |
|---|----------|-----|------|-------|
| 1 | ACORN    | 84  | A    | Onboarding taps |
| 2 | HARVEST  | 100 | A    | 87 notes, 15 **holds** (head + tail = 2 judgments) |
| 3 | EMBER    | 126 | B    | Dense streams |
| 4 | COPPER   | 112 | B    | Off-beat swing, harder than EMBER |
| 5 | BONFIRE  | 140 | B    | Chords (`x` = lanes 0+3, `y` = 1+2) |

World 2 (`FROST` → `WHITEOUT`) and world 3 (`MAPLE` → `LEAFY`) run 116–166 BPM.
AMBER has a four-lane quad hold, LEAFY has one ~8.6s hold.

Grades: `S` ≥95% · `A` ≥87% · `B` ≥75% · `C` ≥60% · `D` below.
Clear a level's goal to unlock the next one.

## Endless

Pick a world and press `E`. Stages keep coming, each faster than the last
(120 → 200 BPM), with freshly generated patterns every run. Your score, combo
and life carry between stages; the run ends when life hits zero.

## Rules

- **Taps** - PERFECT 300 / GREAT 200 / GOOD 100, plus combo bonus (+4, caps at 50).
- **Holds** - hit the head like a tap, keep holding to the tail.
  Tail cleared = +300 + combo. Early release = DROP, combo gone.
- **Mash guard** - empty presses break combo and drain 0.02 life
  (0.08s debounce). Mashing for ~5s straight fails you. No accuracy penalty.
- **Life** - MISS −0.04 · PERFECT +0.03 · GREAT +0.02 · GOOD +0.01.
  Empty bar = FAILED.

## Project layout

```text
main.py          game loop, scoring, holds, unlocks, endless stages
game/levels.py   charts (banks, songs, hold definitions), world + style data
game/chart.py    timing, note generation
game/audio.py    synth (kick/snare/hat/bass/lead, v4 wavs)
game/hit.py      judgment windows, grades
game/input.py    lane keymap
game/progress.py bests, goal checks, offset
game/gui.py      world palettes, text, dither backdrop
game/sprites.py  UI sheets (keys, panels, bars, icons)
game/paths.py    resource paths (source and frozen exe)
assets/          SGQ_ui art (game_ui + inputs)
fonts/           BoldPixels.ttf
export_key.py    dump a keycap PNG in every world palette
```

## Building the .exe

```sh
python -m PyInstaller --clean --noconfirm yabe-beat.spec
```

Output lands in `dist/yabe-beat.exe`.
