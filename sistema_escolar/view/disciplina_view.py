from flet import Column, Text, Container, Page

class DisciplinaView:
    def __init__(self, page: Page):
        self.page = page

    def build(self):
        return Container(
            content=Column(
                [
                    Text("Disciplina View", size=24, weight="bold"),
                    Text("Aqui você pode visualizar as disciplinas disponíveis."),
                ]
            ),
            padding=20,
            expand=True,
        )