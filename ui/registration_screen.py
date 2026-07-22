import flet as ft
from handlers import RegistrationScreenHandler


class RegistrationScreen:
    def __init__(self, dir, callback):
        self.dir = dir
        self.callback = callback
        self.registration_screen_handler = RegistrationScreenHandler(self.dir)

        self.name_input = ft.TextField(hint_text="Имя", max_lines=1)
        self.email_input = ft.TextField(hint_text="Почта", max_lines=1)
        self.password_input = ft.TextField(hint_text="Пароль(для сторонних приложений)", max_lines=1)

        self.screen = ft.View(
            route="/reg",
            controls=[
                ft.Column([
                    ft.Text(value="Создайте аккаунт", size=20),
                    self.name_input, self.email_input, self.password_input,
                    ft.Button(content="Создать аккаунт",
                              on_click=lambda e: self.register(e,
                                                               self.name_input.value,
                                                               self.email_input.value,
                                                               self.password_input.value))
                ])
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.MainAxisAlignment.CENTER
        )


    def register(self, e, name : str, email : str, password : str) -> None:
        if name == "" or email == "" or password == "": return None
        result = self.registration_screen_handler.create_account(name, email, password)
        if result is False: return None
        self.callback()