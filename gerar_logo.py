# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 1920 * SS, 1080 * SS

NAVY_TOP = (13, 39, 71)
NAVY_BOT = (6, 20, 38)
GOLD     = (212, 175, 55)
WHITE    = (245, 248, 252)
LBLUE    = (150, 185, 215)

def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()

BOLD = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
SEMI = ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeuib.ttf"]
SYM  = ["C:/Windows/Fonts/seguisym.ttf", "C:/Windows/Fonts/segoeui.ttf"]

img = Image.new("RGB", (W, H), NAVY_BOT)
d = ImageDraw.Draw(img)

# fundo radial-ish (gradiente vertical)
for y in range(H):
    t = y / H
    c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

cx = W / 2

def ctext(y, text, fnt, fill, track=0):
    if track:
        ws = [d.textlength(ch, font=fnt) for ch in text]
        total = sum(ws) + track * (len(text) - 1)
        x = cx - total / 2
        for ch, w in zip(text, ws):
            d.text((x, y), ch, font=fnt, fill=fill, anchor="lm")
            x += w + track
    else:
        d.text((cx, y), text, font=fnt, fill=fill, anchor="mm")

# Ancora (glifo)
anchor_fnt = font(SYM, 200 * SS)
d.text((cx, 360 * SS), "⚓", font=anchor_fnt, fill=GOLD, anchor="mm")

# Wordmark
ctext(560 * SS, "YACHTS ATLAS", font(BOLD, 112 * SS), WHITE, track=7 * SS)

# linha dourada
d.line([(cx - 330 * SS, 650 * SS), (cx + 330 * SS, 650 * SS)], fill=GOLD, width=2 * SS)

# tagline
ctext(710 * SS, "CUSTÓDIA INTELIGENTE DE ATIVOS DE ALTO VALOR",
      font(SEMI, 34 * SS), LBLUE, track=4 * SS)

# site
ctext(820 * SS, "yachtsatlas.online", font(BOLD, 48 * SS), GOLD, track=2 * SS)

img = img.resize((1920, 1080), Image.LANCZOS)
img.save("logo-yachts-atlas.png")
print("OK logo-yachts-atlas.png", img.size)
