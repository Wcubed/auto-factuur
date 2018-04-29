import logging
import os
import time

from watchdog.observers import Observer

from auto_factuur.pdf_event_handler import PdfEventHandler
from auto_factuur.config import Config

CONFIG_PATH = "../config.json"


def main():
    config = Config()

    setup_logging(config.log_path())

    config.load_config(CONFIG_PATH)

    if not os.path.exists(config.watch_path()):
        os.makedirs(config.watch_path())

    event_handler = PdfEventHandler(config)
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


def setup_logging(log_path):
    log_formatter = logging.Formatter('[%(asctime)s]: %(message)s',
                                      datefmt = '%Y-%m-%d %H:%M:%S')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_logger = logging.FileHandler(log_path)
    file_logger.setFormatter(log_formatter)
    root_logger.addHandler(file_logger)

    console_logger = logging.StreamHandler()
    console_logger.setFormatter(log_formatter)
    root_logger.addHandler(console_logger)


if __name__ == "__main__":
    main()
