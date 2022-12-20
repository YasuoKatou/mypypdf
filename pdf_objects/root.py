import re
from .pdf_reader import PDFReader
from .pages import PDFPages

class PDFRoot:
    _pages = None
    def __init__(self, xref_data):
        #print('/Root:{}'.format(xref_data.toString()))
        reader = PDFReader()
        s = reader.read_object(xref_data.getOffset())
        #print(s)
        obj_id = self._getPages(s)
        #print('Pages Object id:{}'.format(obj_id))
        self._pages = PDFPages(obj_id)

    _RE_PAGES = re.compile(r'.*/Pages\s+(?P<PAGES>\d+)\s+\d+\s+R.*', flags=re.MULTILINE | re.DOTALL)
    def _getPages(self, s):
        m = self._RE_PAGES.match(s)
        if not m:
            raise PDFKeywordNotFoundException('[/Pages] not found')
        return int(m.group('PAGES'))

    def getPageCount(self):
        return self._pages.getPageCount()

    def showPageString(self, page_no):
        self._pages.showPageString(1)
#[EOF]