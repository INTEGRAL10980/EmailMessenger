from core import Contact
from core import get_contact
from utils import Dir
import os
import json

def edit_contact(dir : Dir, contact : Contact, new_name : str, new_email : str, new_last_seen_uid : int, new_last_sent_uid, new_last_message : str) -> Contact:
    """
    Просто перезаписываем информацию о контакте в директории Contacts
    """
    old_path = dir*contact.PATH_TO_CONTACT
    new_path = dir*os.path.join("Contacts", f"[contact]{new_name}")
    path_to_new_ini = os.path.join(new_path, "ini.json")

    if old_path != new_path:
        try:
            os.rename(old_path, new_path)
        except FileExistsError:
            print("Ошибка при редактировании контакта")
            return contact

    with open(path_to_new_ini, "w", encoding="utf-8") as file:
        new_data = {
            "name" : new_name,
            "email" : new_email,
            "last_seen_uid" : new_last_seen_uid,
            "last_sent_uid" : new_last_sent_uid,
            "path_to_contact" : os.path.join("Contacts", f"[contact]{new_name}"),
            "last_message" : new_last_message
        }
        json.dump(new_data, file, ensure_ascii=False, indent=4)

    return get_contact(dir, new_path)