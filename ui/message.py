import flet as ft
import datetime
import os
import subprocess
import platform


class Message(ft.Container):
    def __init__(self, dir, contact, message, **kwargs) :
        super().__init__(**kwargs)
        self.dir = dir
        self.message = message
        self.contact = contact
        self.expand = True
        self.content = ft.Row([
                ft.Column([
                    ft.Text(
                        value=f"{contact.NAME if message['from'] == 'contact' else 'Вы'} в {datetime.datetime.fromisoformat(message['date']).strftime('%H:%M')}:\n{message['text/plain']}",
                        size=15)
                ] + [
                    ft.Button(content=ft.Text(value=os.path.basename(application), size=15), on_click=lambda e: self._open_file(e, self.dir*application))
                    for application in self.message["application"] if application != ""
                ], expand=1),
                ft.Column(expand=1)
            ])

    def _open_file(self, e, path) -> None:
        system = platform.system()
        if system == "Windows":
            os.startfile(path)
        elif system == "Linux":
            subprocess.Popen(["xdg-open", path])
