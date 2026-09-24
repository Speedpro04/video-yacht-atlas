# demonstracao-br — o vídeo de boas-vindas da Marina

**Quem assiste:** o dono da Marina **depois de pagar**. Ele já comprou; este
vídeo não vende nada — mostra o sistema por dentro e diz por onde começar.

**O que muda em relação aos outros dois vídeos do Atlas:**

| | Lançamento / Oficial | Este |
|---|---|---|
| Imagem | o Marcos em avatar + mar de banco de imagens | **só gravação de tela do sistema** |
| Papel | convencer | ensinar |
| Fecho | "vinte Marinas no Brasil inteiro" | "comece por um barco só" |

Os vídeos que já estão no ar (`oficial-br` e o do Lançamento) **não foram
tocados** para fazer este.

---

## Os arquivos

| Arquivo | O que é |
|---|---|
| `textos/` | um arquivo por bloco, na grafia da **pronúncia** ("Iate Atlas", "S-H-A 256") — é o que se cola no ElevenLabs |
| `audios/` | um mp3 por bloco, com o mesmo nome do texto |
| `fontes.tsv` | quais gravações de tela alimentam a versão |
| `trechos.tsv` | a decupagem: qual pedaço de qual gravação cobre qual frase |
| `cartoes/` | capa, os quatro cartões de tema e o fecho (gerados por código) |
| `video-boas-vindas.mp4` | o filme montado — fora do git, refaz-se em um comando |

**Narração:** 3:46 no total — abertura 20 s, Painel 47 s, Pré-Data 35 s, Portal
33 s, Dossiê 69 s, fecho 22 s. Com os seis cartões, o filme fecha em 4:09.

O bloco do Dossiê tem duas escritas: `4-dossie-atlas.txt`, do Marcos, e
`4-dossie-atlas-b.txt`, uma reescrita que integra a frase da nova fonte de
renda ao corpo do texto. O mp3 gravado tem 69 s e serve às duas.

**Se um dia for fazer legenda**, o `pipeline/alinhar.py` espera um `texto.txt`
único na pasta da versão. Ele não existe aqui de propósito: a fonte são os
arquivos de `textos/`, e um texto.txt solto viraria a segunda cópia que
envelhece. Monte-o na hora, concatenando os blocos na ordem.

## Como montar

```bash
python pipeline/gerar_cartoes_temas.py             # capa, 4 temas e fecho
python pipeline/montar_boas_vindas.py demonstracao-br
```

Bloco sem mp3 em `audios/` entra sem fala, com a duração natural dos trechos —
dá para montar com dois ou três prontos e completar depois.

## As gravações

Feitas em 22/09/2026 com a Xbox Game Bar, 1920x1040 a 60 fps, e guardadas fora
do git (550 MB) em `C:\Users\<você>\Videos\Captures`. Outra pasta: variável
`ATLAS_GRAVACOES`.

| Chave | Duração | Conteúdo |
|---|---|---|
| `painel` | 6:04 | painel da Marina, Cofre, Pré-Data, dossiê em PDF, QR de verificação |
| `portal` | 1:39 | Portal do Proprietário com o Fenix Blue populado e selo Gold |

**A moldura do Chrome é cortada na montagem** (88 linhas de abas e barra de
endereço) e o que sobra é centrado em 1080 sobre o navy do próprio app — as
bordas somem contra o fundo da página.

## Três coisas que a decupagem evita de propósito

- **A gravação do Portal de 1:28** (`…14-02-44.mp4`): é anterior aos registros —
  painel vazio — e mostra o código de acesso sendo digitado na tela.
- **Os 40 segundos de login do Portal**: e-mail e código não ensinam nada e
  expõem endereço de e-mail.
- **Os barcos "(TESTE)"**: aparecem em algumas telas do painel. Onde dá, a
  decupagem prefere o Fenix Blue, que tem nome limpo, foto e histórico.

## O que ainda falta gravar

A tela `/verificar` mostrando **o resultado verde** de um documento autêntico.
É a única frase do texto — *"a nossa página confirma que ele é mesmo
verdadeiro"* — sem imagem própria; hoje ela é coberta pelo QR impresso no PDF,
que é o convite à verificação, não a verificação acontecendo.
