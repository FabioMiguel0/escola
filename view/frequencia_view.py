import flet as ft
from services.turma_service import list_turmas, list_alunos_by_turma
from services.frequencia_service import set_presenca, get_presencas_by_turma_date


def FrequenciaView(page: ft.Page):
    page.auto_scroll = True
    title = ft.Text("Frequência", size=18, weight="bold")
    turma_dd = ft.Dropdown(
        label="Turma",
        options=[ft.dropdown.Option("", text="-- selecionar --")]
        + [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in list_turmas()],
    )
    date_field = ft.TextField(label="Data (YYYY-MM-DD)", width=160)
    lista = ft.Column()
    save_btn = ft.ElevatedButton("Salvar Presenças")

    pres_map = {}  # aluno_id -> bool

    def on_turma_change(e):
        lista.controls.clear()
        if not turma_dd.value:
            page.update()
            return
        alunos = list_alunos_by_turma(int(turma_dd.value))
        for a in alunos:
            aid = a["id"]
            chk = ft.Checkbox(label=a.get("nome") or "", value=False)

            def make_cb(aid_local, chk_local):
                def cb(e):
                    pres_map[aid_local] = chk_local.value

                return cb

            chk.on_change = make_cb(aid, chk)
            lista.controls.append(chk)
        page.update()

    def on_save(e):
        if not turma_dd.value or not date_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Selecione turma e data")
            )
            page.snack_bar.open = True
            page.update()
            return
        for aid, presente in pres_map.items():
            set_presenca(int(turma_dd.value), aid, date_field.value, bool(presente))
        page.snack_bar = ft.SnackBar(ft.Text("Presenças registadas"))
        page.snack_bar.open = True
        page.update()

    turma_dd.on_change = on_turma_change
    save_btn.on_click = on_save

    return ft.Container(
        content=ft.Column(
            [title, ft.Divider(), ft.Row([turma_dd, date_field, save_btn]), ft.Divider(), lista]
        ),
        expand=True,
        padding=12,
    )


