import os
from utils import Dir

def create_contacts_folder(dir : Dir) -> bool:
    try:

        os.makedirs(dir*"Contacts", exist_ok=False)
        return True

    except FileExistsError as e:
        return False