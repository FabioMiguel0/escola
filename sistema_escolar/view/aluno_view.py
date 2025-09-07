import flet as ft

class AlunoView:
    def __init__(self, page: ft.Page, role: str, current_user_id: int):
        self.page = page
        self.role = role
        self.current_user_id = current_user_id
        self.content = self.build_view()

    def build_view(self):
        return ft.Column(
            controls=[
                ft.Text("Bem-vindo ao Portal do Aluno", size=24, weight="bold"),
                ft.Divider(),
                self.create_grades_section(),
                self.create_subjects_section(),
                self.create_performance_section(),
                self.create_report_card_section(),
            ],
            expand=True,
            padding=20,
        )

    def create_grades_section(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Suas Notas", size=20, weight="bold"),
                    # Aqui você pode adicionar lógica para exibir as notas do aluno
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            border_radius=5,
        )

    def create_subjects_section(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Suas Disciplinas", size=20, weight="bold"),
                    # Aqui você pode adicionar lógica para exibir as disciplinas do aluno
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_GREEN_50,
            border_radius=5,
        )

    def create_performance_section(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Seu Desempenho", size=20, weight="bold"),
                    # Aqui você pode adicionar lógica para exibir o desempenho do aluno
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_YELLOW_50,
            border_radius=5,
        )

    def create_report_card_section(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Seu Boletim", size=20, weight="bold"),
                    # Aqui você pode adicionar lógica para exibir o boletim do aluno
                ]
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_ORANGE_50,
            border_radius=5,
        )