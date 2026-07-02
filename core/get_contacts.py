from .contact import Contact
from .get_contact import get_contact
from android_utils import Dir
import os

def get_contacts(dir : Dir) -> list[Contact]:
    contacts_list = [get_contact(dir, os.path.join("Contacts", contact_directory)) for contact_directory in os.listdir(dir*"Contacts")
                         if "[contact]" in contact_directory and
                         not (get_contact(dir, os.path.join("Contacts", contact_directory)) is False)]
    return contacts_list