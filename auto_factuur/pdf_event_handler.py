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
            potential_pdf_path = event.src_path
        elif event.event_type == 'moved':
            potential_pdf_path = event.dest_path
        else:
            return None

        logging.info("file " + event.event_type + ": " + potential_pdf_path)

        if is_file_pdf(potential_pdf_path):
            # The filename looks like this might be a pdf.
            logging.info("file is a pdf")

            mail.construct_mail()



def is_file_pdf(src_path):
    return os.path.splitext(src_path)[-1] == '.pdf'
