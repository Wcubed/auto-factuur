import os
import logging
from PyPDF2 import PdfFileReader, PdfFileMerger

# TODO Make a proper config file/argument for this.
METAALUNIE_VOORWAARDEN_PATH = "../resources/test_voorwaarden.pdf"


def attach_voorwaarden(input_pdf):
    output_pdf = os.path.dirname(input_pdf)
    output_pdf = os.path.join(output_pdf, "../Output.pdf")

    logging.info("Attaching voorwaarden to: {}, outputting to: {}".format(input_pdf, output_pdf))

    concat_pdf_files(input_pdf, METAALUNIE_VOORWAARDEN_PATH, output_pdf)


def concat_pdf_files(first, second, output):
    # TODO Fail gracefully.

    merger = PdfFileMerger()

    merger.append(first)
    merger.append(second)

    merger.write(output)