import flet as ft

class ProfessorView:
    def __init__(self, page: ft.Page, role: str, current_user_id: int):
        self.page = page
        self.role = role
        self.current_user_id = current_user_id
        self.content = self.build_view()

    def build_view(self):
        return ft.Column(
            controls=[
                ft.Text("Bem-vindo, Professor!", size=24, weight="bold"),
                ft.Divider(),
                self.classes_section(),
                self.schedule_section(),
                self.subjects_section(),
            ],
            expand=True,
            padding=20,
        )

    def classes_section(self):
        return ft.Column(
            controls=[
                ft.Text("Suas Turmas", size=20, weight="bold"),
                # Aqui você pode adicionar a lógica para listar as turmas do professor
                ft.Text("Lista de turmas será exibida aqui."),
            ]
        )

    def schedule_section(self):
        return ft.Column(
            controls=[
                ft.Text("Seu Horário", size=20, weight="bold"),
                # Aqui você pode adicionar a lógica para mostrar o horário do professor
                ft.Text("Seu horário será exibido aqui."),
            ]
        )

    def subjects_section(self):
        return ft.Column(
            controls=[
                ft.Text("Disciplinas que Você Ensina", size=20, weight="bold"),
                # Aqui você pode adicionar a lógica para listar as disciplinas que o professor ensina
                ft.Text("Lista de disciplinas será exibida aqui."),
            ]
        )