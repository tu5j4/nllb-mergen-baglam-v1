import hashlib
import io
import json
import lzma
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import prepare_model as loader

def digest(data):return hashlib.sha256(data).hexdigest()

class PrepareTests(unittest.TestCase):
    def fixture(self,root):
        data=b'abcdef0123456789xyz'
        chunk=8;width=4
        packed=b''
        for start in range(0,len(data),chunk):
            part=data[start:start+chunk]
            packed+=lzma.compress(b''.join(part[i::width] for i in range(width)))
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w') as archive:archive.writestr('base-bf16/config.json',b'{}')
        support=buffer.getvalue()
        files=[dict(path='base-bf16/config.json',bytes=2,sha256=digest(b'{}')),dict(path='base-bf16/model.safetensors',bytes=len(data),sha256=digest(data))]
        assets=dict(support=dict(name='support.zip',bytes=len(support),sha256=digest(support)),weights=[dict(files[1],archive='base.xz',archive_bytes=len(packed),archive_sha256=digest(packed),width=width,chunk=chunk)])
        (root/'model-files.json').write_text(json.dumps(dict(files=files)),encoding='utf-8')
        (root/'release-assets.json').write_text(json.dumps(assets),encoding='utf-8')
        return data,{'support.zip':support,'base.xz':packed}

    def test_download_restore_verify_and_idempotent_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);data,responses=self.fixture(root)
            with patch.object(loader,'ROOT',root),patch.object(loader,'URL','https://example.invalid/'),patch.object(loader.urllib.request,'urlopen',side_effect=lambda request,**_:io.BytesIO(responses[request.full_url.rsplit('/',1)[-1]])) as network:
                loader.prepare(root/'weights')
                self.assertEqual((root/'weights/base-bf16/model.safetensors').read_bytes(),data)
                self.assertEqual(network.call_count,2)
                loader.prepare(root/'weights')
                self.assertEqual(network.call_count,2)

    def test_corrupt_download_never_publishes_model(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);self.fixture(root)
            with patch.object(loader,'ROOT',root),patch.object(loader.urllib.request,'urlopen',return_value=io.BytesIO(b'corrupt')):
                with self.assertRaises(ValueError):loader.prepare(root/'weights')
            self.assertFalse((root/'weights/base-bf16/model.safetensors').exists())
            self.assertFalse(list((root/'weights').rglob('*.part')))

    def test_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):loader.owned(Path(folder).resolve(),'../outside')

if __name__=='__main__':unittest.main()
