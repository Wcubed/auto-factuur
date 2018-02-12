import logging
import os

from watchdog.events import FileSystemEventHandler
import auto_factuur.mail as mail
import auto_factuur.pdf_tools as pdf_tools

# TODO Make a proper config file/argument for this.
APPENDIX_PATH = "../resources/Metaalunievoorwaarden_2014.pdf"


class PdfEventHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()

        # The event handler ignores changes
        # to the pdf it just created
        # and the pdf it just renamed.
        # This to prevent change loops.
        self._last_output_pdf = ""
        self._last_renamed_pdf = ""

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

            if pdf_tools.pdf_has_appendix(pdf_path, APPENDIX_PATH):
                return None
            # It doesn't already have the attachment.

            logging.info("New pdf detected: {}".format(pdf_path))

            temp_pdf = os.path.dirname(pdf_path)
            temp_pdf = os.path.join(temp_pdf, "temp.pdf")

            self._last_output_pdf = temp_pdf
            self._last_renamed_pdf = pdf_path

            pdf_tools.attach_appendix(pdf_path, APPENDIX_PATH, temp_pdf)
            # Overwrite the input file with the output file,
            # it is no longer needed.
            # TODO This function might not work propperly on OSX. Test that.
            os.replace(temp_pdf, pdf_path)

            new_mail = mail.Mail(to="wybe@ruurdwestra.nl",
                                 subject=os.path.basename(pdf_path),
                                 body="Factuur",
                                 attachment=pdf_path)

            mail.open_mail_program(new_mail)
        except Exception as exception:
            logging.exception(exception)


