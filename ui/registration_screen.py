from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


from android_utils import Dir
from handlers import RegistrationScreenHandler


class RegistrationScreen(Screen):
    def __init__(self, dir : Dir, SIZE : list, color_theme : dict, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dir = dir
        self.registration_screen_handler = RegistrationScreenHandler(self.dir)

        with self.canvas.before:
            Color(*color_theme["main_background"])
            Rectangle(size=SIZE, pos=(0,0))

        input_layout = BoxLayout(orientation="vertical", padding=5, spacing=5, size_hint=(None, None), size=(SIZE[0], SIZE[1]*0.5), pos=(0, SIZE[1]*0.25))
        input_label = Label(text = "Создайте аккаунт", font_size=18)
        name_input = TextInput(foreground_color=[1, 1, 1], background_normal="", background_color=color_theme["widget_background"],
                               hint_text="Имя")
        email_input = TextInput(foreground_color=[1, 1, 1], background_normal="", background_color=color_theme["widget_background"],
                                hint_text="Почта")
        password_input = TextInput(foreground_color=[1, 1, 1], background_normal="", background_color=color_theme["widget_background"],
                                hint_text="Пароль (укажите именно пароль для сторонних приложений)")
        button = Button(text="Создать", background_normal="", background_color=color_theme["widget_background"])
        button.bind(on_press=lambda instance: self.register(instance, name_input.text, email_input.text, password_input.text))

        input_layout.add_widget(input_label)
        input_layout.add_widget(name_input)
        input_layout.add_widget(email_input)
        input_layout.add_widget(password_input)
        input_layout.add_widget(button)

        self.add_widget(input_layout)

    def register(self, instance : Button, name : str, email : str, password : str) -> None:
        if name == "" or email == "" or password == "": return None
        result = self.registration_screen_handler.create_account(name, email, password)
        if result is False: return None
        self.manager.build_application()
        self.manager.remove_widget(self)