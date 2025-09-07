# filepath: sistema_escolar/view/dashboard_view.py
import flet as ft

class DashboardView:
    def __init__(self, page: ft.Page, role: str, username: str, go):
        self.page = page
        self.role = role
        self.username = username
        self.go = go

    def build(self):
        return ft.Column(
            controls=[
                ft.Text(f"Bem-vindo, {self.username}!", size=30),
                ft.Text(f"Seu papel: {self.role}", size=20),
                ft.Divider(),
                self.build_navigation(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def build_navigation(self):
        controls = []
        if self.role == "admin":
            controls.append(ft.TextButton("Gerenciar Usuários", on_click=lambda e: self.go("usuarios")))
            controls.append(ft.TextButton("Gerenciar Professores", on_click=lambda e: self.go("professores")))
            controls.append(ft.TextButton("Gerenciar Alunos", on_click=lambda e: self.go("alunos")))
        elif self.role == "secretaria":
            controls.append(ft.TextButton("Cadastrar Alunos", on_click=lambda e: self.go("alunos")))
        elif self.role == "professor":
            controls.append(ft.TextButton("Ver Minhas Turmas", on_click=lambda e: self.go("turmas")))
            controls.append(ft.TextButton("Ver Minhas Disciplinas", on_click=lambda e: self.go("disciplinas")))
        elif self.role == "aluno":
            controls.append(ft.TextButton("Ver Minhas Notas", on_click=lambda e: self.go("notas")))
            controls.append(ft.TextButton("Ver Minhas Disciplinas", on_click=lambda e: self.go("disciplinas")))
            controls.append(ft.TextButton("Ver Meu Desempenho", on_click=lambda e: self.go("performance")))
            controls.append(ft.TextButton("Ver Meu Boletim", on_click=lambda e: self.go("report_card")))

        return ft.Column(controls=controls)