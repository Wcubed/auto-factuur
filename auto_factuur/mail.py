import os
import sys
import logging
import subprocess


class Mail:

    def __init__(self, to="", subject="", cc="", body="", attachment=None):
        self._to = to
        self._subject = subject
        self._cc = cc
        self._body = body
        self._attachment = attachment

    def get_url(self):
        # TODO: Do we need input sanitation here?
        url = "mailto:{}?subject={}&cc={}&body={}"
        url = url.format(self._to,
                         self.subject(),
                         self._cc,
                         self.body())
        if self._attachment:
            url = url + "&attachment={}".format(self._attachment)

        return url

    def subject(self):
        return self._subject

    def body(self):
        return self._body


def open_mail_program(new_mail=Mail()):
    url = new_mail.get_url()

    platform = sys.platform

    logging.debug("Opening mail program.")

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
