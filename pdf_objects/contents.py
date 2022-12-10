import re
from .pdf_reader import PDFReader
from .cross_reference import PDFCrossReferenceTable

class PDFContents:
    _reader = PDFReader()
    _xref = PDFCrossReferenceTable()
    _RE_OBJECTS = re.compile(r'.*\[(?P<LIST>.+)\].*', flags=re.MULTILINE | re.DOTALL)
    _RE_OBJECT_REF = re.compile(r'(?P<OBJECT_ID>\d+)\s+(?P<GEN_NUM>\d+)\s+R')
    def __init__(self, obj_id):
        d = self._xref.getXrefData(obj_id)
        s = self._reader.read_object(d.getOffset(), dec_code='utf-8', ignore_newline=False)
        m = self._RE_OBJECTS.match(s)
        if m:
            for m in self._RE_OBJECT_REF.finditer(m.group('LIST')):
                self._getStringFromObject(int(m.group('OBJECT_ID')))
        else:
            self._getString(d.getOffset(), s)

    def _getStringFromObject(self, obj_id):
        d = self._xref.getXrefData(obj_id)
        s = self._reader.read_object(d.getOffset(), dec_code='utf-8', ignore_newline=False)
        self._getString(d.getOffset(), s)

    _RE_FILTER_FLATEDECODE = re.compile(r'.*/Filter\s*/FlateDecode.*', flags=re.MULTILINE | re.DOTALL)
    def _getString(self, offset, source):
        m = self._RE_FILTER_FLATEDECODE.match(source)
        if m:
            s = self._reader.read_uncompressed_object(offset)
        print('-------------------')
        print(s)
#[EOF]