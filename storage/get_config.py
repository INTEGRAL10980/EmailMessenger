import json
import os
from android_utils import Dir

def get_config(dir : Dir) -> dict:
    path = dir*"config.json"
    if os.path.isfile(path):
        with open(path, "r", encoding="utf=8") as config:
            data = json.load(config)

        return data
    else:
        with open(path, "w", encoding="utf=8") as config:
            data = {
                "color_theme" : {
                    "main_background" : [0.2, 0.2, 0.25],
                    "widget_background" : [0.25, 0.25, 0.3]
                },
                "SIZE" : [540, 960],
                "time_fetch_sleep" : 1,
                "time_reconnection_sleep" : 120
            }
            json.dump(data, config, ensure_ascii=False, indent=4)

        return data