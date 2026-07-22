from .modified_imap4_ssl import ModifiedIMAP4_SSL
import time
import email as em

def fetch_message_by_uid(email : ModifiedIMAP4_SSL, uid : int) -> em.message.Message | bool:
    for attempt in range(1, 4):
        result, data = email.uid("FETCH", str(uid), '(RFC822)')
        if data[0] != None:
            #print(f"Письмо получено с {attempt} попытки")
            time.sleep(0.2)
            break
    else:
        return False

    raw_email = data[0][1]
    message = em.message_from_bytes(raw_email)

    return message