# -*- coding: utf-8 -*-
import subprocess, os

OUT = "yachts-atlas-v14.mp4"
AUDIO = "yachts-v14-antonio.mp3"
SRT = "yachts-v14-legenda.srt"
ABERTURA = "fecho-yachts.png"   # mesma imagem (logo + site) na abertura e no fecho
FECHO = "fecho-yachts.png"
AB_DUR = 3.5
FE_DUR = 6.0
LEAD = 3.0          # silencio antes da narracao (= tempo de logo na abertura)
OVERLAP = 0.6

# duracao do audio v14
import json
def dur(f):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",f], capture_output=True, text=True)
    return float(r.stdout.strip())
AUDIO_DUR = dur(AUDIO)
TOTAL = LEAD + AUDIO_DUR
print("audio:", AUDIO_DUR, "total timeline:", TOTAL)

A="videos/15905445_3840_2160_30fps.mp4"; B="videos/14987601_2160_3840_30fps.mp4"
C="videos/16207129_2560_1440_30fps.mp4"; D="videos/15128875_2160_3840_30fps.mp4"
E="videos/20620475-uhd_2160_3840_30fps.mp4"; F="videos/12258433_1920_1080_25fps.mp4"

# corpo: (arquivo, inicio, duracao_fonte)
body = [
 (A,0,5.2),(B,0,13),(C,0,8.5),(D,0,9),(E,0,15),(F,0,5.4),
 (B,13,12.8),(D,9,9),(A,0,5.2),(E,0,7.5),(C,0,8.5),(B,0,12),
 (D,0,9),(F,0,5.4),(E,7.5,7.5),(B,13,12.8),
]
body_raw = sum(s[2] for s in body)
nseg = len(body) + 2            # + abertura + fecho
xfades = nseg - 1
sum_targets = TOTAL + OVERLAP*xfades
sum_body_targets = sum_targets - AB_DUR - FE_DUR
factor = sum_body_targets / body_raw
print(f"body_raw={body_raw:.1f} factor={factor:.4f} nseg={nseg}")

# inputs
inputs = ["-loop","1","-t",str(AB_DUR+1),"-i",ABERTURA]
for (f,ss,ln) in body:
    inputs += ["-i", f]
inputs += ["-loop","1","-t",str(FE_DUR+1),"-i",FECHO]
inputs += ["-i", AUDIO]
AB_IDX=0; FE_IDX=len(body)+1; AUD_IDX=len(body)+2

parts=[]
# abertura
parts.append(f"[{AB_IDX}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
             f"trim=duration={AB_DUR},setpts=PTS-STARTPTS,fps=30,setsar=1,"
             f"fade=t=in:st=0:d=0.5,format=yuv420p[vab]")
# corpo
labels=["vab"]
targets=[AB_DUR]
for i,(f,ss,ln) in enumerate(body):
    idx=i+1
    tgt=ln*factor
    parts.append(f"[{idx}:v]trim=start={ss}:duration={ln},setpts={factor:.5f}*(PTS-STARTPTS),"
                 f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                 f"fps=30,setsar=1,format=yuv420p[v{idx}]")
    labels.append(f"v{idx}"); targets.append(tgt)
# fecho
parts.append(f"[{FE_IDX}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
             f"trim=duration={FE_DUR},setpts=PTS-STARTPTS,fps=30,setsar=1,"
             f"fade=t=out:st={FE_DUR-0.8}:d=0.8,format=yuv420p[vfe]")
labels.append("vfe"); targets.append(FE_DUR)

# cadeia xfade
chain=""
prev=labels[0]; acc=targets[0]
for i in range(1,len(labels)):
    off=acc-OVERLAP
    out= f"x{i}" if i<len(labels)-1 else "vmix"
    chain+=f"[{prev}][{labels[i]}]xfade=transition=fade:duration={OVERLAP}:offset={off:.3f}[{out}];"
    acc=acc+targets[i]-OVERLAP
    prev=out
print(f"timeline final ~ {acc:.2f}s")

# legenda
style=("FontName=Arial,Fontsize=16,Bold=1,PrimaryColour=&H00FFFFFF,"
       "OutlineColour=&H00301A10,BorderStyle=1,Outline=2,Shadow=1,MarginV=55,Alignment=2")
chain+=f"[vmix]subtitles={SRT}:force_style='{style}'[vout];"
# audio com 3s de silencio na frente
chain+=f"[{AUD_IDX}:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)}[aout]"

fg=";".join(parts)+";"+chain
cmd=["ffmpeg","-y"]+inputs+["-filter_complex",fg,"-map","[vout]","-map","[aout]",
     "-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p","-r","30",
     "-c:a","aac","-b:a","160k","-shortest",OUT]
print("rodando ffmpeg...")
r=subprocess.run(cmd)
print("EXIT",r.returncode)
