import flet as ft
from services import horario_service, disciplina_service, turma_service, professor_service


class HorariosAdminView:
    def __init__(self, page: ft.Page):
        self.page = page
        self._build_controls()

    def _load_options(self):
        profs = professor_service.list_professores()
        discs = disciplina_service.list_disciplinas()
        turmas = turma_service.list_turmas()
        prof_opts = [ft.dropdown.Option(str(p["id"]), text=p["nome"]) for p in profs]
        disc_opts = [ft.dropdown.Option(str(d["id"]), text=d["nome"]) for d in discs]
        turma_opts = [ft.dropdown.Option(str(t["id"]), text=t["nome"]) for t in turmas]
        return prof_opts, disc_opts, turma_opts

    def _build_controls(self):
        prof_opts, disc_opts, turma_opts = self._load_options()
        self.dd_prof = ft.Dropdown(label="Professor", options=prof_opts, width=240)
        self.dd_disc = ft.Dropdown(label="Disciplina", options=disc_opts, width=240)
        self.dd_turma = ft.Dropdown(label="Turma", options=turma_opts, width=240)
        self.dd_dia = ft.Dropdown(
            label="Dia da semana",
            options=[
                ft.dropdown.Option("Segunda"),
                ft.dropdown.Option("Terça"),
                ft.dropdown.Option("Quarta"),
                ft.dropdown.Option("Quinta"),
                ft.dropdown.Option("Sexta"),
            ],
            width=160,
        )
        self.tf_inicio = ft.TextField(label="Início (HH:MM)", width=140)
        self.tf_fim = ft.TextField(label="Fim (HH:MM)", width=140)
        self.info = ft.Text("")

        def on_add(e):
            try:
                pid = int(self.dd_prof.value)
                did = int(self.dd_disc.value)
                tid = int(self.dd_turma.value)
                dia = self.dd_dia.value
                ini = (self.tf_inicio.value or "").strip()
                fim = (self.tf_fim.value or "").strip()
                if not (pid and did and tid and dia and ini and fim):
                    self.info.value = "Preencha todos os campos"
                    self.info.color = ft.Colors.RED
                    self.page.update()
                    return
                horario_service.create(pid, did, tid, dia, ini, fim)
                self.info.value = "Horário adicionado com sucesso"
                self.info.color = ft.Colors.GREEN
                self._refresh_list()
            except ValueError as ex:
                self.info.value = str(ex)
                self.info.color = ft.Colors.RED
            except Exception as ex:
                self.info.value = f"Erro: {ex}"
                self.info.color = ft.Colors.RED
            self.page.update()

        self.btn_add = ft.ElevatedButton("Adicionar", on_click=on_add)

        self.rows = ft.Column(spacing=6, scroll="auto")
        self.container = ft.Column(
            [
                ft.Text("Gestão de Horários", size=22, weight="bold"),
                ft.Row([self.dd_prof, self.dd_disc, self.dd_turma], wrap=True, spacing=10),
                ft.Row([self.dd_dia, self.tf_inicio, self.tf_fim, self.btn_add], wrap=True, spacing=10),
                self.info,
                ft.Divider(),
                self.rows,
            ],
            tight=True,
        )
        self._refresh_list()

    def _refresh_list(self):
        self.rows.controls.clear()
        items = horario_service.list_all()
        # maps for labels
        profs = {p["id"]: p["nome"] for p in professor_service.list_professores()}
        discs = {d["id"]: d["nome"] for d in disciplina_service.list_disciplinas()}
        turmas = {t["id"]: t["nome"] for t in turma_service.list_turmas()}

        for it in items:
            txt = ft.Text(
                f"{it['dia_semana']} {it['hora_inicio']}-{it['hora_fim']} | Prof: {profs.get(it['professor_id'],'?')} | Disc: {discs.get(it['disciplina_id'],'?')} | Turma: {turmas.get(it['turma_id'],'?')}"
            )

            def make_del(id_):
                def _del(e):
                    try:
                        horario_service.delete(id_)
                        self._refresh_list()
                        self.page.update()
                    except Exception as ex:
                        self.info.value = f"Erro ao remover: {ex}"
                        self.info.color = ft.Colors.RED
                        self.page.update()
                return _del

            self.rows.controls.append(
                ft.Row([
                    txt,
                    ft.IconButton(ft.icons.DELETE, tooltip="Remover", on_click=make_del(it["id"]))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )

    def build(self):
        return ft.Container(content=self.container, expand=True, padding=16)


def HorariosAdmin(page: ft.Page):
    return HorariosAdminView(page).build()


