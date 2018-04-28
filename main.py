import logging
import os
import time

from watchdog.observers import Observer

from auto_factuur.pdf_event_handler import PdfEventHandler
from auto_factuur.contacts_reader import ContactsReader
from auto_factuur.config import Config

CONFIG_PATH = "../config.json"


def main():
    config = Config()

    logging.basicConfig(filename=config.log_path(),
                        level=logging.INFO,
                        format='[%(asctime)s]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    config.load_config(CONFIG_PATH)

    contacts = ContactsReader(config.contacts_path(), config.contacts_sheet_name())

    if not os.path.exists(config.watch_path()):
        os.makedirs(config.watch_path())

    event_handler = PdfEventHandler(config.appendix_path(), config.mail_body())
    observer = Observer()
    observer.schedule(event_handler, config.watch_path(), recursive=True)
    observer.start()

    logging.info("Observing '{}'".format(config.watch_path()))

    logging.info("Setup complete.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exiting.")
        observer.stop()

    observer.join()

    config.save_config(CONFIG_PATH)


if __name__ == "__main__":
    main()
