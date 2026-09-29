import math
import random
import wave
from array import array
from pathlib import Path

RATE = 22050


def _writable_dir(name):
    import os
    import sys
    if getattr(sys, "frozen", False):
        # onefile exe: bundle dir is wiped each launch, keep saves in AppData
        base = Path(os.environ.get("APPDATA", str(Path.home()))) / "yaBe"
        base.mkdir(parents=True, exist_ok=True)
        return base / name
    return Path(__file__).resolve().parent.parent / name


SYNTH_DIR = _writable_dir(".synth")
VERSION = 3

CHORDS = [
    (57, 60, 64),
    (53, 57, 60),
    (48, 52, 55),
    (55, 59, 62),
]

def mtof(m):
    return 440.0 * (2.0 ** ((m - 69) / 12.0))

def _env(n, attack, decay, curve=2.2):
    out = array("d", bytes(8 * n))
    a = max(1, int(attack * RATE))
    for i in range(n):
        if i < a:
            e = i / a
        else:
            t = (i - a) / RATE
            e = math.exp(-t / decay)
        out[i] = e
    for i in range(n):
        out[i] = out[i] ** curve if i >= a else out[i]
    return out

def kick():
    n = int(0.16 * RATE)
    out = array("d", bytes(8 * n))
    ph = 0.0
    for i in range(n):
        t = i / RATE
        f = 120.0 * math.exp(-t * 26) + 44.0
        ph += 2 * math.pi * f / RATE
        out[i] = math.sin(ph) * math.exp(-t * 16) * (1 - math.exp(-i * 0.5))
    return out

def snare():
    n = int(0.18 * RATE)
    out = array("d", bytes(8 * n))
    ph = 0.0
    for i in range(n):
        t = i / RATE
        ph += 2 * math.pi * 190.0 / RATE
        noise = random.uniform(-1, 1)
        out[i] = (noise * 0.7 + math.sin(ph) * 0.3) * math.exp(-t * 22)
    return out

def hat(open_=False):
    n = int((0.09 if open_ else 0.035) * RATE)
    out = array("d", bytes(8 * n))
    prev = 0.0
    for i in range(n):
        t = i / RATE
        noise = random.uniform(-1, 1)
        prev = prev * 0.35 + noise * 0.65
        out[i] = prev * math.exp(-t * (70 if not open_ else 22))
    return out

def bass(midi, dur=0.4):
    n = int(dur * RATE)
    f = mtof(midi)
    out = array("d", bytes(8 * n))
    ph = 0.0
    for i in range(n):
        t = i / RATE
        ph += 2 * math.pi * f / RATE
        sq = 1.0 if math.sin(ph) > 0 else -1.0
        saw = 2.0 * ((ph / (2 * math.pi)) % 1.0) - 1.0
        e = min(1.0, i / (0.006 * RATE)) * math.exp(-t * 3.4)
        out[i] = (sq * 0.45 + saw * 0.35) * e
    return out

def lead(midi, dur=0.2):
    n = int(dur * RATE)
    f = mtof(midi)
    out = array("d", bytes(8 * n))
    ph = 0.0
    for i in range(n):
        t = i / RATE
        ph += 2 * math.pi * f / RATE
        p = 0.25 if (ph / (2 * math.pi)) % 1.0 < 0.25 else -0.75
        e = min(1.0, i / (0.004 * RATE)) * math.exp(-t * 7.5)
        out[i] = p * e
    return out

def mix(buf, start, samples, gain=1.0):
    i = start
    n = len(buf)
    for s in samples:
        if i >= n:
            break
        buf[i] += s * gain
        i += 1

def render(lv, force=False):
    from game import chart

    out = SYNTH_DIR / f"{lv['id']}_{lv['bpm']:g}_v{VERSION}.wav"
    if out.exists() and not force:
        return out

    beat, bar, step = chart.timing(lv)
    random.seed(7)
    total = int(chart.length(lv) * RATE) + 2 * RATE
    buf = array("d", bytes(8 * total))

    drums = {"kick": kick(), "snare": snare()}
    hat_c, hat_o = hat(), hat(True)

    for t, kind, payload in chart.events(lv):
        start = int(t * RATE)
        if kind == "kick":
            mix(buf, start, drums["kick"], 0.85)
        elif kind == "snare":
            mix(buf, start, drums["snare"], 0.45)
        elif kind == "hat":
            mix(buf, start, hat_o if payload else hat_c, 0.22)
        elif kind == "bass":
            mix(buf, start, bass(payload, beat * 0.9), 0.34)
        elif kind == "lead":
            if isinstance(payload, (list, tuple)):
                midi, hold_dur = payload
            else:
                midi, hold_dur = payload, 0.0
            mix(buf, start, lead(midi, step * 1.7 + hold_dur), 0.24)

    pcm = array("h", bytes(2 * total))
    fade = int(0.6 * RATE)
    for i in range(total):
        v = math.tanh(buf[i] * 1.4)
        if i > total - fade:
            v *= (total - i) / fade
        pcm[i] = int(max(-1.0, min(1.0, v)) * 32000)

    SYNTH_DIR.mkdir(exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())
    return out

def tick():
    import pygame
    n = int(0.03 * RATE)
    pcm = array("h", bytes(2 * n))
    ph = 0.0
    for i in range(n):
        t = i / RATE
        ph += 2 * math.pi * 1800.0 / RATE
        pcm[i] = int(math.sin(ph) * math.exp(-t * 160) * 9000)
    return pygame.mixer.Sound(buffer=pcm.tobytes())

def ensure_mixer():
    import pygame
    try:
        pygame.mixer.init(frequency=RATE, size=-16, channels=1, buffer=512)
    except pygame.error:
        pygame.mixer.init()
