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

    def read_binary(self, read_size, offset = 0, dec_code = None, dec_error = 'ignore'):
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
#[EOF]