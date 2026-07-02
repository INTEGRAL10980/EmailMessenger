from core import Contact
from core import load_account
from core import get_contacts
from core import create_contact
from android_utils import Dir


class MainScreenHandler:
    def __init__(self, dir : Dir) -> None:
        self.account = load_account(dir)
        self.contacts = get_contacts(dir)

    def create_contact(self, dir : Dir, name : str, email : str) -> Contact | bool:
        contact = create_contact(dir, name, email)
        return contact

    def get_contacts(self, dir : Dir) -> list[Contact]:
        contacts = get_contacts(dir)
        return contacts