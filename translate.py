import argparse
from mergen_context import Translator

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--model-dir',default='weights')
    p.add_argument('--device',default='cpu')
    p.add_argument('--text',required=True)
    p.add_argument('--previous',action='append',default=[])
    a=p.parse_args()
    print(Translator(a.model_dir,a.device).translate(a.text,a.previous))
