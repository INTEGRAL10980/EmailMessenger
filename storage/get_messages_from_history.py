from core import Contact
from android_utils import Dir
import sqlite3
import os


def get_messages_from_history(dir : Dir, contact : Contact, limit : int) -> list[list]:
    """
    Обращается к history.db в директории контакта и получает историю переписки (последние limit сообщений)
    """
    path = dir*os.path.join(contact.PATH_TO_CONTACT, "history.db")
    if not os.path.isfile(dir*os.path.join(contact.PATH_TO_CONTACT, "history.db")):
        return []

    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT contact_name, date, text, applications FROM messages ORDER BY date DESC")
        rows = cursor.fetchall()
    output = rows[:limit]
    amount_messages = len(output)
    for i in range(amount_messages):
        message = output[i]
        data = {
            "from": message[0],
            "date": message[1],
            "text/plain": message[2],
            "application": message[3].split(",")
        }
        output[i] = data
    output.reverse()
    return output