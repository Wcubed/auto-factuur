import logging
import os

from watchdog.events import FileSystemEventHandler
import auto_factuur.mail as mail


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

        if is_file_pdf(pdf_path):
            # The filename looks like this might be a pdf.
            logging.info("New pdf detected: {}".format(pdf_path))

            new_mail = mail.Mail(title=os.path.basename(pdf_path), body="Factuur")

            mail.open_mail_program(new_mail)


def is_file_pdf(src_path):
    return os.path.splitext(src_path)[-1] == '.pdf'
