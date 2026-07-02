from .contact import Contact
import os
import json
from android_utils import Dir, logging

def get_contact(dir : Dir, path_to_contact : str) -> Contact | bool:
    with open(dir*os.path.join(path_to_contact, "ini.json"), "r", encoding="utf-8") as init:
        data = json.load(init)
        return Contact(data["name"], data["email"], data["last_seen_uid"], data["last_sent_uid"], data["path_to_contact"], data["last_message"])