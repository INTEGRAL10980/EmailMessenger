import json
import os.path
from android_utils import Dir, logging

def create_account(dir : Dir, name : str, email : str, password : str) -> bool:
    path = dir*"account_config.json"
    if os.path.isfile(path):
        return False
    with open(path, "w", encoding="utf-8") as file:
        data = {
            "name" : name,
            "email" : email,
            "password" : password
        }
        json.dump(data, file, ensure_ascii=False, indent=4)
        return True