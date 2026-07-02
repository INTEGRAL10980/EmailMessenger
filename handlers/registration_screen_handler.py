from core import create_account
from android_utils import Dir
from core import Account


class RegistrationScreenHandler:
    def __init__(self, dir : Dir) -> None:
        self.dir = dir

    def create_account(self, name : str, email : str, password : str) -> bool:
        result = create_account(self.dir, name, email, password)
        return result