# -*- coding: utf-8 -*-
"""
tempos.tsv -> legenda.ass.   python pipeline/fazer_ass.py <versao>

BorderStyle=3 com Outline=9 desenha caixa opaca SO ATRAS DAS PALAVRAS -- nao e
tarja de ponta a ponta. Tarja foi tentada e reprovada: flutua no meio do quadro
e corta a imagem ao meio.

LEAD=3.0 desloca tudo, porque remontar.py poe 3s de logo antes da narracao.
"""
import io, sys, os
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_SEG=6.0        # legenda mais longa que isso vira duas
LEAD=3.0

CAB = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Atlas,Arial,44,&H00FFFFFF,&H00FFFFFF,&H1F1F0C01,&H00000000,0,0,0,0,100,100,0,0,3,9,0,2,260,260,80,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

def ts(t):
    return f'{int(t//3600):d}:{int(t%3600//60):02d}:{t%60:05.2f}'

def main(versao):
    p=os.path.join(RAIZ,"versoes",versao)
    linhas=[]
    for l in io.open(os.path.join(p,"tempos.tsv"),encoding='utf-8'):
        a,b,t=l.rstrip('\n').split('\t'); linhas.append([float(a),float(b),t])
    out=[]
    for a,b,t in linhas:
        if b-a<=MAX_SEG or len(t.split())<4: out.append([a,b,t]); continue
        pal=t.split(); meio=len(t)//2; melhor,dist,acc=None,9e9,0
        for i,w in enumerate(pal[:-1]):
            acc+=len(w)+1
            if abs(acc-meio)<dist: dist,melhor=abs(acc-meio),i+1
        t1=' '.join(pal[:melhor]); t2=' '.join(pal[melhor:])
        corte=a+(b-a)*len(t1)/(len(t1)+len(t2))
        out += [[a,corte,t1],[corte,b,t2]]
    ev=[f'Dialogue: 0,{ts(a+LEAD)},{ts(b+LEAD)},Atlas,,0,0,0,,{t}' for a,b,t in out]
    io.open(os.path.join(p,"legenda.ass"),'w',encoding='utf-8').write(CAB+'\n'.join(ev)+'\n')
    print(f"[{versao}] {len(linhas)} -> {len(out)} legendas | mais longa {max(b-a for a,b,_ in out):.1f}s")
if __name__=="__main__":
    if len(sys.argv)<2: sys.exit(__doc__)
    main(sys.argv[1])
