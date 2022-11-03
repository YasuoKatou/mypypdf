import re

_RE_XREF_REC = re.compile(r'(?P<OFFSET>\d+)\s+(?P<GEN_NO>\d+)\s(?P<FLAG>[fn]).*$')
class XRefRecord:
    def getOffset(self):
        return self._offset
    def getGenNo(self):
        return self._gen_no
    def isUse(self):
        return self._is_use

    def toString(self):
        return 'offset : {:10}, gen no : {:5}, flag : {}'.format(
            self._offset, self._gen_no, self._is_use
        )
    def __init__(self, rec, len_check=True):
        if len_check:
            assert len(rec)==20, 'size error not 20 [' + rec + ']'
        m = _RE_XREF_REC.match(rec)
        if m:
            self._offset = int(m.group('OFFSET'))
            self._gen_no = int(m.group('GEN_NO'))
            self._is_use = m.group('FLAG') == 'n'
            #print('offset : [' + m.group('OFFSET') + ']')
            #print('gen no : [' + m.group('GEN_NO') + ']')
            #print('flag   : [' + m.group('FLAG') + ']')
        else:
            assert False, 'not xref record [' + s + ']'

if __name__ == '__main__':
    s = '0000000000 65535 f \n'
    xref_rec = XRefRecord(s)
    print(xref_rec.toString())

    s = '0000011541 00000 n \n'
    xref_rec = XRefRecord(s)
    print(xref_rec.toString())
#[EOF]