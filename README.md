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


## As versões

Cada versão é uma pasta em `versoes/` com o que a define — texto, áudio, legenda
e decupagem. A montagem é a mesma máquina para todas; muda só o conteúdo.

| Versão | O que é | Duração |
|---|---|---|
| `oficial-br` | vídeo da home de `yachtsatlas.online` — o Marcos em avatar, b-roll de mar | 3:01 |
| `demonstracao-br` | **boas-vindas da Marina, depois da compra** — só gravação de tela, quatro blocos com cartão entre eles | 4:09 |

O `demonstracao-br` tem pipeline próprio: `pipeline/montar_boas_vindas.py`, que
monta capa → 01 Painel Técnico → 02 Pré-Data → 03 Portal → 04 Dossiê → fecho,
com o cartão em silêncio antes de cada bloco e o corpo esticado para casar com a
narração daquele bloco. Os cartões saem de `pipeline/gerar_cartoes_temas.py`
(fundo `#010c20`, letras `#c5a059`). O vídeo servido ao cliente fica no Supabase,
assinado — ver o PRD do repositório YACHTS-ATLAS-OFICIAL.

## Como remontar o vídeo
```
python transformar_srt.py     # gera a legenda escrita sincronizada
python montar_final.py        # monta o vídeo final (precisa dos clipes em videos/)
```

> Clipes brutos (`videos/`) e o master em alta (`yachts-atlas-v14.mp4`, 171 MB) não estão versionados por excederem o limite de tamanho do GitHub.
