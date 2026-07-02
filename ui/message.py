from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from datetime import datetime
import webbrowser

from android_utils import Dir
from core import Contact
from ui.media import Media


class Message(BoxLayout):
    def __init__(self, dir : Dir, SIZE : list, contact : Contact, data : dict, color_theme : dict, **kwargs) -> None:
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.size_hint_y = None
        self.size_hint_x = None
        self.width = SIZE[0]*0.55
        self.bind(minimum_height=self.setter('height'))

        with self.canvas.before:
            Color(*color_theme["widget_background"])
            self.bg = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.data = data
        self.contact = contact
        self.SIZE = SIZE
        self.dir = dir
        self.color_theme = color_theme

        self.text = Label(text=f"{'Вы' if data['from'] == 'me' else contact.NAME} в {datetime.fromisoformat(data['date']).strftime('%H:%M')}:\n{data['text/plain']}",
                          font_size=18, width=SIZE[0]*0.6, text_size=(SIZE[0]*0.5, None), size_hint_y=None, halign="left")
        self.text.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        self.media = GridLayout(cols=1, size_hint_y=None)
        self.media.bind(minimum_height=self.media.setter('height'))
        for media in data["application"]:
            if not any(media): continue
            media_button = Media(self.dir, [self.SIZE[0]*0.55, self.SIZE[0]*0.55], media, on_press=self.open_file)
            self.media.add_widget(media_button)

        self.add_widget(self.text)
        self.add_widget(self.media)



    def update_bg(self, *args) -> None:
        self.bg.pos = self.pos
        self.bg.size = self.size

    def open_file(self, instance : Media) -> None:
        webbrowser.open(instance.full_path)