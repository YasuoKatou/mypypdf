import re

from .mypdf_exception import PDFKeywordNotFoundException
from .mypdf_exception import PDFDuplicatedObjectException
from .mypdf_exception import PDFObjectNotFoundException

class XRefData:
    _offset = None
    _gen = None
    _flag = None
    def __init__(self, m):
        self._offset = int(m.group('OFFSET'))
        self._gen = int(m.group('GEN'))
        self.flag = m.group('FLAG')

    def getOffset(self):
        return self._offset

    def toString(self):
        return 'flag:{}, gen:{}, offset:{:,}'.format(self.flag, self._gen, self._offset)

class PDFCrossReferenceTable:
    _xref = {}
    _RE_XREF = re.compile(r'.?^xref\r?\n?(?P<BODY>.*)\r?\n?trailer.*', flags=re.MULTILINE | re.DOTALL)
    _RE_INDEX = re.compile(r'(?P<START>\d+)\s+(?P<NUM>\d+)$')
    _RE_DATA = re.compile(r'(?P<OFFSET>\d+)\s+(?P<GEN>\d+)\s+(?P<FLAG>\w{1})$')
    def __init__(self, source):
        m = self._RE_XREF.match(source)
        if not m:
            raise PDFKeywordNotFoundException('none xref ...')
        b = m.group('BODY')
        #print(b)
        obj_no = None
        obj_count = 0
        for ll in b.split('\n'):
            l = ll.strip()
            m = self._RE_INDEX.match(l)
            if m:
                #print(l)
                obj_no = int(m.group('START'))
                obj_count = int(m.group('NUM'))
                continue
            m = self._RE_DATA.match(l)
            if m:
                #print(l)
                obj_count -= 1
                if obj_count < 0:
                    raise PDFTooManyObjectsException('')
                if obj_no not in self._xref.keys():
                    self._xref[obj_no] = XRefData(m)
                    obj_no += 1
                else:
                    raise PDFDuplicatedObjectException('already object [{}]'.format(l))
                continue
            if len(l) > 0:
                raise PDFKeywordNotFoundException('xref [{}] is missmatch'.format(l))

    def getXrefData(self, id):
        if id in self._xref.keys():
            return self._xref[id]
        else:
            raise PDFObjectNotFoundException('no object id:{}'.format(id))

    def getXrefAllData(self):
        return self._xref

#[EOF]