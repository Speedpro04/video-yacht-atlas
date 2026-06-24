# -*- coding: utf-8 -*-
# Converte a SRT falada (números por extenso, "Iate Atlas")
# para a forma ESCRITA (algarismos, "Yachts Atlas") mantendo o tempo.
import re

SHIFT = 3.0  # segundos de abertura (logo) antes da narração

reps = [
    ("duzentos dólares", "$200"),
    ("trezentos dólares", "300 dólares"),
    ("cem por cento", "100%"),
    ("sessenta pés", "60 pés"),
    ("vinte e um dias", "21 dias"),
    ("dezoito meses", "18 meses"),
    ("doze vagas", "12 vagas"),
    ("doze marinas", "12 marinas"),
    ("sete dias", "7 dias"),
    ("quatro marinas", "4 marinas"),
    ("quatro do litoral", "4 do litoral"),
    ("Iate Atlas", "Yachts Atlas"),
]

def shift_ts(ts):
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    total = int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000 + SHIFT
    h2 = int(total // 3600); total -= h2*3600
    m2 = int(total // 60); total -= m2*60
    s2 = int(total); ms2 = int(round((total - s2)*1000))
    return f"{h2:02d}:{m2:02d}:{s2:02d},{ms2:03d}"

out = []
with open("yachts-v14-srt-cru.srt", encoding="utf-8") as f:
    for line in f:
        l = line.rstrip("\n")
        if "-->" in l:
            a, b = [x.strip() for x in l.split("-->")]
            out.append(f"{shift_ts(a)} --> {shift_ts(b)}")
        else:
            for a, b in reps:
                l = l.replace(a, b)
            out.append(l)

with open("yachts-v14-legenda.srt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("OK yachts-v14-legenda.srt (deslocada +%.1fs)" % SHIFT)
