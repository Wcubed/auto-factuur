import os
import sys
import logging
import subprocess

def open_mail_program():
    title = "Test title."
    body = "Testing body."

    url = "mailto:?subject={}&body={}"
    url = url.format(title, body)


    platform = sys.platform

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
