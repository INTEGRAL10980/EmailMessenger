import imaplib

from .modified_imap4_ssl import ModifiedIMAP4_SSL
from android_utils import logging
import ssl

IMAP_SERVERS = {
    'mail.ru': ('imap.mail.ru', 993),
    'bk.ru': ('imap.mail.ru', 993),
    'list.ru': ('imap.mail.ru', 993),
    'inbox.ru': ('imap.mail.ru', 993),
    'yandex.ru': ('imap.yandex.ru', 993),
    'ya.ru': ('imap.yandex.ru', 993),
    'yandex.by': ('imap.yandex.ru', 993),
    'yandex.kz': ('imap.yandex.ru', 993),
    'yandex.com': ('imap.yandex.ru', 993),
    'gmail.com': ('imap.gmail.com', 993),
    'googlemail.com': ('imap.gmail.com', 993),
    'rambler.ru': ('imap.rambler.ru', 993),
    'ro.ru': ('imap.rambler.ru', 993),
    'myrambler.ru': ('imap.rambler.ru', 993),
    'outlook.com': ('outlook.office365.com', 993),
    'hotmail.com': ('outlook.office365.com', 993),
    'live.com': ('outlook.office365.com', 993),
    'msn.com': ('outlook.office365.com', 993)
}

def login_email(email : str, password : str) -> ModifiedIMAP4_SSL | bool:
    try:

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        server = ModifiedIMAP4_SSL(host=IMAP_SERVERS[email.split("@")[-1]][0], port=IMAP_SERVERS[email.split("@")[-1]][1], ssl_context=context)
        server.login(email, password)
        return server

    except ConnectionError as e:
        logging.error(f"[LOGIN EMAIL] Connection error {e}")
        return False
    except imaplib.IMAP4.error as e:
        logging.error(f"[LOGIN EMAIL] IMAP error {e}")
        return False
    except TimeoutError as e:
        logging.error(f"[LOGIN EMAIL] Timeout {e}")
        return False