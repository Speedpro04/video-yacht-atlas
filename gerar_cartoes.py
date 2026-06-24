# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
NAVY_TOP = (13, 39, 71)
NAVY_BOT = (6, 20, 38)
GOLD     = (212, 175, 55)

def navy_bg():
    img = Image.new("RGB", (W, H), NAVY_BOT)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img.convert("RGBA")

def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()
BOLD = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]

logo = Image.open("logo-transparent.png").convert("RGBA")

def scaled_logo(target_h):
    w, h = logo.size
    nw = int(w * target_h / h)
    return logo.resize((nw, target_h), Image.LANCZOS)

# ---------- ABERTURA: logo centralizada no navy ----------
ab = navy_bg()
L = scaled_logo(820)
ab.alpha_composite(L, ((W - L.width)//2, (H - L.height)//2 - 10))
ab.convert("RGB").save("abertura-yachts.png")
print("OK abertura-yachts.png")

# ---------- FECHO: logo + site (uniao das duas) ----------
fe = navy_bg()
L2 = scaled_logo(680)
fe.alpha_composite(L2, ((W - L2.width)//2, 150))
d = ImageDraw.Draw(fe)
# regra dourada + site
d.line([(W/2 - 300, 880), (W/2 + 300, 880)], fill=GOLD + (255,), width=2)
fnt = font(BOLD, 50)
txt = "yachtsatlas.online"
ws = [d.textlength(ch, font=fnt) for ch in txt]
total = sum(ws) + 2 * (len(txt) - 1)
x = W/2 - total/2
for ch, w in zip(txt, ws):
    d.text((x, 935), ch, font=fnt, fill=GOLD + (255,), anchor="lm")
    x += w + 2
fe.convert("RGB").save("fecho-yachts.png")
print("OK fecho-yachts.png")
