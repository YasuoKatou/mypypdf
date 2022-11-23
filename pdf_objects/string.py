from copy import deepcopy
import operator
import re

class TextMatrix:
    _mtx = None
    _fsz = None
    def __init__(self, mtx):
        w = re.split('\s+', mtx)
        assert w, 'can not split ({})'.format(mtx)
        assert len(w)==6, 'not 6 elements ({})'.format(mtx)
        self._mtx = [float(x) for x in w] 

    _next_pos = None
    def getPos(self, sx, sy):
        x = float(sx)
        y = float(sy)
        if self._next_pos:
            self._next_pos['x'] += x
            self._next_pos['y'] += y
        else:
            self._next_pos = {
                'x': x * self._mtx[0] + y * self._mtx[2] + self._mtx[4],
                'y': x * self._mtx[1] + y * self._mtx[3] + self._mtx[5],
            }
        self._next_pos['y'] -= self._tl
        return deepcopy(self._next_pos)

    _tl = 0
    def setNewLine(self, tl):
        self._tl = tl

class String:
    _fonts = None
    def __init__(self, fonts):
        self._fonts = fonts

    def _getChar(self, fn, code):
        f = self._fonts[fn]
        assert f, '{} not found'.format(fn)
        c = f.getChar(code)

    def printString(self):
        self._text_list.sort(key=operator.itemgetter('x'))
        self._text_list.sort(key=operator.itemgetter('y'), reverse=True)
        s = ''
        for str_info in self._text_list:
            s += str_info['string']
        print(s)

    _RE_STR_CODE = re.compile(r'<(?P<CODE>\S+)>')
    def _getText(self, fn, b):
        m = self._RE_STR_CODE.match(b)
        if m:
            s = ''
            w1 = m.group('CODE')
            for i in range(0, len(w1) // 4):
                s += self._fonts[fn].getChar(int(w1[i*4:i*4+4], 16))
            return s
        else:
            assert False, 'not found <CODES>'

    _text_list = []
    _last_x = -999999.0
    _RE_TF = re.compile(r'^(?P<FONT_NAME>\/\S+)\s+(?P<FONT_SIZE>[\d\.]+)\s+Tf$', flags=re.MULTILINE)
    _RE_TM = re.compile(r'^(?P<TEXT_MATRIX>[\s\d\-\.]+)\s+Tm$', flags=re.MULTILINE)
    _RE_TD_TJ = re.compile(r'(?P<Tx>\S+)\s+(?P<Ty>\S+)\s+Td\s+(?P<WORDS>\S+)\s+Tj')
    def pushString(self, s):
        #print('>>>>>>>>>>{}<<<<<<<<<<'.format(s))
        r = ''
        m = self._RE_TF.search(s)
        assert m, '{} no font infornation'.format(s)
        fn = m.group('FONT_NAME')
        tl = float(m.group('FONT_SIZE')) / 1.2      # 120%
        m = self._RE_TM.search(s)
        assert m, '{} no tm infornation'.format(s)
        tm = TextMatrix(m.group('TEXT_MATRIX'))

        #print('font name : {}'.format(fn))
        for m in self._RE_TD_TJ.finditer(s):
            #print('Tx:{}, Ty:{}, Text : {}'.format(m.group('Tx'), m.group('Ty'), m.group('WORDS')))
            str_info = tm.getPos(m.group('Tx'), m.group('Ty'))
            str_info['string'] = self._getText(fn, m.group('WORDS'))
            if self._last_x < str_info['x']:
                self._last_x = str_info['x']
            elif str_info['x'] < self._last_x:
                self._last_x = str_info['x']
                str_info['y'] -= tl
                tm.setNewLine(tl)
            self._text_list.append(str_info)

            print('x:{}, y{} text:{}'.format(str_info['x'], str_info['y'], str_info['string']))

#[EOF]