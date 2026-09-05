# Pipeline do vídeo Atlas

Uma máquina que recebe **uma narração** e devolve **o filme montado**. Para
LATAM, US e EU muda só o áudio e o texto — a sequência dos 16 trechos, a
abertura, o fecho e o cálculo de tempo são os mesmos.

## Por que remontar, e nunca editar o mp4 pronto

A legenda dos vídeos do Atlas é **queimada nos pixels**. Trocar só o áudio de um
vídeo já renderizado deixa a pessoa **lendo uma frase e ouvindo outra**, e não
existe jeito bonito de esconder o texto velho. Foi tentado, em 05/09/2026, e
reprovado nas quatro tentativas:

| Tentativa | Resultado |
|---|---|
| Borrão sobre a faixa | o fantasma do texto continua legível |
| Tarja opaca | flutua no meio do quadro e corta a imagem ao meio |
| Degradê até a borda | escurece um terço da tela |
| Cortar a faixa fora | come 305 das 1080 linhas |

Remontando dos clipes originais, **a imagem nasce limpa** — nunca houve legenda
para esconder.

## Os quatro passos

```bash
python pipeline/transcrever.py oficial-br      # audio.mp3  -> palavras.json
python pipeline/alinhar.py     oficial-br      # + texto.txt -> tempos.tsv
python pipeline/fazer_ass.py   oficial-br      #             -> legenda.ass
python pipeline/remontar.py    oficial-br      #             -> video.mp4
```

Para uma versão nova (LATAM, US, EU): crie `versoes/<nome>/` com **audio.mp3** e
**texto.txt**, e rode os quatro. O `transcrever.py` aceita o idioma como segundo
argumento (`es`, `en`).

## Onde ficam os clipes 4K

Fora do git — são ~395 MB e o `.gitignore` exclui `videos/`. Eles vivem em:

```
C:\01-heygen-github\videos\
```

Se estiverem em outro lugar, aponte com a variável `ATLAS_CLIPES_4K`. O
`remontar.py` avisa quais faltam em vez de falhar no meio.

## Duas armadilhas já pagas

**Não alinhe legenda por pausa.** Foi tentado duas vezes com `silencedetect`:
distribuir caracteres pelo tempo de fala errou **2 a 4 segundos**, e ancorar nas
maiores pausas errou **16 segundos** — pausa grande não cai só em fim de frase.
Só transcrição com tempo por palavra (`faster-whisper`) resolve.

**Não use alinhamento guloso.** Ele desanda quando erra uma palavra e joga a
última fala 25s para trás. O `alinhar.py` usa `SequenceMatcher` global.

## A grafia diverge de propósito

O áudio fala **"Iate Atlas"** e **"S-H-A 256"**; a legenda escreve
**Yachts Atlas** e **SHA-256**. O ouvido aprende a pronúncia, o olho aprende a
grafia. Escreva o `texto.txt` na grafia correta — ele vira legenda. A pronúncia
é problema do ElevenLabs, não deste arquivo.
