from PyPDF2 import PdfReader, PdfWriter

pdf_file_path = input("Please type in the name of the PDF file: ")
file_base_name = pdf_file_path.replace('.pdf', '')

pdf = PdfReader(pdf_file_path)

n = list(map(int, input("Enter the page numbers (comma separated) to be extracted to a new file: ").split(",")))
pages = map(lambda p: p-1, n)

pdfWriter = PdfWriter()

for page_num in pages:
    pdfWriter.add_page(pdf.pages[page_num])

with open('{0}_subset.pdf'.format(file_base_name), 'wb') as f:
    pdfWriter.write(f)
    f.close()