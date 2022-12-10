import re
from .pdf_reader import PDFReader
from .cross_reference import PDFCrossReferenceTable
from .mypdf_exception import PDFKeywordNotFoundException
from .mypdf_exception import PDFRecordObjectsMissmatchException

class PDFFont:
    _reader = PDFReader()
    _xref = PDFCrossReferenceTable()
    _font_info = {}
    _RE_FONT_REF = re.compile(r'(?P<FONT_NAME>/[\w\/\-_]+)\s+(?P<OBJECT_ID>\d+)\s+(?P<GEN_NUM>\d+)\s+R')
    def __init__(self, font_objs):
        #print('/Font objs [{}]'.format(font_objs))
        for m in self._RE_FONT_REF.finditer(font_objs):
            fn = m.group('FONT_NAME')
            id = int(m.group('OBJECT_ID'))
            #print('{} {}'.format(fn, id))
            self._font_info[fn] = self._readFontInfo(id)

    _RE_TO_UNICODE = re.compile(r'.*/ToUnicode\s+(?P<OBJECT_ID>\d+)\s+(?P<GEN_NUM>\d+)\s+R.*')
    def _readFontInfo(self, obj_id):
        d = self._xref.getXrefData(obj_id)
        s = self._reader.read_object(d.getOffset(), dec_code='utf-8', ignore_newline=True)
        #print(s)
        m = self._RE_TO_UNICODE.match(s)
        if not m :
            raise PDFKeywordNotFoundException('[/ToUnicode] not found in Font')
        id = int(m.group('OBJECT_ID'))
        #print('ToUnicode id:{}'.format(id))
        s = self._read_tounicode(id)
        o = self._getCMap1on1(s)
        return {'CMap1': o}

    _RE_FILTER_FLATEDECODE = re.compile(r'.*/Filter\s*/FlateDecode.*', flags=re.MULTILINE | re.DOTALL)
    def _read_tounicode(self, obj_id):
        d = self._xref.getXrefData(obj_id)
        s = self._reader.read_object(d.getOffset(), dec_code='utf-8', ignore_newline=False)
        m = self._RE_FILTER_FLATEDECODE.match(s)
        if m:
            s = self._reader.read_uncompressed_object(d.getOffset())
            #print('todo Uncompress !!')
        return s

    _RE_BFCHAR = re.compile(r'.*(?P<ITEM_NUM>\d+)\s+beginbfchar(?P<LIST>.*?)endbfchar.*', flags=re.MULTILINE | re.DOTALL)
    _RE_1ON1_CODE = re.compile(r'^<(?P<SRC>[0-9A-Fa-f]+)>\s*<(?P<DIST>[0-9A-Fa-f]+)>$', flags=re.MULTILINE)
    def _getCMap1on1(self, source):
        m = self._RE_BFCHAR.match(source)
        if not m:
            return None
        cmap_1on1 = {}
        n = int(m.group('ITEM_NUM'))
        l = m.group('LIST')
        c = 0
        for m in self._RE_1ON1_CODE.finditer(l):
            s = int(m.group('SRC'), 16)
            d = int(m.group('DIST'), 16)
            #print('{:04x} -> {:04x} [{}]'.format(s, d, chr(d)))
            cmap_1on1[s] = (d, chr(d))
            c += 1
        if c != n:
            raise PDFRecordObjectsMissmatchException('[begin/end]bfchar {} -> {}'.format(n, c))
        return cmap_1on1

#[EOF]