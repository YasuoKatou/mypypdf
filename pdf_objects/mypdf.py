from .base_class import PDFBase
from .mypdf_exception import PDFVersionReadException
from .mypdf_exception import PDFKeywordNotFoundException
from .cross_reference import PDFCrossReferenceTable
from .root import PDFRoot

import re

class MyPDF(PDFBase):
    _pdf_version = None
    def __init__(self, pdf_path):
        super().__init__()
        super().set_pdf_pass(pdf_path)
        self._pdf_version = self._read_pdf_version()
        pos = self._read_xref_pos()
        s = self._read_xref(pos)
        root_obj_no = self._getRoot(s)
        #print('/Root:{}'.format(root_obj_no))
        root = PDFRoot(pdf_path, self._xref.getXrefData(root_obj_no))

    _RE_PDF_VERSION = re.compile(r'^%PDF-(?P<MAJOR>\d+)\.(?P<MINOR>\d+).*')
    def _read_pdf_version(self):
        u = super().read_byte(32, dec_code='utf-8')
        #print(u)
        m = self._RE_PDF_VERSION.match(u)
        if m:
            return (int(m.group('MAJOR')), int(m.group('MINOR')))
        else:
            raise PDFVersionReadException('PDF version is not found')

    _RE_POS_XREF = re.compile(r'.*startxref\r?\n(?P<POS>\d+)\s*\r?\n%%EOF', flags=re.MULTILINE | re.DOTALL)
    def _read_xref_pos(self):
        u = super().read_byte(256, offset=-256, dec_code='utf-8')
        m = self._RE_POS_XREF.match(u)
        if m:
            pos = int(m.group('POS'))
            #print('find xref pos [{:,}]'.format(pos))
            return pos
        else:
            raise PDFKeywordNotFoundException("keyword 'startxref...%%EOF$' is not found")

    _xref = None
    def _read_xref(self, read_offset):
        u = super().read_byte(-1, offset=read_offset, dec_code='utf-8')
        #print(u)
        self._xref = PDFCrossReferenceTable(u)
        #for id, d in self._xref.getXrefAllData().items():
        #    print('id:{}, Data:{}'.format(id, d.toString()))
        return u

    _RE_ROOT_XREF = re.compile(r'.*/Root\s+(?P<ROOT>\d+)\s+\d+\s+R.*', flags=re.MULTILINE | re.DOTALL)
    def _getRoot(self, s):
        m = self._RE_ROOT_XREF.match(s)
        if not m:
            raise PDFKeywordNotFoundException('[/Root] not found')
        return int(m.group('ROOT'))

    _TO_STR_FMT = '''
PDF Path:{}
\tfile size  : {:,} bytes
\tpdf version: {}.{}'''
    def toString(self):
        p = self._pdf_path
        return self._TO_STR_FMT.format(p.resolve(), p.stat().st_size
                                     , self._pdf_version[0], self._pdf_version[1])
#[EOF]