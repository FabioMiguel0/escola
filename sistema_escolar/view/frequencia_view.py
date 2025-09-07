import flet as ft

class FrequenciaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = self.build_view()

    def build_view(self):
        return ft.Column(
            controls=[
                ft.Text("Frequência", size=30, weight="bold"),
                ft.Divider(),
                # Aqui você pode adicionar mais controles para exibir a frequência do aluno
                ft.Text("Aqui você pode visualizar sua frequência."),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
        )

    def get_view(self):
        return self.content