import os
import logging
from PyPDF2 import PdfFileReader, PdfFileMerger


def attach_appendix(input_path, appendix_path, output_path):
    logging.info("Attaching appendix to: {}, outputting to: {}".format(input_path, output_path))

    concat_pdf_files(input_path, appendix_path, output_path)


def concat_pdf_files(first, second, output):
    # TODO Fail gracefully.

    merger = PdfFileMerger()

    merger.append(first)
    merger.append(second)

    merger.write(output)


def is_file_pdf(src_path):
    return os.path.splitext(src_path)[-1] == '.pdf'


def pdf_has_appendix(pdf_path, appendix_path):
    """
    Checks whether the pdf given already has the appendix as a last page.
    APPENDIX SHOULD ONLY BE 1 page long!
    Checks only text, so might fail!
    """
    # TODO Make this work for "metaalunievoorwaarden".

    pdf_file = PdfFileReader(open(pdf_path, 'rb'))
    appendix_file = PdfFileReader(open(appendix_path, 'rb'))

    num_pages = pdf_file.getNumPages()
    last_page = pdf_file.getPage(num_pages-1)
    appendix_page = appendix_file.getPage(0)

    page_content = last_page.extractText()
    appendix_content = appendix_page.extractText()

    logging.debug(page_content)
    logging.debug(appendix_content)

    return page_content == appendix_content