from pathlib import Path
import threading
from .model import ContextModel

__version__='1.0.0'

class Translator:
    """Explicit source history; no hidden state shared between conversations."""
    def __init__(self,model_dir='weights',device='cpu'):
        self.model=ContextModel(Path(model_dir),device)
        self.lock=threading.RLock()

    def translate(self,texts,previous_sources=None,source_lang='eng_Latn'):
        single=isinstance(texts,str)
        texts=[texts] if single else texts
        if not isinstance(texts,list) or any(not isinstance(t,str) for t in texts):
            raise ValueError('metin veya metin listesi gerekiyor')
        if previous_sources is not None and (not isinstance(previous_sources,list) or any(not isinstance(t,str) for t in previous_sources)):
            raise ValueError('geçmiş kaynak metin listesi olmalı')
        history=list(previous_sources or [])[-3:]
        with self.lock:
            results=[]
            for start in range(0,len(texts),3):
                group=texts[start:start+3];histories=[]
                for text in group:
                    histories.append(history[-3:]);history.append(text)
                results.extend(self.model.infer(dict(texts=group,histories=histories,source=source_lang,target='tur_Latn')))
        return results[0] if single else results
