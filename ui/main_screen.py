from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp

from handlers import MainScreenHandler
from android_utils import Dir

class MainScreen(Screen):
    def __init__(self, dir : Dir,  SIZE : list, color_theme : dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = "main"
        self.main_screen_handler = MainScreenHandler(dir)
        self.color_theme = color_theme
        self.SIZE = SIZE

        with self.canvas.before:
            Color(*color_theme["main_background"])
            Rectangle(size=SIZE, pos=(0,0))

        self.add_contact_button = Button(
            text="+", font_size=24, size_hint=(None, None), size=(SIZE[0]*0.15, SIZE[0]*0.15), pos=(SIZE[0]*0.85, SIZE[1]-SIZE[0]*0.15),
            background_normal="", background_color=color_theme["widget_background"], on_press=self._add_contact_popup
        )

        self.scroll_view = ScrollView(size_hint=(None, None), size=(SIZE[0], SIZE[1]-SIZE[0]*0.15), pos=(0,0), scroll_type=['bars', 'content'], bar_width="10dp")
        self.scroll_box = BoxLayout(orientation="vertical", size_hint=(1,None), spacing=2)
        self.scroll_box.bind(minimum_height=self.scroll_box.setter('height'))

        for contact in self.main_screen_handler.contacts:
            contact_button = Button(
                text=contact.NAME, font_size=20, size_hint=(1, None), height=dp(70), halign="left",
                text_size=(self.SIZE[0] * 0.9, None),
                background_normal="", background_color=self.color_theme["widget_background"], on_press=self._go_to_chat
            )
            contact_button.contact = contact
            self.scroll_box.add_widget(contact_button)

        self.add_widget(self.add_contact_button)
        self.scroll_view.add_widget(self.scroll_box)
        self.add_widget(self.scroll_view)


    def _go_to_chat(self, instance : Button) -> None:
        self.manager.current = instance.contact.PATH_TO_CONTACT

    def _add_contact_popup(self, instance : Button) -> None:
        input_layout = BoxLayout(orientation="vertical", padding=5, spacing=5)
        name_input = TextInput(foreground_color=[1, 1, 1], background_normal="", background_color=self.color_theme["widget_background"],
                               hint_text="Имя контакта")
        email_input = TextInput(foreground_color=[1, 1, 1], background_normal="", background_color=self.color_theme["widget_background"],
                                hint_text="Почта контакта")
        button = Button(text="Создать", background_normal="", background_color=self.color_theme["widget_background"])

        input_layout.add_widget(name_input)
        input_layout.add_widget(email_input)
        input_layout.add_widget(button)
        popup = Popup(title="Добавить контакт", size_hint=(.5, .5), content=input_layout, background_color=self.color_theme["main_background"])

        button.bind(on_press=lambda instance: self._add_contact(instance, name_input.text, email_input.text, popup))
        popup.open()

    def _add_contact(self, instance : Button, name : str, email : str, popup : Popup) -> None:
        if name == "" or email == "": return None
        contact = self.main_screen_handler.create_contact(self.dir, name, email)
        if not (contact is False):
            self.manager.add_contact_screen(contact)
            contact_button = Button(
                text=contact.NAME, font_size=20, size_hint=(1, None), height=dp(70), halign="left",
                text_size=(self.SIZE[0] * 0.9, None),
                background_normal="", background_color=self.color_theme["widget_background"], on_press=self.go_to_chat
            )
            contact_button.contact = contact
            self.scroll_box.add_widget(contact_button)
            self.contacts = self.main_screen_handler.get_contacts(self.dir)
        popup.dismiss()