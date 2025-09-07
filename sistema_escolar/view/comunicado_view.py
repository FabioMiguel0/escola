import flet as ft

class ComunicadoView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = self.build_view()

    def build_view(self):
        return ft.Column(
            controls=[
                ft.Text("Comunicados", size=30, weight="bold"),
                ft.Divider(),
                # Placeholder for announcements
                ft.Text("Aqui você pode visualizar os comunicados importantes."),
                ft.Text("Comunicado 1: Exemplo de comunicado."),
                ft.Text("Comunicado 2: Outro exemplo de comunicado."),
                ft.Text("Comunicado 3: Mais um comunicado."),
            ],
            alignment="center",
            spacing=20,
        )

    def get_view(self):
        return ft.View("/comunicados", controls=[self.content])