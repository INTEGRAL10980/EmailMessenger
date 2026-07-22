from .contact import Contact
from .get_contact import get_contact
import os
import json
import sqlite3
from utils import Dir, logging

def create_contact(dir : Dir, name : str, email : str) -> Contact | bool:
    try:

        main_path = dir*os.path.join("Contacts", f"[contact]{name}")

        path_ini = os.path.join(main_path, "ini.json")
        path_db = os.path.join(main_path, "history.db")
        path_images = os.path.join(main_path, "images")
        path_videos = os.path.join(main_path, "videos")
        path_audio = os.path.join(main_path, "audio")

        os.makedirs(main_path, exist_ok=False)
        os.makedirs(path_images, exist_ok=True)
        os.makedirs(path_videos, exist_ok=True)
        os.makedirs(path_audio, exist_ok=True)


        connection = sqlite3.connect(path_db)
        cursor = connection.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS messages (
                            contact_name TEXT,
                            date TEXT,
                            text TEXT,
                            applications TEXT
                        )
                        """)
        connection.commit()
        connection.close()



        with open(path_ini, "w", encoding="utf-8") as file:
            data = {
                "name" : name,
                "email" : email,
                "last_seen_uid": 0,
                "last_sent_uid": 0,
                "path_to_contact": os.path.join("Contacts", f"[contact]{name}"),
                "last_message": ""
            }
            json.dump(data, file, ensure_ascii=False, indent=4)

        return get_contact(dir, os.path.join("Contacts", f"[contact]{name}"))

    except FileExistsError as e:
        return False