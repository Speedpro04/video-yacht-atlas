# -*- coding: utf-8 -*-
"""
texto.txt + palavras.json -> tempos.tsv.   python pipeline/alinhar.py <versao>

Alinhamento GLOBAL (SequenceMatcher), nao guloso: o guloso desanda quando erra
uma palavra e joga o fim do video 25s para tras. E nao tente alinhar por pausa
do silencedetect -- ja foi tentado duas vezes e errou 2-4s para um lado e 16s
para o outro, porque pausa grande nao cai so em fim de frase.
"""
import json, io, re, sys, os, unicodedata
from difflib import SequenceMatcher
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def norm(s):
    s=unicodedata.normalize('NFD',s.lower())
    s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]','',s)

def main(versao):
    p=os.path.join(RAIZ,"versoes",versao)
    tw=[w for w in json.load(open(os.path.join(p,"palavras.json"),encoding='utf-8'))
        if norm(w['w'])]
    B=[norm(w['w']) for w in tw]
    DUR=tw[-1]['e']
    linhas=[l.strip() for l in io.open(os.path.join(p,"texto.txt"),encoding='utf-8') if l.strip()]
    meus=[(i,norm(x)) for i,l in enumerate(linhas) for x in l.split() if norm(x)]
    A=[n for _,n in meus]

    mapa={}
    for bl in SequenceMatcher(None,A,B,autojunk=False).get_matching_blocks():
        for k in range(bl.size): mapa[bl.a+k]=bl.b+k
    print(f"[{versao}] {len(mapa)}/{len(A)} palavras ancoradas ({100*len(mapa)//len(A)}%)")
    idx=sorted(mapa)
    def t_de(i):
        if i in mapa: return tw[mapa[i]]['t'], tw[mapa[i]]['e']
        ant=[k for k in idx if k<i]; dep=[k for k in idx if k>i]
        if not ant: return (tw[mapa[dep[0]]]['t'],)*2
        if not dep: return (tw[mapa[ant[-1]]]['e'],)*2
        a,b=ant[-1],dep[0]; ta,tb=tw[mapa[a]]['e'],tw[mapa[b]]['t']
        v=ta+(tb-ta)*((i-a)/(b-a)); return v,v

    por={}
    for k,(li,_) in enumerate(meus): por.setdefault(li,[]).append(t_de(k))
    saida=[]; ult=0.0
    for i,l in enumerate(linhas):
        ts=por[i]; ini=max(min(t[0] for t in ts),ult); fim=max(max(t[1] for t in ts),ini+0.7)
        saida.append([ini,fim,l]); ult=fim
    for k in range(len(saida)-1): saida[k][1]=min(saida[k+1][0], saida[k][1]+0.30)
    saida[-1][1]=min(DUR, saida[-1][1]+0.4)
    io.open(os.path.join(p,"tempos.tsv"),'w',encoding='utf-8').write(
        '\n'.join(f'{a:.3f}\t{b:.3f}\t{l}' for a,b,l in saida))
    print(f"[{versao}] {len(saida)} legendas -> tempos.tsv")
if __name__=="__main__":
    if len(sys.argv)<2: sys.exit(__doc__)
    main(sys.argv[1])
