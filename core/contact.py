from dataclasses import dataclass

@dataclass
class Contact:
    """
    Префикс [contact] служит для фильтрации папок контактов в директории Contacts
    """
    NAME : str
    EMAIL : str
    LAST_SEEN_UID : int
    LAST_SENT_UID : int
    PATH_TO_CONTACT : str
    LAST_MESSAGE : str