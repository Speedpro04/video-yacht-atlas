# -*- coding: utf-8 -*-
"""
Remonta o video do Atlas a partir dos clipes 4K originais.

Uso:  python pipeline/remontar.py <versao>
Ex.:  python pipeline/remontar.py oficial-br

Espera encontrar em versoes/<versao>/:
    audio.mp3     narracao final (ElevenLabs)
    legenda.ass   legenda ja alinhada (ver pipeline/README.md)

Por que remontar em vez de editar o mp4 pronto: a legenda dos videos do Atlas
e QUEIMADA nos pixels. Trocar so o audio deixa a pessoa lendo uma frase e
ouvindo outra, e nao existe jeito bonito de esconder -- borrao deixa fantasma,
tarja corta o quadro, degrade escurece um terco da tela, e cortar a faixa come
305 das 1080 linhas. Remontando, a imagem nasce limpa.
"""
import subprocess, sys, os

RAIZ   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPES = os.environ.get("ATLAS_CLIPES_4K", r"C:/01-heygen-github/videos/")
LOGO   = os.path.join(RAIZ, "fecho-yachts.png")

AB_DUR, FE_DUR, LEAD, OVERLAP = 3.5, 6.0, 3.0, 0.6   # iguais ao montar_final.py

def dur(f):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",f], capture_output=True, text=True)
    return float(r.stdout.strip())

def main(versao):
    pasta = os.path.join(RAIZ, "versoes", versao)
    audio = os.path.join(pasta, "audio.mp3")
    ass   = os.path.join(pasta, "legenda.ass")
    saida = os.path.join(pasta, "video.mp4")
    for f in (audio, ass, LOGO):
        if not os.path.exists(f): sys.exit(f"faltando: {f}")

    AUDIO_DUR = dur(audio); TOTAL = LEAD + AUDIO_DUR

    V = CLIPES
    A=V+"15905445_3840_2160_30fps.mp4"; B=V+"14987601_2160_3840_30fps.mp4"
    C=V+"16207129_2560_1440_30fps.mp4"; D=V+"15128875_2160_3840_30fps.mp4"
    E=V+"20620475-uhd_2160_3840_30fps.mp4"; F=V+"12258433_1920_1080_25fps.mp4"
    body=[(A,0,5.2),(B,0,13),(C,0,8.5),(D,0,9),(E,0,15),(F,0,5.4),
          (B,13,12.8),(D,9,9),(A,0,5.2),(E,0,7.5),(C,0,8.5),(B,0,12),
          (D,0,9),(F,0,5.4),(E,7.5,7.5),(B,13,12.8)]
    faltando=[f for f,_,_ in body if not os.path.exists(f)]
    if faltando: sys.exit("clipes 4K nao encontrados. Ajuste ATLAS_CLIPES_4K.\n"
                          + "\n".join(sorted(set(faltando))))

    body_raw=sum(s[2] for s in body); nseg=len(body)+2
    # o corpo estica ou encolhe para caber no audio desta versao
    factor=(TOTAL+OVERLAP*(nseg-1)-AB_DUR-FE_DUR)/body_raw
    print(f"[{versao}] audio={AUDIO_DUR:.1f}s  total={TOTAL:.1f}s  factor={factor:.4f}")

    inputs=["-loop","1","-t",str(AB_DUR+1),"-i",LOGO]
    for f,_,_ in body: inputs+=["-i",f]
    inputs+=["-loop","1","-t",str(FE_DUR+1),"-i",LOGO,"-i",audio]
    FE_IDX=len(body)+1; AUD_IDX=len(body)+2
    SC="scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"

    parts=[f"[0:v]{SC},trim=duration={AB_DUR},setpts=PTS-STARTPTS,fps=30,setsar=1,"
           f"fade=t=in:st=0:d=0.5,format=yuv420p[vab]"]
    labels=["vab"]; targets=[AB_DUR]
    for i,(f,ss,ln) in enumerate(body):
        parts.append(f"[{i+1}:v]trim=start={ss}:duration={ln},"
                     f"setpts={factor:.5f}*(PTS-STARTPTS),{SC},fps=30,setsar=1,"
                     f"format=yuv420p[v{i+1}]")
        labels.append(f"v{i+1}"); targets.append(ln*factor)
    parts.append(f"[{FE_IDX}:v]{SC},trim=duration={FE_DUR},setpts=PTS-STARTPTS,fps=30,"
                 f"setsar=1,fade=t=out:st={FE_DUR-0.8}:d=0.8,format=yuv420p[vfe]")
    labels.append("vfe"); targets.append(FE_DUR)

    chain=""; prev=labels[0]; acc=targets[0]
    for i in range(1,len(labels)):
        out=f"x{i}" if i<len(labels)-1 else "vmix"
        chain+=(f"[{prev}][{labels[i]}]xfade=transition=fade:duration={OVERLAP}:"
                f"offset={acc-OVERLAP:.3f}[{out}];")
        acc+=targets[i]-OVERLAP; prev=out
    print(f"[{versao}] timeline ~ {acc:.1f}s")

    ass_ff = ass.replace("\\","/").replace(":","\\:")   # ffmpeg engasga com C:
    chain+=f"[vmix]subtitles='{ass_ff}'[vout];"
    chain+=f"[{AUD_IDX}:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)}[aout]"

    cmd=["ffmpeg","-y"]+inputs+["-filter_complex",";".join(parts)+";"+chain,
         "-map","[vout]","-map","[aout]",
         "-c:v","libx264","-preset","slow","-crf","20",
         "-maxrate","3800k","-bufsize","7600k",
         "-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","192k",
         "-shortest","-movflags","+faststart",saida]
    print(f"[{versao}] rodando ffmpeg (16 clipes 4K, demora)...")
    r=subprocess.run(cmd)
    print(f"[{versao}] EXIT {r.returncode} -> {saida}")

if __name__=="__main__":
    if len(sys.argv)<2: sys.exit(__doc__)
    main(sys.argv[1])
