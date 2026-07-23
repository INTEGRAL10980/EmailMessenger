from typing import Callable
import asyncio
import time

from network import create_message
from utils import Dir
from core import Contact
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
    def __init__(self, dir, contact, callback_method, run_task_method):

        self.dir = dir
        self.account = load_account(dir)
        self.contact = contact
        self.server = create_server(self.account.EMAIL, self.account.EMAIL_PASSWORD)
        self.config = get_config(dir)
        self.callback_method = callback_method
        self.run_task_method = run_task_method
        self.incoming_thread_email = login_email(self.account.EMAIL, self.account.EMAIL_PASSWORD)
        self.sent_thread_email = login_email(self.account.EMAIL, self.account.EMAIL_PASSWORD)
        self.sent_thread_email.sent_mailbox = self.sent_thread_email.get_sent_mailbox()

        self.running = True
        self.locker = asyncio.Lock()

    def run(self):
        self.run_task_method(self._fetch_messages)
        self.run_task_method(self._update_smtp_connection)
        self.run_task_method(self._update_imap_connection)

    async def _update_smtp_connection(self):
        while True:
            if self.running is False: return
            try:
                await asyncio.sleep(self.config["time_smtp_reconnection_sleep"])
                async with self.locker:
                    self.server = await asyncio.to_thread(create_server, self.account.EMAIL, self.account.EMAIL_PASSWORD)
            except:
                await asyncio.sleep(5)

    async def _update_imap_connection(self):
        while True:
            if self.running is False: return
            try:
                await asyncio.sleep(self.config["time_imap_reconnection_sleep"])
                async with self.locker:
                    self.incoming_thread_email = await asyncio.to_thread(login_email, self.account.EMAIL, self.account.EMAIL_PASSWORD)
                    self.sent_thread_email = await asyncio.to_thread(login_email, self.account.EMAIL, self.account.EMAIL_PASSWORD)
                    self.sent_thread_email.sent_mailbox = await asyncio.to_thread(self.sent_thread_email.get_sent_mailbox)
            except:
                await asyncio.sleep(5)

    async def _fetch_messages(self):
        while True:
            if self.running is False: return
            try:
                async with self.locker:
                    messages = await asyncio.to_thread(fetch_incoming_messages, self.dir, self.incoming_thread_email, self.contact)
                    messages += await asyncio.to_thread(fetch_sent_messages, self.dir, self.sent_thread_email, self.contact, self.account)
            except:
                messages = []
            if len(messages) == 0:
                await asyncio.sleep(self.config["time_fetch_sleep"])
                continue
            for message in messages:

                await asyncio.to_thread(append_message_to_history, self.dir, self.contact, message["from"], message["date"], message["text/plain"],
                                          message["application"])
                self.callback_method(message)

    def send_message(self, text, applications):
        self.run_task_method(self._send_message, text, applications)
    async def _send_message(self, text, applications):
        email_message = await asyncio.to_thread(create_message, self.dir, self.account.EMAIL, self.contact.EMAIL, text, applications) #made with MIME
        for attempt in range(3):
            async with self.locker:
                server = self.server
                email = self.sent_thread_email
            try:
                result = await asyncio.to_thread(send_message, server, email, self.account, self.contact, email_message)
                break
            except:
                print("dfdfdf")
                await asyncio.sleep(2)
                continue

    def _load_history(self, limit):
        output = get_messages_from_history(self.dir, self.contact, limit)
        for message in output:
            self.callback_method(message)
    def load_history(self, limit = 30):
        self._load_history(limit)

    def stop(self):
        self.running = False
