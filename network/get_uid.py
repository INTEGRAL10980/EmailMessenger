import imaplib
from android_utils import logging
from .modified_imap4_ssl import ModifiedIMAP4_SSL
from core import Contact, Account


def get_uid_list(email : ModifiedIMAP4_SSL, contact : Contact, account : Account = False) -> list:
    """account = False - get mess from contact
        else - get mess from me"""

    if account is False:

        result, data = email.uid('SEARCH', None, f'(SUBJECT "[Fizmatovskii Patrioticheski Messendger]" FROM "{contact.EMAIL}" UID {contact.LAST_SEEN_UID+1}:*)')
        if result != "OK": return []
        uid_list = [int(uid) for uid in data[0].split() if int(uid) > contact.LAST_SEEN_UID]

    else:

        result, data = email.uid('SEARCH', None, f'(SUBJECT "[Fizmatovskii Patrioticheski Messendger]" TO "{contact.EMAIL}" FROM "{account.EMAIL}" UID {contact.LAST_SENT_UID+1}:*)')
        if result != "OK":
            return []
        uid_list = [int(uid) for uid in data[0].split() if int(uid) > contact.LAST_SENT_UID]

    if len(uid_list) == 0: return []
    uid_list.sort()
    return uid_list