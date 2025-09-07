import flet as ft
from services.nota_service import get_notas_by_aluno, get_boletim_summary
from services.frequencia_service import get_presencas_by_aluno
from services.horario_service import list_horario_by_turma
from services.aluno_service import get as get_aluno

def ProfileView(page: ft.Page, aluno_id: int = None):
    page.auto_scroll = True
    if not aluno_id:
        return ft.Container(content=ft.Text("Aluno não identificado."), expand=True, padding=12)

    aluno = get_aluno(aluno_id) or {"nome": "—", "turma_id": None}
    title = ft.Text(f"Perfil — {aluno.get('nome')}", size=18, weight="bold")

    # Notas
    try:
        notas = get_notas_by_aluno(aluno_id)
    except Exception:
        notas = []
    notas_col = ft.Column([ft.Text("Notas", weight="bold")])
    if notas:
        for n in notas:
            notas_col.controls.append(ft.Row([ft.Text(n.get("disciplina") or "—", width=220), ft.Text(str(n.get("valor") or "—"), width=80), ft.Text(n.get("periodo") or "—")], alignment="spaceBetween"))
    else:
        notas_col.controls.append(ft.Text("Nenhuma nota registada."))

    # Desempenho (médias por disciplina)
    desempenho_col = ft.Column([ft.Text("Desempenho", weight="bold")])
    if notas:
        by_disc = {}
        for n in notas:
            d = n.get("disciplina") or "—"
            by_disc.setdefault(d, []).append(n.get("valor") or 0)
        for disc, vals in by_disc.items():
            avg = sum(vals) / len(vals) if vals else 0
            desempenho_col.controls.append(ft.Row([ft.Text(disc, width=220), ft.Text(f"{avg:.2f}")]))
    else:
        desempenho_col.controls.append(ft.Text("Sem dados de desempenho."))

    # Boletim (média por período)
    try:
        boletim = get_boletim_summary(aluno_id)
    except Exception:
        boletim = []
    boletim_col = ft.Column([ft.Text("Boletim", weight="bold")])
    if boletim:
        for b in boletim:
            boletim_col.controls.append(ft.Row([ft.Text(b.get("periodo") or "—", width=160), ft.Text(f"{b.get('media'):.2f}" if b.get("media") is not None else "—")]))
    else:
        boletim_col.controls.append(ft.Text("Boletim não disponível."))

    # Frequência
    try:
        pres = get_presencas_by_aluno(aluno_id)
    except Exception:
        pres = []
    freq_col = ft.Column([ft.Text("Frequência", weight="bold")])
    if pres:
        for p in pres:
            freq_col.controls.append(ft.Row([ft.Text(p.get("data") or "—", width=140), ft.Text("Presente" if p.get("presente") else "Ausente")]))
    else:
        freq_col.controls.append(ft.Text("Nenhuma frequência registada."))

    # Horário (pela turma do aluno)
    turma_id = aluno.get("turma_id")
    horario_col = ft.Column([ft.Text("Horário", weight="bold")])
    if turma_id:
        try:
            slots = list_horario_by_turma(turma_id)
        except Exception:
            slots = []
        if slots:
            for s in slots:
                horario_col.controls.append(ft.Row([ft.Text(s.get("dia") or "", width=120), ft.Text(s.get("hora") or "", width=120), ft.Text(s.get("disciplina") or "", expand=True, no_wrap=False, overflow=ft.TextOverflow.ELLIPSIS)]))
        else:
            horario_col.controls.append(ft.Text("Horário não definido para a sua turma."))
    else:
        horario_col.controls.append(ft.Text("Aluno sem turma atribuída."))

    body = ft.Column(
        [
            title,
            ft.Divider(),
            notas_col,
            ft.Divider(),
            desempenho_col,
            ft.Divider(),
            boletim_col,
            ft.Divider(),
            freq_col,
            ft.Divider(),
            horario_col,
        ],
        spacing=12,
    )

    return ft.Container(content=body, expand=True, padding=12)