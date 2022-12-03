import re
from .base_class import PDFBase
from .cross_reference import PDFCrossReferenceTable

class PDFPages(PDFBase):
    def __init__(self, pdf_path, obj_id):
        super().set_pdf_pass(pdf_path)
        xref = PDFCrossReferenceTable()
        d = xref.getXrefData(obj_id)
        s = super().read_object(d.getOffset(), dec_code='utf-8')
        print(s)

#[EOF]