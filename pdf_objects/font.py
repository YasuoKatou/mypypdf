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
        s = self._reader.read_object(d.getOffset(), ignore_newline=True)
        #print(s)
        m = self._RE_TO_UNICODE.match(s)
        if not m :
            raise PDFKeywordNotFoundException('[/ToUnicode] not found in Font')
        id = int(m.group('OBJECT_ID'))
        #print('ToUnicode id:{}'.format(id))
        d = self._xref.getXrefData(id)
        s = self._reader.read_object(d.getOffset(), ignore_newline=False)
        o = self._getCMap1on1(s)
        r = self._getCMapRange(s)
        return {'CMap1': o, 'CMapRange': r}

    _RE_BFCHAR = re.compile(r'^(?P<ITEM_NUM>\d+)\s+beginbfchar(?P<LIST>.*?)endbfchar$', flags=re.MULTILINE | re.DOTALL)
    _RE_1ON1_CODE = re.compile(r'^<(?P<SRC>[0-9A-Fa-f]+)>\s*<(?P<DIST>[0-9A-Fa-f]+)>$', flags=re.MULTILINE)
    def _getCMap1on1(self, source):
        cmap_1on1 = {}
        nt = 0
        for m in self._RE_BFCHAR.finditer(source):
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
                print(source)
                raise PDFRecordObjectsMissmatchException('[begin/end]bfchar {} -> {}'.format(n, c))
            nt += n
        if nt == 0:
            return None
        return cmap_1on1

    _RE_BFRANGE = re.compile(r'^(?P<ITEM_NUM>\d+)\s+beginbfrange(?P<LIST>.*?)endbfrange$', flags=re.MULTILINE | re.DOTALL)
    _RE_RANGE1_CODE = re.compile(r'^<(?P<START>[0-9A-Fa-f]+)>\s*<(?P<END>[0-9A-Fa-f]+)>\s*<(?P<BASE>[0-9A-Fa-f]+)>$', flags=re.MULTILINE)
    _RE_RANGE2_CODE = re.compile(r'^<(?P<START>[0-9A-Fa-f]+)>\s*<(?P<END>[0-9A-Fa-f]+)>\s*\[(?P<LIST>.*)\].*', flags=re.MULTILINE)
    _RE_RANGE2_CODES = re.compile(r'<(?P<CODE>[0-9A-Fa-f]+)>')
    def _getCMapRange(self, source):
        cmap_range = {}
        nt = 0
        for m in self._RE_BFRANGE.finditer(source):
            #print(m.group('LIST'))
            n = int(m.group('ITEM_NUM'))
            l = m.group('LIST')
            c = 0
            for m in self._RE_RANGE1_CODE.finditer(l):
                s = int(m.group('START'), 16)
                e = int(m.group('END'), 16)
                b = int(m.group('BASE'), 16)
                #print('{:04x} {:04x} -> {:04x} [{}]'.format(s, e, b, chr(b)))
                cmap_range[(s, e)] = b
                c += 1
            for m in self._RE_RANGE2_CODE.finditer(l):
                s = int(m.group('START'), 16)
                e = int(m.group('END'), 16)
                l2 = m.group('LIST')
                codes = []
                #cs = ''
                for m2 in self._RE_RANGE2_CODES.finditer(l2):
                    codes.append(int(m2.group('CODE'), 16))
                    #cs += chr(b)
                #print('{:04x} {:04x} -> [{}]'.format(s, e, cs))
                cmap_range[(s, e)] = codes
                c += 1
            if c != n:
                print(source)
                raise PDFRecordObjectsMissmatchException('[begin/end]range {} -> {}'.format(n, c))
            nt += n
        if nt == 0:
            return None
        return cmap_range

    def getUtf8(self, font_name, code):
        f = self._font_info['/' + font_name]
        if f['CMap1']:
            for c, v in f['CMap1'].items():
                if c == code:
                    return v[1]

        if f['CMapRange']:
            for c, v in f['CMapRange'].items():
                if (c[0] <= code) and (code <= c[1]):
                    if isinstance(v, list):
                        return chr(v[code - c[0]])
                    else:
                        return chr(code - c[0] + v)

        raise PDFKeywordNotFoundException('character {:04x} not found in /{}'.format(code, font_name))
        #return '.'

#[EOF]