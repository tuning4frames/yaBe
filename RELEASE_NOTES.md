# Release notes

## v1.1 — small fixes, endless mode, two new worlds

Windows build: `dist/yabe-beat.exe` (15.4 MB, single file, no install).

### Endless is actually endless now
- When the bar fills, you **level up into the next stage** instead of hitting
  the results screen. Score, combo, accuracy and life carry over (+0.15 heal).
  Only an empty life bar ends the run.
- Every stage is **faster**: 120 BPM +10 per stage, capped at 200, ~24 bars each.
- **Every run is different.** Stage layouts, bank picks and holds come from a
  fresh random seed per run, and each stage adds its own twist (rests thin out,
  an extra off-beat hold from stage 4).
- Endless music matches the world you're playing in.
- HUD shows `STAGE n`, the current BPM and total survived time; the next stage
  renders in the background so transitions are instant.

### Two new worlds
- **World 2 — winter.** Deep blue / ice blue / snow white palette, dark driving
  groove, plus-shaped pixel snow falling on the level select.
- **World 3 — ember.** Maroon / burnt orange / gold palette with its own warm
  progression, unlocked by clearing the end of world 2.
- Worlds unlock in order, each with its own unlock animation. Palette, music
  style, snow and the window titlebar all follow the world you're in.

### Renamed tracks (your saves are safe)
Only display names changed, so bests and unlocks carry over untouched.

| World | Tracks |
|-------|--------|
| 1 | ACORN · HARVEST · EMBER · COPPER · BONFIRE |
| 2 | FROST · BLIZZARD · GLACIER · AURORA · WHITEOUT |
| 3 | MAPLE · PUMPKIN · CIDER · AMBER · LEAFY |

### World 3 has its own tricks
- **AMBER** — a quad hold: grab all four lanes at once and hold ~3s while the
  rest bars keep the drums going.
- **LEAFY** — one very long hold on `K` (~8.6s) with the other lanes playing
  around it.
- **CIDER** — its own contour instead of a repeat.

### Small fixes
- Locked-level rows: the speckle no longer breaks the border, so the corners meet
  cleanly on all four sides.
- Level select: up/down now wrap inside a world (5 → 1), left/right wrap between
  worlds, and the footer is icon-based with the world counter in the header.
- Removed the dev menu and its cheats, plus the unused winter wallpapers.
- Fixed a crash: level navigation had shadowed the `start()` function.

### Notes for players
- **First launch of the .exe** synthesizes audio as it goes, so the very first
  level can take an extra second or two. It writes `.synth/` next to the exe and
  reuses it after that.
- Progress saves to `progress.json` next to the exe, so keep it if you want your
  bests.
- If a track ever feels off-beat, `]` / `[` nudge the audio offset by 10ms.