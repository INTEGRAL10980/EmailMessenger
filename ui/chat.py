import flet as ft
import os
import webbrowser

from handlers import ChatHandler
from .message import Message

class Chat:
    def __init__(self, dir, page : ft.Page, contact):
        super().__init__()
        self.page = page
        self.dir = dir
        self.chat_handler = ChatHandler(dir, contact, self.add_message, page.run_task)

        self.messages_list_view = ft.ListView(
            controls=[], spacing=20, expand=True, auto_scroll=True
        )
        self.input_field = ft.TextField(label="Введите сообщение", multiline=True, max_lines=5, expand=True)
        self.application_panel = ft.Row(controls=[], expand=True, spacing=20, scroll=ft.ScrollMode.AUTO)
        self.layout = ft.Column(
            controls=[
            ft.Row([
                ft.Button(content=ft.Text(value=contact.NAME, size=16), expand=True), ft.IconButton(icon=ft.icons.Icons.EDIT)
            ]),
            self.messages_list_view,
            ft.Column([
                self.application_panel,
                ft.Row([
                    self.input_field, ft.IconButton(icon=ft.icons.Icons.ATTACH_FILE, on_click=self.pick_files), ft.IconButton(icon=ft.icons.Icons.SEND, on_click=self._send_message)
                ])
            ])
        ], expand=3, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        self.messages_from_history = self.chat_handler.load_history(50)
        self.chat_handler.run()

        self.applications = []

    def add_message(self, message):
        self.messages_list_view.controls.append(
            Message(self.dir, self.chat_handler.contact, message)
        )
        self.page.update()

    def _send_message(self, e) -> None:
        text = self.input_field.value
        if text == "": return
        self.chat_handler.send_message(text, self.applications)
        self.applications = []
        self.application_panel.controls = []
        self.input_field.value = ""
        self.page.update()

    async def pick_files(self, e):
        files = await ft.FilePicker().pick_files(allow_multiple=False)
        if len(files) == 0: return
        for file in files:
            path = str(file.path)
            self.applications.append(path)
            filename=os.path.basename(path)
            self.application_panel.controls.append(ft.Row([
                ft.IconButton(icon=ft.icons.Icons.CLOSE, on_click=lambda e, _path=path: self._unpin(e, _path)), ft.Button(content=filename, on_click=lambda e, _path=path: webbrowser.open(_path))
            ], spacing=0))

    def _unpin(self, e, path):
        self.application_panel.controls.remove(e.control.parent)
        self.applications.remove(path)