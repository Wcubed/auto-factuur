import logging
import os
import re

from watchdog.events import FileSystemEventHandler
import auto_factuur.mail as mail
import auto_factuur.pdf_tools as pdf_tools


class PdfEventHandler(FileSystemEventHandler):

    def __init__(self, appendix_path, mail_body):
        super().__init__()

        # The event handler ignores changes
        # to the pdf it just created
        # and the pdf it just renamed.
        # This to prevent change loops.
        self._last_output_pdf = ""
        self._last_renamed_pdf = ""

        self.appendix_path = appendix_path
        self.mail_body = mail_body

    def on_any_event(self, event, **kwargs):
        try:
            # TODO: Proper error handling.
            # I know it is not right to put the whole operation in one
            # big try-except block, but I need to log any weird errors that
            # crop up in here.

            if event.is_directory:
                return None

            elif event.event_type == 'created':
                pdf_path = event.src_path
            elif event.event_type == 'moved':
                pdf_path = event.dest_path
            else:
                return None

            if pdf_path == self._last_output_pdf or pdf_path == self._last_renamed_pdf:
                # We just edited this pdf ourselves, so better not try and do it again.
                return None

            if not pdf_tools.is_file_pdf(pdf_path):
                return None
            # The filename says it is a pdf.

            if pdf_tools.pdf_has_appendix(pdf_path,  self.appendix_path):
                return None
            # It doesn't already have the attachment.

            logging.info("New pdf detected: {}".format(pdf_path))

            temp_pdf = os.path.dirname(pdf_path)
            temp_pdf = os.path.join(temp_pdf, "temp.pdf")

            self._last_output_pdf = temp_pdf
            self._last_renamed_pdf = pdf_path

            pdf_tools.attach_appendix(pdf_path,  self.appendix_path, temp_pdf)
            # Overwrite the input file with the output file,
            # it is no longer needed.
            os.replace(temp_pdf, pdf_path)

            self.get_invoice_number(os.path.basename(pdf_path))

            new_mail = mail.Mail(to="wybe@ruurdwestra.nl",
                                 subject=os.path.basename(pdf_path),
                                 body=self.mail_body,
                                 attachment=pdf_path)

            mail.open_mail_program(new_mail)
        except Exception as exception:
            logging.exception(exception)



    def get_invoice_number(self, filename):
        """
        Gets the invoice number from the filename.
        Returns None if no number is found.
        The invoice number is always at the front of the filename, like so:
            1_test.pdf
            23_bla.pdf
            242_bla_test_something.pdf
        """
        maybe_number = re.search(r'^\d+', filename)

        number = None

        if maybe_number is not None:
            number = maybe_number.group()
            logging.info("Invoice number is: {}".format(number))
        else:
            logging.info("No invoice number found.")

        return number
