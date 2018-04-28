import logging
import os

from openpyxl import load_workbook


class ContactsReader:

    def __init__(self, path, sheet_name):
        logging.info("Loading contacts file: '{}'".format(path))
        if os.path.exists(path):
            try:
                with open(path) as f:
                    self.workbook = load_workbook(path)
            except IOError as e:
                logging.error(
                    """Contact file '{}' exists, but could not be read.
                    Error: {}.""".format(path, e))
        else:
            logging.error("No contact file found.")
        # TODO: What to do if we don't have, or cant read, the contacts?

        # TODO: Give an error when the sheet does not exist.

        self.sheet = self.workbook[sheet_name]

        logging.info("{}".format(self.sheet["A1"].value))
