#!/usr/bin/env python3
# *_* coding: utf-8 *_*
""" Simple script to fix URLs in UAS emails
"""
import imaplib
import logging
import re
import sys
from email import message_from_bytes
from email.header import decode_header
import pypass

## The directory for log files
LOG_PATH = "."
## The name of the log file
LOG_FILE = "imapmodifier"

HOST = "mail.frankfurt-university.de"
USER = "uas0016465"
PASS_KEY = "ff/uas0016465"

if __name__ == '__main__':
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-8.8s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(f"{LOG_PATH}/{LOG_FILE}.log")

    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.addHandler(consoleHandler)

    MAILBOX = "INBOX"
    if len(sys.argv) < 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <subject> [mailbox]\n")
        sys.exit()
    elif len(sys.argv) > 2:
        MAILBOX = sys.argv[2]

    SUBJECT = '"' + sys.argv[1] + '"'

    p = pypass.PasswordStore()
    p_entry = p.get_decrypted_password(PASS_KEY)
    if p_entry:
        password = p_entry.split('\n')[0]
    else:
        sys.exit()

    with imaplib.IMAP4(host=HOST) as M:
        logger = logging.getLogger()
        M.starttls()
        M.login(USER, password)
        M.select(MAILBOX)
        logger.debug("Searching for emails with subject: %s", SUBJECT)
        resp, mails = M.search('', 'SUBJECT', SUBJECT)
        logger.debug("Found %s", str(mails))
        ENCODED_SUBJECT = ""
        for num in mails[0].split():
            resp, mail = M.fetch(num, '(INTERNALDATE RFC822)')
            for response in mail:
                if isinstance(response, tuple):
                    msg = message_from_bytes(response[1])
                    ENCODED_SUBJECT = msg["Subject"]
                    logger.debug("parsed_subject: %s", ENCODED_SUBJECT)
            date = '"'+mail[0][0].decode().split('"')[1]+'"'
            mail_body = mail[0][1]
            new_mail = re.sub(r'https://urldefense.com/v3/__([^ ]+)__[^ ]*',
                              '\\1', mail_body.decode()).encode()
            encoded_subject, encoding = decode_header(ENCODED_SUBJECT)[0]

            subject = encoded_subject.decode(encoding)
            response = input(f"Found mail from {date} with subject: {subject}\n " \
                             "Should I save a copy with cleaned links? (yes/no) ")
            if (response.lower() == "yes") or (response.lower() == "y"):
                logger.debug("Saving copy")
                M.append(MAILBOX, '', date, new_mail)
            else:
                logger.debug("Skipping")
        M.logout()
