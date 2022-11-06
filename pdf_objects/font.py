import re

class Font:
    _font_name = None
    def __init__(self, font_name):
        self._font_name = font_name

    def _getInfo(self, info):
        if len(info) == 1:
            return info[0]
        elif len(info) == 2:
            return info[1]
        else:
            assert False, 'too many objects'

    _toUnicodeRefNo = None
    _RE_TO_UNICODE = re.compile(r'.*/ToUnicode\s+(?P<OBJECT_NO>\d+)\s+(?P<GEN_NUM>\d+)\s+R.*', flags=re.MULTILINE | re.DOTALL)
    def setFontInfo(self, info):
        i = self._getInfo(info)
        m = self._RE_TO_UNICODE.match(i)
        assert m, 'no /ToUnicode in \n' + i
        self._toUnicodeRefNo = m.group('OBJECT_NO')
        #print('/ToUnicode ' + self._toUnicodeRef)

    def getToUnicodeRefNo(self):
        return self._toUnicodeRefNo

    _RE_BFCHAR = re.compile(r'.*(?P<ITEM_NUM>\d+)\s+beginbfchar(?P<LIST>.*)endbfchar.*', flags=re.MULTILINE | re.DOTALL)
    _RE_BFRANGE = re.compile(r'.*(?P<ITEM_NUM>\d+)\s+beginbfrange(?P<LIST>.*)endbfrange.*', flags=re.MULTILINE | re.DOTALL)
    def setCMap(self, objs):
        i = self._getInfo(objs)
        #print(i)
        m = self._RE_BFCHAR.match(i)
        if m:
            self.setCMap1on1(int(m.group('ITEM_NUM')), m.group('LIST'))
        else:
            print('not found [begin/end]bfchar in ' + self._font_name)

        m = self._RE_BFRANGE.match(i)
        if m:
            self.setCMapRange(int(m.group('ITEM_NUM')), m.group('LIST'))
        else:
            print('not found [begin/end]range in ' + self._font_name)

    _cmap_1on1 = {}
    _RE_1ON1_CODE = re.compile(r'^<(?P<SRC>[0-9A-Fa-f]+)>\s*<(?P<DIST>[0-9A-Fa-f]+)>$', flags=re.MULTILINE)
    def setCMap1on1(self, num, bfchar):
        #print('cmap 1 on 1 list (' + str(num) + ')\n' + bfchar)
        c = 0
        for m in self._RE_1ON1_CODE.finditer(bfchar):
            s = int(m.group('SRC'), 16)
            d = int(m.group('DIST'), 16)
            #print('{:04x} -> {:04x} [{}]'.format(s, d, chr(d)))
            self._cmap_1on1[s] = (d, chr(d))
            c += 1
        if c != num:
            print('count miss match. check [begin/end]bfchar {} -> {}'.format(num, c))

    _cmap_range = {}
    _RE_RANGE_CODE = re.compile(r'^<(?P<START>[0-9A-Fa-f]+)>\s*<(?P<END>[0-9A-Fa-f]+)>\s*<(?P<BASE>[0-9A-Fa-f]+)>$', flags=re.MULTILINE)
    def setCMapRange(self, num, rng):
        #print('cmap range list (' + str(num) + ')\n' + rng)
        c = 0
        for m in self._RE_RANGE_CODE.finditer(rng):
            s = int(m.group('START'), 16)
            e = int(m.group('END'), 16)
            b = int(m.group('BASE'), 16)
            #print('{:04x} {:04x} -> {:04x} [{}]'.format(s, e, b, chr(b)))
            self._cmap_range[(s, e)] = b
            c += 1
        if c != num:
            print('count miss match. check [begin/end]range {} -> {}'.format(num, c))

    def getChar(self, code):
        if code in self._cmap_1on1:
            return self._cmap_1on1[code][1]
        for rng, b in self._cmap_range.items():
            if rng[0] <= code and code <= rng[1]:
                return chr(b + code - rng[0])
        assert False, '{:04x} is nou found in CMap. font : '.format(code, self._font_name)

#[EOF]