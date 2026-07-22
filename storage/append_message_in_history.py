from core import Contact
from utils import Dir
import sqlite3
import os


def append_message_to_history(dir : Dir, contact : Contact, user : str, date : str, text : str, applications : list[str]) -> None:

    path = dir*os.path.join(contact.PATH_TO_CONTACT, "history.db")
    if not os.path.isfile(dir*os.path.join(contact.PATH_TO_CONTACT, "history.db")):
        return None

    with sqlite3.connect(path) as connection:
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

        cursor.execute(
            "INSERT INTO messages (contact_name, date, text, applications) VALUES (?, ?, ?, ?)",
            (user, date, text, ",".join(applications))
        )
        connection.commit()