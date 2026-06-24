# -*- coding: utf-8 -*-
import subprocess, sys, os

AUDIO = "yachts-v5-antonio.mp3"
SRT   = "yachts-v5-legendas.srt"
OUT   = "yachts-atlas-final.mp4"
MUSIC = "musica.mp3"
OVERLAP = 0.7
AUDIO_DUR = 79.488

A = "videos/15905445_3840_2160_30fps.mp4"   # 04 aerea marina 16:9
B = "videos/14987601_2160_3840_30fps.mp4"   # 02 marina vertical
C = "videos/16207129_2560_1440_30fps.mp4"   # 05 por do sol 16:9
D = "videos/15128875_2160_3840_30fps.mp4"   # 03 marina vertical
F = "videos/12258433_1920_1080_25fps.mp4"   # 01 jetski 16:9
E = "videos/20620475-uhd_2160_3840_30fps.mp4"  # 06 iate navegando vertical

# (arquivo, start, duracao_fonte) — ordem narrativa, termina no iate navegando
segs = [
    (A, 0.0,  5.20),   # abertura aerea
    (B, 0.0,  12.90),  # marina p1
    (C, 0.0,  8.45),   # por do sol
    (D, 0.0,  8.95),   # marina dubai p1
    (F, 0.0,  5.35),   # jetski
    (B, 12.90,12.85),  # marina p2
    (D, 9.0,  8.95),   # marina dubai p2
    (E, 0.0,  14.95),  # iate navegando (final)
]

src_sum = sum(s[2] for s in segs)
n = len(segs)
need = AUDIO_DUR + (n - 1) * OVERLAP
factor = need / src_sum
print(f"src_sum={src_sum:.2f} need={need:.2f} factor={factor:.4f}")

# inputs (videos na ordem dos segmentos) + audio
inputs = []
for (f, ss, ln) in segs:
    inputs += ["-i", f]
inputs += ["-i", AUDIO]
audio_idx = n  # indice do input de audio

# processa cada segmento
parts = []
for i, (f, ss, ln) in enumerate(segs):
    parts.append(
        f"[{i}:v]trim=start={ss}:duration={ln},setpts={factor:.5f}*(PTS-STARTPTS),"
        f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
        f"fps=30,setsar=1,format=yuv420p[v{i}]"
    )

# cadeia de xfade
target = [ln * factor for (_, _, ln) in segs]
chain = ""
prev = "v0"
acc = target[0]
for i in range(1, n):
    off = acc - OVERLAP
    out = f"x{i}" if i < n - 1 else "vx"
    chain += f"[{prev}][v{i}]xfade=transition=fade:duration={OVERLAP}:offset={off:.3f}[{out}];"
    acc = acc + target[i] - OVERLAP
    prev = out
print(f"duracao final estimada: {acc:.2f}s")

# legenda queimada
sub_style = ("FontName=Arial,Fontsize=15,Bold=1,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H00203040,BorderStyle=1,Outline=2,Shadow=1,"
             "MarginV=42,Alignment=2")
chain += f"[vx]subtitles={SRT}:force_style='{sub_style}'[vout];"

# audio: narracao (+ musica baixinha se existir)
if os.path.exists(MUSIC):
    inputs += ["-i", MUSIC]
    music_idx = audio_idx + 1
    chain += (f"[{audio_idx}:a]volume=1.0[narr];"
              f"[{music_idx}:a]volume=0.12,afade=t=out:st={AUDIO_DUR-3:.2f}:d=3[mus];"
              f"[narr][mus]amix=inputs=2:duration=first:dropout_transition=0[aout]")
    amap = "[aout]"
    print("COM musica")
else:
    amap = f"{audio_idx}:a"
    print("SEM musica")

filtergraph = ";".join(parts) + ";" + chain

cmd = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", filtergraph,
    "-map", "[vout]", "-map", amap,
    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-shortest", OUT
]

print("rodando ffmpeg...")
r = subprocess.run(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
print(r.stdout[-1500:])
print("EXIT", r.returncode)
