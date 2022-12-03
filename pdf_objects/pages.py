import re
from .base_class import PDFBase
from .kids import PDFKids
from .cross_reference import PDFCrossReferenceTable
from .mypdf_exception import PDFKeywordNotFoundException

class PDFPages(PDFBase):
    _kids = None
    def __init__(self, pdf_path, obj_id):
        super().set_pdf_pass(pdf_path)
        xref = PDFCrossReferenceTable()
        d = xref.getXrefData(obj_id)
        s = super().read_object(d.getOffset(), dec_code='utf-8')
        #print(s)
        self._getCount(s)
        self._kids = PDFKids(pdf_path, s)

    _count = 0
    _RE_COUNT = re.compile(r'.*/Count\s+(?P<NUM>\d+).*', flags=re.MULTILINE | re.DOTALL)
    def _getCount(self, s):
        m = self._RE_COUNT.match(s)
        if m:
            self._count = int(m.group('NUM'))
        else:
            raise PDFKeywordNotFoundException('[/Count] not found in Pages')

    def getPageCount(self):
        return self._count

#[EOF]