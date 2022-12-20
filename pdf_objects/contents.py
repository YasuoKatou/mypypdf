import re
from .pdf_reader import PDFReader
from .cross_reference import PDFCrossReferenceTable

class CharInfo:
    def __init__(self, m):
        self._x = float(m.group('X'))
        self._y = float(m.group('Y'))
        self._code = int(m.group('CODE'), 16)
        print('x:{}, y:{}, code:{:04x}'.format(self._x, self._y, self._code))

    def getCode(self):
        return self._code

class StringBlock:
    _RE_TEXT_TF = re.compile(r'/(?P<FONT_NAME>[\w\d]+)\s+\d+\.*\d*\s+Tf')
    _RE_TEXT_TM = re.compile(r'(?P<A>[\-\d\.]+)\s+(?P<B>[\-\d\.]+)\s+(?P<C>[\-\d\.]+)\s+(?P<D>[\-\d\.]+)\s+(?P<E>[\-\d\.]+)\s+(?P<F>[\-\d\.]+)\s+Tm')
    _RE_TEXT_TD_TJ = re.compile(r'(?P<X>[\-\d\.]+)\s+(?P<Y>[\-\d\.]+)\s+Td\s+<(?P<CODE>[0-9A-Fa-f]+)>\s+Tj')
    def __init__(self, b):
        #print('++++++++++++++')
        #print(b)
        m = self._RE_TEXT_TF.search(b)
        if m:
            self._font_name = m.group('FONT_NAME')
            print(self._font_name)
        m = self._RE_TEXT_TM.search(b)
        if m:
            self._tm = (float(m.group('A')), float(m.group('B')), float(m.group('C')),
                        float(m.group('D')), float(m.group('E')), float(m.group('F')))
            print('a:{}, b:{}, c:{}, d:{}, e:{}, f:{}'.format(
                self._tm[0], self._tm[1], self._tm[2],
                self._tm[3], self._tm[4], self._tm[5]
            ))
        self._chars = []
        for m in self._RE_TEXT_TD_TJ.finditer(b):
            self._chars.append(CharInfo(m))

    def editString(self, font):
        s = ''
        for c in self._chars:
            s += font.getUtf8(self._font_name, c.getCode())
        return s

class PDFContents:
    _reader = PDFReader()
    _xref = PDFCrossReferenceTable()
    _RE_OBJECTS = re.compile(r'.*obj\r?\n?\[(?P<LIST>.+)\]\r?\n?endobj.*', flags=re.MULTILINE | re.DOTALL)
    _RE_OBJECT_REF = re.compile(r'(?P<OBJECT_ID>\d+)\s+(?P<GEN_NUM>\d+)\s+R')
    def __init__(self, obj_id):
        self._str_block = []
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
    def _getString(self, offset, source):
        #print('--------------')
        #print(source)
        for m in self._RE_TEXT_BLOCK.finditer(source):
            self._str_block.append(StringBlock(m.group('BODY')))

    def showPageString(self, font):
        s = ''
        for sb in self._str_block:
            s += sb.editString(font)
        print(s)
#[EOF]