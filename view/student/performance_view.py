import flet as ft
from services.nota_service import get_notas_by_aluno
from services.aluno_service import get as get_aluno

def PerformanceView(page: ft.Page, aluno_id: int = None):
    page.auto_scroll = True
    if not aluno_id:
        return ft.Container(content=ft.Text("Aluno não identificado."), expand=True, padding=12)

    aluno = get_aluno(aluno_id) or {"nome": "—"}
    title = ft.Text(f"Desempenho — {aluno.get('nome')}", size=18, weight="bold")

    notas = []
    try:
        notas = get_notas_by_aluno(aluno_id)
    except Exception:
        notas = []

    if not notas:
        body = ft.Column([ft.Text("Sem dados de desempenho.")])
    else:
        # mostra média simples por disciplina
        by_disc = {}
        for n in notas:
            d = n.get("disciplina") or "—"
            by_disc.setdefault(d, []).append(n.get("valor") or 0)
        rows = [ft.Row([ft.Text("Disciplina", weight="bold", width=220), ft.Text("Média", weight="bold")])]
        for disc, vals in by_disc.items():
            avg = sum(vals) / len(vals) if vals else 0
            rows.append(ft.Row([ft.Text(disc, width=220), ft.Text(f"{avg:.2f}")]))
        body = ft.Column(rows, spacing=6)

    return ft.Container(content=ft.Column([title, ft.Divider(), body]), expand=True, padding=12)