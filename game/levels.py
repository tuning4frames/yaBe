LEVELS = [
    {
        "id": "warmup",
        "bank": 0,
        "name": "ACORN",
        "bpm": 84,
        "song": "0101232345456237",
        "stars": 1,
        "target": "A",
    },
    {
        "id": "steady",
        "bank": 1,
        "name": "HARVEST",
        "bpm": 100,
        "song": "01012323454.567567.7",
        "stars": 2,
        "target": "A",
        # hold notes: [song_bar_idx, step_0_15, lane_0_3, len_steps]
        # head must match an existing tap; tail = head + len_steps * 16th.
        # len 3 = 0.45s, len 4 = 0.6s, len 6 = 0.9s at 100bpm.
        "holds": [
            [0, 0, 0, 3], [0, 4, 1, 3], [0, 8, 2, 3], [0, 12, 3, 3],
            [2, 0, 0, 3], [2, 4, 1, 3], [2, 8, 2, 3], [2, 12, 3, 3],
            [14, 0, 0, 4], [14, 4, 3, 4],
            [17, 0, 0, 6], [17, 4, 3, 4], [17, 8, 0, 2],
            [19, 0, 0, 6], [19, 4, 3, 4],
        ],
    },
    {
        "id": "rush",
        "bank": 3,
        "name": "EMBER",
        "bpm": 126,
        "song": "0012.123345454.6767123457",
        "stars": 3,
        "target": "B",
    },
    {
        "id": "swing",
        "bank": 2,
        "name": "COPPER",
        "bpm": 112,
        "song": "01223345.12345664567",
        "stars": 4,
        "target": "B",
    },
    {
        "id": "overdrive",
        "bank": 4,
        "name": "BONFIRE",
        "bpm": 140,
        "song": "0121233.45456677.1236740",
        "stars": 5,
        "target": "B",
    },
    # ---- page two ----
    {
        "id": "pulse",
        "bank": 1,
        "name": "FROST",
        "bpm": 116,
        "song": "0123456765432101234567",
        "stars": 3,
        "target": "B",
        "style": "dark",
    },
    {
        "id": "mirage",
        "bank": 2,
        "name": "BLIZZARD",
        "bpm": 122,
        "song": "00112233445566776543210",
        "stars": 4,
        "target": "B",
        "style": "dark",
        "holds": [
            [0, 0, 0, 4], [4, 8, 3, 4],
            [12, 0, 1, 4], [16, 12, 2, 4],
        ],
    },
    {
        "id": "thunder",
        "bank": 3,
        "name": "GLACIER",
        "bpm": 148,
        "song": "012345670123456701234567",
        "stars": 5,
        "target": "B",
        "style": "dark",
    },
    {
        "id": "neon",
        "bank": 4,
        "name": "AURORA",
        "bpm": 130,
        "song": "01212334545667712367401",
        "stars": 5,
        "target": "B",
        "style": "dark",
    },
    {
        "id": "abyss",
        "bank": 3,
        "name": "WHITEOUT",
        "bpm": 160,
        "song": "0123456776543210011223344",
        "stars": 5,
        "target": "C",
        "style": "dark",
    },
    # ---- page three (autumn ember world) ----
    {
        "id": "maple",
        "bank": 1,
        "name": "MAPLE",
        "bpm": 134,
        "song": "012321076543210123",
        "stars": 4,
        "target": "B",
        "style": "ember",
    },
    {
        "id": "pumpkin",
        "bank": 2,
        "name": "PUMPKIN",
        "bpm": 142,
        "song": "01023201324536450123",
        "stars": 4,
        "target": "B",
        "style": "ember",
        "holds": [
            [0, 0, 0, 4], [4, 8, 3, 4],
            [12, 0, 1, 4], [16, 12, 2, 4],
        ],
    },
    {
        "id": "cider",
        "bank": 3,
        "name": "CIDER",
        "bpm": 150,
        "song": "0321476523.776510321",
        "stars": 5,
        "target": "B",
        "style": "ember",
    },
    {
        "id": "amber",
        "bank": 4,
        "name": "AMBER",
        "bpm": 158,
        "song": "0121233454..67712367",
        "stars": 5,
        "target": "B",
        "style": "ember",
        "holds": [
            [0, 0, 0, 4], [0, 8, 3, 4],
            [8, 4, 1, 5], [12, 12, 2, 4],
            [16, 0, 0, 6], [16, 8, 3, 4],
            # quad hold: grab all 4 lanes through the rest bars (~3s)
            [10, 0, 0, 32], [10, 0, 1, 32],
            [10, 0, 2, 32], [10, 0, 3, 32],
        ],
    },
    {
        "id": "leafy",
        "bank": 4,
        "bank_map": [4] * 10 + [0] * 6 + [4] * 4,
        "name": "LEAFY",
        "bpm": 166,
        "song": "01234567760505050112",
        "stars": 5,
        "target": "A",
        "style": "ember",
        "holds": [
            # epic: one lane-3 hold across the whole bank-0 stretch (~8.7s)
            [10, 0, 3, 96],
        ],
    },
]

INTRO_BARS = 2
OUTRO_BARS = 2

BANKS = [
    [
        "0.......2.......",
        "1.......3.......",
        "0...1...2...3...",
        "3...2...1...0...",
        "0...0...3...3...",
        "1...2...1...2...",
        "0...2...1...3...",
        "0.......3.......",
    ],
    [
        "0...1...2...3...",
        "3...2...1...0...",
        "0...2...0...2...",
        "0...1.2.3...2...",
        "3...2.1.0...1...",
        "0.2.1...3.1.2...",
        "1...1...2.3.2...",
        "0...3...0.3.0...",
    ],
    [
        "0...2...1...3...",
        "0..2..1...3.....",
        "0..2..1...3...1.",
        "3..1..2...0...2.",
        "0.1...2.3...1...",
        "3.2...1.0...2...",
        "0..3..0...3.2.1.",
        "0.......3..2..1.",
    ],
    [
        "0...2...1...3...",
        "0.2.1.3.0.2.1.3.",
        "3.1.2.0.3.1.2.0.",
        "0.2.0.2.1.3.1.3.",
        "0.1.2.3.2.1.0...",
        "3.2.1.0.1.2.3...",
        "0.2.1.3...3.1.2.",
        "0...3...0.2.1.3.",
    ],
    [
        "x...y...x...y...",
        "0.2.1.3.0.2.1.3.",
        "3.1.2.0.3.1.2.0.",
        "02..13..02..13..",
        "0.1.2.3.x...y...",
        "3.2.1.0.y...x...",
        "02..31..20..y...",
        "x.2.1.3.y.0.3.1.",
    ],
]

CHORDS = {"x": (0, 3), "y": (1, 2)}

# Musical identity per style. Gameplay charts are untouched by this -
# only the backing track (progression, bass groove, hats, drums) changes.
# classic: bright Am F C G, syncopated bass, 8th hats (world 1).
# dark: tense Em Fm Em Dm, pumping 8th bass, 16th hats, pickup kick (world 2).
# ember: warm C G F Dm, driving bass, 8th hats (world 3).
STYLES = {
    "classic": {
        "roots": (57, 53, 48, 55),
        "kick": (0, 4, 8, 12),
        "snare": (4, 12),
        "hat_every": 2,
        "hat_gain": 0.22,
        "bass": (0, 6, 10, 14),
        "bass_gain": 0.34,
    },
    "dark": {
        "roots": (52, 53, 52, 50),
        "kick": (0, 4, 8, 12, 14),
        "snare": (4, 12),
        "hat_every": 1,
        "hat_gain": 0.14,
        "bass": (0, 2, 4, 6, 8, 10, 12, 14),
        "bass_gain": 0.26,
    },
    "ember": {
        "roots": (48, 55, 53, 50),
        "kick": (0, 4, 8, 12),
        "snare": (4, 12),
        "hat_every": 2,
        "hat_gain": 0.20,
        "bass": (0, 4, 10, 14),
        "bass_gain": 0.30,
    },
}

def style_of(lv, song_bi=None):
    # endless morphs from classic into dark partway through.
    if (song_bi is not None and lv.get("style2_at") is not None
            and song_bi >= lv["style2_at"]):
        return STYLES.get(lv.get("style2", "dark"), STYLES["dark"])
    return STYLES.get(lv.get("style", "classic"), STYLES["classic"])

def lanes_of(c):
    if c in CHORDS:
        return CHORDS[c]
    if c.isdigit():
        return (int(c),)
    return ()

def level(i):
    return LEVELS[max(0, min(len(LEVELS) - 1, i))]

def count():
    return len(LEVELS)

def main_bars(lv):
    return len(lv["song"])

def bars(lv):
    return INTRO_BARS + main_bars(lv) + OUTRO_BARS

def pattern(lv, i):
    c = lv["song"][i]
    if c == ".":
        return "." * 16
    # endless / mixed-bank levels can specify a bank per song-bar.
    bank_map = lv.get("bank_map")
    bank = bank_map[i] if bank_map else lv["bank"]
    return BANKS[bank][int(c)]

def star_string(n):
    n = max(1, min(5, int(n)))
    return "*" * n + "-" * (5 - n)


WORLD_SIZE = 5


def world_count():
    return max(1, -(-len(LEVELS) // WORLD_SIZE))


def world_of(i):
    return max(0, min(world_count() - 1, int(i) // WORLD_SIZE))


def world_range(w):
    w = max(0, min(world_count() - 1, int(w)))
    return range(w * WORLD_SIZE, min(len(LEVELS), (w + 1) * WORLD_SIZE))


# Endless: infinite escalating stages. Each stage is short (a few dozen
# bars), gets faster, and uses a fresh random seed every run.
ENDLESS_BPM = 120
ENDLESS_BPM_STEP = 10
ENDLESS_BPM_CAP = 200
ENDLESS_BARS = 24
ENDLESS_ID = "endless"


def endless_level(style=None, stage=1, seed=None):
    # style=None keeps the legacy classic-into-dark morph (single run).
    # Otherwise the whole stage is one style so endless can match the
    # selected world. id stays "endless" so progress keys are unaffected.
    import random
    rng = random.Random(1337 if seed is None else seed)
    bpm = min(ENDLESS_BPM + (stage - 1) * ENDLESS_BPM_STEP, ENDLESS_BPM_CAP)
    if stage <= 1:
        pool = [0, 1, 1, 0]
    elif stage == 2:
        pool = [1, 2, 1, 2]
    elif stage == 3:
        pool = [2, 3, 2, 3]
    elif stage == 4:
        pool = [3, 3, 4, 2]
    else:
        pool = [3, 4, 4, 3, 4]
    rest_p = max(0.0, 0.06 - 0.015 * (stage - 1))
    song_chars = []
    bank_map = []
    for bi in range(ENDLESS_BARS):
        bank_map.append(rng.choice(pool))
        # early breather rests, none once it gets hard
        if bi >= 8 and rng.random() < rest_p:
            song_chars.append(".")
        else:
            song_chars.append(str(rng.randrange(8)))
    holds = []
    for bi in range(4, ENDLESS_BARS, 8):
        lane = rng.randrange(4)
        step = rng.choice([0, 4, 8, 12])
        holds.append([bi, step, lane, rng.choice([3, 4, 4, 5])])
    if stage >= 4:
        # extra off-beat hold once it gets spicy
        holds.append([12, rng.choice([2, 6, 10, 14]),
                      rng.randrange(4), rng.choice([3, 4])])
    lv = {
        "id": ENDLESS_ID,
        "bank": 3,
        "bank_map": bank_map,
        "name": "ENDLESS",
        "bpm": bpm,
        "song": "".join(song_chars),
        "stars": 5,
        "target": None,
        "holds": holds,
        "endless": True,
        "style": "classic",
        "seed": 1337 if seed is None else seed,
        "stage": stage,
    }
    if style is None:
        lv["style2"] = "dark"
        lv["style2_at"] = 60
    else:
        lv["style"] = style
    return lv
