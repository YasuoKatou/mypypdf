import re
from pdf_objects.xref_record import XRefRecord
from pdf_objects.objects import PdfObject

class XRefTable:
    _objMap = {}
    _RE_OBJ_NO_NUM = re.compile(r'(?P<START_NO>\d+)\s+(?P<OBJ_NUM>\d+)\r?$')
    _RE_XREF = re.compile(r'xref\r?')
    _RE_TRAILER = re.compile(r'trailer\r?')
    def __init__(self, recs):
        for r in recs.split('\n'):
            if self._RE_XREF.match(r):
                continue
            elif self._RE_TRAILER.match(r):
                break
            m = self._RE_OBJ_NO_NUM.match(r)
            if m:
                objNo = int(m.group('START_NO'))
                objNum = int(m.group('OBJ_NUM'))
            else:
                self._objMap[objNo] = XRefRecord(r, len_check=False)
                objNo += 1
                #print(r)

    def getObject(self, p, n, byte_read = False):
        rec = self._objMap[n]
        if byte_read:
            obj = PdfObject()
            return obj.readBytes(p, rec.getOffset())
        else:
            obj = PdfObject(p, rec.getOffset())
        return obj.getObjectDecoded()

    def getUncompressedObject(self, p, n):
        obj = self.getObject(p, n, byte_read=True)
        #print(obj)
        return obj

    def dumpAll(self, p):
        print('dump all start ----------------')
        #print(self._objMap)
        for objNo, rec in self._objMap.items():
            print('[object no {}:{}]'.format(objNo, rec.isUse()))
            if rec.isUse():
                obj = PdfObject(p, rec.getOffset())
                print(obj.getObjectDecoded())
        print('dump all end   ----------------')

    def printObjectMap(self):
        for no, xrefRec in self._objMap.items():
            print('objNo:{:>3}, {}'.format(no, xrefRec.toString()))
#[EOF]