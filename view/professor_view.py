import flet as ft
from services.professor_service import list_professores, create, delete

def ProfessorView(page: ft.Page, role=None, current_user_id=None):
    nome = ft.TextField(label="Nome do Professor", width=360)
    list_view = ft.ListView(expand=True, spacing=8, padding=8)

    def load():
        list_view.controls.clear()
        for p in list_professores():
            row = ft.Row([ft.Text(str(p["id"]), width=40), ft.Text(p["nome"], expand=True, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS),
                          ft.IconButton(ft.Icons.DELETE, on_click=lambda e, pid=p["id"]: on_delete(pid))],
                         alignment="spaceBetween")
            list_view.controls.append(row)
        page.update()

    def on_add(e):
        if role != "admin":
            page.snack_bar = ft.SnackBar(ft.Text("Apenas admin pode cadastrar professores")); page.snack_bar.open = True; page.update(); return
        if not nome.value: return
        create(nome.value); nome.value = ""; load()

    def on_delete(pid):
        if role != "admin":
            page.snack_bar = ft.SnackBar(ft.Text("Apenas admin pode remover professores")); page.snack_bar.open = True; page.update(); return
        delete(pid); load()

    add_btn = ft.ElevatedButton("Adicionar", on_click=on_add, disabled=(role != "admin"))
    container = ft.Container(content=ft.Column([ft.Text("Professores", size=18), ft.Row([nome, add_btn]), ft.Divider(), list_view]), expand=True)
    load()
    return container
