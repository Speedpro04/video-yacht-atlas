# -*- coding: utf-8 -*-
"""audio.mp3 -> palavras.json (tempo por palavra).  python pipeline/transcrever.py <versao>"""
import sys, os, json
from faster_whisper import WhisperModel
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def main(versao, idioma="pt"):
    pasta=os.path.join(RAIZ,"versoes",versao)
    m=WhisperModel("small", device="cpu", compute_type="int8")
    segs,_=m.transcribe(os.path.join(pasta,"audio.mp3"), language=idioma,
                        word_timestamps=True, vad_filter=False)
    pal=[{"t":w.start,"e":w.end,"w":w.word.strip()} for s in segs for w in (s.words or [])]
    json.dump(pal, open(os.path.join(pasta,"palavras.json"),"w",encoding="utf-8"),
              ensure_ascii=False)
    print(f"[{versao}] {len(pal)} palavras | ultima em {pal[-1]['e']:.1f}s")
if __name__=="__main__":
    if len(sys.argv)<2: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else "pt")
