import re
from .pdf_reader import PDFReader
from .cross_reference import PDFCrossReferenceTable

class PDFContents:
    _reader = PDFReader()
    _xref = PDFCrossReferenceTable()
    _RE_OBJECTS = re.compile(r'.*obj\r?\n?\[(?P<LIST>.+)\]\r?\n?endobj.*', flags=re.MULTILINE | re.DOTALL)
    _RE_OBJECT_REF = re.compile(r'(?P<OBJECT_ID>\d+)\s+(?P<GEN_NUM>\d+)\s+R')
    def __init__(self, obj_id):
        d = self._xref.getXrefData(obj_id)
        s = self._reader.read_object(d.getOffset(), ignore_newline=False)
        m = self._RE_OBJECTS.match(s)
        if m:
            for m in self._RE_OBJECT_REF.finditer(m.group('LIST')):
                self._getStringFromObject(int(m.group('OBJECT_ID')))
        else:
            self._getString(d.getOffset(), s)

    def _getStringFromObject(self, obj_id):
        d = self._xref.getXrefData(obj_id)
        s = self._reader.read_object(d.getOffset(), ignore_newline=False)
        self._getString(d.getOffset(), s)

    _RE_TEXT_BLOCK = re.compile(r'^BT\n(?P<BODY>.*?)^ET\n?', flags=re.MULTILINE | re.DOTALL)
    _RE_TEXT_TF = re.compile(r'/(?P<FONT_NAME>[\w\d]+)\s+\d+\.*\d*\s+Tf', flags=re.MULTILINE)
    _RE_TEXT_TM = re.compile(r'')
    _RE_TEXT_TJ = re.compile(r'')
    def _getString(self, offset, source):
        #print('--------------')
        #print(source)
        for m in self._RE_TEXT_BLOCK.finditer(source):
            b = m.group('BODY')
            #print('++++++++++++++')
            #print(b)
            mf = self._RE_TEXT_TF.match(b)
            if mf:
                print(mf.group('FONT_NAME'))
#[EOF]