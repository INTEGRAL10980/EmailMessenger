import smtplib
from utils import logging

SERVERS = {
        'gmail.com': ('smtp.gmail.com', 587),
        'yandex.ru': ('smtp.yandex.ru', 587),
        'ya.ru': ('smtp.yandex.ru', 587),
        'mail.ru': ('smtp.mail.ru', 587),
        'bk.ru': ('smtp.mail.ru', 587),
        'list.ru': ('smtp.mail.ru', 587),
        'inbox.ru': ('smtp.mail.ru', 587),
        'rambler.ru': ('smtp.rambler.ru', 587),
        'yahoo.com': ('smtp.mail.yahoo.com', 587),
        'outlook.com': ('smtp-mail.outlook.com', 587),
        'hotmail.com': ('smtp.live.com', 587),
        'icloud.com': ('smtp.mail.me.com', 587),
    }

def create_server(email : str, email_password : str) -> smtplib.SMTP | bool:
    try:

        domain, port = SERVERS[email.split("@")[1]]
        server = smtplib.SMTP(domain, port)
        server.starttls()
        server.login(email, email_password)
        return server

    except smtplib.SMTPConnectError as e:
        logging.error(f"[CREATE SERVER] SMTP connection error {e}")
        return False
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"[CREATE SERVER] Authentication error {e}")
        return False
    except TimeoutError as e:
        logging.error(f"[GET UID] Timeout error {e}")
        return False