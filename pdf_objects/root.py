from .base_class import PDFBase

class PDFRoot(PDFBase):
    def __init__(self, pdf_path, xref_data):
        super().__init__()
        super().set_pdf_pass(pdf_path)
        #print('/Root:{}'.format(xref_data.toString()))
        s = super().read_object(xref_data.getOffset(), dec_code='utf-8')
        print(s)

#[EOF]