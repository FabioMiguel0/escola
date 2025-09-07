import flet as ft
from services.comunicado_service import list_comunicados


def CalendarioView(page: ft.Page):
    eventos = [c for c in list_comunicados()]

    list_view = ft.ListView(expand=True, spacing=8, padding=8)
    for e in eventos:
        list_view.controls.append(
            ft.Column(
                [
                    ft.Text(e["titulo"], weight="bold"),
                    ft.Text(e["data"]),
                    ft.Text(e["texto"]),
                ]
            )
        )

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Calendário Escolar", size=24, weight="bold"),
                ft.Divider(),
                list_view,
            ]
        ),
        expand=True,
    )
    return container


