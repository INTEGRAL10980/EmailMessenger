import imaplib


class ModifiedIMAP4_SSL(imaplib.IMAP4_SSL):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_mailbox = None
        self.sent_mailbox = None

    def select(self, mailbox : str = "INBOX") -> tuple:
        result, data = super().select(mailbox)
        if result == "OK":
            self.current_mailbox = mailbox
        else:
            self.current_mailbox = None
        return result, data

    def get_sent_mailbox(self) -> str | None:

        result, data = self.list()
        if result != "OK":
            return ""
        for mailbox in data:
            mailbox_str = mailbox.decode('utf-8', errors='ignore')
            if "sent" in mailbox_str.lower():
                mailbox_name = mailbox_str.split(" ")[-1].replace('"', "")
                return mailbox_name
