import re
import zlib

class PdfObject:
    def _read_block(self, f, block_size=128):
        b = f.read(block_size)
        while b:
            yield b
            b = f.read(block_size)
        return None

    def getObjectDecoded(self):
        return self._obj

    def _bytes2str(self, b):
        try:
            return b.decode('utf-8')
        except UnicodeDecodeError as ex:
            return b.decode('utf-8', errors='replace')

    _RE_OBJ_END = re.compile(r'\r?\nendobj\r?\n', flags=re.MULTILINE | re.DOTALL)
    _obj = ''
    def __init__(self, p = None, offset = 0):
        if not p:
            return
        with p.open(mode='rb') as f:
            f.seek(offset)
            for blk in self._read_block(f):
                assert blk, 'not found endobj'
                #self._obj += blk.decode('utf-8', errors='ignore')
                self._obj += self._bytes2str(blk)
                m = self._RE_OBJ_END.search(self._obj)
                if m:
                    self._obj = self._obj[:m.end()]
                    break

    _END_OBJ_BYTES = b'endobj'
    def readBytes(self, p, offset):
        b = b''
        with p.open(mode='rb') as f:
            f.seek(offset)
            for blk in self._read_block(f):
                assert blk, 'not found endobj'
                b += blk
                idx = b.find(self._END_OBJ_BYTES)
                if idx > -1:
                    b = b[:idx+len(self._END_OBJ_BYTES)]
                    break
        #print(b)
        return b

class Decompresses:
    _STREAM_START_BYTES = b'stream\r\n'
    _STREAM_END_BYTES = b'\nendstream'
    def stream(self, content):
        #print(content)
        s = content.find(self._STREAM_START_BYTES) + len(self._STREAM_START_BYTES)
        #print(s)
        #print(content.find(self._STREAM_END_BYTES) - s)
        zs = content[s:content.find(self._STREAM_END_BYTES)]
        #print(zs)
        #print(zlib.decompress(zs))
        return zlib.decompress(zs)

if __name__ == '__main__':
    from pathlib import Path

    p = Path('../../pdfrw01/sample001_pdf.pdf')
    obj = PdfObject(p, 11592)
    print(obj.getObjectDecoded())
#[EOF]