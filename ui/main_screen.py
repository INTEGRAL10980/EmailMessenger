import flet as ft

from handlers import MainScreenHandler
from .chat import Chat

class MainScreen:
    def __init__(self, dir, page):
        super().__init__()
        self.page = page
        self.dir = dir
        self.main_screen_handler = MainScreenHandler(dir)

        self.selected_contact = self.main_screen_handler.contacts[0].NAME
        self.chats={
        }

        for contact in self.main_screen_handler.contacts:
            chat = Chat(self.dir, self.page, contact)
            self.chats[contact.NAME] = chat

        self.contacts_list_view = ft.ListView(
            controls=[ft.IconButton(icon=ft.icons.Icons.ADD, on_click=self._add_contact_dialog)]+[
                ft.Button(content=ft.Text(value=contact.NAME, size=16), on_click=lambda e, name=contact.NAME: self._go_to_chat(e, name),
                          height=100, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                )
                for contact in self.main_screen_handler.contacts
            ],
            expand=1, spacing=3
        )

        self.screen = ft.View(
            route="/main",
            controls=[
                ft.Row(controls=[
                    self.contacts_list_view,
                    self.chats[self.selected_contact].layout
                ], expand=True)
            ]
        )


    def _go_to_chat(self, e, name):
        self.selected_contact = name
        self.screen.controls[0].controls = [self.contacts_list_view, self.chats[self.selected_contact].layout]

    def _add_contact_dialog(self):
        name_field = ft.TextField(hint_text="Имя контакта")
        email_field = ft.TextField(hint_text="Почта контакта")
        dialog = ft.AlertDialog(
            modal=False,
            title="Добавить контакт",
            content=ft.Column(
                controls=[
                    name_field, email_field
            ])
        )
        dialog.actions =[
                ft.IconButton(ft.icons.Icons.CHECK, on_click=lambda e: self._add_contact(e, name_field.value, email_field.value))
            ]
        self.page.overlay.append(dialog)
        dialog.open = True

    def _add_contact(self, e, name, email):
        contact = self.main_screen_handler.create_contact(name, email)
        if contact is False: return
        print(contact.PATH_TO_CONTACT)
        self.main_screen_handler.contacts = self.main_screen_handler.get_contacts()

        chat = Chat(self.dir, self.page, contact)
        self.chats[contact.NAME] = chat

        self.contacts_list_view.controls.append(ft.ElevatedButton(content=ft.Text(value=contact.NAME, size=16), on_click=lambda e, name=contact.NAME: self._go_to_chat(e, name),
                          height=100, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                ))
        e.control.parent.open = False