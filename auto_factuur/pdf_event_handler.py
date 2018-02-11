import logging
from watchdog.events import FileSystemEventHandler


class PdfEventHandler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event, **kwargs):
        logging.info(str(event.event_type) + " " + str(event.src_path))

        if event.is_directory:
            return None
