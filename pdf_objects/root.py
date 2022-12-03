import re
from .base_class import PDFBase
from .pages import PDFPages

class PDFRoot(PDFBase):
    _pages = None
    def __init__(self, pdf_path, xref_data):
        super().set_pdf_pass(pdf_path)
        #print('/Root:{}'.format(xref_data.toString()))
        s = super().read_object(xref_data.getOffset(), dec_code='utf-8')
        #print(s)
        obj_id = self._getPages(s)
        #print('Pages Object id:{}'.format(obj_id))
        self._pages = PDFPages(pdf_path, obj_id)

    _RE_PAGES = re.compile(r'.*/Pages\s+(?P<PAGES>\d+)\s+\d+\s+R.*', flags=re.MULTILINE | re.DOTALL)
    def _getPages(self, s):
        m = self._RE_PAGES.match(s)
        if not m:
            raise PDFKeywordNotFoundException('[/Pages] not found')
        return int(m.group('PAGES'))

    def getPageCount(self):
        return self._pages.getPageCount()
#[EOF]