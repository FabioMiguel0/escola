from flet import Column, Text, ElevatedButton, Page

class UsersView:
    def __init__(self, page: Page, current_user):
        self.page = page
        self.current_user = current_user

    def build(self):
        return Column(
            controls=[
                Text(f"Bem-vindo, {self.current_user}!"),
                ElevatedButton("Cadastrar Professor", on_click=self.cadastrar_professor),
                ElevatedButton("Cadastrar Aluno", on_click=self.cadastrar_aluno),
                ElevatedButton("Visualizar Usuários", on_click=self.visualizar_usuarios),
            ]
        )

    def cadastrar_professor(self, e):
        # Implementar lógica para cadastrar professor
        pass

    def cadastrar_aluno(self, e):
        # Implementar lógica para cadastrar aluno
        pass

    def visualizar_usuarios(self, e):
        # Implementar lógica para visualizar usuários
        pass