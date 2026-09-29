# yaBe

no mouse. no tab. just keys.

A 4-lane retro rhythm game built with pygame. Hit taps, hold long notes,
don't mash - and clear each level's goal grade to unlock the next.

**Repo: https://github.com/tuning4frames/yaBe**

Made for Hack Club. 🕹️

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
| Select | `UP`/`DOWN` choose · `SPACE` play · `1`–`5` jump · `[`/`]` audio offset ±10ms · `Q` quit |
| Play   | `D` `F` `J` `K` lanes · `ESC` pause · `F11` fullscreen |
| Result | `SPACE` retry · `N` next level (if goal met) · `ESC` back to levels |

## Levels

| # | Name      | BPM | Goal | Notes |
|---|-----------|-----|------|-------|
| 1 | WARM UP   | 84  | A    | Onboarding taps |
| 2 | STEADY    | 100 | A    | 87 notes, 15 **holds** (head + tail = 2 judgments) |
| 3 | RUSH      | 126 | B    | Dense streams |
| 4 | SWING     | 112 | B    | Off-beat swing, harder than Rush |
| 5 | OVERDRIVE | 140 | B    | Chords (`x` = lanes 0+3, `y` = 1+2) |

Grades: `S` ≥95% · `A` ≥87% · `B` ≥75% · `C` ≥60% · `D` below.
Clear a level's goal to unlock the next one.

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
main.py          game loop, scoring, holds, unlocks
game/levels.py   charts (banks, songs, hold definitions)
game/chart.py    timing, note generation
game/audio.py    synth (kick/snare/hat/bass/lead, v3 wavs)
game/hit.py      judgment windows, grades
game/input.py    lane keymap
game/progress.py bests, goal checks, offset
game/gui.py      palette, text, dither backdrop
game/sprites.py  UI sheets (keys, panels, bars, icons)
assets/          SGQ_ui art (game_ui + inputs)
fonts/           BoldPixels.ttf
```
