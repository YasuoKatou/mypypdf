from pathlib import Path
from .mypdf_exception import PDFPathException

class PDFBase:
    _pdf_path = None
    def set_pdf_pass(self, pdf_path):
        self._pdf_path = self._path_check(pdf_path)

    def _path_check(self, pdf_path):
        p = Path(pdf_path)
        if not p.exists():
            raise PDFPathException('file not found ({}) '.format(fp))
        if not p.is_file():
            raise PDFPathException('path is not data file ({})'.format(fp))
        #print('file : {}, ({:,} bytes)'.format(p.resolve(), p.stat().st_size))
        return p

    def read_byte(self, read_size, offset = 0, dec_code = None, dec_error = 'ignore'):
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


    _END_OBJ_BYTES = b'endobj'
    def read_object(self, offset, dec_code = None, dec_error = 'ignore'):
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
        if dec_code:
            return b.decode(dec_code, errors=dec_error)
        else:
            return b

#[EOF]