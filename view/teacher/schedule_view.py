import flet as ft
from services.horario_service import list_horario_by_professor

def ScheduleView(page: ft.Page, role=None, current_user_id=None):
    page.auto_scroll = True
    title = ft.Text("Horário", size=18, weight="bold")
    if not current_user_id:
        return ft.Container(content=ft.Text("Professor não identificado."), expand=True, padding=12)
    slots = list_horario_by_professor(current_user_id)
    if not slots:
        body = ft.Column([ft.Text("Horário não definido.")])
    else:
        rows = []
        for s in slots:
            rows.append(ft.Row([ft.Text(s.get("dia") or "", width=120), ft.Text(s.get("hora") or "", width=120), ft.Text(s.get("disciplina") or "", expand=True, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS), ft.Text(str(s.get("turma_id") or ""))]))
        body = ft.Column(rows)
    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)