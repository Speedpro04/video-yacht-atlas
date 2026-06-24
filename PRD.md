# PRD — Vídeo de Venda Yachts Atlas (versão final v14)

> **Documento de requisitos do produto.** Descreve, de ponta a ponta, **qual é o vídeo exato** que está sendo entregue, de que partes ele é feito, como é montado e quais regras de marca/criativo ele obedece.

---

## 1. Resumo (o vídeo exato)

| Item | Valor |
|---|---|
| **Arquivo MASTER** | `yachts-atlas-v14.mp4` (178 MB, alta qualidade) |
| **Arquivo WEB (entrega)** | `yachts-atlas-v14-web.mp4` (84,7 MB) |
| **Resolução** | 1920 × 1080 (Full HD, 16:9 horizontal) |
| **Frame rate** | 30 fps |
| **Codec vídeo / áudio** | H.264 (libx264, CRF 21) / AAC 160 kbps |
| **Duração total** | ~143,7 s (≈ 2 min 24 s) |
| **Script de montagem** | [`montar_final.py`](montar_final.py) |
| **Gerado em** | 2026-06-24 |

O vídeo é um **anúncio de venda B2B** (oferta para marinas fundadoras) do produto **Yachts Atlas** — dossiê digital de custódia de documentação de iates. É um produto **high ticket**, então toda a direção é **premium/luxo**.

---

## 2. Marca — regra de ouro (forma dupla)

> Decisão final do usuário em 2026-06-24. **Imutável.**

- **ESCRITO** (logo, legenda, card, site, qualquer texto na tela) = **"Yachts Atlas"**
  - Site oficial: **`yachtsatlas.online`**
  - Nome oficial da marca (consta na camisa do apresentador).
- **FALADO** (narração/áudio) = **"Iate Atlas"**
  - Porque "iate" é palavra portuguesa e soa natural em pt-BR; "Yachts" trava a fala.

➡️ **A voz diz "Iate Atlas", a tela escreve "Yachts Atlas".** A legenda `.srt` já está corrigida para "Yachts Atlas" (ver linhas 8 e 25 do SRT).

---

## 3. Estrutura exata da timeline

O vídeo tem **3 blocos**: abertura → corpo (clipes) → fecho. Tudo costurado com `xfade` (crossfade de **0,6 s**) entre cada segmento.

```
[ ABERTURA 3,5s ]  →  [ 16 clipes de B-roll de iates ]  →  [ FECHO 6,0s ]
   logo + site            narração + legendas                 logo + site + CTA
```

### 3.1 Abertura (3,5 s)
- Imagem: **`fecho-yachts.png`** (logo "Yachts Atlas" + site `yachtsatlas.online`).
- `fade in` de 0,5 s.
- **3,0 s de silêncio** (LEAD) antes da narração começar — dá respiro cinematográfico e tempo de leitura do logo.

### 3.2 Corpo — 16 clipes de B-roll (em `videos/`)
Sequência exata definida em `montar_final.py` (lista `body`), cada clipe re-escalado para 1920×1080 (crop center) e com velocidade ajustada por `factor` para casar com a narração:

| # | Arquivo | trecho (início→dur. fonte) |
|---|---|---|
| 1 | `15905445_3840_2160_30fps.mp4` (A) | 0 → 5,2 s |
| 2 | `14987601_2160_3840_30fps.mp4` (B) | 0 → 13 s |
| 3 | `16207129_2560_1440_30fps.mp4` (C) | 0 → 8,5 s |
| 4 | `15128875_2160_3840_30fps.mp4` (D) | 0 → 9 s |
| 5 | `20620475-uhd_2160_3840_30fps.mp4` (E) | 0 → 15 s |
| 6 | `12258433_1920_1080_25fps.mp4` (F) | 0 → 5,4 s |
| 7 | B | 13 → 12,8 s |
| 8 | D | 9 → 9 s |
| 9 | A | 0 → 5,2 s |
| 10 | E | 0 → 7,5 s |
| 11 | C | 0 → 8,5 s |
| 12 | B | 0 → 12 s |
| 13 | D | 0 → 9 s |
| 14 | F | 0 → 5,4 s |
| 15 | E | 7,5 → 7,5 s |
| 16 | B | 13 → 12,8 s |

> O `factor` é calculado dinamicamente para que a soma dos clipes preencha exatamente a duração da narração + overlaps. Não é fixo — recalcula a cada montagem.

### 3.3 Fecho (6,0 s)
- Imagem: **`fecho-yachts.png`** (mesma da abertura — logo + site, CTA "Acesse nossa página oficial").
- `fade out` de 0,8 s no final.

---

## 4. Áudio

| Item | Valor |
|---|---|
| **Narração** | `yachts-v14-antonio.mp3` (voz "Antonio", ~140,7 s) |
| **Atraso** | `adelay` de 3,0 s (silêncio inicial = tempo do logo na abertura) |
| **Fala "Iate Atlas"** | ✅ (regra de marca) |

O roteiro completo da narração está em [`roteiro-v14.txt`](roteiro-v14.txt).

---

## 5. Legendas (queimadas no vídeo)

- Fonte: `yachts-v14-legenda.srt` (25 blocos, já com "Yachts Atlas" escrito).
- Queimadas via filtro `subtitles` do ffmpeg.
- **Estilo:** Arial, tamanho 16, **bold**, branco (`&H00FFFFFF`), contorno escuro `&H00301A10` (outline 2 + shadow 1), `MarginV=55`, centralizado (Alignment=2).

> ⚠️ Ponto de atenção de marca: o estilo atual usa **Arial bold**, que contradiz a diretriz de "tipografia elegante/serifada, não Arial bold genérico". Candidato a melhoria numa v15 se quiser refinar o acabamento premium.

---

## 6. Direção criativa (regras high ticket)

Conforme posicionamento premium do produto:

- **Paleta:** azul-marinho profundo + dourado + branco (consistente com card e camisa do apresentador).
- **Ritmo:** lento, cinematográfico; color grade premium nos clipes.
- **Copy:** tom confiante, escassez **real** (12 vagas), foco em valor de ativo — nunca "promoção barata".
- **Trilha:** discreta e elegante. *(Obs.: a montagem atual não inclui música de fundo — só narração. Avaliar adicionar trilha leve numa próxima versão.)*

---

## 7. Oferta comunicada no vídeo

- **Produto:** sistema de custódia/dossiê digital de iates (dados imutáveis na nuvem, verificáveis por QR Code).
- **Preço:** **US$ 200/mês** para as **12 primeiras marinas fundadoras**.
- **Bônus:** 18 meses de Dossiê Premium.
- **Indicação:** marina que indicar outra em 21 dias fica com 100% da receita de cada dossiê.
- **Distribuição:** 4 marinas SC + 4 SP + 4 RJ.
- **Urgência:** 7 dias para decidir.
- **CTA final:** "Acesse nossa página oficial — venha fazer parte da Yachts Atlas!" (`yachtsatlas.online`).

---

## 8. Assets do projeto

| Asset | Caminho |
|---|---|
| Vídeo master | `yachts-atlas-v14.mp4` |
| Vídeo web (entrega) | `yachts-atlas-v14-web.mp4` |
| Narração | `yachts-v14-antonio.mp3` |
| Legenda | `yachts-v14-legenda.srt` |
| Roteiro | `roteiro-v14.txt` |
| Abertura/Fecho | `fecho-yachts.png` |
| Card oferta | `card-oferta.png` |
| Logo | `logo-yachts-atlas.png` |
| Avatar/apresentador | `avatar.png` |
| B-roll | `videos/` (6 clipes de iates 4K/HD) |
| Script de montagem | `montar_final.py` |

---

## 9. Como reproduzir a montagem

```bash
cd C:\01-heygen-github
python montar_final.py     # gera yachts-atlas-v14.mp4
```

Requer `ffmpeg` e `ffprobe` no PATH. O script calcula a duração do áudio, ajusta a velocidade dos clipes, costura tudo com crossfade, queima a legenda e exporta em H.264/AAC.

---

*Última atualização: 2026-06-24.*
