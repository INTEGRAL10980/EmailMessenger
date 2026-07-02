import imaplib
import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from core import Account
from core import Contact
from android_utils import Dir, logging
from network.modified_imap4_ssl import ModifiedIMAP4_SSL


def create_message(dir : Dir, from_email : str, by_email : str,
                   text_content : str,
                   applications : list[str]) -> MIMEMultipart:
    print("Создается письмо")
    multipart_message = MIMEMultipart()
    multipart_message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0300")
    multipart_message["From"] = from_email
    multipart_message["To"] = by_email
    multipart_message["Subject"] = "[Fizmatovskii Patrioticheski Messendger]"

    multipart_message.attach(MIMEText(text_content, "plain"))

    for file_directory in applications:
        print(file_directory)
        with open(dir*file_directory, "rb") as file:
            data = file.read()
            part = MIMEApplication(data)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.split(file_directory)[-1])
            multipart_message.attach(part)

    return multipart_message


def send_message(dir : Dir, server : smtplib.SMTP, email : ModifiedIMAP4_SSL,
                 account : Account, contact : Contact,
                 text_content : str,
                 applications : list[str]) -> bool:
    try:

        multipart_message = create_message(dir, account.EMAIL, contact.EMAIL, text_content, applications)
        server.sendmail(account.EMAIL, contact.EMAIL, multipart_message.as_string())
        result = email.append(email.sent_mailbox, r"(\Seen)", None, multipart_message.as_string().encode('utf-8'))
        return True

    except imaplib.IMAP4.error as e:
        logging.error(f"[SEND MESSAGE] IMAP error {e}")
        return False
    except smtplib.SMTPDataError as e:
        logging.error(f"[SEND MESSAGE] Data error {e}")
        return False
    except ConnectionError as e:
        logging.error(f"[SEND MESSAGE] Connection error {e}")
        return False