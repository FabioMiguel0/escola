import flet as ft
from services.nota_service import get_boletim_summary
from services.aluno_service import get as get_aluno

def ReportCardView(page: ft.Page, aluno_id: int = None):
    page.auto_scroll = True
    if not aluno_id:
        return ft.Container(content=ft.Text("Aluno não identificado."), expand=True, padding=12)

    aluno = get_aluno(aluno_id) or {"nome": "—"}
    title = ft.Text(f"Boletim — {aluno.get('nome')}", size=18, weight="bold")

    boletim = []
    try:
        boletim = get_boletim_summary(aluno_id)
    except Exception:
        boletim = []

    if not boletim:
        body = ft.Column([ft.Text("Boletim não disponível.")])
    else:
        rows = [ft.Row([ft.Text("Período", weight="bold", width=160), ft.Text("Média", weight="bold")])]
        for b in boletim:
            rows.append(ft.Row([ft.Text(b.get("periodo") or "—", width=160), ft.Text(f"{b.get('media'):.2f}" if b.get("media") is not None else "—")]))
        body = ft.Column(rows, spacing=6)

    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)