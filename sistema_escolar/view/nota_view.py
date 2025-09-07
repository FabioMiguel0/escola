import flet as ft

class NotaView:
    def __init__(self, page: ft.Page, role: str, aluno_id: int):
        self.page = page
        self.role = role
        self.aluno_id = aluno_id
        self.content = self.build_view()

    def build_view(self):
        if self.role == "aluno":
            return self.build_student_view()
        else:
            return ft.Container(content=ft.Text("Acesso negado."), expand=True)

    def build_student_view(self):
        return ft.Column(
            controls=[
                ft.Text("Notas", size=30, weight="bold"),
                self.get_grades(),
                self.get_subjects(),
                self.get_performance(),
                self.get_report_card(),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )

    def get_grades(self):
        # Placeholder for fetching grades from the database
        return ft.Text("Aqui estão suas notas.")

    def get_subjects(self):
        # Placeholder for fetching subjects from the database
        return ft.Text("Aqui estão suas disciplinas.")

    def get_performance(self):
        # Placeholder for fetching performance data from the database
        return ft.Text("Aqui está seu desempenho.")

    def get_report_card(self):
        # Placeholder for fetching report card data from the database
        return ft.Text("Aqui está seu boletim.")