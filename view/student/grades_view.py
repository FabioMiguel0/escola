import flet as ft
from services.nota_service import get_notas_by_aluno
from services.aluno_service import get as get_aluno

def GradesView(page: ft.Page, aluno_id: int = None):
    page.auto_scroll = True
    if not aluno_id:
        return ft.Container(content=ft.Text("Aluno não identificado."), expand=True, padding=12)

    aluno = get_aluno(aluno_id) or {"nome": "—"}
    title = ft.Text(f"Notas — {aluno.get('nome')}", size=18, weight="bold")

    try:
        notas = get_notas_by_aluno(aluno_id)
    except Exception:
        notas = []

    if not notas:
        body = ft.Column([ft.Text("Nenhuma nota registada.")])
    else:
        header = ft.Row([ft.Text("Disciplina", weight="bold", width=220),
                         ft.Text("Período", weight="bold", width=100),
                         ft.Text("Valor", weight="bold")], alignment="spaceBetween")
        rows = [header, ft.Divider()]
        for n in notas:
            rows.append(ft.Row([
                ft.Text(n.get("disciplina") or "—", width=220),
                ft.Text(n.get("periodo") or "—", width=100),
                ft.Text(str(n.get("valor") or "—")),
            ], alignment="spaceBetween"))
        body = ft.Column(rows, spacing=6)

    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)