import re

class Trailer:
    _RE_TRAILER_BODY = re.compile(r'.*trailer(?P<TAILER_BODY>.+)startxref.+', flags=re.MULTILINE | re.DOTALL)
    _RE_SIZE = re.compile(r'.*/Size\s+(?P<TRAILER_BODY_SIZE>\d+)\D+', flags=re.MULTILINE | re.DOTALL)
    _RE_ROOT = re.compile(r'.*/Root\s+(?P<TRAILER_BODY_ROOT>[\w\s]+).+', flags=re.MULTILINE | re.DOTALL)
    _RE_INFO = re.compile(r'.*/Info\s+(?P<TRAILER_BODY_INFO>[\w\s]+).+', flags=re.MULTILINE | re.DOTALL)
    _size = 0
    _root = ''
    _info = ''

    def getRoot(self):
        return self._root

    def __init__(self, s, isPrint=False):
        m = self._RE_TRAILER_BODY.match(s)
        assert m, 'not foud trailer'

        wk = m.group('TAILER_BODY')

        m = self._RE_SIZE.match(wk)
        assert m, 'not /Size in trailer'
        self._size = int(m.group('TRAILER_BODY_SIZE'))
        if isPrint:
            print('trailer size : {}'.format(self._size))

        m = self._RE_ROOT.match(wk)
        assert m, 'not /Root in trailer'
        self._root = m.group('TRAILER_BODY_ROOT')
        if isPrint:
            print('trailer root : [{}]'.format(self._root))

        m = self._RE_INFO.match(wk)
        assert m, 'not /Info in trailer'
        self._info = m.group('TRAILER_BODY_INFO')
        if isPrint:
            print('trailer info : [{}]'.format(self._info))

#[EOF]