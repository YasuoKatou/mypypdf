import re

class String:
    _fonts = None
    def __init__(self, fonts):
        self._fonts = fonts

    def _getChar(self, fn, code):
        f = self._fonts[fn]
        assert f, '{} not found'.format(fn)
        c = f.getChar(code)

    def printString(self):
        print(self._string)

    _string = ''
    _RE_STR_CODE = re.compile(r'<(?P<CODE>\S+)>')
    def _setText(self, fn, b):
        m = self._RE_STR_CODE.match(b)
        if m:
            w1 = m.group('CODE')
            for i in range(0, len(w1) // 4):
                w2 = self._fonts[fn].getChar(int(w1[i*4:i*4+4], 16))
                self._string += w2

    _RE_TF = re.compile(r'^(?P<FONT_NAME>\/[\w\-_]+)', flags=re.MULTILINE)
    _RE_TD_TJ = re.compile(r'(?P<Tx>\S+)\s+(?P<Ty>\S+)\s+Td\s+(?P<WORDS>\S+)\s+Tj')
    def pushString(self, s):
        #print('>>>>>>>>>>{}<<<<<<<<<<'.format(s))
        r = ''
        m = self._RE_TF.search(s)
        if m:
            fn = m.group('FONT_NAME')
            #print('font name : {}'.format(fn))
            for m in self._RE_TD_TJ.finditer(s):
                #print('Tx:{}, Ty:{}, Text : {}'.format(m.group('Tx'), m.group('Ty'), m.group('WORDS')))
                self._setText(fn, m.group('WORDS'))

#[EOF]