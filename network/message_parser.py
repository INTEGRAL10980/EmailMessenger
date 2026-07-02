from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from android_utils import Dir, logging
from core import Contact
import os

def get_message_text(part : MIMEText) -> str:
    payload = part.get_payload(decode=True)
    if payload: return payload.decode('utf-8', errors='ignore')
    return ""

def get_message_application(dir : Dir, part : MIMEApplication, contact : Contact) -> str | bool:
    payload = part.get_payload(decode=True)
    filename = part.get_filename()
    folder_name = ""
    if filename.split(".")[-1] in ["png", "jpg", "webp", "svg"]: folder_name = "images"
    elif filename.split(".")[-1] in ["mp3", "ogg", "wav", "acc", "fla"]: folder_name = "audio"
    elif filename.split(".")[-1] in ["mp4", "gif"]: folder_name = "videos"
    elif filename.split(".")[-1] in ["txt", "csv", "docx", "json", "py", "cpp", "h", "md",
                                     "ini", "xml"]: folder_name = "videos"
    else: return ""
    path = os.path.join(contact.PATH_TO_CONTACT, folder_name, filename)
    if os.path.isfile(dir*path):
        return False
    with open(dir*path, "wb") as file:
        file.write(payload)
    return path