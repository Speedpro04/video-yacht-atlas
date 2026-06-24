# Yachts Atlas — Vídeo institucional

Vídeo promocional da **Yachts Atlas** (custódia inteligente / dossiê digital de iates e parceria com marinas fundadoras).

## Marca
- **Escrito** (logo, legenda, card, site): **Yachts Atlas** — `yachtsatlas.online`
- **Falado** (narração): "Iate Atlas" — soa mais natural em português.

## Conteúdo
| Arquivo | Descrição |
|---|---|
| `yachts-atlas-v14-web.mp4` | Vídeo final (1080p): abertura na logo → clipes + narração + legenda → fecho na logo |
| `yachts-v14-antonio.mp3` | Narração (edge-tts, voz Antonio pt-BR, +3%) |
| `roteiro-v14.txt` | Roteiro do áudio (forma falada) |
| `LEGENDA-yachts-atlas.txt` | Texto da legenda (forma escrita, algarismos) |
| `yachts-v14-legenda.srt` | Legenda sincronizada (já deslocada para a abertura) |
| `card-oferta.png` | Card da oferta (550×350) |
| `logo-transparent.png` | Logo oficial Atlas Yachts (PNG transparente) |
| `abertura-yachts.png` / `fecho-yachts.png` | Cartões de abertura e fecho (logo + site sobre navy) |
| `avatar.png` | Foto do apresentador |
| `*.py` | Scripts de geração (cards, logo, legenda, montagem do vídeo) |

## Como remontar o vídeo
```
python transformar_srt.py     # gera a legenda escrita sincronizada
python montar_final.py        # monta o vídeo final (precisa dos clipes em videos/)
```

> Clipes brutos (`videos/`) e o master em alta (`yachts-atlas-v14.mp4`, 171 MB) não estão versionados por excederem o limite de tamanho do GitHub.
