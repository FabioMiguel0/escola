import flet as ft
from services.disciplina_service import list_disciplinas, create

def DisciplinaView(page: ft.Page, role=None):
    nome = ft.TextField(label="Nome da Disciplina", width=360)
    list_view = ft.ListView(expand=True, spacing=8, padding=8)

    def load():
        list_view.controls.clear()
        for d in list_disciplinas():
            list_view.controls.append(ft.Row([ft.Text(d["nome"], expand=True)]))
        page.update()

    def on_add(e):
        if not nome.value: return
        create(nome.value); nome.value = ""; load()

    container = ft.Container(content=ft.Column([ft.Text("Disciplinas", size=18), ft.Row([nome, ft.ElevatedButton("Adicionar", on_click=on_add)]), ft.Divider(), list_view]), expand=True)
    load()
    return container
