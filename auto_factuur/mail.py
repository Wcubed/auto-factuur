import os
import sys
import logging
import subprocess


class Mail:

    def __init__(self, title="", body=""):
        self._title = title
        self._body = body

    def get_url(self):
        url = "mailto:?subject={}&body={}"
        return url.format(self.title(), self.body())

    def title(self):
        return self._title

    def body(self):
        return self._body


def open_mail_program(new_mail=Mail()):
    url = new_mail.get_url()

    platform = sys.platform

    logging.info("Opening mail program.")

    # TODO: Test this vvv.
    # TODO: Make this return nice errors when stuff fails vvv.

    if platform == 'win32':
        os.startfile(url)
    elif platform == 'darwin':
        subprocess.Popen(['open', url])
    elif platform == 'linux':
        subprocess.Popen(['xdg-email', url])
    else:
        logging.error("Can't open mail client. Unknown OS: " + platform)
        return
