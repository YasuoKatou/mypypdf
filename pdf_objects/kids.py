import re
from .base_class import PDFBase
from .cross_reference import PDFCrossReferenceTable
from .mypdf_exception import PDFKeywordNotFoundException

class PDFKids(PDFBase):
    _RE_KIDS = re.compile(r'.*/Kids\s*\[(?P<BODY>[\d\w\s]+)\].*', flags=re.MULTILINE | re.DOTALL)
    def __init__(self, pdf_path, source):
        super().set_pdf_pass(pdf_path)
        m = self._RE_KIDS.match(source.replace('\n', ''))
        if m:
            #print('kids[{}]'.format(m.group('BODY')))
            self._readKids(m.group('BODY'))
        else:
            raise PDFKeywordNotFoundException('[/Kids] not found in Pages')

    _kids = []
    _RE_OBJ_INFO = re.compile(r'(?P<OBJ_ID>\d+)\s+(?P<GEN_NO>\d+)\s+R')
    def _readKids(self, obj_list):
        xref = PDFCrossReferenceTable()
        for m in self._RE_OBJ_INFO.finditer(obj_list):
            #print(m.group('OBJ_ID'))
            obj_id = int(m.group('OBJ_ID'))
            d = xref.getXrefData(obj_id)
            s = super().read_object(d.getOffset(), dec_code='utf-8')
            print(s)

#[EOF]