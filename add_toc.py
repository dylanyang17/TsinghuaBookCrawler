from PyPDF2 import PdfWriter, PdfReader


def add_toc(input_pdf, output_pdf, chapter_data):
    """
    Add a table of contents to an existing PDF

    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file
        chapter_data: List of tuples (chapter_name, page_number)
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add all pages from the original PDF
    for page in reader.pages:
        writer.add_page(page)

    # Add chapter entries
    for chapter_name, page_num in chapter_data:
        writer.add_outline_item(chapter_name, page_num)

    # Save the new PDF
    with open(output_pdf, "wb") as f:
        writer.write(f)
