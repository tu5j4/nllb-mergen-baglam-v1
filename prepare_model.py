"""Fetch pinned release artifacts and restore exact model bytes, without ML packages."""
import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path
import shutil
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parent
URL='https://github.com/tu5j4/nllb-mergen-baglam-v1/releases/download/v1.0.0/'

def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def owned(root,name):
    if Path(name).is_absolute():raise ValueError('geçersiz dosya yolu')
    path=(root/name).resolve()
    if not path.is_relative_to(root):raise ValueError('dosya yolu model klasörü dışında')
    return path

def valid(path,row):
    return path.is_file() and path.stat().st_size==row['bytes'] and digest(path)==row['sha256']

def download(root,row):
    target=owned(root,row['name']);target.parent.mkdir(parents=True,exist_ok=True)
    if valid(target,row):return target
    temp=target.with_name(target.name+'.part')
    try:
        request=urllib.request.Request(URL+row['name'],headers={'User-Agent':'nllb-mergen-baglam-v1'})
        with urllib.request.urlopen(request,timeout=60) as response,temp.open('wb') as stream:
            size=0
            while block:=response.read(1024*1024):
                size+=len(block)
                if size>row['bytes']:raise ValueError('indirme beklenenden büyük')
                stream.write(block)
        if not valid(temp,row):raise ValueError('indirilen model dosyası doğrulanamadı')
        os.replace(temp,target)
        return target
    finally:temp.unlink(missing_ok=True)

def prepare(output):
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/'model-files.json').read_text(encoding='utf-8'))
    if all(valid(owned(output,row['path']),row) for row in manifest['files']):return
    artifacts=json.loads((ROOT/'release-assets.json').read_text(encoding='utf-8'))
    cache=output/'.downloads';cache.mkdir(exist_ok=True)
    support=download(cache,artifacts['support'])
    rows={r['path']:r for r in manifest['files']}
    with zipfile.ZipFile(support) as archive:
        for info in archive.infolist():
            if info.filename not in rows or info.file_size!=rows[info.filename]['bytes']:
                raise ValueError('destek paketinde beklenmeyen dosya')
            target=owned(output,info.filename);target.parent.mkdir(parents=True,exist_ok=True)
            temp=target.with_name(target.name+'.part')
            try:
                with archive.open(info) as source,temp.open('wb') as dest:shutil.copyfileobj(source,dest)
                if not valid(temp,rows[info.filename]):raise ValueError('destek dosyası doğrulanamadı')
                os.replace(temp,target)
            finally:temp.unlink(missing_ok=True)
    for row in artifacts['weights']:
        target=owned(output,row['path'])
        if valid(target,row):continue
        packed=download(cache,dict(name=row['archive'],bytes=row['archive_bytes'],sha256=row['archive_sha256']))
        target.parent.mkdir(parents=True,exist_ok=True)
        temp=target.with_name(target.name+'.restore')
        try:
            with lzma.open(packed,'rb') as source,temp.open('wb') as dest:
                size=0
                while data:=source.read(row['chunk']):
                    size+=len(data)
                    if size>row['bytes']:raise ValueError('model dosyası beklenenden büyük')
                    out=bytearray(len(data));offset=0
                    for index in range(row['width']):
                        length=(len(data)+row['width']-1-index)//row['width']
                        out[index::row['width']]=data[offset:offset+length];offset+=length
                    dest.write(out)
            if not valid(temp,row):raise ValueError('ağırlık dosyası doğrulanamadı')
            os.replace(temp,target);packed.unlink()
        finally:temp.unlink(missing_ok=True)
    if not all(valid(owned(output,row['path']),row) for row in manifest['files']):
        raise ValueError('model dosyaları eksik veya bozuk')
    support.unlink(missing_ok=True)
    print('model hazır')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('weights'))
    prepare(p.parse_args().output)
