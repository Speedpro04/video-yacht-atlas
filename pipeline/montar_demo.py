# -*- coding: utf-8 -*-
"""
Monta uma versao feita de GRAVACAO DE TELA (nao dos clipes 4K).

Mesma ideia do remontar.py — abertura de logo, corpo, fecho de logo, e o corpo
esticado por um `factor` para casar com a narracao —, com duas diferencas que
vem do material:

1. Gravacao do Windows sai 1920x1040 COM a moldura do Chrome (abas, barra de
   endereco, botao de extensao). A moldura e cortada e o que sobra e centrado
   em 1920x1080 sobre o navy do proprio app, que some contra o fundo da tela.

2. A ordem dos trechos nao e uma lista no codigo: vive em `trechos.tsv` dentro
   da versao, porque quem decupa olhando o video quer editar uma linha, nao
   mexer em Python.

Sem `audio.mp3` na pasta da versao, monta o CORTE BRUTO com as duracoes da
decupagem — serve para aprovar a sequencia antes de gravar a narracao. Com
audio, estica o corpo para fechar no tempo da fala, como as outras versoes.
Se existir `legenda.ass`, ela e queimada no ultimo passo.

    python pipeline/montar_demo.py demonstracao-br
"""
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GRAVACOES = Path(os.environ.get(
    "ATLAS_GRAVACOES", Path.home() / "Videos" / "Captures"))

# Moldura do Chrome numa janela maximizada de 1920x1040: abas + barra de
# endereco ocupam as 88 primeiras linhas. O resto e pagina.
TOPO_CHROME = 88
FUNDO = "0x010c20"          # navy do app — as bordas somem contra a pagina
AB_DUR, FE_DUR, LEAD, OVERLAP = 3.0, 5.0, 3.0, 0.5


def duracao(arquivo: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(arquivo)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def ler_tsv(caminho: Path) -> list[list[str]]:
    linhas = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        linhas.append(linha.split("\t"))
    return linhas


def main(versao: str) -> int:
    pasta = RAIZ / "versoes" / versao
    if not pasta.is_dir():
        print(f"versao nao encontrada: {pasta}")
        return 1

    fontes = {c[0]: GRAVACOES / c[1].strip() for c in ler_tsv(pasta / "fontes.tsv")}
    faltando = [str(a) for a in fontes.values() if not a.exists()]
    if faltando:
        # Avisar QUAL falta, em vez de quebrar no meio do ffmpeg meia hora
        # depois — mesma decisao do remontar.py com os clipes 4K.
        print("gravacao nao encontrada:")
        for a in faltando:
            print("  ", a)
        print(f"\n(procurei em {GRAVACOES} — use ATLAS_GRAVACOES para mudar)")
        return 1

    trechos = [(fontes[c[0]], float(c[1]), float(c[2])) for c in ler_tsv(pasta / "trechos.tsv")]
    bruto = sum(t[2] for t in trechos)

    audio = pasta / "audio.mp3"
    legenda = pasta / "legenda.ass"
    tem_audio = audio.exists()

    nseg = len(trechos) + 2                      # + abertura + fecho
    if tem_audio:
        total = LEAD + duracao(audio)
        factor = (total + OVERLAP * (nseg - 1) - AB_DUR - FE_DUR) / bruto
        print(f"narracao={duracao(audio):.1f}s  alvo={total:.1f}s  factor={factor:.4f}")
    else:
        factor = 1.0
        print(f"sem audio.mp3 — corte bruto de {bruto:.0f}s de tela")

    logo = RAIZ / "fecho-yachts.png"
    entradas = ["-loop", "1", "-t", str(AB_DUR + 1), "-i", str(logo)]
    for arq, _ini, _dur in trechos:
        entradas += ["-i", str(arq)]
    entradas += ["-loop", "1", "-t", str(FE_DUR + 1), "-i", str(logo)]
    if tem_audio:
        entradas += ["-i", str(audio)]

    # Tela: tira a moldura, centra o que sobra em 1080 sobre o navy.
    tela = (f"crop=1920:{1040 - TOPO_CHROME}:0:{TOPO_CHROME},"
            f"pad=1920:1080:0:{(1080 - (1040 - TOPO_CHROME)) // 2}:{FUNDO}")
    cartao = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"

    partes = [f"[0:v]{cartao},trim=duration={AB_DUR},setpts=PTS-STARTPTS,fps=30,setsar=1,"
              f"fade=t=in:st=0:d=0.5,format=yuv420p[vab]"]
    rotulos, alvos = ["vab"], [AB_DUR]
    for i, (_arq, ini, dur) in enumerate(trechos):
        partes.append(
            f"[{i + 1}:v]trim=start={ini}:duration={dur},setpts={factor:.5f}*(PTS-STARTPTS),"
            f"{tela},fps=30,setsar=1,format=yuv420p[v{i + 1}]")
        rotulos.append(f"v{i + 1}")
        alvos.append(dur * factor)
    idx_fecho = len(trechos) + 1
    partes.append(
        f"[{idx_fecho}:v]{cartao},trim=duration={FE_DUR},setpts=PTS-STARTPTS,fps=30,setsar=1,"
        f"fade=t=out:st={FE_DUR - 0.8}:d=0.8,format=yuv420p[vfe]")
    rotulos.append("vfe")
    alvos.append(FE_DUR)

    cadeia, anterior, acumulado = "", rotulos[0], alvos[0]
    for i in range(1, len(rotulos)):
        saida = f"x{i}" if i < len(rotulos) - 1 else "vmix"
        cadeia += (f"[{anterior}][{rotulos[i]}]xfade=transition=fade:duration={OVERLAP}:"
                   f"offset={acumulado - OVERLAP:.3f}[{saida}];")
        acumulado += alvos[i] - OVERLAP
        anterior = saida
    print(f"linha do tempo ~ {acumulado:.1f}s")

    if legenda.exists():
        cadeia += f"[vmix]subtitles={legenda.name}[vout];"
    else:
        cadeia += "[vmix]null[vout];"

    saida = pasta / ("video.mp4" if tem_audio else "corte-bruto.mp4")
    mapa = ["-map", "[vout]"]
    if tem_audio:
        cadeia += f"[{len(trechos) + 2}:a]adelay={int(LEAD * 1000)}|{int(LEAD * 1000)}[aout]"
        mapa += ["-map", "[aout]"]
    else:
        cadeia = cadeia.rstrip(";")

    cmd = (["ffmpeg", "-y"] + entradas +
           ["-filter_complex", ";".join(partes) + ";" + cadeia] + mapa +
           ["-c:v", "libx264", "-preset", "medium", "-crf", "21",
            "-pix_fmt", "yuv420p", "-r", "30"] +
           (["-c:a", "aac", "-b:a", "192k", "-shortest"] if tem_audio else ["-an"]) +
           ["-movflags", "+faststart", str(saida)])

    print("rodando ffmpeg...")
    codigo = subprocess.run(cmd, cwd=pasta).returncode
    print("EXIT", codigo, "->", saida if codigo == 0 else "")
    return codigo


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "demonstracao-br"))
