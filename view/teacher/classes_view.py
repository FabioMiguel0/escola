import flet as ft
from services.turma_service import list_turmas, list_alunos_by_turma

def ClassesView(page: ft.Page, role=None, current_user_id=None):
    page.auto_scroll = True
    title = ft.Text("Minhas Turmas", size=18, weight="bold")
    turmas = list_turmas()
    minhas = [t for t in turmas if current_user_id and t.get("professor_id")==current_user_id] or []
    rows = []
    for t in minhas:
        btn = ft.ElevatedButton("Ver alunos", on_click=lambda e, tid=t["id"]: page.client_storage.set("go_to_turma", tid) or page.update())
        rows.append(ft.Row([ft.Text(str(t.get("id")), width=60), ft.Text(t.get("nome") or "", expand=True, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS), btn]))
    body = ft.Column(rows or [ft.Text("Nenhuma turma atribuída.")])
    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)