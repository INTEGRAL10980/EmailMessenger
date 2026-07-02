from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from core import Contact
from .message import Message
from android_utils import Dir
from handlers import ChatHandler

class Chat(Screen):
    def __init__(self, dir : Dir, SIZE : list, contact : Contact, color_theme : dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.chat_handler = ChatHandler(dir, self.name, self.add_message_widget)
        self.SIZE = SIZE
        self.color_theme = color_theme
        self.applications = []

        self.messages_layout = ScrollView(size=(SIZE[0], SIZE[1]-0.2*SIZE[0]), size_hint=(None, None), scroll_y=0, pos=(0, SIZE[0]*0.1), scroll_type=['bars', 'content'], bar_width="10dp")
        self.messages_box = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=10)
        self.messages_box.bind(minimum_height=self.messages_box.setter('height'))
        self.chat_handler.load_history()
        self.input = TextInput(foreground_color=[1,1,1], size=(SIZE[0]-SIZE[0]*0.1, 0.1*SIZE[0]), size_hint=(None, None), background_normal="", background_color=color_theme["widget_background"], hint_text="Введите сообщение")
        self.input_button = Button(text=">", font_size=25, size_hint=(None, None), size=(0.1*SIZE[0], 0.1*SIZE[0]), pos=(SIZE[0]-SIZE[0]*0.1, 0), background_normal="", background_color=color_theme["widget_background"], on_press=self._send_message)
        self.contact_button = Button(text=contact.NAME, size=(SIZE[0]*0.9, SIZE[0]*0.1), size_hint=(None, None), pos=(SIZE[0]*0.1, SIZE[1]-SIZE[0]*0.1), halign="left", text_size=(SIZE[0]*0.9*0.95, None), font_size=20,
                                     background_normal="", background_down="", background_color=color_theme["widget_background"])
        self.return_button = Button(text="<", font_size=25, size_hint=(None, None), size=(0.1*SIZE[0], 0.1*SIZE[0]), pos=(0, SIZE[1]-SIZE[0]*0.1), background_normal="", background_color=color_theme["widget_background"], on_press=self._return_to_main_screen)

        with self.messages_layout.canvas.before:
            Color(*color_theme["main_background"])
            self.rect = Rectangle(size=self.SIZE, pos=(0,0))

        self.messages_layout.add_widget(self.messages_box)
        self.add_widget(self.messages_layout)
        self.add_widget(self.input)
        self.add_widget(self.input_button)
        self.add_widget(self.contact_button)
        self.add_widget(self.return_button)

        Window.bind(on_drop_file=self._on_drop_file)
        self.chat_handler.run()

    def add_message_widget(self, message : dict) -> None:
        Clock.schedule_once(lambda dt: self._add_message_widget(dt, message))
    def _add_message_widget(self, dt : float, message : dict) -> None:
        message_widget = Message(self.chat_handler.dir, self.SIZE, self.chat_handler.contact, message, self.color_theme)
        self.messages_box.add_widget(message_widget)
        message_widget.pos_hint = {"x": 0}

    def _send_message(self, instance : Button) -> None:
        text = self.input.text
        if text == "": return
        self.chat_handler.send_message(text, self.applications)
        self.applications = []
        self.input.text = ""
    def _on_drop_file(self, window : Window, filename : str, *args) -> None:
        file_path = filename.decode('utf-8')
        self.applications.append(file_path)

    def _return_to_main_screen(self, instance : Button) -> None:
        self.manager.current = "main"
    def on_stop(self) -> None:
        self.email.close()