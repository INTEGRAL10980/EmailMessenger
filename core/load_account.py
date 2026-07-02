from .account import Account
import json
import os
from android_utils import Dir, logging

def load_account(dir : Dir) -> Account | bool:

    if not os.path.isfile(dir*"account_config.json"): return False

    with open(dir*"account_config.json", "r", encoding="utf-8") as init:
        data = json.load(init)
        return Account(data["name"], data["email"], data["password"])