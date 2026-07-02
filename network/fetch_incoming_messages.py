from storage import edit_contact
from core import Contact
from android_utils import Dir, logging
import imaplib
from .modified_imap4_ssl import ModifiedIMAP4_SSL
from .fetch_message_by_uid import fetch_message_by_uid
from .get_message_as_dict import get_message_as_dict
from .get_uid import get_uid_list
from .message_parser import *



def fetch_incoming_messages(dir : Dir, email : ModifiedIMAP4_SSL, contact : Contact) -> list[dict]:

    try:

        output = []

        if email is False:
            return []
        if email.current_mailbox != "inbox":
            result, data = email.select("inbox")
            if result != "OK": return []
        uid_list = get_uid_list(email, contact, False)

        for uid in uid_list:
            message = fetch_message_by_uid(email, uid)
            message_data = get_message_as_dict(dir, message, contact, "contact")
            output.append(message_data)

        if len(output) != 0:
            contact.LAST_SEEN_UID = max(uid_list)
            contact = edit_contact(dir, contact, contact.NAME, contact.EMAIL, contact.LAST_SEEN_UID, contact.LAST_SENT_UID, contact.LAST_MESSAGE)
        return output

    except imaplib.IMAP4.error as e:
        logging.error(f"[GET UID] IMAP error {e}")
        return []
    except ConnectionError as e:
        logging.error(f"[GET UID] Connection error {e}")
        return []
    except TimeoutError as e:
        logging.error(f"[GET UID] Timeout error {e}")
        return []