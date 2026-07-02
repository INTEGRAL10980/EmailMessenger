from kivy.uix.button import Button

import os

from android_utils import Dir


class Media(Button):
    def __init__(self, dir : Dir,  SIZE : list, local_path : str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dir = dir
        self.local_path = local_path
        self.full_path = self.dir*self.local_path
        self.media_type = self.local_path.split(".")[-1]
        self.width = SIZE[0]
        self.size_hint = (None, None)

        self.filename = os.path.split(local_path)[-1]
        self.text = self.filename
        self.background_color = [0,0,0,0]
        self.font_size = 20
        self.text_size = (self.width, self.height)
        self.halign = "left"
        self.valign = "center"