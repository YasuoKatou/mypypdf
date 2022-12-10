import re
from .pdf_reader import PDFReader
from .kids import PDFKids
from .cross_reference import PDFCrossReferenceTable
from .mypdf_exception import PDFKeywordNotFoundException

class PDFPages:
    _kids = None
    def __init__(self, obj_id):
        reader = PDFReader()
        xref = PDFCrossReferenceTable()
        d = xref.getXrefData(obj_id)
        s = reader.read_object(d.getOffset(), dec_code='utf-8', ignore_newline=True)
        #print(s)
        self._getCount(s)
        self._kids = PDFKids(s)

    _count = 0
    _RE_COUNT = re.compile(r'.*/Count\s+(?P<NUM>\d+).*')
    def _getCount(self, s):
        m = self._RE_COUNT.match(s)
        if m:
            self._count = int(m.group('NUM'))
        else:
            raise PDFKeywordNotFoundException('[/Count] not found in Pages')

    def getPageCount(self):
        return self._count

#[EOF]