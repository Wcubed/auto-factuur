
import logging
import json
import os


class Config:

    DEFAULT_CONFIG = {
        "appendix_path": "../resources/Metaalunievoorwaarden_2014.pdf",
        "log_path": "../log.txt",
        "watch_path": "../test_dir/",
        "mail_body": "Factuur\nFactuur!",
    }

    def __init__(self):
        self.config = self.DEFAULT_CONFIG

    def load_config(self, path):
        logging.info("Loading config file: '{}'".format(path))
        if os.path.exists(path):
            try:
                with open(path) as f:
                    self.config = json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                logging.error(
                    """Config file '{}' exists, but could not be read.
                    Error: {}.
                    Continuing using the default config.""".format(path, e))
        else:
            logging.info("No config file found.")
            self.save_config(path)

    def save_config(self, path):
        logging.info("Saving config file: '{}'".format(path))
        try:
            with open(path, 'w') as f:
                json.dump(self.config, f, sort_keys=True, indent=4)
        except IOError as e:
            logging.error(
                """Something went wrong while trying to save config file: '{}'.
                Error: {}.
                Continuing using the default config.""".format(path, e))

    def _get_key_or_return_default(self, key):
        """
        Tries to get the supplied key from the currently loaded configuration.
        If the current configuration does not have the key,
        it is fetched from the default configuration.
        """
        try:
            return self.config[key]
        except KeyError:
            try:
                return self.DEFAULT_CONFIG[key]
            except KeyError:
                logging.error("Tried to read non-existing config option: '{}'.".format(key))
                return None

    def log_path(self):
        return self._get_key_or_return_default("log_path")

    def watch_path(self):
        return self._get_key_or_return_default("watch_path")

    def appendix_path(self):
        return self._get_key_or_return_default("appendix_path")

    def mail_body(self):
        return self._get_key_or_return_default("mail_body")
