from pathlib import Path
import argparse
import re

from pdf_objects.xref_table import XRefTable
from pdf_objects.trailer import Trailer
from pdf_objects.objects import Decompresses

class MyPdf:
    _pdf_path = None
    _xref_str = None
    _xref_table = None
    _trailer = None
    _decomp = Decompresses()

    def __init__(self, pdf_path):
        self._pdf_path = pdf_path

    def path_check(self):
        p = Path(self._pdf_path)
        assert p.exists(), 'file not found ({}) '.format(fp)
        assert p.is_file(), 'path is not data file ({})'.format(fp)
        print('file : {}, ({:,} bytes)'.format(p.resolve(), p.stat().st_size))
        return p

    _RE_PDF_VERSION = re.compile(r'^%PDF-(?P<MAJOR>\d+)\.(?P<MINOR>\d+).*')
    def read_pdf_version(self):
        p = Path(self._pdf_path)
        with p.open(mode='rb') as f:
            b = f.read(32)
            u = b.decode('utf-8', errors='ignore')
            #print(u)
            m = self._RE_PDF_VERSION.match(u)
            if m:
                return (int(m.group('MAJOR')), int(m.group('MINOR')))
            else:
                assert False, "PDF version is not found"

    def read_xref(self):
        p = Path(self._pdf_path)
        offset = self.read_xref_pos(p)
        self._xref_str = ''
        with p.open(mode='rb') as f:
            f.seek(offset)
            b = f.read()
            self._xref_str = b.decode('utf-8', errors='ignore')
        self._xref_table = XRefTable(self._xref_str)
        self._trailer = Trailer(self._xref_str, isPrint=True)

    def printXref(self):
        self._xref_table.printObjectMap()

    _RE_POS_XREF = re.compile(r'.*startxref\r?\n(?P<POS>\d+)\r?\n%%EOF', flags=re.MULTILINE | re.DOTALL)
    def read_xref_pos(self, p):
        file_size = p.stat().st_size
        pos = -1
        with p.open(mode='rb') as f:
            f.seek(file_size - 256)
            b = f.read(256)
            #print(b.decode(), end='')
            u = b.decode('utf-8', errors='ignore')
            m = self._RE_POS_XREF.match(u)
            if m:
                #print('['+m.group('POS')+']')
                pos = int(m.group('POS'))
                print('find xref pos [{:,}]'.format(pos))
            else:
                assert False, "keyword 'startxref...%%EOF$' is not found"
        return pos

    _fontRefs = {}
    _RE_FONT_REF_MAP = re.compile(r'.*/Font<<(?P<FONT_LIST>[\w\/\-_ ]+)>>.*', flags=re.MULTILINE | re.DOTALL)
    _RE_FONT_REF = re.compile(r'.*/Font<</(?P<FONT_NAME>\w+)\s+(?P<OBJECT_NO>\d+)\s+(?P<GEN_NUM>\d+)\s+R>>.*', flags=re.MULTILINE | re.DOTALL)
    def pushFonts(self, s):
        m = self._RE_FONT_REF_MAP.match(s)
        if m:
            print('hit font map : ' + m.group('FONT_LIST'))
            #self._fontRefs[m.group('FONT_NAME')] = (int(m.group('OBJECT_NO')), int(m.group('GEN_NUM')))
            #print('hit font info ' + str(self._fontRefs))

    _RE_FILTER_FLATEDECODE = re.compile(r'.*/Filter/FlateDecode.*', flags=re.MULTILINE | re.DOTALL)
    def dump_Object(self, objNo):
        p = Path(self._pdf_path)
        s = self._xref_table.getObject(p, objNo)
        m = self._RE_FILTER_FLATEDECODE.match(s)
        if m:
            o = self._xref_table.getUncompressedObject(p, objNo)
            d = self._decomp.stream(o)
            print('[mypypdf Decompresses]')
            s = d.decode()
        print(s)
        self.pushFonts(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='my PDF Reader')
    parser.add_argument('--file-path', type=str, help='file path', required=True)
    args = parser.parse_args()
    #print(args.file_path)
    pdf = MyPdf(args.file_path)
    pdf.path_check()
    pdf_ver = pdf.read_pdf_version()
    print('pdf version [%d.%d]' % (pdf_ver))
    pdf.read_xref()
    #pdf.printXref()
    while True:
        objNo = input('input object no (e:end, l:list): ')
        if objNo == 'e':
            break;
        elif objNo == 'l':
            pdf.printXref()
            continue
        pdf.dump_Object(int(objNo))

#[EOF]