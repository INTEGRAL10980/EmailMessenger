from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from .main_screen import MainScreen
from .registration_screen import RegistrationScreen
from .chat import Chat
from handlers import ApplicationHandler

from core import Contact
from android_utils import Dir



class Application(App):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.dir = Dir(self.user_data_dir)
        self.application_handler = ApplicationHandler(self.dir)
        self.config = self.application_handler.get_config()
        self.SIZE = self.config["SIZE"]
        self.color_theme = self.config["color_theme"]
        self.account = self.application_handler.account



        self.screen_manager = ScreenManager()
        self.screen_manager.add_contact_screen = self.add_contact_screen
        self.screen_manager.build_application = self.build_application

        if self.account is False:
            self.registration_screen = RegistrationScreen(dir=self.dir, SIZE=self.SIZE, color_theme=self.color_theme)
            self.screen_manager.add_widget(self.registration_screen)
        else:
            self.build_application()



    def build(self) -> ScreenManager:
        return self.screen_manager

    def window_set_config(self) -> None:
        Window.softinput_mode = "below_target"
        Window.size = self.config["SIZE"]

    def add_contact_screen(self, contact : Contact) -> None:
        chat = Chat(dir=self.dir, SIZE=self.SIZE, name = contact.PATH_TO_CONTACT,
                    contact=contact, color_theme=self.color_theme)
        self.screen_manager.add_widget(chat)
        self.contacts = self.application_handler.get_contacts()

    def build_application(self) -> None:
        self.application_handler.create_contacts_folder()

        self.account = self.application_handler.reload_account()
        self.contacts = self.application_handler.get_contacts()

        self.main_screen = MainScreen(self.dir, self.SIZE, self.color_theme)
        self.screen_manager.add_widget(self.main_screen)

        for contact in self.contacts:
            self.add_contact_screen(contact)

        self.screen_manager.current = "main"