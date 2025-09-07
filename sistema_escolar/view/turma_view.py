import flet as ft

class TurmaView:
    def __init__(self, page: ft.Page, role: str):
        self.page = page
        self.role = role
        self.content = self.build_view()

    def build_view(self):
        if self.role == "admin":
            return self.admin_view()
        elif self.role == "secretaria":
            return self.secretaria_view()
        else:
            return ft.Container(content=ft.Text("Acesso negado."), expand=True)

    def admin_view(self):
        return ft.Column([
            ft.Text("Gerenciar Turmas", size=20, weight="bold"),
            # Add controls for adding, editing, and removing classes
            ft.Button("Adicionar Turma", on_click=self.add_class),
            ft.Button("Editar Turma", on_click=self.edit_class),
            ft.Button("Remover Turma", on_click=self.remove_class),
            # Placeholder for displaying classes
            ft.ListView(id="class_list")
        ])

    def secretaria_view(self):
        return ft.Column([
            ft.Text("Visualizar Turmas", size=20, weight="bold"),
            # Placeholder for displaying classes
            ft.ListView(id="class_list")
        ])

    def add_class(self, e):
        # Logic to add a class
        pass

    def edit_class(self, e):
        # Logic to edit a class
        pass

    def remove_class(self, e):
        # Logic to remove a class
        pass

    def get_view(self):
        return self.content