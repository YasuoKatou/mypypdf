from .pdf_reader import PDFReader
from .root import PDFRoot
from .mypdf_exception import PDFVersionReadException
from .mypdf_exception import PDFKeywordNotFoundException
from .cross_reference import PDFCrossReferenceTable

import re

class MyPDF:
    _pdf_version = None
    _root = None
    _reader = None
    def __init__(self, pdf_path):
        self._reader = PDFReader()
        self._reader.set_pdf_pass(pdf_path)
        self._pdf_version = self._read_pdf_version()
        pos = self._read_xref_pos()
        s = self._read_xref(pos)
        obj_id = self._getRoot(s)
        self._root = PDFRoot(self._xref.getXrefData(obj_id))

    _RE_PDF_VERSION = re.compile(r'^%PDF-(?P<MAJOR>\d+)\.(?P<MINOR>\d+).*')
    def _read_pdf_version(self):
        u = self._reader.read_byte(32, dec_code='utf-8')
        #print(u)
        m = self._RE_PDF_VERSION.match(u)
        if m:
            return (int(m.group('MAJOR')), int(m.group('MINOR')))
        else:
            raise PDFVersionReadException('PDF version is not found')

    _RE_POS_XREF = re.compile(r'.*startxref(?P<POS>\d+)\s*%%EOF')
    def _read_xref_pos(self):
        u = self._reader.read_byte(256, offset=-256, dec_code='utf-8', ignore_newline=True)
        m = self._RE_POS_XREF.match(u)
        if m:
            pos = int(m.group('POS'))
            #print('find xref pos [{:,}]'.format(pos))
            return pos
        else:
            raise PDFKeywordNotFoundException("keyword 'startxref...%%EOF$' is not found")

    _xref = None
    def _read_xref(self, read_offset):
        u = self._reader.read_byte(-1, offset=read_offset, dec_code='utf-8')
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
\tpdf version: {}.{}
\tpages      : {:,}'''
    def toString(self):
        p = self._reader.getPdfPath()
        return self._TO_STR_FMT.format(p.resolve(), p.stat().st_size
                                     , self._pdf_version[0], self._pdf_version[1]
                                     , self._root.getPageCount())

    def showPageString(self, page_no):
        self._root.showPageString(1)
#[EOF]