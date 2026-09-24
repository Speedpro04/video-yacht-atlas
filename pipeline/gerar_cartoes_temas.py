# -*- coding: utf-8 -*-
"""
Cartoes de transicao do video de boas-vindas: um por tema, entre um bloco e
o seguinte.

Fundo #010c20 — o MESMO navy do fundo do app, e nao o gradiente dos cartoes de
abertura. E proposital: quando o cartao corta para a tela do sistema, o fundo
nao muda, so o conteudo aparece. Letras em #c5a059, o dourado do proprio
painel, pelo mesmo motivo.

    python pipeline/gerar_cartoes_temas.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "versoes" / "demonstracao-br" / "cartoes"

W, H = 1920, 1080
NAVY = (1, 12, 32)          # #010c20 — fundo do app
GOLD = (197, 160, 89)       # #c5a059 — dourado do app
BRANCO = (255, 255, 255)

TEMAS = [
    ("01", "PAINEL TÉCNICO", "Onde cada barco da sua Marina vive"),
    ("02", "PRÉ-DATA", "O que vem do píer, antes de virar registro"),
    ("03", "PORTAL DO PROPRIETÁRIO", "O que o dono do barco vê"),
    ("04", "DOSSIÊ ATLAS", "A vida do barco em um documento"),
]

SERIF = ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/timesbd.ttf"]
SANS = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
SANS_BOLD = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]


def fonte(caminhos, tamanho):
    for p in caminhos:
        try:
            return ImageFont.truetype(p, tamanho)
        except OSError:
            continue
    return ImageFont.load_default()


def espacado(d, texto, fnt, y, cor, tracking, largura=W):
    """Desenha centrado com espacamento entre letras.

    A identidade do Atlas usa maiuscula espacada; sem o tracking o titulo fica
    parecendo texto de sistema, nao marca.
    """
    larguras = [d.textlength(ch, font=fnt) for ch in texto]
    total = sum(larguras) + tracking * (len(texto) - 1)
    x = largura / 2 - total / 2
    for ch, w in zip(texto, larguras):
        d.text((x, y), ch, font=fnt, fill=cor, anchor="lm")
        x += w + tracking
    return total


def cartao(numero, titulo, subtitulo, destino):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Titulo grande; encolhe se nao couber com folga de 200px de cada lado.
    tam = 96
    while tam > 40:
        f = fonte(SANS_BOLD, tam)
        largura = sum(d.textlength(c, font=f) for c in titulo) + 14 * (len(titulo) - 1)
        if largura <= W - 620:
            break
        tam -= 4
    f_titulo = fonte(SANS_BOLD, tam)

    espacado(d, numero, fonte(SANS, 30), H / 2 - 150, GOLD, 10)
    espacado(d, titulo, f_titulo, H / 2 - 20, GOLD, 14)
    d.line([(W / 2 - 130, H / 2 + 55), (W / 2 + 130, H / 2 + 55)], fill=GOLD, width=2)
    espacado(d, subtitulo, fonte(SANS, 34), H / 2 + 125, (215, 222, 234), 2)

    img.save(destino)
    return destino


def capa(destino, com_site=False):
    """Abertura e fecho do filme — o mesmo navy dos cartoes de tema.

    O `abertura-yachts.png` da raiz usa gradiente; aqui o fundo e chapado
    porque este filme corta direto do cartao para a tela do sistema, e um
    gradiente faria o fundo "pular" na emenda.
    """
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # O nome NAO e escrito embaixo do logo: o proprio logo ja o traz gravado,
    # e ali ele se le "ATLAS YACHTS". As duas grafias na mesma tela, uma sob a
    # outra, foi o motivo de o Marcos escolher esta versao (22/09/2026).
    logo = Image.open(RAIZ / "logo-transparent.png").convert("RGBA")
    altura = 560
    logo = logo.resize((int(logo.width * altura / logo.height), altura), Image.LANCZOS)
    img.paste(logo, ((W - logo.width) // 2, 210), logo)

    d.line([(W / 2 - 200, 830), (W / 2 + 200, 830)], fill=GOLD, width=2)
    rodape = "yachtsatlas.online" if com_site else "Bem-vindo ao Programa Atlas"
    espacado(d, rodape, fonte(SANS, 38), 895, (215, 222, 234), 4)

    img.save(destino)
    return destino


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    print("OK", capa(SAIDA / "cartao-0-capa.png"))
    for i, (numero, titulo, sub) in enumerate(TEMAS, 1):
        destino = SAIDA / f"cartao-{i}.png"
        cartao(numero, titulo, sub, destino)
        print("OK", destino)
    print("OK", capa(SAIDA / "cartao-5-fecho.png", com_site=True))
