import flet as ft
from services.disciplina_service import list_disciplinas

def SubjectsTaughtView(page: ft.Page, role=None, current_user_id=None):
    page.auto_scroll = True
    title = ft.Text("Disciplinas que leciono", size=18, weight="bold")
    try:
        disciplinas = list_disciplinas()
    except Exception:
        disciplinas = []
    rows = [ft.Row([ft.Text(str(d.get("id")), width=60), ft.Text(d.get("nome") or "", expand=True, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS)]) for d in disciplinas]
    return ft.Container(content=ft.Column([title, ft.Divider(), ft.Column(rows or [ft.Text("Nenhuma disciplina.")])]), expand=True, padding=12)