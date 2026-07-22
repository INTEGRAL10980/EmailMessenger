from core import Contact, Account
from core import get_contacts
from core import load_account
from core import create_contacts_folder
from storage import get_config
from utils import Dir




class ApplicationHandler:
    def __init__(self, dir : Dir) -> None:

        self.dir = dir
        self.create_contacts_folder()
        self.account = load_account(dir)
        self.contacts = get_contacts(dir)

    def get_config(self) -> dict:
        config = get_config(self.dir)
        return config

    def create_contacts_folder(self) -> None:
        create_contacts_folder(self.dir)

    def reload_account(self) -> Account | bool:
        self.account = load_account(self.dir)
        return self.account

    def get_contacts(self) -> list[Contact]:
        self.contacts = get_contacts(self.dir)
        return self.contacts