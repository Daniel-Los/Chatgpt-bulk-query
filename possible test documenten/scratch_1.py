root = 'Onderzoek-luchtkwaliteit-en-gezondheid-in-Brabant-2022-Rapport.pdf'

import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    out_file = io.StringIO()
    # codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resource_manager, out_file, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
    for page in PDFPage.get_pages(fp, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    text = out_file.getvalue()
    out_file.close()
    return text

text = convert_pdf_to_txt(root)
print(text)