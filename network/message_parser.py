from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils import Dir, logging
from core import Contact
import os

def get_message_text(part : MIMEText) -> str:
    payload = part.get_payload(decode=True)
    if payload: return payload.decode('utf-8', errors='ignore')
    return ""

def get_message_application(dir : Dir, part : MIMEApplication, contact : Contact) -> str | bool:
    payload = part.get_payload(decode=True)
    filename = part.get_filename()
    print(filename)
    folder_name = ""
    if filename.split(".")[-1] in ["png", "jpg", "jpeg", "webp", "svg", "bmp", "gif", "ico", "tiff", "tif", "heic", "heif", "avif"]:
        folder_name = "images"
    elif filename.split(".")[-1] in ["mp3", "ogg", "wav", "aac", "flac", "m4a", "wma", "opus", "aiff", "alac"]:
        folder_name = "audio"
    elif filename.split(".")[-1] in ["mp4", "gif", "avi", "mkv", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "m4v"]:
        folder_name = "videos"
    else: folder_name = "videos"
    path = os.path.join(contact.PATH_TO_CONTACT, folder_name, filename)
    if os.path.isfile(dir*path):
        return path
    with open(dir*path, "wb") as file:
        file.write(payload)
    return path