import flet as ft
import os
import logging

from ui.main_screen import MainScreen
from ui.registration_screen import RegistrationScreen
from utils import Dir
from handlers import ApplicationHandler

logging.getLogger("flet").setLevel(logging.INFO)

class Application:
    def __init__(self):
        self.page : ft.Page | None = None


    def _build(self, page : ft.Page):
        self.page = page
        self.page.on_route_change =self._route_screens
        self.page.theme_mode = "dark"
        self.page.title = "Физмат Мессенджер"
        self.page.window.icon = os.path.abspath("assets/icon.ico")
        self.page.update()

        self.user_data_dir = os.path.join(os.getenv("APPDATA"), "FizmatMessenger")
        if not os.path.isdir(self.user_data_dir):
            os.mkdir(self.user_data_dir)
        self.dir = Dir(self.user_data_dir)
        self.application_handler = ApplicationHandler(self.dir)

        self.account = self.application_handler.account

        if not self.account:
            self.registration_screen = RegistrationScreen(self.dir, self._build_application)
            self.page.go("/reg")
        else:
            self._build_application()



    def _build_application(self):
        self.account = self.application_handler.reload_account()
        self.contacts = self.application_handler.get_contacts()

        self.main_screen = MainScreen(self.dir, self.page)

        self.page.go("/main")

    def _route_screens(self, route):
        self.page.views.clear()
        if self.page.route == "/reg":
            self.page.views.append(self.registration_screen.screen)
        elif self.page.route == "/main":
            self.page.views.append(self.main_screen.screen)

    def run(self):
        ft.app(target=self._build)