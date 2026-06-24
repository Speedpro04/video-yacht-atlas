# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

SS = 3                      # supersampling
W, H = 550 * SS, 350 * SS

# Paleta nautica
NAVY_TOP = (13, 39, 71)     # #0D2747
NAVY_BOT = (7, 24, 46)      # #07182E
GOLD     = (212, 175, 55)   # #D4AF37
WHITE    = (245, 248, 252)
LBLUE    = (138, 178, 209)  # azul claro

def font(path_list, size):
    for p in path_list:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()

BOLD = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
SEMI = ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
REG  = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]

img = Image.new("RGB", (W, H), NAVY_BOT)
d = ImageDraw.Draw(img)

# fundo em gradiente vertical
for y in range(H):
    t = y / H
    c = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# borda dourada dupla (cantos arredondados)
m = 12 * SS
d.rounded_rectangle([m, m, W - m, H - m], radius=4 * SS, outline=GOLD, width=2 * SS)
m2 = 18 * SS
d.rounded_rectangle([m2, m2, W - m2, H - m2], radius=3 * SS, outline=(GOLD[0]//2+30, GOLD[1]//2+30, GOLD[2]//3), width=1 * SS)

def ctext(y, text, fnt, fill, tracking=0):
    # texto centralizado horizontalmente, com tracking opcional
    if tracking:
        widths = [d.textlength(ch, font=fnt) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (W - total) / 2
        for ch, wch in zip(text, widths):
            d.text((x, y), ch, font=fnt, fill=fill, anchor="lm")
            x += wch + tracking
    else:
        d.text((W / 2, y), text, font=fnt, fill=fill, anchor="mm")

# Rotulo topo
ctext(52 * SS, "CONDIÇÃO ESPECIAL · MARINA FUNDADORA",
      font(SEMI, 17 * SS), GOLD, tracking=2 * SS)

# Hero: $200 /mês
hero = font(BOLD, 92 * SS)
small = font(SEMI, 30 * SS)
s1, s2 = "$200", " /mês"
w1 = d.textlength(s1, font=hero)
w2 = d.textlength(s2, font=small)
x0 = (W - (w1 + w2)) / 2
yh = 118 * SS
d.text((x0, yh), s1, font=hero, fill=WHITE, anchor="lm")
d.text((x0 + w1, yh + 18 * SS), s2, font=small, fill=LBLUE, anchor="lm")

# Subtitulo
ctext(170 * SS, "entre na parceria agora", font(REG, 18 * SS), LBLUE)

# Divisor
d.line([(70 * SS, 196 * SS), (W - 70 * SS, 196 * SS)], fill=GOLD, width=1 * SS)

# Duas estatisticas
def stat(cx, big, l1, l2):
    d.text((cx, 238 * SS), big, font=font(BOLD, 46 * SS), fill=GOLD, anchor="mm")
    d.text((cx, 272 * SS), l1, font=font(SEMI, 16 * SS), fill=WHITE, anchor="mm")
    d.text((cx, 290 * SS), l2, font=font(REG, 15 * SS), fill=LBLUE, anchor="mm")

stat(W * 0.30, "100%", "da receita", "por dossiê")
stat(W * 0.70, "12", "vagas", "exclusivas")
# divisor vertical entre stats
d.line([(W/2, 220 * SS), (W/2, 300 * SS)], fill=(70, 95, 130), width=1 * SS)

# Rodape - site
ctext(326 * SS, "yachtsatlas.online", font(BOLD, 19 * SS), GOLD, tracking=1 * SS)

# downscale para 550x350 (antialias)
img = img.resize((550, 350), Image.LANCZOS).convert("RGBA")

# cantos arredondados com raio 5px (fora do raio = transparente)
mask = Image.new("L", (550, 350), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, 549, 349], radius=5, fill=255)
img.putalpha(mask)

img.save("card-oferta.png")
print("OK card-oferta.png", img.size)
