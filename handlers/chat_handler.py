from typing import Callable
import threading
import time

from android_utils import Dir
from core import get_contact
from core import load_account
from network import fetch_incoming_messages
from network import create_server
from network import fetch_sent_messages
from network import login_email
from network import send_message
from storage import get_config
from storage import append_message_to_history
from storage import get_messages_from_history




class ChatHandler:
    def __init__(self, dir : Dir, path_to_contact : str, callback_method : Callable) -> None:

        self.dir = dir
        self.account = load_account(dir)
        self.contact = get_contact(dir, path_to_contact)
        self.server = create_server(self.account.EMAIL, self.account.EMAIL_PASSWORD)
        self.config = get_config(dir)
        self.callback_method = callback_method
        self.incoming_thread_email = login_email(self.account.EMAIL, self.account.EMAIL_PASSWORD)
        self.sent_thread_email = login_email(self.account.EMAIL, self.account.EMAIL_PASSWORD)
        self.sent_thread_email.sent_mailbox = self.sent_thread_email.get_sent_mailbox()

        self.locker = threading.Lock()

    def run(self) -> None:
        self.fetch_incoming_messages_thread = threading.Thread(target=self._fetch_incoming_messages, daemon=True)
        self.update_server_connection_thread = threading.Thread(target=self._update_server_connection, daemon=True)

        self.fetch_incoming_messages_thread.start()
        self.update_server_connection_thread.start()

    def _update_server_connection(self) -> None:
        while True:
            time.sleep(self.config["time_reconnection_sleep"])
            with self.locker:
                self.server = create_server(self.account.EMAIL, self.account.EMAIL_PASSWORD)

    def _fetch_incoming_messages(self) -> None:
        while True:
            messages = fetch_incoming_messages(self.dir, self.incoming_thread_email, self.contact)
            if len(messages) == 0:
                time.sleep(self.config["time_fetch_sleep"])
                continue
            for message in messages:
                append_message_to_history(self.dir, self.contact, message["from"], message["date"], message["text/plain"],
                                          message["application"])
                self.callback_method(message)

    def send_message(self, text : str, applications : list) -> list:
        output = []
        send_thread = threading.Thread(target=self._send_message, args=[text, applications, output])
        send_thread.start()
        return output
    def _send_message(self, text : str, applications : list, output : list) -> None:
        result = send_message(self.dir, self.server, self.sent_thread_email, self.account, self.contact, text, applications)
        if result is False: return None
        messages = fetch_sent_messages(self.dir, self.sent_thread_email, self.contact, self.account)
        for message in messages:
            append_message_to_history(self.dir, self.contact, message["from"], message["date"], message["text/plain"],
                                      message["application"])
            self.callback_method(message)
        output.extend(messages)

    def _load_history(self, limit : int) -> None:
        output = get_messages_from_history(self.dir, self.contact, limit)
        for message in output:
            self.callback_method(message)
    def load_history(self, limit : int = 30) -> None:
        thread = threading.Thread(target=self._load_history, args=[limit])
        thread.start()