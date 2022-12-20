import re
from .pdf_reader import PDFReader
from .font import PDFFont
from .contents import PDFContents
from .cross_reference import PDFCrossReferenceTable
from .mypdf_exception import PDFKeywordNotFoundException
from .mypdf_exception import PDFObjectNotFoundException

class PDFKids:
    _RE_KIDS = re.compile(r'.*/Kids\s*\[(?P<BODY>[\d\w\s]+)\].*')
    def __init__(self, source):
        m = self._RE_KIDS.match(source.replace('\n', ''))
        if m:
            #print('kids[{}]'.format(m.group('BODY')))
            self._readKids(m.group('BODY'))
        else:
            raise PDFKeywordNotFoundException('[/Kids] not found in Pages')

    _kids = []
    _RE_OBJ_INFO = re.compile(r'(?P<OBJ_ID>\d+)\s+(?P<GEN_NO>\d+)\s+R')
    _RE_FONT_KEYWD = re.compile(r'.*/Font\s*<<(?P<FONT_OBJS>[^>]+)?>>.*')
    _RE_RESOUCE_INFO = re.compile(r'.*/Resources\s+(?P<OBJ_ID>\d+)\s+(?P<GEN_NO>\d+)\s+R.*')
    _RE_CONTENTS_INFO  = re.compile(r'.*/Contents\s+(?P<OBJ_ID>\d+)\s+(?P<GEN_NO>\d+)\s+R.*')
    def _readKids(self, obj_list):
        xref = PDFCrossReferenceTable()
        reader = PDFReader()
        for m in self._RE_OBJ_INFO.finditer(obj_list):
            #print(m.group('OBJ_ID'))
            obj_id = int(m.group('OBJ_ID'))
            d = xref.getXrefData(obj_id)
            s = reader.read_object(d.getOffset(), ignore_newline=True)
            #print(s)

            m = self._RE_FONT_KEYWD.match(s)
            fo = None
            if m:
                fo = PDFFont(m.group('FONT_OBJS'))
            if not fo:
                m = self._RE_RESOUCE_INFO.match(s)
                if m:
                    obj_id = int(m.group('OBJ_ID'))
                    d = xref.getXrefData(obj_id)
                    w = reader.read_object(d.getOffset(), ignore_newline=True)
                    m = self._RE_FONT_KEYWD.match(w)
                    if m:
                        fo = PDFFont(m.group('FONT_OBJS'))
            if not fo:
                raise PDFObjectNotFoundException('Font not found')

            m = self._RE_CONTENTS_INFO.match(s)
            if not m:
                raise PDFKeywordNotFoundException('[/Contents] not found in Pages')
            #print('Contents id {}'.format(m.group('OBJ_ID')))
            co = PDFContents(int(m.group('OBJ_ID')))

            self._kids.append({'font': fo, 'contents': co})

    def showPageString(self, page_no):
        o = self._kids[page_no - 1]
        o['contents'].showPageString(o['font'])

#[EOF]