import logging
import os

from watchdog.events import FileSystemEventHandler
import auto_factuur.mail as mail
import auto_factuur.pdf_tools as pdf_tools

# TODO Make a proper config file/argument for this.
APPENDIX_PATH = "../resources/Metaalunievoorwaarden_2014.pdf"


class PdfEventHandler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event, **kwargs):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            pdf_path = event.src_path
        elif event.event_type == 'moved':
            pdf_path = event.dest_path
        else:
            return None

        if not pdf_tools.is_file_pdf(pdf_path):
            return None

        # The filename says it is a pdf.

        if pdf_tools.pdf_has_appendix(pdf_path, APPENDIX_PATH):
            return None

        # It doesn't already have the attachment.

        logging.info("New pdf detected: {}".format(pdf_path))

        pdf_tools.attach_appendix(pdf_path, APPENDIX_PATH)

        new_mail = mail.Mail(to="wybe@ruurdwestra.nl",
                             subject=os.path.basename(pdf_path),
                             body="Factuur",
                             attachment=pdf_path)

        mail.open_mail_program(new_mail)


