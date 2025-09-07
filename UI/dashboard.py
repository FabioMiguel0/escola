import flet as ft
from services.metrics_service import MetricsService
from . import estilos as est

class Dashboard(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.content = ft.Column([
            ft.Text("Bem-vindo ao Dashboard!", size=24, weight="bold"),
            # ...adicione outros widgets aqui...
        ])

    def build(self):
        metrics_service = MetricsService()
        c = metrics_service.get_counts()
        cards = ft.ResponsiveRow(controls=[
            ft.Column(col={"xs":12, "sm":6, "md":3}, controls=[est.card_metric("Alunos", str(c["alunos"]), ft.Icons.HOME)]),
            ft.Column(col={"xs":12, "sm":6, "md":3}, controls=[est.card_metric("Professores", str(c["professores"]), ft.Icons.PEOPLE)]),
            ft.Column(col={"xs":12, "sm":6, "md":3}, controls=[est.card_metric("Turmas", str(c["turmas"]), ft.Icons.GROUPS)]),
            ft.Column(col={"xs":12, "sm":6, "md":3}, controls=[est.card_metric("Comunicados", str(c["comunicados"]), ft.Icons.CAMPAIGN)]),
        ], spacing=12)

        ev_rows = []
        for d, ev, desc in metrics_service.get_proximos_eventos():
            ev_rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(d)), ft.DataCell(ft.Text(ev)), ft.DataCell(ft.Text(desc))]))

        eventos = ft.Container(
            bgcolor=est.CARD_COLOR, border_radius=16, padding=16,
            shadow=ft.BoxShadow(blur_radius=14, color="#00000010"),
            content=ft.Column([
                est.titulo("Próximos eventos"),
                ft.DataTable(columns=[ft.DataColumn(ft.Text("Data")),
                                      ft.DataColumn(ft.Text("Evento")),
                                      ft.DataColumn(ft.Text("Descrição"))],
                             rows=ev_rows if ev_rows else [ft.DataRow(cells=[ft.DataCell(ft.Text("-")), ft.DataCell(ft.Text("Sem eventos")),
                                                                              ft.DataCell(ft.Text("-"))])])
            ], spacing=12)
        )

        # tabela exemplo (últimas notas fictícias ou placeholder)
        records = ft.Container(
            bgcolor=est.CARD_COLOR, border_radius=16, padding=16,
            shadow=ft.BoxShadow(blur_radius=14, color="#00000010"),
            content=ft.Column([
                est.titulo("Registos recentes"),
                ft.DataTable(columns=[ft.DataColumn(ft.Text("Aluno")), ft.DataColumn(ft.Text("Nota")), ft.DataColumn(ft.Text("Disciplina"))],
                             rows=[
                                 ft.DataRow(cells=[ft.DataCell(ft.Text("Ana Sousa")), ft.DataCell(ft.Text("18")), ft.DataCell(ft.Text("Matemática"))]),
                                 ft.DataRow(cells=[ft.DataCell(ft.Text("Bruno Lima")), ft.DataCell(ft.Text("17")), ft.DataCell(ft.Text("Português"))]),
                             ])
            ], spacing=12)
        )

        return ft.Column([est.titulo("Quadro de Instrumentos"), cards, ft.ResponsiveRow([
            ft.Column(col={"xs":12, "md":7}, controls=[eventos]),
            ft.Column(col={"xs":12, "md":5}, controls=[records]),
        ], spacing=12)], spacing=16)
