import os
import sys
import logging
import subprocess


class Mail:

    def __init__(self, to="", subject="", body="", attachment=None):
        self._to = to
        self._subject = subject
        self._body = body
        self._attachment=attachment

    def get_url(self):
        url = "mailto:{}?subject={}&body={}&attachment={}"
        return url.format(self._to,
                          self.subject(),
                          self.body(),
                          self._attachment)

    def subject(self):
        return self._subject

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
