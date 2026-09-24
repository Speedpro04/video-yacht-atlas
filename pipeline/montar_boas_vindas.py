# -*- coding: utf-8 -*-
"""
Monta o video de boas-vindas: capa, quatro temas com cartao antes de cada um,
e fecho.

    capa -> 01 Painel Tecnico -> 02 Pre-Data -> 03 Portal -> 04 Dossie -> fecho

Cada bloco e independente: tem o seu cartao, o seu texto, o seu mp3 e os seus
trechos de gravacao. O bloco dura EXATAMENTE o tempo da sua narracao — os
trechos sao esticados ou comprimidos para caber, bloco a bloco. E por isso que
regravar so um tema nao mexe nos outros.

Sem os mp3 em `audios/`, monta o corte bruto com as duracoes naturais.

    python pipeline/montar_boas_vindas.py demonstracao-br
"""
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
GRAVACOES = Path(os.environ.get(
    "ATLAS_GRAVACOES", Path.home() / "Videos" / "Captures"))

TOPO_CHROME = 88          # abas + barra de endereco numa janela de 1920x1040
FUNDO = "0x010c20"        # o navy do app — igual ao dos cartoes
CARTAO_DUR = 3.0          # quanto tempo o cartao fica na tela
RESPIRO = 0.4             # silencio depois do cartao, antes da fala

# (bloco, cartao, onde entra o cartao). O fecho e o unico com o cartao DEPOIS:
# o filme termina na marca, nao numa tela de sistema.
BLOCOS = [
    ("0-abertura", "cartao-0-capa.png", "antes"),
    ("1-painel-tecnico", "cartao-1.png", "antes"),
    ("2-pre-data", "cartao-2.png", "antes"),
    ("3-portal-do-proprietario", "cartao-3.png", "antes"),
    ("4-dossie-atlas", "cartao-4.png", "antes"),
    ("5-fecho", "cartao-5-fecho.png", "depois"),
]

# A pagina do dossie dentro do visualizador do Chrome. Medido nas gravacoes de
# 22/09/2026: a pagina e navy (1,11,31) sobre o cinza (39,39,39) do visualizador,
# sempre na mesma caixa. Recortada assim, ela flutua sobre o #010c20 do video
# sem moldura, sem barra de miniaturas e sem o cinza em volta.
PDF_CAIXA = (793, 897, 706, 143)   # largura, altura, x, y


def duracao(arquivo):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(arquivo)], capture_output=True, text=True)
    return float(r.stdout.strip())


def ler_tsv(caminho):
    linhas = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.strip() and not linha.lstrip().startswith("#"):
            linhas.append(linha.split("\t"))
    return linhas


def main(versao):
    pasta = RAIZ / "versoes" / versao
    fontes = {c[0]: GRAVACOES / c[1].strip() for c in ler_tsv(pasta / "fontes.tsv")}
    faltando = [str(a) for a in fontes.values() if not a.exists()]
    if faltando:
        print("gravacao nao encontrada:")
        for a in faltando:
            print("  ", a)
        return 1

    # trechos.tsv: bloco <TAB> fonte <TAB> inicio <TAB> duracao <TAB> corte <TAB> descricao
    por_bloco = {}
    for c in ler_tsv(pasta / "trechos.tsv"):
        corte = c[4].strip() if len(c) > 4 else "tela"
        por_bloco.setdefault(c[0], []).append((fontes[c[1]], float(c[2]), float(c[3]), corte))

    entradas, partes, pedacos = [], [], []
    trilha, n = [], 0
    tempo = 0.0

    for bloco, cartao, onde in BLOCOS:
        trechos = por_bloco.get(bloco, [])
        audio = pasta / "audios" / f"{bloco}.mp3"
        tem_audio = audio.exists()
        fala = duracao(audio) if tem_audio else 0.0

        # O CARTAO E SEMPRE SILENCIO. A fala do bloco so comeca quando a
        # imagem do sistema ja esta na tela: ler o titulo e ouvir a frase ao
        # mesmo tempo faz perder as duas coisas.
        def poe_cartao(n, dur=CARTAO_DUR):
            entradas.extend(["-loop", "1", "-t", str(dur + 1), "-i", str(pasta / "cartoes" / cartao)])
            partes.append(
                f"[{n}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                f"trim=duration={dur},setpts=PTS-STARTPTS,fps=30,setsar=1,"
                f"fade=t=in:st=0:d=0.4,fade=t=out:st={dur - 0.4}:d=0.4,format=yuv420p[p{n}]")
            pedacos.append(f"[p{n}]")
            return n + 1

        if onde == "antes":
            n = poe_cartao(n)
            tempo += CARTAO_DUR

        if not trechos:
            continue

        bruto = sum(t[2] for t in trechos)
        # Bloco sem mp3 ainda: usa a duracao natural dos trechos.
        alvo = (fala + RESPIRO) if tem_audio else bruto
        factor = alvo / bruto if bruto else 1.0

        if tem_audio:
            trilha.append((str(audio), tempo + RESPIRO))

        tela = (f"crop=1920:{1040 - TOPO_CHROME}:0:{TOPO_CHROME},"
                f"pad=1920:1080:0:{(1080 - (1040 - TOPO_CHROME)) // 2}:{FUNDO}")
        pw, ph, px, py = PDF_CAIXA
        pagina = (f"crop={pw}:{ph}:{px}:{py},scale=-1:1010,"
                  f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:{FUNDO}")

        for arq, ini, dur, corte in trechos:
            entradas += ["-i", str(arq)]
            partes.append(
                f"[{n}:v]trim=start={ini}:duration={dur},setpts={factor:.5f}*(PTS-STARTPTS),"
                f"{pagina if corte == 'pdf' else tela},fps=30,setsar=1,format=yuv420p[p{n}]")
            pedacos.append(f"[p{n}]")
            n += 1
        tempo += alvo

        if onde == "depois":
            n = poe_cartao(n, 5.0)
            tempo += 5.0

    cadeia = "".join(partes) and ";".join(partes)
    cadeia += ";" + "".join(pedacos) + f"concat=n={len(pedacos)}:v=1:a=0[vout]"

    mapa = ["-map", "[vout]"]
    saida = pasta / ("video-boas-vindas.mp4" if trilha else "corte-bruto.mp4")
    if trilha:
        # Cada narracao entra atrasada ate o ponto do seu bloco; o amix junta
        # tudo numa trilha so. Como os blocos nao se sobrepoem, nada se mistura.
        marcas = []
        for caminho, offset in trilha:
            entradas += ["-i", caminho]
            partes_audio = f"[{n}:a]adelay={int(offset * 1000)}|{int(offset * 1000)}[a{n}]"
            cadeia += ";" + partes_audio
            marcas.append(f"[a{n}]")
            n += 1
        cadeia += ";" + "".join(marcas) + f"amix=inputs={len(marcas)}:normalize=0[aout]"
        mapa += ["-map", "[aout]"]

    cmd = (["ffmpeg", "-y"] + entradas + ["-filter_complex", cadeia] + mapa +
           ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30"] +
           (["-c:a", "aac", "-b:a", "192k"] if trilha else ["-an"]) +
           ["-movflags", "+faststart", str(saida)])

    print(f"linha do tempo ~ {tempo:.0f}s  ({len(pedacos)} pedacos)")
    print("rodando ffmpeg...")
    codigo = subprocess.run(cmd, cwd=pasta).returncode
    print("EXIT", codigo, "->", saida if codigo == 0 else "")
    return codigo


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "demonstracao-br"))
