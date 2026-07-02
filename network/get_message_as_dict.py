from email.utils import parsedate_to_datetime
from core import Contact
import email
from android_utils import Dir, logging
from .message_parser import get_message_text
from .message_parser import get_message_application


def get_message_as_dict(dir : Dir, message : email.message.Message, contact : Contact, user : str) -> dict | bool:

    try:

        if message is False:
            return False

        message_data = {
            "from": user,
            "text/plain": "",
            "application": [],
            "date": parsedate_to_datetime(message["Date"]).isoformat()
        }

        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                message_data["text/plain"] = get_message_text(part)
            elif content_type in ["application/octet-stream", "audio/wav", "audio/mpeg",
                                  "audio/ogg", "audio/ogg", "video/mp4", "audio/wav"]:
                application = get_message_application(dir, part, contact)
                if not (application is False): message_data["application"].append(application)

        return message_data

    except Exception as e:
        logging.error(f"[GET MESSAGE AS DICT] Error {e}")
        return False