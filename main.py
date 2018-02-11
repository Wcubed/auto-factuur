import logging
import os
import time

from watchdog.observers import Observer

from auto_factuur.pdf_event_handler import PdfEventHandler

TEST_DIRECTORY = "../test_dir/"


def main():
    if not os.path.exists(TEST_DIRECTORY):
        os.makedirs(TEST_DIRECTORY)

    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = PdfEventHandler()
    observer = Observer()
    observer.schedule(event_handler, TEST_DIRECTORY, recursive=False)
    observer.start()

    logging.info("Setup complete.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exiting.")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
