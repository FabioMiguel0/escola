import flet as ft
from services.nota_service import list_notas, add_nota, update_nota, delete_nota
from services.turma_service import list_turmas, list_alunos_by_turma
from services.aluno_service import get_all as list_alunos, get as get_aluno

def NotaView(page: ft.Page, role="aluno", aluno_id=None, current_user_id=None):
    page.auto_scroll = True

    title = ft.Text("Notas", size=18, weight="bold")
    notas_list = ft.ListView(expand=True, spacing=6, padding=6)
    turma_dd = ft.Dropdown(label="Turma", options=[ft.dropdown.Option("", text="-- selecionar --")] + [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()])
    aluno_dd = ft.Dropdown(label="Aluno", options=[ft.dropdown.Option("", text="-- selecionar --")])
    disciplina_field = ft.TextField(label="Disciplina", width=260)
    valor_field = ft.TextField(label="Valor", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    periodo_field = ft.TextField(label="Período", width=140)
    save_btn = ft.ElevatedButton("Salvar", visible=False)
    add_btn = ft.ElevatedButton("Adicionar")

    def load_notas():
        notas_list.controls.clear()
        # aluno_id filtra se aluno logado
        if role == "aluno" and aluno_id:
            notas = list_notas(aluno_id=aluno_id)
        else:
            notas = list_notas()
        for n in notas:
            txt = ft.Row([
                ft.Text(str(n.get("id")), width=40),
                ft.Text(n.get("disciplina") or "", width=220),
                ft.Text(str(n.get("valor") or ""), width=80),
                ft.Text(n.get("periodo") or "", width=120),
                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, nid=n["id"]: on_edit(nid)),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, nid=n["id"]: on_delete(nid)),
            ], alignment="spaceBetween")
            notas_list.controls.append(txt)
        page.update()

    def on_turma_change(e):
        tid = turma_dd.value
        if not tid:
            aluno_dd.options = [ft.dropdown.Option("", text="-- selecionar --")]
            aluno_dd.value = ""
            page.update(); return
        alunos = list_alunos_by_turma(int(tid))
        aluno_dd.options = [ft.dropdown.Option("", text="-- selecionar --")] + [ft.dropdown.Option(str(a["id"]), text=a["nome"]) for a in alunos]
        aluno_dd.value = ""
        page.update()

    def _can_modify():
        return role in ("professor", "admin")

    def on_add(e):
        if not _can_modify():
            page.snack_bar = ft.SnackBar(ft.Text("Sem permissão")); page.snack_bar.open=True; page.update(); return
        target_aluno = aluno_id
        if not target_aluno:
            if not aluno_dd.value:
                page.snack_bar = ft.SnackBar(ft.Text("Selecione aluno")); page.snack_bar.open=True; page.update(); return
            target_aluno = int(aluno_dd.value)
        discipl = disciplina_field.value.strip() if disciplina_field.value else None
        if not discipl:
            page.snack_bar = ft.SnackBar(ft.Text("Informe disciplina")); page.snack_bar.open=True; page.update(); return
        try:
            val = float(valor_field.value)
        except Exception:
            page.snack_bar = ft.SnackBar(ft.Text("Valor inválido")); page.snack_bar.open=True; page.update(); return
        periodo = periodo_field.value.strip() if periodo_field.value else None
        turma_id = int(turma_dd.value) if turma_dd.value else None
        add_nota(target_aluno, discipl, val, periodo, turma_id, current_user_id)
        disciplina_field.value = valor_field.value = periodo_field.value = ""
        page.update()
        load_notas()

    def on_edit(nid):
        n = next((x for x in list_notas() if x["id"]==nid), None)
        if not n: return
        disciplina_field.value = n.get("disciplina") or ""
        valor_field.value = str(n.get("valor") or "")
        periodo_field.value = n.get("periodo") or ""
        turma_dd.value = str(n.get("turma_id")) if n.get("turma_id") else ""
        aluno_dd.value = str(n.get("aluno_id")) if n.get("aluno_id") else ""
        save_btn.visible = True
        add_btn.visible = False
        save_btn.data = nid
        page.update()

    def on_save(e):
        nid = save_btn.data
        try:
            target_aluno = int(aluno_dd.value) if aluno_dd.value else None
            discipl = disciplina_field.value.strip()
            val = float(valor_field.value)
            periodo = periodo_field.value.strip() if periodo_field.value else None
            turma_id = int(turma_dd.value) if turma_dd.value else None
            update_nota(nid, target_aluno, discipl, val, periodo, turma_id, current_user_id)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}")); page.snack_bar.open=True; page.update(); return
        disciplina_field.value = valor_field.value = periodo_field.value = ""
        turma_dd.value = aluno_dd.value = ""
        save_btn.visible = False; add_btn.visible = True
        page.update()
        load_notas()

    def on_delete(nid):
        try:
            delete_nota(nid)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}")); page.snack_bar.open=True; page.update(); return
        load_notas()

    turma_dd.on_change = on_turma_change
    add_btn.on_click = on_add
    save_btn.on_click = on_save

    # professor/admin pode escolher turma/ aluno; aluno vê só lista
    controls = []
    if role in ("professor", "admin"):
        controls.append(ft.Row([turma_dd, aluno_dd, disciplina_field, valor_field, periodo_field, add_btn, save_btn]))
    else:
        # aluno: mostra apenas suas notas, sem formulário
        controls.append(ft.Row([ft.Text("As suas notas aparecem abaixo.")]))
    controls.append(ft.Divider())
    controls.append(notas_list)

    container = ft.Container(content=ft.Column([title, ft.Divider()] + controls), expand=True, padding=12)
    load_notas()
    return container
