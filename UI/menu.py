import flet as ft
from services.user_service import menu_for_role
from . import estilos as est

class Shell:
    """
    App shell responsivo:
    - desktop: sidebar fixa
    - mobile: appbar + drawer (hambúrguer)
    """
    def __init__(self, page: ft.Page, username: str, role: str, on_route_change, content_builder):
        self.page = page
        self.username = username
        self.role = role
        self.on_route_change = on_route_change
        self.content_builder = content_builder

        self.routes = menu_for_role(role)  # [(label, route), ...]
        self.drawer = None

    def _build_sidebar(self):
        items = []
        for label, route in self.routes:
            items.append(
                ft.Container(
                    ink=True, padding=12, border_radius=12, bgcolor=est.PRIMARY_COLOR_DARK,
                    on_click=lambda e, r=route: self.on_route_change(r),
                    content=ft.Row([ft.Icon(ft.Icons.CHEVRON_RIGHT, color="white"),
                                    ft.Text(label, color="white")], spacing=10)
                )
            )
        # Botão Sair (voltar ao login)
        items.append(
            ft.Container(
                ink=True, padding=12, border_radius=12, bgcolor="#ef4444",
                on_click=lambda e: self.on_route_change("logout"),
                content=ft.Row([ft.Icon(ft.Icons.LOGOUT, color="white"),
                                ft.Text("Sair", color="white")], spacing=10)
            )
        )
        return ft.Container(
            width=260, bgcolor=est.PRIMARY_COLOR, padding=16,
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.HOME, color="white"), ft.Text("EduGestão", color="white", size=18, weight="bold")]),
                ft.Divider(color="#ffffff33"),
                *items,
                ft.Container(expand=True),
                ft.Divider(color="#ffffff33"),
                ft.Row([ft.CircleAvatar(content=ft.Text(self.username[:1].upper()), color=est.PRIMARY_COLOR, bgcolor="white"),
                        ft.Text(f"{self.username} ({self.role})", color="white")])
            ], expand=True, spacing=10)
        )

    def _build_appbar(self, title: str):
        def open_drawer(_): self.page.open_drawer()
        return ft.AppBar(
            title=ft.Text(title, color="white"),
            leading=ft.IconButton(ft.Icons.MENU, icon_color="white", on_click=open_drawer),
            bgcolor=est.PRIMARY_COLOR,
            actions=[ft.IconButton(ft.Icons.LOGOUT, icon_color="white", on_click=lambda _: self.on_route_change("logout"))]
        )

    def build(self):
        is_mobile = self.page.width <= 800
        self.page.on_resize = lambda e: self.page.update()

        current_title = "Dashboard"
        content = ft.Container(bgcolor=est.BACKGROUND_COLOR, expand=True, padding=16,
                               content=self.content_builder())

        if is_mobile:
            self.drawer = ft.NavigationDrawer(
                controls=[ft.Container(height=8),
                          ft.Text("EduGestão", size=20, weight="bold", color=est.PRIMARY_COLOR),
                          ft.Divider(),
                          *[ft.NavigationDrawerDestination(ft.Icons.CHEVRON_RIGHT, label) for (label, _) in self.routes]],
                on_change=lambda e: self.on_route_change(self.routes[e.control.selected_index][1])
            )
            self.page.drawer = self.drawer
            return ft.View(route="/", controls=[self._build_appbar(current_title), content], padding=0)
        else:
            return ft.View(route="/", padding=0, controls=[
                ft.Row([self._build_sidebar(), ft.VerticalDivider(width=1, color="#00000010"), content], expand=True)
            ])
