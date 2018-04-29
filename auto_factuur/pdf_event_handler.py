import logging
import os
import re

from watchdog.events import FileSystemEventHandler
import auto_factuur.mail as mail
import auto_factuur.pdf_tools as pdf_tools


class PdfEventHandler(FileSystemEventHandler):

    def __init__(self, config):
        super().__init__()

        # The event handler ignores changes
        # to the pdf it just created
        # and the pdf it just renamed.
        # This to prevent change loops.
        self._last_output_pdf = ""
        self._last_renamed_pdf = ""

        self.appendix_path = config.appendix_path()
        self.mail_subject = config.mail_subject()
        self.mail_cc = config.mail_cc()
        self.mail_body = config.mail_body()

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

            invoice_number = self.get_invoice_number(os.path.basename(pdf_path))

            body = self.mail_body
            subject = self.mail_subject

            if invoice_number is None:
                invoice_number = 0

            try:
                body = body.format(num=invoice_number)
                subject = subject.format(num=invoice_number)
            except KeyError as e:
                logging.error("Problem formatting mail string:\n"
                              "It looks like there is a formatting string in the config file that looks like this: "
                              "\'{{{}}}\' that is not understood. Please remove it."
                              .format(e))
            except IndexError as e:
                logging.error("Problem formatting mail string:\n"
                              "It looks like there is a formatting string in the config file that looks like this: "
                              "\'{}\'. Please remove it.")

            new_mail = mail.Mail(to="",
                                 cc=self.mail_cc,
                                 subject=subject,
                                 body=body,
                                 attachment=pdf_path)

            logging.info("Mail url: '{}'".format(new_mail.get_url()))

            mail.open_mail_program(new_mail)
        except Exception as exception:
            logging.exception(exception)

    @staticmethod
    def get_invoice_number(filename):
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
