import flet as ft
from services.turma_service import list_turmas, create, delete

def TurmaView(page: ft.Page, role=None):
    nome = ft.TextField(label="Nome da Turma", width=300)
    list_view = ft.ListView(expand=True, spacing=8, padding=8)

    def load():
        list_view.controls.clear()
        for t in list_turmas():
            row = ft.Row([ft.Text(str(t["id"]), width=40), ft.Text(t["nome"], expand=True, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS),
                          ft.IconButton(ft.Icons.DELETE, on_click=lambda e, tid=t["id"]: on_delete(tid))],
                         alignment="spaceBetween")
            list_view.controls.append(row)
        page.update()

    def on_add(e):
        if not nome.value: return
        create(nome.value); nome.value = ""; load()

    def on_delete(tid):
        delete(tid); load()

    add_btn = ft.ElevatedButton("Criar Turma", on_click=on_add)
    container = ft.Container(content=ft.Column([ft.Text("Gestão de Turmas", size=18), ft.Row([nome, add_btn]), ft.Divider(), list_view]), expand=True)
    load()
    return container
