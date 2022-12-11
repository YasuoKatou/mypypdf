import re
import zlib
from pathlib import Path
from .mypdf_exception import PDFPathException

class Decompresses:
    _STREAM_START_BYTES1 = b'stream\r\n'
    _STREAM_START_BYTES2 = b'stream\n'
    _STREAM_END_BYTES = b'\nendstream'
    def stream(self, content):
        #print(content)
        s1 = content.find(self._STREAM_START_BYTES1)
        if s1 != -1:
            s = s1 + len(self._STREAM_START_BYTES1)
        else:
            s1 = content.find(self._STREAM_START_BYTES2)
            if s1 != -1:
                s = s1 + len(self._STREAM_START_BYTES2)
            else:
                assert False, 'not found stream'
        #print(s)
        #print(content.find(self._STREAM_END_BYTES) - s)
        zs = content[s:content.find(self._STREAM_END_BYTES)]
        #print(zs)
        #print(zlib.decompress(zs))
        return zlib.decompress(zs)

class _Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(_Singleton, cls).__new__(cls)
        return cls._instance

class PDFReader(_Singleton):
    _decomp = Decompresses()
    _RE_NEWLINE = re.compile('[\n\r]')
    _pdf_path = None
    def set_pdf_pass(self, pdf_path):
        if isinstance(pdf_path, Path):
            self._pdf_path = pdf_path
        else:
            self._pdf_path = self._path_check(pdf_path)

    def getPdfPath(self):
        return self._pdf_path

    def _path_check(self, pdf_path):
        p = Path(pdf_path)
        if not p.exists():
            raise PDFPathException('file not found ({}) '.format(fp))
        if not p.is_file():
            raise PDFPathException('path is not data file ({})'.format(fp))
        #print('file : {}, ({:,} bytes)'.format(p.resolve(), p.stat().st_size))
        return p

    def read_byte(self, read_size, offset = 0, dec_code = None, dec_error = 'ignore', ignore_newline = False):
        with self._pdf_path.open(mode='rb') as f:
            if offset > 0:
                f.seek(offset)
            elif offset < 0:
                f.seek(self._pdf_path.stat().st_size + offset)
            if dec_code:
                if read_size > 0:
                    b = f.read(read_size)
                else:
                    b = f.read()
                if ignore_newline:
                    return self._RE_NEWLINE.sub('', b.decode(dec_code, errors=dec_error))
                return b.decode(dec_code, errors=dec_error)
            else:
                if read_size > 0:
                    return f.read(read_size)
                else:
                    return f.read()

    def _read_block(self, f, block_size=128):
        b = f.read(block_size)
        while b:
            yield b
            b = f.read(block_size)
        return None


    _RE_FILTER_FLATEDECODE = re.compile(r'.*/Filter\s*/FlateDecode.*', flags=re.MULTILINE | re.DOTALL)
    _END_OBJ_BYTES = b'endobj'
    def read_object(self, offset, ignore_newline = False, decomp = True):
        b = b''
        with self._pdf_path.open(mode='rb') as f:
            f.seek(offset)
            for blk in self._read_block(f):
                assert blk, 'not found endobj'
                b += blk
                idx = b.find(self._END_OBJ_BYTES)
                if idx > -1:
                    b = b[:idx+len(self._END_OBJ_BYTES)]
                    break
        #print(b)
        if not decomp:
            return b
        dec_code = 'utf-8'
        dec_error = 'ignore'
        s = b.decode(dec_code, errors=dec_error)
        if decomp:
            m = self._RE_FILTER_FLATEDECODE.match(s)
            if m:
                s = self._read_uncompressed_object(offset)
        if ignore_newline:
            return self._RE_NEWLINE.sub('', s)
        return s

    def _read_uncompressed_object(self, offset, ignore_newline = False):
        b = self.read_object(offset, decomp = False)
        d = self._decomp.stream(b)
        s = d.decode('utf-8', errors='ignore')
        if ignore_newline:
            return self._RE_NEWLINE.sub('', s)
        return s

#[EOF]