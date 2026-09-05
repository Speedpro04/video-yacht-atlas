## O vídeo virou pipeline, não arquivo — 05/09/2026

Decisão do fundador: *"pegue todo código do vídeo, áudio, legenda, o visual, tudo
e salve no repositório video atlas, pq temos outras páginas para trabalharmos
depois, LATAM, US e EU"*. Concordo, e por um motivo mais forte que economizar
trabalho: **o que existe agora não é um vídeo, é uma máquina de fazer vídeo**. O
`remontar.py` recebe um áudio e devolve o filme montado; para as outras versões
muda só a narração e o texto da legenda.

Havia urgência real nisso: os scripts estavam numa pasta de `Downloads`. Uma
limpeza e sumiriam.

### O que entrou

```
pipeline/     transcrever.py -> alinhar.py -> fazer_ass.py -> remontar.py
versoes/
  oficial-br/ audio.mp3, texto.txt, legenda.ass, palavras.json, tempos.tsv, poster.jpg
```

Quatro comandos produzem uma versão inteira. Versão nova é uma pasta com
`audio.mp3` e `texto.txt`.

### O que NÃO entrou, e por quê

Os **clipes 4K** (~395 MB) continuam fora — o `.gitignore` já excluía `videos/`.
Eles vivem em `C:\01-heygen-github\videos\` e o `remontar.py` aceita
`ATLAS_CLIPES_4K` para achá-los em outro lugar; se faltarem, ele **diz quais**
em vez de falhar no meio do ffmpeg. O **mp4 renderizado** também fica fora
(`versoes/*/video.mp4` no `.gitignore`): ele se refaz a qualquer momento, e
guardar 75 MB por versão em histórico de git é dívida que não se paga.

### As armadilhas ficaram escritas, não só resolvidas

Duas custaram caro e estão no `pipeline/README.md` para não voltarem:

**Legenda não se alinha por pausa.** Tentado duas vezes com `silencedetect`:
distribuir caracteres pelo tempo de fala errou **2 a 4 segundos**; ancorar nas
maiores pausas errou **16 segundos**, porque pausa grande não cai só em fim de
frase. Só transcrição com tempo por palavra resolve.

**Alinhamento guloso desanda.** Ao errar uma palavra ele não se recupera e joga
a última fala **25 segundos** para trás. O `alinhar.py` usa `SequenceMatcher`
global, e registra a taxa de ancoragem (96% no `oficial-br`).

E a razão de tudo isso existir: **a legenda dos vídeos do Atlas é queimada nos
pixels**. Editar o mp4 pronto é impossível sem estragar — borrão deixa fantasma,
tarja corta o quadro, degradê escurece um terço da tela, corte come 305 das 1080
linhas. As quatro foram tentadas e reprovadas no mesmo dia. Remontando da fonte,
o problema não existe.

---
